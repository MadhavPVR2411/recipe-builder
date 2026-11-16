class ServiceError(Exception):
 pass


class UsernameAlreadyExistsException(ServiceError):
 pass


class InvalidCredentialsException(ServiceError):
 pass


class AllergenNotFoundException(ServiceError):
 pass

class RecipeNotFoundException(ServiceError):
 pass

class PantryItemNotFoundException(ServiceError):
 pass


class IngredientNotFoundException(ServiceError):
 pass


class InvalidUnitException(ServiceError):
 def __init__(self, unit: str, allowed: list[str]):
  self.allowed = allowed
  super().__init__(f"Unit '{unit}' not allowed, use one of: {', '.join(allowed)}")

