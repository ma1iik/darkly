# Cross-Site Request Forgery (no Origin/Referer validation)

**OWASP category:** A01:2021 – Broken Access Control

## How it works
`POST /profile/me/settings` changes account data. It has no CSRF token and never
checks the `Origin` or `Referer` header. The server acts on any request that carries
the session cookie, whoever sent it. So a forged request from another origin is
accepted.

## How I exploited it
1. Log in to get a session cookie.
2. `POST /profile/me/settings` with `Origin: https://evil.com` (a domain we don't
   own) and the profile fields.
3. The server accepts it and returns the flag in the redirect instead of rejecting
   the cross-origin request.

## Impact
An attacker's page can make a logged-in victim's browser change the victim's account
settings (email and other fields) without them knowing. Account takeover with no
stolen password or token.

## How it could have been prevented
- Use a per-session CSRF token on every state-changing request and check it.
- Validate `Origin`/`Referer` against an allow-list on the server.
- Set the session cookie `SameSite=Strict` (or Lax) so the browser does not send it
  cross-site.
