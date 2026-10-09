#!/usr/bin/env python3
# Run every NN-*/exploit.py and summarise the flags found.
#   python3 run_all.py
#   TARGET=http://<ip>:4942 python3 run_all.py
import sys, subprocess, pathlib

here = pathlib.Path(__file__).resolve().parent
scripts = sorted(d / "exploit.py" for d in here.iterdir()
                 if d.is_dir() and d.name[0].isdigit() and (d / "exploit.py").is_file())

ok = fail = 0
for s in scripts:
    name = s.parent.name
    print(f"### {name}")
    r = subprocess.run([sys.executable, str(s)])
    flag_file = s.parent / "flag"
    if r.returncode == 0:
        if flag_file.is_file() and flag_file.read_text().strip():
            print(f">> flag: {flag_file.read_text().strip()}")
        else:
            print(">> ok (no flag)")
        ok += 1
    else:
        print(">> FAILED")
        fail += 1
    print()

print(f"=== {ok} ran, {fail} failed ===")
print("flags:")
for d in sorted(here.glob("[0-9]*")):
    f = d / "flag"
    if f.is_file():
        print(f"  {d.name}: {f.read_text().strip()}")
