# Local File Inclusion via path traversal

**OWASP category:** A01:2021 – Broken Access Control / A05 – Misconfiguration

## How it works
`/projects/download?file=` just joins our value to the docs folder path. There is
no check on it. One `../` goes up and out of that folder. So we can read files the
endpoint should not serve, like `private_notes.txt`. The `/backup` response even
gives that filename in an `X-Backup-Exclude` header.

## How I exploited it
1. `GET /backup`: a header shows the sensitive filename.
2. Log in (the download endpoint needs a session).
3. `GET /projects/download?file=../private_notes.txt` returns the file with the
   flag inside.

## Impact
We can read any file the app user can access: source code, secrets, other users'
data. It often leads to a bigger compromise.

## How it could have been prevented
- Don't build file paths from user input. Map an id to a known file, or resolve the
  path and check it stays inside the allowed folder (reject `..`).
- Run the app with low privileges so traversal reaches less.
