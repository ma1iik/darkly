# Open redirect

**OWASP category:** A01:2021 – Broken Access Control (unvalidated redirect)

## How it works
`/redirect?next=` sends the browser to whatever URL is in the `next` parameter, with
no allow-list check. Any external host is accepted, and a protocol-relative value
like `//evil.com` works too.

## How I exploited it
`GET /redirect?next=https://evil.example.com` returns a redirect whose `Location`
header points at the attacker's site.

## Impact
Phishing under a trusted domain. A link that starts on the real site sends the
victim to a fake one. Chained with OAuth-style flows it can also leak tokens.

## How it could have been prevented
- Redirect only to a fixed allow-list of internal paths, or use opaque keys that map
  to known destinations.
- Reject absolute and protocol-relative URLs. Never redirect to raw user input.
