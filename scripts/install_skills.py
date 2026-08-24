#!/usr/bin/env python3
"""Install course skills into a Hermes profile.

Copies skills from this repository into the selected Hermes profile.
No financial data, tokens or credentials are copied.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
COURSE_SKILLS = [
    "assistente-financeiro-meta",
    "assistente-financeiro-runtime",
]


def default_hermes_home(profile: str | None) -> Path:
    env_home = os.environ.get("HERMES_HOME")
    if env_home:
        return Path(env_home).expanduser().resolve()
    base = Path.home() / ".hermes"
    if profile and profile != "default":
        return (base / "profiles" / profile).resolve()
    return base.resolve()


def copy_skill(name: str, dest_skills: Path, overwrite: bool) -> dict:
    src = REPO_ROOT / "skills" / name
    if not src.exists():
        return {"name": name, "ok": False, "error": f"source not found: {src}"}
    dest = dest_skills / name
    if dest.exists():
        if not overwrite:
            return {"name": name, "ok": True, "installed": False, "reason": "already exists", "path": str(dest)}
        shutil.rmtree(dest)
    shutil.copytree(src, dest)
    return {"name": name, "ok": True, "installed": True, "path": str(dest)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", default=os.environ.get("HERMES_PROFILE", "default"))
    parser.add_argument("--hermes-home", help="Explicit Hermes home or profile directory")
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--skills", nargs="*", default=COURSE_SKILLS)
    args = parser.parse_args()

    hermes_home = Path(args.hermes_home).expanduser().resolve() if args.hermes_home else default_hermes_home(args.profile)
    dest_skills = hermes_home / "skills"
    dest_skills.mkdir(parents=True, exist_ok=True)

    results = [copy_skill(name, dest_skills, args.overwrite) for name in args.skills]
    ok = all(item.get("ok") for item in results)
    print(json.dumps({
        "ok": ok,
        "profile": args.profile,
        "hermes_home": str(hermes_home),
        "skills_dir": str(dest_skills),
        "results": results,
        "next_action": "start a new Hermes session or reload skills before using them"
    }, ensure_ascii=False, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
