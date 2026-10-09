# Privilege escalation via mass assignment on the role field

**OWASP category:** A01:2021 – Broken Access Control (mass assignment)

## How it works
Editing your profile sends `PATCH /api/profile`. The form only changes name and bio,
but the user object the API hands back also has a `role` field. The endpoint does not
limit which fields you can send, so I copied that `role` name into the body and it got
saved. This is mass assignment: a sensitive field (`role`) can be set by the user it
controls. Once you are `cadet` the staff dashboard opens, and it shows a flag. `staff`
and `god` are refused with `403 "role not assignable"`, so `cadet` is as far as this
gets you.

## How I exploited it
1. Log in as a normal student.
2. `PATCH /api/profile` with `{"role":"cadet"}`. Accepted (200), role is now cadet.
3. `GET /staff/dashboard`, now open, and read the flag.

## Impact
Any student can make themselves cadet and reach staff-only pages. Direct
self-service privilege escalation.

## How it could have been prevented
- Do not let clients set sensitive fields. Allow-list the editable ones and leave
  `role` out.
- Only change roles through a server-side admin flow.
- Protect `/staff/*` by a verified role, not a role the user can set on themselves.
