# Information Disclosure: server leaks its stack and internals

**OWASP category:** A05:2021 – Security Misconfiguration (information disclosure)

## How it works
The app sends back headers and content that show how it is built and what runs
behind it. None of it is secret, but it gives an attacker a free map: exact versions
to look up exploits for, where the backend is, and more hidden paths to try.

## What is leaked
From the HTTP response headers (e.g. on `/api/profile`):

| Source | Leak | Why it helps an attacker |
|--------|------|--------------------------|
| `X-Powered-By: Python/3.11 FastAPI/0.104` | exact framework + version | look up version-specific vulns |
| `Server: uvicorn/0.24.0 Linux` | web server + version, OS | narrows known exploits |
| `X-Pocketbase: http://localhost:8090` | a second backend service | new attack surface on port 8090 |
| `X-42-Internal: campus=paris` | a custom internal header exposed publicly | internal detail that should not ship |

More leaks:
- `robots.txt` lists private paths (`/admin`, `/staff`, `/internal`, `/backup`,
  `/api/grades`, `/internal/config`, ...). A list of the hidden areas.
- The `/staff` "Platform status" panel prints config: unrestricted file uploads,
  an unsafe XML parser, and `session cookie httponly=false`.

## How I exploited it
1. GET `/api/profile`, read the response headers.
2. Keep only the revealing headers (see `exploit.py`).
3. GET `/robots.txt` for the hidden paths.

## Impact
On its own it breaks nothing, but it makes an attack faster. Version numbers point
to known exploits. `robots.txt` shows where to look. The config panel confirms
which other bugs (uploads, XXE, XSS from `httponly=false`) are worth trying.

## How it could have been prevented
- Remove or override identifying headers (`Server`, `X-Powered-By`) in production.
- Do not send custom internal headers (`X-42-Internal`, `X-Pocketbase`) to clients.
- Do not show config or status on a page anyone can reach.
- Put only what you need in `robots.txt`. Protect sensitive routes with real
  authorization, do not just list them.
