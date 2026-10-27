"""Deterministic generator for the DEMO/sample dataset.

Produces data/raw/products.csv and data/raw/reviews.csv. The data is
synthetic sample data for development and demos only - it does not represent
real products or real customer reviews. All downstream analysis (sentiment,
aspects, trends, etc.) is computed from this text at runtime; nothing is
hard-coded.

Run:  python data/scripts/generate_sample_data.py
"""
import csv
import json
import random
from datetime import date, timedelta
from pathlib import Path

RAW = Path(__file__).resolve().parent.parent / "raw"
RAW.mkdir(parents=True, exist_ok=True)
SEED = 42
ANCHOR = date(2025, 10, 1)  # "today" for deterministic review dates

# aspect -> list of keyword phrases (shared contract with the aspect analyzer)
ASPECT_KEYWORDS = {
    "camera": ["camera", "photo", "photos", "picture", "pictures", "lens", "selfie"],
    "battery": ["battery", "charge", "charging", "battery life", "backup"],
    "display": ["display", "screen", "brightness", "resolution"],
    "performance": ["performance", "speed", "fast", "lag", "processor", "smooth"],
    "design": ["design", "look", "looks", "build look", "aesthetic", "premium"],
    "price": ["price", "value", "cost", "expensive", "cheap", "worth"],
    "build quality": ["build quality", "build", "durability", "sturdy", "plasticky"],
    "sound": ["sound", "audio", "speaker", "speakers", "bass", "music"],
    "software": ["software", "ui", "os", "update", "app", "bloatware"],
    "gaming": ["gaming", "game", "games", "fps", "graphics"],
    "comfort": ["comfort", "comfortable", "fit", "ergonomic", "wear"],
    "keyboard": ["keyboard", "keys", "typing", "trackpad"],
}

CATEGORY_ASPECTS = {
    "smartphone": ["camera", "battery", "display", "performance", "design", "price", "build quality", "software", "gaming"],
    "laptop": ["performance", "battery", "display", "design", "price", "build quality", "software", "gaming", "keyboard"],
    "headphones": ["sound", "battery", "design", "price", "build quality", "comfort", "software"],
    "smartwatch": ["battery", "display", "design", "price", "build quality", "software", "performance"],
}

POS = [
    "The {a} is excellent and exceeded my expectations.",
    "Really impressed with the {a}, top notch.",
    "Great {a}, one of the best I have used.",
    "The {a} performs wonderfully day to day.",
    "Loving the {a}, clearly a strong point.",
]
NEG = [
    "The {a} is disappointing and needs work.",
    "Not happy with the {a} at all.",
    "The {a} is easily the weakest part.",
    "The {a} could be much better for this product.",
    "Struggled with poor {a} throughout.",
]
NEU = [
    "The {a} is okay, nothing special.",
    "The {a} is average for this segment.",
    "Decent {a}, about what I expected.",
    "The {a} is fine for the price.",
]

# product_id, name, brand, category, base_price, description, specs, aspect_profile
# aspect_profile: aspect -> probability the review sentiment is positive
PRODUCTS = [
    ("P001", "Nova X1 Pro", "Nova", "smartphone", 699, "Flagship smartphone with a focus on camera and gaming.",
     {"ram": "8GB", "storage": "128GB", "screen": "6.5 in", "weight": "189 g"},
     {"camera": 0.9, "battery": 0.3, "display": 0.85, "performance": 0.85, "design": 0.7, "price": 0.5, "build quality": 0.75, "software": 0.7, "gaming": 0.85}),
    ("P002", "Zenith Edge 5", "Zenith", "smartphone", 549, "Mid-range smartphone balancing value and display quality.",
     {"ram": "6GB", "storage": "128GB", "screen": "6.4 in", "weight": "182 g"},
     {"camera": 0.5, "battery": 0.6, "display": 0.8, "performance": 0.55, "design": 0.75, "price": 0.85, "build quality": 0.6, "software": 0.6, "gaming": 0.45}),
    ("P003", "Pulse Lite 4", "Pulse", "smartphone", 299, "Budget smartphone for everyday essentials.",
     {"ram": "4GB", "storage": "64GB", "screen": "6.2 in", "weight": "175 g"},
     {"camera": 0.35, "battery": 0.8, "display": 0.4, "performance": 0.35, "design": 0.45, "price": 0.9, "build quality": 0.3, "software": 0.5, "gaming": 0.25}),
    ("P004", "Aero Max Ultra", "Aero", "smartphone", 999, "Premium smartphone with best-in-class performance.",
     {"ram": "12GB", "storage": "256GB", "screen": "6.7 in", "weight": "210 g"},
     {"camera": 0.9, "battery": 0.85, "display": 0.9, "performance": 0.95, "design": 0.85, "price": 0.35, "build quality": 0.9, "software": 0.8, "gaming": 0.9}),
    ("P005", "Vortex Book 14", "Vortex", "laptop", 1099, "Thin-and-light laptop for productivity and travel.",
     {"ram": "16GB", "storage": "512GB SSD", "screen": "14 in", "weight": "1.3 kg"},
     {"performance": 0.8, "battery": 0.85, "display": 0.8, "design": 0.85, "price": 0.5, "build quality": 0.8, "software": 0.7, "gaming": 0.4, "keyboard": 0.8}),
    ("P006", "Vortex Gamer 16", "Vortex", "laptop", 1599, "High-performance gaming laptop with a fast display.",
     {"ram": "32GB", "storage": "1TB SSD", "screen": "16 in", "weight": "2.4 kg"},
     {"performance": 0.95, "battery": 0.3, "display": 0.9, "design": 0.6, "price": 0.4, "build quality": 0.75, "software": 0.65, "gaming": 0.95, "keyboard": 0.75}),
    ("P007", "Breeze Air 13", "Breeze", "laptop", 749, "Affordable everyday laptop for students.",
     {"ram": "8GB", "storage": "256GB SSD", "screen": "13 in", "weight": "1.4 kg"},
     {"performance": 0.45, "battery": 0.7, "display": 0.5, "design": 0.55, "price": 0.9, "build quality": 0.4, "software": 0.6, "gaming": 0.2, "keyboard": 0.6}),
    ("P008", "Echo Studio Pods", "Echo", "headphones", 249, "Premium noise-cancelling over-ear headphones.",
     {"type": "Over-ear", "anc": "Yes", "battery": "30 h", "weight": "250 g"},
     {"sound": 0.9, "battery": 0.8, "design": 0.8, "price": 0.45, "build quality": 0.85, "comfort": 0.85, "software": 0.7}),
    ("P009", "Echo Buds Mini", "Echo", "headphones", 99, "Compact wireless earbuds for daily use.",
     {"type": "In-ear", "anc": "Basic", "battery": "18 h", "weight": "45 g"},
     {"sound": 0.6, "battery": 0.55, "design": 0.7, "price": 0.85, "build quality": 0.5, "comfort": 0.6, "software": 0.55}),
    ("P010", "Tempo Sound Max", "Tempo", "headphones", 179, "Bass-heavy wireless headphones for music lovers.",
     {"type": "Over-ear", "anc": "Yes", "battery": "24 h", "weight": "270 g"},
     {"sound": 0.8, "battery": 0.6, "design": 0.6, "price": 0.65, "build quality": 0.55, "comfort": 0.5, "software": 0.5}),
    ("P011", "Pulse Watch Fit", "Pulse", "smartwatch", 149, "Fitness-focused smartwatch with long battery life.",
     {"display": "1.4 in AMOLED", "battery": "10 d", "gps": "Yes", "weight": "32 g"},
     {"battery": 0.9, "display": 0.7, "design": 0.65, "price": 0.8, "build quality": 0.6, "software": 0.55, "performance": 0.6}),
    ("P012", "Aero Watch Pro", "Aero", "smartwatch", 329, "Premium smartwatch with rich software features.",
     {"display": "1.5 in AMOLED", "battery": "4 d", "gps": "Yes", "weight": "38 g"},
     {"battery": 0.4, "display": 0.88, "design": 0.85, "price": 0.45, "build quality": 0.85, "software": 0.85, "performance": 0.8}),
]

REVIEWS_PER_PRODUCT = 16


def polarity_for(prob: float, rnd: random.Random) -> str:
    r = rnd.random()
    if r < prob:
        return "pos"
    if r < prob + (1 - prob) * 0.35:
        return "neu"
    return "neg"


def sentence(aspect: str, pol: str, rnd: random.Random) -> str:
    bank = {"pos": POS, "neu": NEU, "neg": NEG}[pol]
    return rnd.choice(bank).format(a=aspect)


def rating_from(pols: list[str]) -> int:
    score = sum({"pos": 2, "neu": 0, "neg": -2}[p] for p in pols) / max(len(pols), 1)
    return max(1, min(5, round(3 + score)))


def main() -> None:
    rnd = random.Random(SEED)

    # products.csv
    with (RAW / "products.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["product_id", "name", "brand", "category", "price", "description", "specs"])
        for pid, name, brand, cat, price, desc, specs, _profile in PRODUCTS:
            w.writerow([pid, name, brand, cat, price, desc, json.dumps(specs)])

    # reviews.csv
    rows = []
    rid = 1
    for pid, name, brand, cat, price, desc, specs, profile in PRODUCTS:
        aspects = CATEGORY_ASPECTS[cat]
        for i in range(REVIEWS_PER_PRODUCT):
            n = rnd.choice([1, 2, 2, 3])
            chosen = rnd.sample(aspects, min(n, len(aspects)))
            pols, parts = [], []
            for a in chosen:
                # slight positive drift for more recent reviews (trend signal)
                pol = polarity_for(profile[a], rnd)
                pols.append(pol)
                parts.append(sentence(a, pol, rnd))
            # join with a contrast word when polarity is mixed
            if len(parts) > 1 and len(set(pols)) > 1:
                text = parts[0] + " However, " + " ".join(parts[1:])
            else:
                text = " ".join(parts)
            rating = rating_from(pols)
            days_ago = int((i / REVIEWS_PER_PRODUCT) * 330) + rnd.randint(0, 25)
            rdate = (ANCHOR - timedelta(days=330 - days_ago)).isoformat()
            rows.append([f"R{rid:04d}", pid, text, rating, rdate, f"user_{rnd.randint(100, 999)}"])
            rid += 1

    # inject a few near-duplicate reviews to give the authenticity detector signal
    dup_base = rows[0][2]
    for k in range(3):
        rows.append([f"R{rid:04d}", "P001", dup_base, 5, (ANCHOR - timedelta(days=5)).isoformat(), f"user_{200 + k}"])
        rid += 1

    with (RAW / "reviews.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["review_id", "product_id", "review_text", "rating", "date", "author"])
        w.writerows(rows)

    print(f"Wrote {len(PRODUCTS)} products and {len(rows)} reviews to {RAW}")


if __name__ == "__main__":
    main()
