import re

VEG, EGG, NON_VEG = "veg", "egg", "non_veg"
RANK = {VEG: 0, EGG: 1, NON_VEG: 2}

_NON_VEG_TERMS = [
    # meat & poultry
    "chicken", "beef", "pork", "mutton", "lamb", "goat", "veal", "venison",
    "turkey", "duck", "goose", "bacon", "ham", "salami", "pepperoni",
    "prosciutto", "pancetta", "sausages?", "chorizo", "hot ?dogs?",
    "meat", "meatballs?", "steaks?", "ground beef", "keema",
    # seafood
    "fish", "salmon", "tuna", "cod", "tilapia", "trout", "halibut", "mackerel",
    "anchov(?:y|ies)", "sardines?", "shrimps?", "prawns?", "crabs?",
    "lobsters?", "clams?", "mussels?", "oysters?", "scallops?", "squid",
    "calamari", "octopus", "caviar", "roe",
    # hidden animal products
    "gelatin(?:e)?", "lard", "suet", "tallow", "fish sauce", "oyster sauce",
    "worcestershire(?: sauce)?", "bone broth",
]
_EGG_TERMS = ["eggs?", "egg (?:whites?|yolks?)", "mayonnaise", "mayo", "meringue"]

# Checked first: phrases that contain a keyword but are vegetarian.
_EXCLUDE_TERMS = [
    "eggplants?", "egg-?free", "eggless", "crab ?apples?", "duck sauce",
    "vegetable (?:broth|stock)", "vegan", "veggie", "vegetarian",
    "imitation", "meatless", "plant[- ]based", "egg replacer",
]


def _compile(terms):
    return re.compile(r"\b(?:" + "|".join(terms) + r")\b")


_NON_VEG_RE = _compile(_NON_VEG_TERMS)
_EGG_RE = _compile(_EGG_TERMS)
_EXCLUDE_RE = _compile(_EXCLUDE_TERMS)

# Food.com tags that mark a recipe as containing meat/seafood.
MEAT_TAGS = {"meat", "poultry", "seafood", "pork", "beef", "chicken",
             "lamb-sheep", "fish", "shellfish", "turkey", "duck", "veal"}


def ingredient_diet(name: str) -> str:
    n = name.lower().strip()
    if _EXCLUDE_RE.search(n):
        return VEG
    if _NON_VEG_RE.search(n):
        return NON_VEG
    if _EGG_RE.search(n):
        return EGG
    return VEG


def recipe_diet(ingredients, tags=None) -> str:
    level = max((ingredient_diet(i) for i in ingredients), key=RANK.get, default=VEG)
    if tags and MEAT_TAGS & {t.lower() for t in tags}:
        return NON_VEG
    return level


_DIET_ALIASES = {
    "veg": VEG, "vegetarian": VEG,
    "egg": EGG, "eggetarian": EGG, "ovo": EGG,
    "non-veg": NON_VEG, "non_veg": NON_VEG, "nonveg": NON_VEG, "non-vegetarian": NON_VEG,
}


def normalize_diet(value: str) -> str | None:

    return _DIET_ALIASES.get(value.strip().lower())


def allowed_diets(preference: str) -> list[str]:

    level = normalize_diet(preference)
    if level is None:
        raise ValueError(f"Unknown diet preference: {preference!r}")
    return [d for d in (VEG, EGG, NON_VEG) if RANK[d] <= RANK[level]]
