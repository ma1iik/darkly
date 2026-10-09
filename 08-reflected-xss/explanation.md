# Reflected XSS via the newsletter email parameter

**OWASP category:** A03:2021 – Injection (Cross-Site Scripting)

## How it works
When you subscribe to the newsletter, the form sends your email in the URL and the
page loads `/newsletter?email=<your email>&msg=subscribed`. The page then puts that
`email` value straight back into the HTML it shows you (the "subscribed" message).

The problem: it does not escape it first, so whatever is in `email` is dropped into
the page as-is. If `email` is `<script>alert(1)</script>`, the browser does not see
text, it sees a real `<script>` tag and runs it.

## How I exploited it
See `exploit.py`:
1. Build the URL `/newsletter?email=<script>alert(1)</script>&msg=subscribed`. This
   is the same URL the form would make, just with a script in the email instead of a
   real address.
2. Open it. The response contains `<script>alert(1)</script>` as a real tag, so the
   browser runs it and an alert pops.

The script checks the payload comes back as a live tag and was not escaped to
`&lt;script&gt;` (escaped would mean the browser prints it as text and it is safe).

## Impact
An attacker sends the victim a link that carries JavaScript. When the victim opens
it, the script runs in their browser with their session. The session is a JWT
cookie with `httponly=false`, so the script can read it with `document.cookie` and
steal it. That means session theft and account takeover.

## How it could have been prevented
- Escape reflected values on output so `<` and `>` show as text.
- Set the session cookie `HttpOnly` so scripts cannot read it.
- Add a Content-Security-Policy to block inline scripts.
- Do not print raw request parameters into the page.
