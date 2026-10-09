# IDOR: reading another user's private profile note

**OWASP category:** A01:2021 – Broken Access Control (IDOR)

## How it works
Every user has a profile at `/profile/<id>` with a "Private note" marked "only
visible to <user>". The server does no access check: it never asks for a login and
never checks the profile is yours. So anyone, even a guest with no session, can open
any profile by its id and read the note. The `<id>` points straight to an object with
no ownership check. That is what makes it an Insecure Direct Object Reference (IDOR).

## How I exploited it
See `exploit.py`:
1. As a guest (no cookie), GET `/forum`. The author links point to profiles, e.g.
   `wil`, a staff member, at `/profile/k1asdfeditojrb4`.
2. GET each of those profiles with no session. One of them (wil's staff note) comes
   back with the flag.

No account needed. Logging in first works too but is not required, which makes it
worse than a normal IDOR.

## Impact
Anyone can read every user's private data, including higher-privilege accounts,
without even signing up. The same profile also shows emails and roles, which help
the reset takeover and other steps.

## How it could have been prevented
- Require a login, then check ownership on every request. The server must confirm
  the profile belongs to the logged-in user (or that the user is allowed) before
  returning private data.
- Do not show private fields to anyone but the owner.
- Random ids help a bit, but never rely on them for access control.
