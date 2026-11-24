#!/usr/bin/env python3
"""The Dog Ate My Homework: Funniest Excuse.

Writes one line, under 200 characters, to entry.txt: a dog explaining,
in its own voice, why it ate the homework after being caught.

Pure Python standard library only.
"""

import os
import stat
import sys
import tempfile

LINE = "It was on the floor. Everything on the floor is mine. I don't make the rules \u2014 I just eat them."


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.txt")

    data = LINE.encode("utf-8")
    text = data.decode("utf-8")
    if not 1 <= len(text) <= 200:
        print(f"gate failed: {len(text)} characters", file=sys.stderr)
        return 1
    if text != text.strip() or not text.strip():
        print("gate failed: blank or padded line", file=sys.stderr)
        return 1

    fd, tmp = tempfile.mkstemp(dir=out_dir, prefix=".entry-", suffix=".tmp")
    try:
        with os.fdopen(fd, "wb") as fh:
            fh.write(data)
            fh.flush()
            os.fsync(fh.fileno())
        os.chmod(tmp, 0o644)
        os.replace(tmp, target)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise

    # Read back and verify bytes, UTF-8, mode and the 1-200 char gate.
    with open(target, "rb") as fh:
        back = fh.read()
    if back != data:
        print("verify failed: bytes differ", file=sys.stderr)
        return 1
    back_text = back.decode("utf-8")
    if not 1 <= len(back_text) <= 200:
        print("verify failed: gate", file=sys.stderr)
        return 1
    mode = stat.S_IMODE(os.stat(target).st_mode)
    if mode != 0o644:
        print(f"verify failed: mode {mode:o}", file=sys.stderr)
        return 1

    print(f"wrote {target} ({len(back_text)} characters)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
