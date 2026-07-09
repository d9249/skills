#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["PyYAML>=6.0.2"]
# ///
# How to run:
# uv run scripts/hermes_link_skills.py --dry-run
# uv run scripts/hermes_link_skills.py

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Final

import yaml


EXCLUDED_DIRS: Final[frozenset[str]] = frozenset(
    {".git", ".github", ".omx", ".codegraph", "__pycache__"}
)
DEFAULT_LINK_ROOT: Final[str] = "git-synced"

YamlScalar = str | int | float | bool | None
YamlValue = YamlScalar | list["YamlValue"] | dict[str, "YamlValue"]
YamlMap = dict[str, YamlValue]


@dataclass(frozen=True, slots=True)
class Skill:
    folder_name: str
    name: str
    path: Path


@dataclass(frozen=True, slots=True)
class Args:
    repo: Path
    hermes_home: Path
    link_root_name: str
    dry_run: bool


class LinkError(RuntimeError):
    pass


def git_root() -> Path:
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        check=True,
        capture_output=True,
        text=True,
    )
    return Path(result.stdout.strip()).resolve()


def parse_args() -> Args:
    parser = argparse.ArgumentParser(
        description="Link repo skills into the active Hermes skill directory.",
    )
    parser.add_argument("--repo", type=Path, default=git_root())
    parser.add_argument("--hermes-home", type=Path, default=Path.home() / ".hermes")
    parser.add_argument("--link-root-name", default=DEFAULT_LINK_ROOT)
    parser.add_argument("--dry-run", action="store_true")
    raw = parser.parse_args()
    return Args(
        repo=raw.repo.expanduser().resolve(),
        hermes_home=raw.hermes_home.expanduser().resolve(),
        link_root_name=raw.link_root_name,
        dry_run=raw.dry_run,
    )


def normalize_yaml(value) -> YamlValue:
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, list):
        return [normalize_yaml(item) for item in value]
    if isinstance(value, dict):
        normalized: YamlMap = {}
        for key, item in value.items():
            if isinstance(key, str):
                normalized[key] = normalize_yaml(item)
        return normalized
    return str(value)


def read_yaml_map(path: Path) -> YamlMap:
    if not path.exists():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    normalized = normalize_yaml(data)
    if isinstance(normalized, dict):
        return normalized
    raise LinkError(f"{path} does not contain a YAML mapping")


def write_yaml_map(path: Path, data: YamlMap, dry_run: bool) -> None:
    payload = yaml.safe_dump(data, sort_keys=False, allow_unicode=True)
    if dry_run:
        print(f"DRY RUN write {path}")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        backup = path.with_name(f"{path.name}.skills-link-{time.strftime('%Y%m%d-%H%M%S')}.bak")
        shutil.copy2(path, backup)
        print(f"backup {backup}")
    with tempfile.NamedTemporaryFile(
        "w",
        encoding="utf-8",
        dir=path.parent,
        delete=False,
        prefix=f".{path.name}.",
        suffix=".tmp",
    ) as handle:
        handle.write(payload)
        tmp_name = handle.name
    os.replace(tmp_name, path)


def frontmatter_name(skill_md: Path, fallback: str) -> str:
    text = skill_md.read_text(encoding="utf-8", errors="replace")
    if not text.startswith("---\n"):
        return fallback
    _, _, rest = text.partition("---\n")
    frontmatter, marker, _body = rest.partition("\n---")
    if not marker:
        return fallback
    try:
        data = normalize_yaml(yaml.safe_load(frontmatter) or {})
    except yaml.YAMLError:
        return fallback
    if isinstance(data, dict):
        name = data.get("name")
        if isinstance(name, str) and name.strip():
            return name.strip()
    return fallback


def repo_skills(repo: Path) -> list[Skill]:
    skills: list[Skill] = []
    for child in sorted(repo.iterdir(), key=lambda path: path.name):
        if child.name in EXCLUDED_DIRS or child.name.startswith("."):
            continue
        skill_md = child / "SKILL.md"
        if child.is_dir() and skill_md.is_file():
            skills.append(
                Skill(
                    folder_name=child.name,
                    name=frontmatter_name(skill_md, child.name),
                    path=child.resolve(),
                )
            )
    if not skills:
        raise LinkError(f"No skills found in {repo}")
    return skills


def ensure_external_dir(config_path: Path, repo: Path, dry_run: bool) -> None:
    config = read_yaml_map(config_path)
    skills_cfg = config.get("skills")
    if not isinstance(skills_cfg, dict):
        skills_cfg = {}
        config["skills"] = skills_cfg

    raw_dirs = skills_cfg.get("external_dirs")
    dirs: list[YamlValue]
    if raw_dirs is None:
        dirs = []
    elif isinstance(raw_dirs, list):
        dirs = list(raw_dirs)
    elif isinstance(raw_dirs, str):
        dirs = [raw_dirs]
    else:
        raise LinkError("skills.external_dirs must be a list or string")

    repo_str = str(repo)
    normalized_existing = {str(item) for item in dirs}
    if repo_str in normalized_existing:
        print(f"external_dirs already includes {repo_str}")
        return
    dirs.append(repo_str)
    skills_cfg["external_dirs"] = dirs
    print(f"add skills.external_dirs: {repo_str}")
    write_yaml_map(config_path, config, dry_run)


def skill_lookup_names(skill: Skill) -> tuple[str, str]:
    return (skill.name, skill.folder_name)


def excluded_skill_path(skill_md: Path, skills_root: Path) -> bool:
    try:
        parts = skill_md.relative_to(skills_root).parts
    except ValueError:
        return True
    return any(part in EXCLUDED_DIRS or part.startswith(".") for part in parts)


def existing_skill_dirs(skills_root: Path) -> dict[str, Path]:
    existing: dict[str, Path] = {}
    if not skills_root.exists():
        return existing
    for root, dirs, files in os.walk(skills_root, followlinks=True):
        root_path = Path(root)
        if excluded_skill_path(root_path / "SKILL.md", skills_root):
            dirs[:] = []
            continue
        if "SKILL.md" not in files:
            continue
        skill_md = root_path / "SKILL.md"
        skill_dir = skill_md.parent
        if not skill_dir.is_dir():
            continue
        name = frontmatter_name(skill_md, skill_dir.name)
        existing.setdefault(name, skill_dir)
        existing.setdefault(skill_dir.name, skill_dir)
    return existing


def backup_existing(path: Path, skills_root: Path, backup_root: Path, dry_run: bool) -> None:
    relative = path.relative_to(skills_root)
    target = backup_root / relative
    print(f"backup copied skill {path} -> {target}")
    if dry_run:
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(path), str(target))


def link_path(link_path: Path, target: Path, dry_run: bool, after_backup: bool = False) -> None:
    if link_path.is_symlink() and link_path.resolve() == target:
        print(f"linked {link_path} -> {target}")
        return
    if dry_run and after_backup:
        print(f"link {link_path} -> {target}")
        return
    if link_path.exists() or link_path.is_symlink():
        raise LinkError(f"Refusing to overwrite non-matching path: {link_path}")
    print(f"link {link_path} -> {target}")
    if dry_run:
        return
    link_path.parent.mkdir(parents=True, exist_ok=True)
    link_path.symlink_to(target, target_is_directory=True)


def sync_symlinks(args: Args, skills: list[Skill]) -> None:
    skills_root = args.hermes_home / "skills"
    link_root = skills_root / args.link_root_name
    backup_root = skills_root / ".archive" / "repo-link-backups" / time.strftime("%Y%m%d-%H%M%S")
    existing = existing_skill_dirs(skills_root)

    for skill in skills:
        matched = next(
            (existing[name] for name in skill_lookup_names(skill) if name in existing),
            None,
        )
        if matched is not None and matched.resolve() != skill.path:
            backup_existing(matched, skills_root, backup_root, args.dry_run)
            link_path(matched, skill.path, args.dry_run, after_backup=True)
            continue
        if matched is not None:
            print(f"already linked {matched} -> {skill.path}")
            continue
        link_path(link_root / skill.folder_name, skill.path, args.dry_run)


def run(args: Args) -> None:
    if not args.repo.is_dir():
        raise LinkError(f"Repository not found: {args.repo}")
    skills = repo_skills(args.repo)
    print(f"found {len(skills)} repo skills")
    ensure_external_dir(args.hermes_home / "config.yaml", args.repo, args.dry_run)
    sync_symlinks(args, skills)


def main() -> int:
    try:
        run(parse_args())
    except (LinkError, OSError, subprocess.CalledProcessError, yaml.YAMLError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
