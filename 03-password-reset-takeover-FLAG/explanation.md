# Account takeover via broken password reset

**OWASP category:** A07:2021 – Identification and Authentication Failures

## How it works
Two weaknesses chain together. First, a public profile page (`/profile/<id>`)
shows a real user's email to anyone, no login needed. Second, the reset flow is
broken. The token that should prove you own the inbox is just `md5(email)`, which
anyone can compute. With the email and its md5, you set a new password for the
account without ever seeing the inbox.

A comment on benjamin's forum post even hints the token is md5 of the email, so we
did not have to guess it.

## How I exploited it
See `exploit.py`:
1. GET the public profile and take the victim email (`benjamin@student.42.tech`,
   the student whose recovery_code holds the flag).
2. Compute the token as `md5(email)`.
3. POST email + token + `new_password` to `/reset-password/confirm`.
4. POST to `/login` with the new password. A `302` confirms the takeover.

## Impact
Full takeover of any student account when you know its email, with no access to
the inbox. Emails are shown on profiles, so every student account is reachable.
This puts the attacker inside the app as that user, the start of privilege
escalation. Staff and god accounts use 42 SSO, so they cannot be reset this way.

## How it could have been prevented
- Never build the reset token from the email. Email a one-time link instead.
- Make tokens single-use, short-lived, and hard to guess.
- Do not show user emails on public pages (set email visibility to private).
- Answer the same whether the account exists or not, so you do not confirm who is a user.
