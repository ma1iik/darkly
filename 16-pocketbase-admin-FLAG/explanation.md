# PocketBase admin takeover via leaked credentials

**OWASP category:** A05:2021 – Security Misconfiguration / A07 Auth Failures

## How it works
PocketBase, the backend database, has an admin panel at `/_/` on port 8090 (listed
as `Disallow: /_/` in robots.txt). Its superuser credentials leaked in
`/internal/config`, which we read through the XXE to SSRF breach (12). With those
credentials we log into the PocketBase admin API and get full read/write on every
collection, including `internal_audit`, which stores a flag.

## How I exploited it
See `exploit.py`:
1. Use the leaked creds (`admin@42network.local` / `Darkly42Admin!`).
2. POST to `:8090/api/admins/auth-with-password` to get an admin token.
3. GET `/api/collections/internal_audit/records` and read the flag from the audit
   note.

(In a browser do same at `http://<vm>:8090/_/`.)

## Impact
Full compromise of the database: read and change every user, grade, post, and
config. An attacker can create accounts, change grades, or read all the data.

## How it could have been prevented
- Never store admin credentials in a reachable config endpoint (and fix the XXE that
  exposed it).
- Don't expose the PocketBase admin panel to the network. Bind it to localhost or
  put it behind a VPN/allow-list.
- Use strong, unique admin credentials and rotate any that may have leaked.
