import pytest

from src.diet import EGG, NON_VEG, VEG, allowed_diets, ingredient_diet, normalize_diet, recipe_diet


@pytest.mark.parametrize("name, expected", [
    # plain cases
    ("chicken breast", NON_VEG),
    ("ground beef", NON_VEG),
    ("prawns", NON_VEG),
    ("eggs", EGG),
    ("egg yolks", EGG),
    ("paneer", VEG),
    ("onion", VEG),
    # false-positive traps
    ("eggplant", VEG),
    ("graham crackers", VEG),
    ("champagne", VEG),
    ("crab apples", VEG),
    ("duck sauce", VEG),
    ("vegetable broth", VEG),
    ("vegan sausage", VEG),
    ("imitation crab", VEG),
    ("eggless mayonnaise", VEG),
    ("minced garlic", VEG),
    # hidden animal products
    ("fish sauce", NON_VEG),
    ("gelatin", NON_VEG),
    ("worcestershire sauce", NON_VEG),
    ("chicken stock", NON_VEG),
    ("lard", NON_VEG),
    ("mayonnaise", EGG),
])
def test_ingredient_diet(name, expected):
    assert ingredient_diet(name) == expected


def test_recipe_takes_highest_level():
    assert recipe_diet(["rice", "onion"]) == VEG
    assert recipe_diet(["flour", "eggs", "sugar"]) == EGG
    assert recipe_diet(["eggs", "bacon", "bread"]) == NON_VEG


def test_meat_tag_overrides_ingredients():
    assert recipe_diet(["rice", "spices"], tags=["main-dish", "chicken"]) == NON_VEG


def test_empty_recipe_is_veg():
    assert recipe_diet([]) == VEG


def test_allowed_diets():
    assert allowed_diets("veg") == [VEG]
    assert allowed_diets("egg") == [VEG, EGG]
    assert allowed_diets("non_veg") == [VEG, EGG, NON_VEG]


@pytest.mark.parametrize("raw, expected", [
    ("veg", VEG), ("Vegetarian", VEG),
    ("egg", EGG), ("Eggetarian", EGG),
    ("non-veg", NON_VEG), ("Non_Veg", NON_VEG), ("nonveg", NON_VEG),
    ("pescatarian", None),
])
def test_normalize_diet(raw, expected):
    assert normalize_diet(raw) == expected


def test_allowed_diets_rejects_unknown():
    with pytest.raises(ValueError):
        allowed_diets("carnivore")
