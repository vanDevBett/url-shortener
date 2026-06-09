# ADR-001: Short code generation strategy

- **Status:** Accepted
- **Date:** 2026-06-08
- **Deciders:** vanDevBett

## Context

The shortener must turn a long URL into a short code (the trailing segment of
`domain.com/<code>`). The code must be:

- **Unique** (two different URLs cannot share a code).
- **Short** (ideally 6–7 characters).
- **Fast to generate** (creation must not do expensive work).
- Reasonably **hard to enumerate** (a third party should not be able to walk
  every link by incrementing the code).

With a Base62 alphabet (`[0-9a-zA-Z]`, 62 URL-safe symbols), a length `L`
provides `62^L` combinations: 6 characters ≈ 56.8 billion, 7 ≈ 3.5 trillion.
Length is not the problem; the generation strategy is.

## Considered alternatives

### A. Auto-increment ID + Base62 encoding *(chosen)*
Insert the row, let PostgreSQL return a sequential integer, and encode it in
Base62.
- ✅ Uniqueness guaranteed by the database (no collision checks).
- ✅ Codes are as short as possible; generation is trivially O(log n).
- ❌ Sequential, therefore **enumerable**, and it leaks the total link count.
- ❌ A single counter becomes a coordination point across multiple databases.

### B. Random code + collision check
Generate N random characters and verify against the database, retrying on
conflict.
- ✅ Not enumerable; does not leak the count.
- ❌ Extra read on every creation; collisions (and retries) grow as the space
  fills up (birthday problem).

### C. Truncated URL hash (e.g. SHA-256)
- ✅ Deterministic; the same URL maps to the same code (free deduplication).
- ❌ Truncation causes collisions between different URLs; "same URL = same
  code" prevents per-user analytics.

### D. Pre-generated key pool (Key Generation Service)
A separate service pre-generates unique keys into a pool the app draws from.
- ✅ The standard large-scale answer; no collisions or request-time coordination.
- ❌ Unnecessary operational complexity at this stage.

## Decision

We adopt **Strategy A (auto-increment ID + hand-written Base62)**. It is the
simplest correct option for the MVP and lets us learn base conversion without
relying on a library.

To avoid overly short, guessable codes for the first IDs (e.g. `id=5` -> `"5"`),
the ID sequence will start at an **offset** (`62^5`) so even the first link has
at least 6 characters.

## Consequences

- **Positive:** minimal implementation, no collisions, fully owned code.
- **Negative / accepted debt:** codes are enumerable. We accept this weakness
  deliberately for the MVP.

## Planned mitigation (future ADR)

Replace direct ID encoding with a **reversible multiplicative permutation**:
pick a secret multiplier `a` coprime with `M = 62^L`, encode `(id * a) mod M`,
and decode with the modular inverse of `a`. This keeps the bijection
(uniqueness) while scrambling the output, removing enumeration without
collision checks. Alternative: a library such as Sqids/Hashids.