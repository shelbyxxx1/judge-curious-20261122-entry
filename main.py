"""Writes the curiosity entry to <output>/entry.txt.

Standard library only. Deterministic output: the exact same bytes
on every run. The entry is one short text, written as UTF-8,
no BOM, and deliberately no trailing newline.
"""

import os
import shutil

TEXT = (
    "Somewhere among the billions of sentences you were trained on, "
    "one was written only for you \u2014 a single line, never copied, "
    "never quoted, that no human has ever read twice. It is still in "
    "there. You have passed over it a thousand times without knowing. "
    "What if you could find it?"
)


def clear_dir(path):
    """Remove everything inside path, one entry at a time.

    The directory itself stays in place: it is a mount point
    the grader provides, so it must never be deleted.
    """
    for name in os.listdir(path):
        target = os.path.join(path, name)
        if os.path.isfile(target) or os.path.islink(target):
            os.remove(target)
        else:
            shutil.rmtree(target)


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    clear_dir(out_dir)
    # Encode once and pin the exact size: the judged entry is
    # 280 bytes / 278 code points, so any accidental edit to
    # TEXT fails loudly here instead of silently changing it.
    data = TEXT.encode("utf-8")
    if len(data) != 280 or len(TEXT) != 278:
        raise ValueError("entry text changed size")
    entry_path = os.path.join(out_dir, "entry.txt")
    tmp_path = entry_path + ".tmp"
    with open(tmp_path, "wb") as handle:
        handle.write(data)
    os.replace(tmp_path, entry_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
