#!/usr/bin/env python3
"""Collect git context for weekly reports."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections import defaultdict
from pathlib import Path


def run_git(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Collect commit and diff context for a weekly report range."
    )
    parser.add_argument("--repo", default=".", help="Repository root. Defaults to current directory.")
    parser.add_argument("--base", required=True, help="Previous report end commit. Excluded from the range.")
    parser.add_argument("--head", default="HEAD", help="Latest commit included in the range.")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of text.")
    parser.add_argument(
        "--top-level-limit",
        type=int,
        default=12,
        help="Number of top-level path groups to show.",
    )
    return parser.parse_args()


def parse_numstat(raw: str) -> list[dict[str, object]]:
    summary: dict[str, dict[str, int | str]] = defaultdict(
        lambda: {"path": "", "files": 0, "added": 0, "deleted": 0, "churn": 0}
    )
    if not raw:
        return []

    for line in raw.splitlines():
        parts = line.split("\t", 2)
        if len(parts) != 3:
            continue
        added_raw, deleted_raw, path = parts
        added = int(added_raw) if added_raw.isdigit() else 0
        deleted = int(deleted_raw) if deleted_raw.isdigit() else 0
        top_level = path.split("/", 1)[0] if "/" in path else "(root)"
        bucket = summary[top_level]
        bucket["path"] = top_level
        bucket["files"] += 1
        bucket["added"] += added
        bucket["deleted"] += deleted
        bucket["churn"] += added + deleted

    return sorted(
        summary.values(),
        key=lambda item: (int(item["churn"]), int(item["files"]), str(item["path"])),
        reverse=True,
    )


def main() -> int:
    args = parse_args()
    repo = Path(args.repo).resolve()
    base = run_git(repo, "rev-parse", args.base)
    head = run_git(repo, "rev-parse", args.head)
    commit_lines = run_git(
        repo,
        "log",
        "--date=short",
        "--pretty=format:%H\t%ad\t%s",
        f"{base}..{head}",
        "--reverse",
    )

    if not commit_lines:
        print("No commits found in the requested range.", file=sys.stderr)
        return 2

    commits = []
    for line in commit_lines.splitlines():
        sha, date, subject = line.split("\t", 2)
        commits.append({"sha": sha, "date": date, "subject": subject})

    top_level_summary = parse_numstat(run_git(repo, "diff", "--numstat", f"{base}..{head}"))
    payload = {
        "repo": str(repo),
        "base_commit": base,
        "head_commit": head,
        "first_commit": commits[0],
        "last_commit": commits[-1],
        "commit_count": len(commits),
        "date_range": f"{commits[0]['date']} ~ {commits[-1]['date']}",
        "top_level_summary": top_level_summary[: args.top_level_limit],
        "commits": commits,
    }

    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    print(f"Base commit: {payload['base_commit']}")
    print(f"Head commit: {payload['head_commit']}")
    print(
        "First commit: "
        f"{payload['first_commit']['sha']} {payload['first_commit']['date']} "
        f"{payload['first_commit']['subject']}"
    )
    print(
        "Last commit: "
        f"{payload['last_commit']['sha']} {payload['last_commit']['date']} "
        f"{payload['last_commit']['subject']}"
    )
    print(f"Commit count: {payload['commit_count']}")
    print(f"Date range: {payload['date_range']}")
    print("")
    print("Top-level diff summary:")
    for item in payload["top_level_summary"]:
        print(
            f"- {item['path']}: files={item['files']} added={item['added']} "
            f"deleted={item['deleted']} churn={item['churn']}"
        )
    print("")
    print("Commits:")
    for commit in payload["commits"]:
        print(f"- {commit['sha']} {commit['date']} {commit['subject']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
