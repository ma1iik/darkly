# XXE to SSRF via the agenda XML importer

**OWASP category:** A05:2021 – Security Misconfiguration (XXE) → SSRF (A10)

## How it works
The agenda importer parses our XML with a parser that resolves external entities
(`xml.etree` without `defusedxml`). The parser fetches the entity content and puts
it inside the document. `file://` is blocked here, but `http://` works. So this
turns into server-side request forgery: the server makes HTTP requests for us, from
its own network.

That lets us reach `http://localhost:4942/internal/config`. It is restricted to
localhost, so we get 403 directly, but the server itself can reach it. Its JSON has
no XML-breaking characters, so it drops straight into the event title we get back.

## How I exploited it
See `exploit.py` (the same payload is in `demo-xxe.xml`):
1. Upload XML declaring `<!ENTITY xxe SYSTEM "http://localhost:4942/internal/config">`
   and reference `&xxe;` in an event title.
2. The server fetches the internal config and returns it inside the imported event.

The leaked config had the JWT secret (`42network`), the PocketBase admin
credentials (`admin@42network.local` / `Darkly42Admin!`), and the flag.

## Impact
- Reads internal, localhost-only resources (SSRF), past the network restriction.
- Leaks secrets: the JWT signing key and the database admin credentials, which give
  full control of the PocketBase backend.
- The XML parser can also be hit with entity-expansion DoS.

## How it could have been prevented
- Parse XML with a safe parser (`defusedxml`), or turn off DTD and external entity
  resolution.
- Don't let user XML trigger outbound requests. Block internal targets.
- Don't keep secrets in a reachable config endpoint.
