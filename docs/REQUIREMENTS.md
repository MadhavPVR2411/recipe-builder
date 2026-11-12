# Recipe Book — Project Requirements

Source: Tektalis training meeting, 26 Oct 2026.
Status: **Kick-off by Wednesday 28 Oct 2026.**

## 1. Scope

The Recipe Book project covers the full cycle: **user study → build → testing → deployment**.
It recommends recipes from the ingredients a user has, filtered by diet (veg / egg / non-veg),
allergies and favourite cuisines, and ranked by pantry match and cooking complexity.

## 2. Requirements from the meeting

| # | Requirement | Notes |
|---|---|---|
| R1 | User study, testing and deployment | Each phase is a deliverable, not an afterthought |
| R2 | **FastAPI** as the API layer | Priority 1 |
| R3 | **Database** (PostgreSQL) | Priority 2 |
| R4 | **Docker** deployment | App + Postgres containers |
| R5 | **Kubernetes** must be looked at for Docker | At minimum a study + basic manifests |
| R6 | Proper documentation, as in a full-scale project | See §5 |
| R7 | File-system storage not important | Persistence goes through the database |
| R8 | No UI for now | API only |
| R9 | Manual API testing with **Postman** | Commit an exported collection |
| R10 | Automation tests with **Playwright** | Playwright's API testing (`APIRequestContext`) |
| R11 | **MVC architecture** is a must | With design principles and a design workflow |
| R12 | **DAO** and **DTO** layers | Noted as "Dao, Deo" — confirm DTO with mentor |
| R13 | Programme length | Noted as "8 - 1- weeks" — confirm with mentor |

## 3. Starting point (Stage 1) vs. target
 
| Area | Today (Stage 1) | Target |
|---|---|---|
| Interface | CLI (`main.py`) | FastAPI REST endpoints, no UI |
| Data access | `Repository` class with raw SQL | DAO per entity (`RecipeDAO`, `IngredientDAO`, `UserProfileDAO`, `PantryDAO`) |
| Data transfer | Dataclasses in `src/models.py` | Pydantic DTOs for requests/responses, separate from DB models |
| Business logic | `src/services/` (filter, match, scoring, diet) | Kept as the service layer, reused by controllers |
| Architecture | Layered, but CLI mixes input + flow | MVC: Model (entities + DAO), View (JSON/DTOs), Controller (FastAPI routers) |
| Tests | 44 pytest unit tests | Unit (pytest) + API automation (Playwright) + Postman collection |
| Deployment | Local Postgres via Homebrew | `Dockerfile`, `docker-compose.yml`, Kubernetes manifests |
| Data | 6 hand-written seed recipes | Food.com Kaggle subset with computed diet + complexity |

## 4. Proposed structure (MVC + DAO/DTO)

```
app/
  main.py              # FastAPI app factory
  controllers/         # Controllers: FastAPI routers (recipes, pantry, profiles)
  dto/                 # View layer: Pydantic request/response schemas
  models/              # Domain entities
  dao/                 # Data access objects (one per table)
  services/            # Business logic: diet, filter, match, scoring
  db.py                # Connection pool / transaction handling
tests/
  unit/                # pytest
  api/                 # Playwright API tests
postman/               # Exported Postman collection
deploy/
  Dockerfile
  docker-compose.yml
  k8s/                 # Deployment, Service, ConfigMap, Secret
docs/
```

## 5. Documentation set

- `README.md`: setup, running, testing
- `docs/REQUIREMENTS.md`: this file
- `docs/ARCHITECTURE.md`: MVC layers, DAO/DTO responsibilities, request flow diagram
- `docs/API.md`: endpoints, request/response examples (plus FastAPI's `/docs`)
- `docs/DATABASE.md`: ER diagram, table definitions, diet classification rules
- `docs/TESTING.md`: test strategy, how to run pytest / Playwright / Postman
- `docs/DEPLOYMENT.md`: Docker and Kubernetes steps
- `docs/USER_STUDY.md`: target users, questions, findings
- `CHANGELOG.md`: per-stage changes

## 6. Open questions

- Does "Deo" mean DTO? (Resolved: yes, DTOs are in `app/dto/`.)
- Is the programme 8 weeks, 10 weeks, or 8–10 weeks?
- Is Kubernetes expected to be deployed, or only studied for this phase?

## 7. Decisions

- R10: manual testing through Swagger and Postman was agreed with the manager. Playwright is deferred.
- The database layer uses SQLAlchemy ORM with Alembic migrations instead of hand-written SQL files.
- MVP scope: auth, profile, recipes, pantry, suggestions and Docker. Cooking, expiry alerts and
  allergen filtering in suggestions come after.

## 8. Progress

1) The recipe database schema has been built.
2) Authentication layer started on 2-11-2026, with bcrypt passwords and JWT tokens.
3) Moved to SQLAlchemy ORM and Alembic, with many-to-many relations for user allergens and recipe ingredients.
4) Profile (diet and allergens) and Recipes (list, filter, detail) are done. Seed data: 73 ingredients, 30 recipes.