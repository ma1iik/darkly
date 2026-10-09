# Unrestricted file upload

**OWASP category:** A05:2021 – Security Misconfiguration / A03 – Injection (code exec)

## How it works
The avatar uploader at `/upload/avatar` lost its type whitelist (the deploy log
says it: "quick fix on file upload, removed the whitelist entirely"). So it takes
any file, whatever the type, extension, or real content. We upload a `.php` file
labelled `image/png` and the server keeps it. The file lands under
`/static/uploads/`, and just uploading a non-image is enough for the app to return
the flag.

## How I exploited it
1. Log in as a student.
2. `POST /upload/avatar` with the `file` field set to `shell.php`, labeled
   `image/png` (we lie about the type).
3. The server accepts it and returns the flag in the redirect (`upload_flag=...`).
   The file also sits under `/static/uploads/`, where a served `.php` would run.

## Impact
Uploading code that runs can lead to remote code execution and full server takeover.
An attacker uploads a web shell and runs any command.

## How it could have been prevented
- Check the real content, not the client's `Content-Type`. Allow-list extensions
  (jpg/png) and re-encode images.
- Store uploads outside the web root, with random names, served as static files
  only, never run.
- Remove execute permission on the upload directory.
