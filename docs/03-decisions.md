# Architecture Decisions

Format: decision, why, tradeoff. Add new entries at the bottom.

## ADR-001: UUID primary keys instead of auto-increment integers
- **Decision:** All tables use UUID primary keys.
- **Why:** Integer IDs are guessable (`/items/42` then `/items/43`). If an ownership check is ever forgotten in one route, UUIDs still block casual enumeration (defense in depth).
- **Tradeoff:** Slightly larger storage and indexes, harder to read when debugging.

## ADR-002: No RBAC, ownership checks only
- **Decision:** No roles or permissions table. Authentication via JWT, authorization via one rule: a user can only access rows with their own `user_id`.
- **Why:** All users have identical permissions and there is no shared or cross-user data, so no action exists that one user may do and another may not.
- **Tradeoff:** If an admin role is ever needed, I'd add a role column, put it in the token, and add a permission-check dependency and tests per role.

## ADR-003: Vision LLM instead of a custom-trained model
- **Decision:** Classify clothing type and color by calling a multimodal LLM with a constrained JSON prompt.
- **Why:** Training a model needs a large labeled dataset, GPUs and ML expertise. An LLM gets an end-to-end MVP working quickly, and structured-output extraction is a skill reused in the next projects. The provider SDK is only imported in `services/vision.py`, so it can be swapped.
- **Tradeoff:** Higher cost per call than a dedicated classifier, and dependence on an external API. Can be replaced by a fine-tuned model later.

## ADR-004: Two-step upload with a `status` flag instead of temporary storage
- **Decision:** Upload saves the image to permanent storage immediately and creates an item with `status = pending`. A separate confirm endpoint sets `confirmed`. A scheduled job deletes stale `pending` items.
- **Why:** One storage path, no move operation, and orphaned files become a simple query. Keeps junk out of confirmed data.
- **Tradeoff:** Unconfirmed files briefly occupy storage until the cleanup job runs.

## ADR-005: Long-lived access token, no refresh flow
- **Decision:** A single JWT access token valid for about 7 days.
- **Why:** The project is single-user in scope, so refresh-token rotation adds complexity without meaningfully reducing risk here.
- **Tradeoff:** A leaked token stays valid longer. A production app with real users would use short-lived tokens plus refresh rotation.

## ADR-006: Type/subtype consistency validated in application code
- **Decision:** The confirm endpoint checks that `subtype.type_id == item.type_id`. There is no database-level constraint.
- **Why:** A mismatch only causes a wrong filter option in the UI (low severity), while a composite-key or trigger solution is awkward to build and maintain.
- **Tradeoff:** Any new code path that writes items must remember the check.

## ADR-007: `types` and `weather_conditions` as seeded tables, `status` as an Enum
- **Decision:** `types` and `weather_conditions` are lookup tables seeded once, with no create endpoint. `items.status` stays a database Enum.
- **Why:** `subtypes` needs a real foreign key to `types`, which an Enum can't provide, and one relational pattern is simpler than three. `status` is internal application state, not a domain concept anyone browses.
- **Tradeoff:** Queries involving type need a join, and the "fixed" guarantee comes from not exposing an endpoint, not from the database.

## ADR-008: FastAPI runs locally, only Postgres runs in Docker (for now)
- **Decision:** `uvicorn --reload` locally, Postgres via `docker compose`.
- **Why:** Hot reload gives the fastest feedback loop during development, and Postgres is the part worth containerizing.
- **Tradeoff:** Dev is less production-like. FastAPI gets containerized when CI/CD and deployment are set up.

---

## Template for new entries
```markdown
## ADR-00X: <short title>
- **Decision:** what you chose
- **Why:** the reason, in 1-2 lines
- **Tradeoff:** what you gave up or risk
```
