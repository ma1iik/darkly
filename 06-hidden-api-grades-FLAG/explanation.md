# Hidden / unprotected API endpoint

**OWASP category:** A01:2021 – Broken Access Control

## How it works
`/api/grades` is not linked anywhere in the UI, so it looks hidden. But there is no
real check behind it. Any logged-in user can request it directly and get the data
plus a flag. Hidden is not the same as protected.

## How I found it
Two ways:
1. `robots.txt` lists `/api/grades` as `Disallow`, so it points right at it.
2. Even without that, you can brute force the paths. `/api/grades` returns 302 (it
   exists, it just wants a login), while junk paths return 404. So a short loop over a
   wordlist, or a tool like gobuster (`gobuster dir -u <url> -w wordlist.txt -b 404`),
   finds it.

## How I exploited it
See `exploit.py`:
1. As a guest, `GET /api/grades` returns 302: the endpoint exists but wants a login.
2. Log in as a normal student (no cadet or staff role) and `GET /api/grades` again.
   Now it returns the data and the flag. A plain student reaches it, and that is the bug.

## Impact
Any logged-in user reads data the app thought was hidden. Here it is grades.
Treating unlisted routes as safe hides a lot more.

## How it could have been prevented
- Check the role or ownership on every endpoint, not just whether the URL is known.
- Deny by default. A route with no access rule should reject.
