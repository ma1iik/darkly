# Weak JWT secret to token forgery

**OWASP category:** A02:2021 – Cryptographic Failures (also A07 auth failures)

## How it works
The session cookie is a JWT signed with HS256. Its safety depends only on a secret
key that the server keeps. Here the secret is a short, guessable word (`42network`),
so it cracks offline in seconds with a wordlist. The same value also leaks in two
places we saw earlier: the deploy-log comment in the page source ("jwt secret was
42, wil changed it to 42network", breach 01), and `/internal/config`, read through
the XXE in breach 12. Once you know the secret, you can forge a token with any
claims you want. The token can no longer prove who you are or your role.

## How I exploited it
See `exploit.py`:
1. Log in normally and capture the signed JWT.
2. Take the secret straight from the leak: it is in the deploy-log comment in the
   page source (`42network`, breach 01). No guessing needed. To be sure it is the
   real one, I re-sign my captured token with it and check the signature matches.
3. Forge a new token with any claims (e.g. `sub` of another user, `role:staff`) and
   sign it with that secret.
4. The server accepts the forged token (valid signature), so we can impersonate any
   account, including staff/god ones that log in via SSO and have no password to
   reset.

(It is also short enough to fall to an offline wordlist in seconds even if it had not
leaked, but since it leaked there is no reason to brute force it.)

## Impact
Full auth bypass and impersonation. You can make a token for any user id and any
role, with no credentials. Note: on this build the server checks the signature but
does not gate extra pages on the token's `role`, and the profile UI reads the role
from the database.

## How it could have been prevented
- Use a long, random signing secret (32+ random bytes), never a word.
- Keep the secret out of code, configs, and any client-visible hint.
- Rotate the secret and invalidate old tokens if you suspect it leaked.
- Prefer asymmetric signing (RS256) so the verifier cannot also make tokens.
