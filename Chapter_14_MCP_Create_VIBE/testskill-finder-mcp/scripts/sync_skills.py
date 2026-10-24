"""Re-download the upstream skills from GitHub into ./skills (local-only skills are kept).

Usage:  uv run python scripts/sync_skills.py
"""

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = "https://github.com/PramodDutta/skillmasterclass.git"
SUBDIR = "skillmasterclass/skills"
DEST = Path(__file__).resolve().parents[1] / "skills"


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        clone = Path(tmp) / "repo"
        git = ["git", "-c", "core.longpaths=true"]
        subprocess.run([*git, "clone", "--depth", "1", "--filter=blob:none", "--sparse", REPO, str(clone)], check=True)
        subprocess.run([*git, "-C", str(clone), "sparse-checkout", "set", SUBDIR], check=True)
        src = clone / SUBDIR
        if not src.is_dir():
            print(f"{SUBDIR} not found in upstream repo", file=sys.stderr)
            return 1
        count = 0
        for skill_md in src.rglob("SKILL.md"):
            rel = skill_md.parent.relative_to(src)
            target = DEST / rel
            if target.exists():
                shutil.rmtree(target)
            shutil.copytree(skill_md.parent, target)
            count += 1
        shutil.copy2(src / "README.md", DEST / "README.md")
    total = sum(1 for _ in DEST.rglob("SKILL.md"))
    print(f"Synced {count} upstream skills; {total} skills now in {DEST}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
