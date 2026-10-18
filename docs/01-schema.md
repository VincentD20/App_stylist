# Schema

All primary keys are UUIDs (see ADR-001).

## Core tables

| Table | Columns | Notes |
|---|---|---|
| `users` | id, email (unique), username (unique), hashed_password | Never store the raw password |
| `items` | id, user_id, type_id, subtype_id (nullable), color, material (nullable), fit (nullable), image_url, status | `status`: pending / confirmed / failed |
| `outfits` | id, user_id, name (nullable) | Occasion is expressed through tags |
| `types` | id, name (unique) | Seeded once, no create endpoint |
| `subtypes` | id, name, type_id, created_by_user_id (nullable) | NULL creator = system default, visible to all users |
| `tags` | id, name, created_by_user_id (nullable) | Same pattern as subtypes; covers occasion/style (streetwear, casual, work, formal, sport) |
| `weather_conditions` | id, name (unique) | Seeded once, fixed list |

## Junction tables (many-to-many)

| Table | Columns |
|---|---|
| `item_tags` | item_id, tag_id |
| `item_weather` | item_id, weather_condition_id |
| `item_outfits` | outfit_id, item_id, layer |
| `outfit_tags` | outfit_id, tag_id |
| `outfit_weather` | outfit_id, weather_condition_id |

All junction tables use a composite primary key over their two foreign keys.

## Rules of thumb
- One value per item means a plain column. Multiple possible values means a junction table.
- Before adding a table, check whether the concept already exists under another name (occasion turned out to be tags).

## Cascade rules
- Deleting an **item** removes its rows in `item_tags`, `item_weather`, `item_outfits`.
- Deleting an **outfit** removes its rows in `item_outfits`, `outfit_tags`, `outfit_weather`.
- Deleting an outfit **never** deletes items, because an item can belong to many outfits.
- Implemented with `ondelete="CASCADE"` on the junction table foreign keys.

## Validation done in application code
- `subtype.type_id` must equal the item's `type_id`. Checked in the confirm endpoint, not in the database (see ADR-006).

## Open design point
- `outfit_tags` and `outfit_weather` start as a union of the item values when an outfit is created, but are stored, so the user can override them.
