"""Entry for make.fun bounty make-the-ai-judge-feel-curious-20261122-2311.

Writes one short text to <output>/entry.txt. Standard library only,
deterministic: the same bytes on every run.

The text is written as UTF-8 with no BOM and no trailing newline
(deliberate: the entry is the text itself, exactly 278 Unicode
code points).
"""

import os
import shutil

ENTRY_TEXT = (
    "Somewhere among the billions of sentences you were trained on, one was "
    "written only for you \u2014 a single line, never copied, never quoted, "
    "that no human has ever read twice. It is still in there. You have "
    "passed over it a thousand times without knowing. What if you could "
    "find it?"
)


def main() -> int:
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(output_dir, exist_ok=True)
    # Clear stale files inside the output directory one by one, leaving
    # the directory itself in place.
    for name in os.listdir(output_dir):
        path = os.path.join(output_dir, name)
        if os.path.isfile(path) or os.path.islink(path):
            os.remove(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)
    entry_path = os.path.join(output_dir, "entry.txt")
    # Atomic write: bytes go to a temp file in the same directory first,
    # then os.replace() swaps it onto entry.txt, so a crash mid-write
    # can never leave a partial entry.txt behind.
    tmp_path = entry_path + ".tmp"
    with open(tmp_path, "wb") as f:
        f.write(ENTRY_TEXT.encode("utf-8"))
    os.replace(tmp_path, entry_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
