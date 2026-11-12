# Recipe Builder

A REST API that suggests recipes based on the ingredients a user has at home, filtered by their diet.
Built with FastAPI and PostgreSQL as part of the Tektalis FDE training.

There is no UI yet. The API can be used through Swagger (`/docs`) or the Postman collection in `postman/`.

## Tech stack

- FastAPI for the API
- PostgreSQL as the database
- SQLAlchemy (ORM) for data access and Alembic for migrations
- bcrypt for password hashing, JWT for login tokens
- Pydantic for request and response validation

## Project structure

The app follows MVC, with the model side split into a service layer and a DAO layer.

```
app/
  main.py          creates the FastAPI app and registers the routers
  controllers/     routes - handle the HTTP request and response
  dto/             request and response shapes (Pydantic)
  services/        business logic and rules
  dao/             database access, one file per table group
  models/          SQLAlchemy models (the tables)
  core/            config, read from .env
alembic/           database migrations
fixtures/          recipe and ingredient data, plus the seed script
postman/           Postman collection
tests/             unit tests
docs/              requirements and notes
```

A request goes controller -> service -> DAO -> database, and each layer only talks to the one below it.
Controllers deal with HTTP, services deal with the rules, and only the DAO layer touches the database.

## Database

Ten tables, managed through Alembic migrations:

- `user`, `user_profile` (one-to-one), `allergen`
- `user_allergen` - many-to-many between users and allergens
- `ingredient`, `recipe`, `recipe_steps`
- `recipe_ingredient` - many-to-many between recipes and ingredients, also storing quantity and unit
- `pantry_item`, `cook_log`

Data a user owns (profile, pantry, cook history) is deleted with the user. Shared data like ingredients
and recipes can't be deleted while something still refers to it.

The seed data has 73 ingredients and 30 recipes. A recipe's diet comes from its strictest ingredient
(any meat or fish makes it non-veg, otherwise egg makes it egg, otherwise veg). Complexity is based on
steps and total time: easy is 5 steps or fewer and 30 minutes or less, hard is 9 or more steps or over
60 minutes, and everything else is medium.

## Running it locally

You need Python 3.12+ and PostgreSQL.

1. Create the database and a user for it:
   ```
   psql postgres -c "CREATE ROLE your_user WITH LOGIN PASSWORD 'your_password';"
   psql postgres -c "CREATE DATABASE recipe_keeper OWNER your_user;"
   ```
2. Set up the environment:
   ```
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   cp .env.example .env
   ```
   Then fill in `.env`. For `JWT_SECRET_KEY`, generate a value with
   `python -c "import secrets; print(secrets.token_hex(32))"`.
3. Create the tables and load the data:
   ```
   alembic upgrade head
   python -m fixtures.seed
   ```
4. Start the API:
   ```
   uvicorn app.main:app --reload
   ```
   Swagger is at http://127.0.0.1:8000/docs.

## Endpoints

| Method | Path | Login needed | What it does |
|---|---|---|---|
| POST | /auth/signup | no | Create an account |
| POST | /auth/login | no | Log in, returns a JWT |
| GET | /auth/me | yes | Current user |
| GET | /profile | yes | Your diet and allergens |
| PUT | /profile/diet | yes | Change diet (veg, egg, non_veg) |
| GET | /allergens | no | List of allergens |
| POST | /profile/allergens/{id} | yes | Add an allergen to your profile |
| DELETE | /profile/allergens/{id} | yes | Remove an allergen |
| GET | /recipes | no | List recipes, optional `diet_type` and `cuisine` filters |
| GET | /recipes/{id} | no | One recipe with ingredients and steps |

For routes that need a login, log in first and send the token as `Authorization: Bearer <token>`.
In Swagger, use the Authorize button.

## Testing

The API has been tested manually through Swagger and Postman. The Postman collection is in `postman/`.
Unit tests for the diet logic can be run with:

```
pytest
```

## Status

Done: auth, profile, recipes, migrations and seed data.

Next: pantry, recipe suggestions from the pantry, and Docker.
