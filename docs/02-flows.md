# Flows

## 1. Item upload and confirm

```
POST /items/upload
  1. Rate-limit check (Redis)
  2. Validate file: size limit, then magic-byte check (python-magic)
  3. Save image to S3
  4. Create items row with status = pending
  5. Call vision LLM with constrained prompt (type and color from allowed lists)
  6. Parse JSON; on failure, retry up to N times
  7. Success: return predictions
     All retries fail: status = failed, return empty predictions

PATCH /items/:id/confirm
  1. User submits corrected type, subtype, color, material, fit, tags, weather
  2. Validate subtype.type_id == type_id
  3. status = confirmed
```

- Auto-detected: `type`, `color`. Entered by the user: `material`, `fit`.
- The review step is the safety net for wrong predictions, so there is no confidence-score logic.
- Stale `pending` items (older than about 24 hours) are removed by a scheduled cleanup job.
- A `failed` item uses the same review screen, just with empty predictions.

## 2. Outfit suggestion

```
GET /outfits/suggest?weather=cold&occasion=work
  1. Filter confirmed items by weather and tag (DB query)
  2. Generate combinations: 1 top + 1 bottom + 1 shoe, optional extra layers
  3. Score each combination by shared tags (in memory)
  4. Take the top N by tag score
  5. Send only those N to the LLM for a color-harmony score (1-10)
  6. AI succeeded: rank by combined score
     AI failed: fall back to tag-score ranking
  7. Return ranked list; user picks one and may save it
```

Principle: cheap filtering first, expensive AI call last, and the AI only enhances the ranking and is never required for it.

## 3. Authentication

```
POST /auth/register
  hash password, create user, return JWT (auto-login)

POST /auth/login
  verify password hash, return JWT

Protected routes
  dependency: read Authorization: Bearer <token>
  -> verify signature -> check exp -> extract user_id from "sub"
```

- JWT payload: `sub` (user UUID) and `exp`. Nothing sensitive goes in the payload, because it is readable.
- Access token lifetime is about 7 days, with no refresh flow (see ADR-005).
- Passwords are hashed with bcrypt, using the library's verify function.

## 4. Upload security and cost control
- File size limit and magic-byte validation happen before anything reaches S3 or the LLM.
- Rate limit on uploads: Redis counter at `rate_limit:upload:{user_id}`, TTL about 1 hour, reject with 429 above the limit.
