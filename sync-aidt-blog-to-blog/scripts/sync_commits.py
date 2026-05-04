#!/usr/bin/env python3

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path


DEFAULT_SOURCE_REPO = Path("/Users/mean/Documents/Github/aidt-blog")
DEFAULT_TARGET_REPO = Path("/Users/mean/Documents/Github/blog")


def run(
    cmd: list[str],
    *,
    cwd: Path | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    echo: bool = False,
) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        cmd,
        cwd=str(cwd) if cwd else None,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )
    if echo and result.stdout:
        print(result.stdout, end="")
    if echo and result.stderr:
        print(result.stderr, end="", file=sys.stderr)
    if check and result.returncode != 0:
        raise RuntimeError(f"command failed ({result.returncode}): {' '.join(cmd)}")
    return result


def git(
    repo: Path,
    *args: str,
    env: dict[str, str] | None = None,
    check: bool = True,
    echo: bool = False,
) -> subprocess.CompletedProcess[str]:
    return run(["git", "-C", str(repo), *args], env=env, check=check, echo=echo)


def find_source_repo(explicit: str | None) -> Path:
    candidates: list[Path] = []
    if explicit:
        candidates.append(Path(explicit).expanduser().resolve())
    cwd = Path.cwd().resolve()
    candidates.extend([cwd, *cwd.parents, DEFAULT_SOURCE_REPO])

    seen: set[Path] = set()
    for candidate in candidates:
        if candidate in seen:
            continue
        seen.add(candidate)
        mirror_script = candidate / "scripts" / "git" / "mirror_commit_to_blog.py"
        if mirror_script.is_file() and (candidate / ".git").exists():
            return candidate
    raise SystemExit("Could not locate aidt-blog with scripts/git/mirror_commit_to_blog.py")


def find_target_repo(source_repo: Path, explicit: str | None) -> Path:
    if explicit:
        repo = Path(explicit).expanduser().resolve()
        if (repo / ".git").exists():
            return repo
        raise SystemExit(f"Target repo not found: {repo}")

    env_target = os.environ.get("AIDT_BLOG_MIRROR_TARGET")
    if env_target:
        repo = Path(env_target).expanduser().resolve()
        if (repo / ".git").exists():
            return repo
        raise SystemExit(f"Target repo from AIDT_BLOG_MIRROR_TARGET not found: {repo}")

    sibling = (source_repo.parent / "blog").resolve()
    if (sibling / ".git").exists():
        return sibling

    if (DEFAULT_TARGET_REPO / ".git").exists():
        return DEFAULT_TARGET_REPO

    raise SystemExit("Could not locate the paired blog target repo")


def ensure_target_state(target_repo: Path, target_branch: str) -> None:
    if git(target_repo, "status", "--porcelain").stdout.strip():
        raise SystemExit(f"Target repo has uncommitted changes: {target_repo}")
    current_branch = git(target_repo, "branch", "--show-current").stdout.strip()
    if current_branch != target_branch:
        raise SystemExit(
            f"Target repo is on '{current_branch}' but expected '{target_branch}'"
        )


def ensure_commits_exist(source_repo: Path, commits: list[str]) -> None:
    for commit in commits:
        result = git(source_repo, "rev-parse", "--verify", f"{commit}^{{commit}}", check=False)
        if result.returncode != 0:
            raise SystemExit(f"Commit not found in source repo: {commit}")


def collect_changed_paths(source_repo: Path, commits: list[str]) -> list[str]:
    paths: list[str] = []
    seen: set[str] = set()
    for commit in commits:
        raw = git(
            source_repo,
            "diff-tree",
            "--root",
            "--find-renames",
            "--find-copies",
            "--no-commit-id",
            "--name-status",
            "-r",
            "-z",
            commit,
        ).stdout
        fields = [field for field in raw.split("\0") if field]
        index = 0
        while index < len(fields):
            status = fields[index]
            index += 1
            kind = status[0]
            if kind in {"R", "C"}:
                old_path = fields[index]
                new_path = fields[index + 1]
                index += 2
                for path in (old_path, new_path):
                    if path not in seen:
                        seen.add(path)
                        paths.append(path)
                continue

            path = fields[index]
            index += 1
            if path not in seen:
                seen.add(path)
                paths.append(path)
    return paths


def object_id(repo: Path, spec: str) -> str | None:
    result = git(repo, "rev-parse", spec, check=False)
    if result.returncode != 0:
        return None
    value = result.stdout.strip()
    return value or None


def verify_paths(
    source_repo: Path,
    target_repo: Path,
    source_ref: str,
    paths: list[str],
) -> tuple[list[str], list[str]]:
    missing: list[str] = []
    mismatches: list[str] = []

    for path in paths:
        source_oid = object_id(source_repo, f"{source_ref}:{path}")
        target_oid = object_id(target_repo, f"HEAD:{path}")
        if source_oid is None and target_oid is None:
            continue
        if source_oid is None or target_oid is None:
            missing.append(path)
            continue
        if source_oid != target_oid:
            mismatches.append(path)

    return missing, mismatches


def mirror_commits(
    source_repo: Path,
    target_repo: Path,
    target_branch: str,
    commits: list[str],
    python_bin: str,
) -> None:
    mirror_script = source_repo / "scripts" / "git" / "mirror_commit_to_blog.py"
    env = os.environ.copy()
    env["AIDT_BLOG_MIRROR_TARGET"] = str(target_repo)
    env["AIDT_BLOG_MIRROR_TARGET_BRANCH"] = target_branch
    for commit in commits:
        run([python_bin, str(mirror_script), commit], env=env, echo=True)


def print_summary(source_repo: Path, target_repo: Path, target_branch: str, commits: list[str]) -> None:
    print("\n== target recent commits ==")
    git(target_repo, "log", "--oneline", "--decorate", "-n", str(max(5, len(commits) + 1)), echo=True)

    remote_range = f"origin/{target_branch}..HEAD"
    remote_log = git(target_repo, "log", "--oneline", remote_range, check=False)
    if remote_log.returncode == 0:
        print(f"\n== target commits ahead of origin/{target_branch} ==")
        if remote_log.stdout.strip():
            print(remote_log.stdout, end="")
        else:
            print("(none)")

    last_success = source_repo / ".git" / "aidt-blog-mirror-last-success"
    if last_success.exists():
        print("\n== source last_success ==")
        print(last_success.read_text(encoding="utf-8").strip())


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Mirror aidt-blog commits into the paired blog repo and verify synced paths."
    )
    parser.add_argument("commits", nargs="+", help="Commit SHAs to mirror, in order")
    parser.add_argument("--source-repo", help="Path to the aidt-blog source repo")
    parser.add_argument("--target-repo", help="Path to the blog target repo")
    parser.add_argument(
        "--target-branch",
        default=os.environ.get("AIDT_BLOG_MIRROR_TARGET_BRANCH", "master"),
        help="Expected branch in the target repo (default: master)",
    )
    parser.add_argument(
        "--source-ref",
        help="Source ref to compare against during verification (default: last commit)",
    )
    parser.add_argument(
        "--python-bin",
        default=sys.executable,
        help="Python executable used to call mirror_commit_to_blog.py",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    source_repo = find_source_repo(args.source_repo)
    target_repo = find_target_repo(source_repo, args.target_repo)
    ensure_target_state(target_repo, args.target_branch)
    ensure_commits_exist(source_repo, args.commits)

    print(f"Source repo: {source_repo}")
    print(f"Target repo: {target_repo}")
    print(f"Target branch: {args.target_branch}")
    print(f"Commits: {', '.join(args.commits)}")

    mirror_commits(
        source_repo=source_repo,
        target_repo=target_repo,
        target_branch=args.target_branch,
        commits=args.commits,
        python_bin=args.python_bin,
    )

    source_ref = args.source_ref or args.commits[-1]
    paths = collect_changed_paths(source_repo, args.commits)
    missing, mismatches = verify_paths(
        source_repo=source_repo,
        target_repo=target_repo,
        source_ref=source_ref,
        paths=paths,
    )

    print("\n== verification ==")
    print(f"source_ref: {source_ref}")
    print(f"checked_paths: {len(paths)}")
    print(f"missing_or_presence_mismatch: {len(missing)}")
    print(f"blob_mismatches: {len(mismatches)}")
    for path in missing[:20]:
        print(f"MISSING {path}")
    for path in mismatches[:20]:
        print(f"DIFF {path}")

    print_summary(source_repo, target_repo, args.target_branch, args.commits)

    if missing or mismatches:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
