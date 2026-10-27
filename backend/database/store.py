"""Unified document store: MongoDB when reachable, local JSON otherwise.

Exposes a small, consistent collection API (insert_one / find / find_one /
update_one / delete_one / delete_many / count) so services don't care which
backend is active. The JSON fallback persists to data/store/<collection>.json.

Limitation: the JSON fallback is process-local file storage. It persists across
restarts on the same machine but is not concurrent-safe across processes and is
not a substitute for a real database in production.
"""
import json
import threading
from pathlib import Path

from backend import config
from backend.database import connection

_lock = threading.RLock()


def _matches(doc: dict, query: dict) -> bool:
    return all(doc.get(k) == v for k, v in query.items())


class JsonCollection:
    def __init__(self, path: Path):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def _read(self) -> list[dict]:
        if not self.path.exists():
            return []
        try:
            return json.loads(self.path.read_text(encoding="utf-8"))
        except Exception:
            return []

    def _write(self, docs: list[dict]) -> None:
        self.path.write_text(json.dumps(docs, ensure_ascii=False, indent=2), encoding="utf-8")

    def insert_one(self, doc: dict) -> dict:
        with _lock:
            docs = self._read()
            docs.append(doc)
            self._write(docs)
            return doc

    def find(self, query: dict | None = None) -> list[dict]:
        with _lock:
            docs = self._read()
        query = query or {}
        return [d for d in docs if _matches(d, query)]

    def find_one(self, query: dict) -> dict | None:
        res = self.find(query)
        return res[0] if res else None

    def update_one(self, query: dict, patch: dict, upsert: bool = False) -> dict | None:
        with _lock:
            docs = self._read()
            for d in docs:
                if _matches(d, query):
                    d.update(patch)
                    self._write(docs)
                    return d
            if upsert:
                new = {**query, **patch}
                docs.append(new)
                self._write(docs)
                return new
            return None

    def delete_one(self, query: dict) -> int:
        with _lock:
            docs = self._read()
            for i, d in enumerate(docs):
                if _matches(d, query):
                    docs.pop(i)
                    self._write(docs)
                    return 1
            return 0

    def delete_many(self, query: dict) -> int:
        with _lock:
            docs = self._read()
            keep = [d for d in docs if not _matches(d, query)]
            removed = len(docs) - len(keep)
            self._write(keep)
            return removed

    def count(self, query: dict | None = None) -> int:
        return len(self.find(query or {}))


class MongoCollection:
    """Thin adapter over a pymongo collection with the same subset API."""

    _PROJ = {"_id": 0}

    def __init__(self, coll):
        self.coll = coll

    def insert_one(self, doc: dict) -> dict:
        self.coll.insert_one(dict(doc))
        return doc

    def find(self, query: dict | None = None) -> list[dict]:
        return list(self.coll.find(query or {}, self._PROJ))

    def find_one(self, query: dict) -> dict | None:
        return self.coll.find_one(query, self._PROJ)

    def update_one(self, query: dict, patch: dict, upsert: bool = False) -> dict | None:
        self.coll.update_one(query, {"$set": patch}, upsert=upsert)
        return self.find_one({**query, **patch}) or self.find_one(query)

    def delete_one(self, query: dict) -> int:
        return self.coll.delete_one(query).deleted_count

    def delete_many(self, query: dict) -> int:
        return self.coll.delete_many(query).deleted_count

    def count(self, query: dict | None = None) -> int:
        return self.coll.count_documents(query or {})


class Store:
    def __init__(self):
        self.backend = "json"
        self._db = None
        if config.USE_MONGO != "0":
            if config.USE_MONGO == "1" or connection.ping():
                try:
                    self._db = connection.get_db()
                    self.backend = "mongo"
                except Exception:
                    self._db = None
        self._json: dict[str, JsonCollection] = {}

    def collection(self, name: str):
        if self.backend == "mongo" and self._db is not None:
            return MongoCollection(self._db[name])
        if name not in self._json:
            self._json[name] = JsonCollection(config.STORE_DIR / f"{name}.json")
        return self._json[name]


_store: Store | None = None


def get_store() -> Store:
    global _store
    if _store is None:
        _store = Store()
    return _store
