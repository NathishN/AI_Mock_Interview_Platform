# InterviewAce AI — Phase 1: Backend foundation

FastAPI + PostgreSQL + Alembic + JWT auth, with the **complete database schema** for all later phases
(questions, rubrics, interview sessions/turns, HR answer drafts).

## Run with Docker

```bash
cp .env.example .env        # set POSTGRES_PASSWORD and JWT_SECRET_KEY (+ optional admin)
docker compose up --build
```

API docs: http://localhost:8000/docs (disabled when `ENVIRONMENT=production`).
On startup the container runs `alembic upgrade head`, then `python -m app.scripts.bootstrap`
(default rubrics, optional admin; idempotent, never overwrites edited rubrics).

## Run tests (no Postgres needed; tests use in-memory SQLite)

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
pytest
```

## API (prefix `/api/v1`)

| Method | Path | Auth | Purpose |
|---|---|---|---|
| GET | `/health`, `/health/ready` | – | Liveness / DB readiness |
| POST | `/auth/register`, `/auth/login` | – | Returns user + access/refresh tokens |
| POST | `/auth/refresh` | refresh token | New token pair |
| GET | `/auth/me` | user | Current user |
| GET/PUT | `/profile/me` | user | Onboarding fields; PUT is partial |
| GET | `/questions` | user | Filters: `category, difficulty, role, stage, tag, q`, paging |
| GET | `/questions/summary`, `/questions/{id}` | user | Counts / single question |
| POST | `/admin/questions/import` | admin | Atomic bulk import/upsert (how the 500 questions get loaded) |
| POST/PUT/DELETE | `/admin/questions[/{id}]` | admin | Create / edit / soft-delete |
| GET/PUT | `/admin/rubrics[/{key}]` | admin | Rubrics; weights must sum to 100 |

## Design decisions

- **Schema:** `questions` (string IDs like `hr-001`, unique normalised-text hash to block duplicates),
  `rubrics` (configurable weighted dimensions), `interview_sessions` + `interview_turns`
  (state persisted per turn, evaluation JSON, latency/tokens/attempts/error columns that never hold answer text),
  `hr_answer_drafts` (user-supplied facts only). JSONB on PostgreSQL, JSON on SQLite.
- **Categories and stages are strings validated in code**, so adding questions never needs a migration.
- **Question import is all-or-nothing** and reports every problem by index.
- **Auth:** bcrypt, short-lived access token + refresh token, token type enforced, constant-time-ish login for unknown emails.
- **Production guard:** the app refuses to start in production with a weak `JWT_SECRET_KEY`.

## Known limitations (deliberate, for later)

- Refresh tokens are stateless: no server-side revocation/logout yet (add a `jti` denylist table).
- No login rate limiting; put the API behind a reverse proxy with rate limits, or add a limiter in phase 5.
- Passwords reset / email verification not implemented.
- The Postgres path was verified by rendering the migration SQL (JSONB/UUID) and running migrations and tests on SQLite;
  run `docker compose up` once locally to confirm against a real Postgres.

---

# Phase 2: Knowledge base (in progress)

**Status: Category A (HR) and B (Behavioral) complete, 160 / 500.** The other six categories are added the same way.

## Layout

```
backend/data/src/<category>/_defaults.json   id prefix, category, target count, default roles/stages/criteria
backend/data/src/<category>/NN.json          compact records (q, sub, d, ans, kp, cm, fu, tags)
backend/data/questions_seed.json             GENERATED, importable seed with full records
```

IDs are assigned in file order (`hr-001`, `hr-002`, ...). **Only append; never reorder or delete**,
because interview history references IDs. Retire a question through the admin API (soft delete).

## Commands (run from `backend/`)

```bash
python -m app.scripts.kb build            # expand sources -> seed JSON (refuses to write if validation fails)
python -m app.scripts.kb validate         # validate the seed file
python -m app.scripts.kb build --strict   # must be exactly 500, with the exact per-category counts
python -m app.scripts.kb seed             # insert missing questions into the DB
python -m app.scripts.kb seed --update    # also overwrite existing ones
```

Docker start-up runs `kb seed` (insert-only, so admin edits survive restarts). Set `SEED_QUESTIONS=false` to skip.
Questions can also be added at runtime with `POST /api/v1/admin/questions/import`, no code change needed.

## Automatic checks

Schema validation (required fields non-empty, valid category/difficulty/stage), unique IDs, exact-duplicate
and near-duplicate detection (token overlap), per-category count limits, strict 500 total, and warnings for thin
answers or personal-experience answers without a clearly labelled *illustrative* example.

The collection is described as curated and commonly encountered, not a statistically ranked "top 500".
