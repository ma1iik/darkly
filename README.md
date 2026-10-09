# Darkly v2 (42 web security project)

A security audit of the Darkly platform (42 Network, subject v6.0). The target is
the web app served at `http://<vm-ip>:4942`, with a PocketBase backend on port 8090.
Everything here was done against the web app only. The VM and its OS were never
touched, which the subject asks for.

## What is in here

The subject says the platform has 19 vulnerabilities and hides 10 flags. The
mandatory part asks for 6 flags and 10 explained vulnerabilities. The bonus part,
graded only if the mandatory part is perfect, asks for 10 flags and 15
vulnerabilities.

This repo recovers all 10 flags and explains 16 of the vulnerabilities, so it covers
both the mandatory and the bonus part.

## Layout

One folder per breach, numbered in the order I actually went through the app: recon
first, then stepping up privileges, then the injection and server-side bugs, then the
backend takeover. A `-FLAG` in the folder name means that breach gives a flag. Each
folder has:

- `exploit.py`, the script that reproduces the attack. These are my own. No turn-key
  tools like hydra, gobuster or sqlmap.
- `explanation.md`, how it works, the impact, and how it could have been fixed.
- `flag`, the token, when the breach gives one.

Shared code lives in `lib.py` (a small requests wrapper, the login helper and the
flag finder). `run_all.py` runs every breach and prints the flags.

## Flags

| Breach | OWASP | Flag |
|--------|-------|------|
| [03 password reset takeover](03-password-reset-takeover-FLAG/) | A07 | `FLAG{r3s3t_t0k3n_w4s_just_md5_lol}` |
| [05 IDOR on profiles](05-idor-profile-FLAG/) | A01 | `FLAG{1d0r_ur_pr0f1l3_1s_m1n3}` |
| [06 hidden api endpoint](06-hidden-api-grades-FLAG/) | A01 | `FLAG{md5_1s_4_n4m3pl4t3_n0t_4_l0ck}` |
| [07 mass assignment (role)](07-mass-assignment-role-FLAG/) | A01 | `FLAG{just_p4tch_y0ur_0wn_r0l3_lol}` |
| [09 stored XSS (moderation bot)](09-stored-xss-forum-FLAG/) | A03 | `FLAG{xss_st0r3d_1s_n0t_4_f34tur3_w1l}` |
| [10 unrestricted file upload](10-unrestricted-file-upload-FLAG/) | A05/A03 | `FLAG{unr3str1ct3d_upl0ad_g0_brrr}` |
| [11 LFI / path traversal](11-lfi-path-traversal-FLAG/) | A01 | `FLAG{d0t_d0t_sl4sh_4ll_th3_w4y_d0wn}` |
| [12 XXE to SSRF](12-xxe-to-ssrf-FLAG/) | A05/A10 | `FLAG{d3fus3dxml_n3xt_spr1nt_pr0m1s3}` |
| [13 CSRF (no origin check)](13-csrf-origin-FLAG/) | A01 | `FLAG{csrf_4ny_0r1g1n_1s_w3lc0m3}` |
| [16 PocketBase admin takeover](16-pocketbase-admin-FLAG/) | A05/A07 | `FLAG{th3_und3rsc0r3_sl4sh_kn0ws_th3_w4y}` |

## Explained, no flag

| Breach | OWASP |
|--------|-------|
| [01 information disclosure](01-information-disclosure/) | A05 |
| [02 broken access to /staff](02-broken-access-staff/) | A01 |
| [04 brute force (weak password)](04-bruteforce-weak-password/) | A07 |
| [08 reflected XSS](08-reflected-xss/) | A03 |
| [14 weak / leaked JWT secret](14-jwt-weak-secret/) | A02 |
| [15 open redirect](15-open-redirect/) | A01 |

## Running it

Needs `python3` and the `requests` library. If `requests` is missing, install it with
`pip install --user requests`, that is the only dependency.

The default target is `http://localhost:4942`, where the VM sits with VirtualBox's
default NAT, so usually you just run:

```bash
python3 run_all.py                       # run every breach and print the flags
python3 05-idor-profile-FLAG/exploit.py  # just one breach
```

If the VM is on another address, point `TARGET` at it:

```bash
TARGET=http://<vm-ip>:4942 python3 run_all.py
```
