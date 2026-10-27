"""Shared lexicons: aspect keywords and a sentiment word list.

Keyword/rule based (no large model download) so local startup stays reliable.
Aspect keywords are the runtime contract used by aspect extraction.
"""

ASPECT_KEYWORDS = {
    "camera": ["camera", "photo", "photos", "picture", "pictures", "lens", "selfie"],
    "battery": ["battery", "charge", "charging", "battery life", "backup"],
    "display": ["display", "screen", "brightness", "resolution"],
    "performance": ["performance", "speed", "fast", "lag", "laggy", "processor", "smooth"],
    "design": ["design", "look", "looks", "aesthetic", "premium", "sleek"],
    "price": ["price", "value", "cost", "expensive", "cheap", "worth", "affordable"],
    "build quality": ["build quality", "build", "durability", "sturdy", "plasticky"],
    "sound": ["sound", "audio", "speaker", "speakers", "bass", "music"],
    "software": ["software", "ui", "os", "update", "updates", "app", "bloatware"],
    "gaming": ["gaming", "game", "games", "fps", "graphics"],
    "comfort": ["comfort", "comfortable", "fit", "ergonomic", "wear"],
    "keyboard": ["keyboard", "keys", "typing", "trackpad"],
}

# Order matters: match multi-word phrases before single words.
ASPECT_PHRASES = sorted(
    ((kw, aspect) for aspect, kws in ASPECT_KEYWORDS.items() for kw in kws),
    key=lambda x: -len(x[0]),
)

POSITIVE_WORDS = {
    "excellent", "great", "amazing", "impressed", "loving", "love", "best",
    "good", "wonderful", "wonderfully", "fantastic", "superb", "solid",
    "strong", "exceeded", "top", "notch", "premium", "smooth", "fast",
    "reliable", "worth", "vibrant", "sturdy", "comfortable", "satisfied",
    "nice", "perfect", "outstanding",
}

NEGATIVE_WORDS = {
    "disappointing", "disappointed", "poor", "weak", "weakest", "bad",
    "terrible", "struggled", "struggle", "slow", "laggy", "lag", "drains",
    "drain", "cheap", "plasticky", "dull", "heats", "heat", "heating",
    "expensive", "overpriced", "worse", "worst", "broken", "issue", "issues",
    "problem", "problems", "unhappy",
}

NEGATORS = {"not", "no", "never", "hardly", "barely", "cannot", "cant", "dont", "doesnt", "isnt", "wasnt"}

# Phrases that flip or set polarity regardless of individual words.
NEGATIVE_PHRASES = ["could be much better", "weakest part", "needs work", "not happy", "nothing special"]
NEUTRAL_PHRASES = ["okay", "average", "decent", "fine for the price", "as expected", "nothing special"]
