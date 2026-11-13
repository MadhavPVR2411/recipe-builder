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

