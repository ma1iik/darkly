# Broken Access Control: Staff area open to anyone

**OWASP category:** A01:2021 – Broken Access Control

## How it works
The `/staff` page is only for staff and admins. The site "hides" it by keeping it
out of the menu and putting it under `Disallow` in `robots.txt`. Hiding a URL does
not protect it. The server never checks who is asking before it serves the page.
Any visitor who knows the path `/staff`, or reads it in `robots.txt`, gets the full
staff area with no login.

This is broken access control. The app does not enforce authorization on a
protected page.

## How I exploited it
1. Read `robots.txt`: it lists `Disallow: /staff`, a hidden page.
2. GET `/staff` as a guest, no cookie, no login (see `exploit.py`).
3. The server replied `200 OK` and returned the private "Staff area" page, with an
   internal dashboard and a "Platform status" panel.

## Impact
- Internal content is shown to the public.
- The page leaks more attack surface (a second service on port 8090, unrestricted
  file uploads, an unsafe XML parser, a `PATCH /api/profile` hint). These lead to
  bigger breaches later.

## How it could have been prevented
- Enforce authorization server-side on every protected route. Check that the user
  is logged in and has the staff role before returning the page.
- Do not use obscurity (hidden links, `robots.txt`) as security. `robots.txt` is
  public and only talks to search engines.
- Deny by default. A route should need an explicit permission to be reachable.
