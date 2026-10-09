# Brute force of a weak account password

**OWASP category:** A07:2021 – Identification and Authentication Failures

## How it works
The login form has no rate limit and no lockout. You can send thousands of guesses
at `/login` and nothing slows you down or warns anyone. jdoe's password is also a
common word (`abc123`), so a normal wordlist finds it. No prior info needed, just
try common passwords until one works.

## How I exploited it
See `exploit.py`. It is our own loop, no external brute-force tool. It reads a
wordlist and for each word sends `POST /login` with jdoe's email and that password.

The trick is telling a hit from a miss by the status code:
- wrong password: the login page is re-rendered, status `200`.
- right password: the server redirects to `/`, status `302`.

So the loop stops on the first `302`. On jdoe it lands on `abc123`, and that `302` is
the proof we got in.

A small `wordlist.txt` ships with the script so it runs anywhere. For a real run you
point it at a bigger list, which you download at eval time:
`WORDS=/usr/share/wordlists/rockyou.txt python3 exploit.py`.

(hydra could do the same thing in one line, but the subject says the exploit script
has to be our own, so we wrote the loop ourselves.)

## Impact
An attacker can take over any account with a weak password. There is no throttling,
so the attack can run as long as it needs without raising an alarm.

## How it could have been prevented
- Rate-limit and lock out repeated failed logins (per account and per IP). Add
  delays and a CAPTCHA after a few tries.
- Set a password policy so weak words like `abc123` are refused.
- Log and alert on bursts of failed logins.
