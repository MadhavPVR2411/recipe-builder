# Recipe Builder

An app that suggests recipes based on the ingredients a user has at home, filtered by their diet.
FastAPI and PostgreSQL on the backend, React on the frontend. Built as part of the Tektalis FDE training.

## Tech stack

- FastAPI for the API, Pydantic for request and response validation
- PostgreSQL, with SQLAlchemy (ORM) and Alembic for migrations
- bcrypt for password hashing, JWT for login tokens
- React + Vite for the frontend, styled with Tailwind
- Docker Compose to run the API and database together

## Project structure

The backend follows MVC, with the model side split into a service layer and a DAO layer.

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
frontend/          React app (one folder per screen in src/)
postman/           Postman collection
tests/             unit tests
docs/              requirements and notes
```

A request goes controller -> service -> DAO -> database, and each layer only talks to the one below it.
Controllers deal with HTTP, services deal with the rules, and only the DAO layer touches the database.

The frontend is split the same way by feature: `auth/`, `pantry/`, `suggestions/`, `recipes/` and
`profile/`, with all API calls going through `src/api.js`.

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

## Suggestions

`GET /suggestions` compares the user's pantry with every recipe their diet allows and returns two lists:

- `can_make` - every ingredient is in the pantry
- `missing_one` - exactly one ingredient is missing, along with its name

Veg users only see veg recipes, egg users see veg and egg, and non-veg users see everything.
Pantry items with a quantity of 0 don't count.

## Running with Docker

You need Docker Desktop running.

```
cp .env.example .env
```

Fill in `.env` (see below for `JWT_SECRET_KEY`), then:

```
docker compose up --build
```

This starts Postgres, runs the migrations, loads the seed data and starts the API.
Swagger is at http://localhost:8001/docs.

`docker compose down` stops everything and keeps the data. `docker compose down -v` also deletes the database.

## Running locally

You need Python 3.12+, PostgreSQL and Node 20+.

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
5. In a second terminal, start the frontend:
   ```
   cd frontend
   npm install
   npm run dev
   ```
   Open http://localhost:5173. Vite forwards the API calls to port 8000.

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
| GET | /pantry | yes | Your pantry items |
| POST | /pantry | yes | Add an item (ingredient name, quantity, unit, optional expiry date) |
| PATCH | /pantry/{id} | yes | Update quantity, unit or expiry date |
| DELETE | /pantry/{id} | yes | Remove an item |
| GET | /suggestions | yes | Recipes you can make, and ones missing a single ingredient |

For routes that need a login, log in first and send the token as `Authorization: Bearer <token>`.
In Swagger, use the Authorize button. Tokens expire after `JWT_EXPIRE_MINUTES` (60 by default).

## Testing

The API has been tested manually through Swagger and Postman. The Postman collection is in `postman/`.
Unit tests for the diet logic can be run with:

```
pytest
```

The frontend can be linted with `npm run lint` inside `frontend/`.

## Status

Done: auth, profile, recipes, pantry, suggestions, migrations and seed data, Docker for the API and
database, and a React frontend for all of the above.

Next: serving the React build from Docker, an ingredient dropdown in the pantry with units tied to each
ingredient, and allergen filtering in suggestions. Later: cooking a recipe (taking the quantities out of
the pantry) and expiry alerts.
