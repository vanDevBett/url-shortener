# ADR-002: Assigning short codes via sequence pre-allocation

- **Status:** Accepted
- **Date:** 2026-06-10
- **Deciders:** (your name)

## Context

ADR-001 chose `short_code = Base62(id)`. But the `id` is assigned by the
database on insert, while `short_code` is `NOT NULL`. This creates a
chicken-and-egg problem: we need the `id` to build the code, but the `id` does
not exist until the row is inserted.

## Considered alternatives

### A. Sequence pre-allocation *(chosen)*
Reserve the next `id` from the table's sequence (`nextval`) *before* inserting,
encode it with Base62, and insert a complete row using that explicit `id`.
- ✅ Keeps `short_code` `NOT NULL` (the schema invariant holds).
- ✅ The code stays exactly equal to the row's primary key.
- ✅ A single `INSERT`.
- ❌ One extra round-trip (`nextval`) before the insert.
- ❌ Couples to PostgreSQL (`pg_get_serial_sequence`).

### B. Two-phase insert
Insert with a `NULL` `short_code`, flush to obtain the `id`, then update the
row with the encoded code.
- ❌ Requires making `short_code` nullable, weakening the schema invariant for a
  value that is in fact never null after creation.

## Decision

We adopt **Strategy A (sequence pre-allocation)**. The repository exposes
`reserve_next_id()` (a `nextval` on the column's sequence) and `create()`
accepts an explicit `link_id`. The service reserves the id, encodes it, and
persists a complete row.

## Consequences

- **Positive:** clean invariant, code equals the primary key, single insert.
- **Negative:** an extra query per creation and a PostgreSQL-specific call.

## Follow-up

The `62^5` offset from ADR-001 (so the first code has at least 6 characters)
will be applied to the sequence's start value in the upcoming Alembic migration.