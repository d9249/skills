#!/usr/bin/env python3
"""Collect Hugging Face model context and draft a Korean research briefing."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qs, quote, unquote, urlparse
from urllib.request import Request, urlopen

USER_AGENT = "research-hf-model/1.0"
TIMEOUT_SECONDS = 30
MAX_TEXT_BYTES = 200_000
HF_HOSTS = {"huggingface.co", "www.huggingface.co", "hf.co"}
FORMAT_TOKENS = {
    "mlx",
    "gguf",
    "awq",
    "gptq",
    "exl2",
    "bnb",
    "fp8",
    "fp16",
    "bf16",
    "4bit",
    "8bit",
    "int4",
    "int8",
    "quantized",
    "quant",
}
BENCHMARK_HINTS = ("benchmark", "bench", "eval", "leaderboard")
SERVING_HINTS = ("serving", "launch", "usage", "notes", "chat_template")
PAPER_HOSTS = {
    "aclanthology.org",
    "arxiv.org",
    "dl.acm.org",
    "doi.org",
    "ieeexplore.ieee.org",
    "jmlr.org",
    "openaccess.thecvf.com",
    "openreview.net",
    "papers.nips.cc",
    "proceedings.mlr.press",
    "proceedings.neurips.cc",
    "www.aclanthology.org",
    "www.arxiv.org",
    "www.jmlr.org",
    "www.openreview.net",
}
NON_PAPER_SUFFIXES = (
    ".bin",
    ".csv",
    ".gguf",
    ".jpg",
    ".json",
    ".jsonl",
    ".md",
    ".parquet",
    ".png",
    ".py",
    ".safetensors",
    ".svg",
    ".txt",
    ".webp",
    ".yaml",
    ".yml",
    ".zip",
)
PAPER_PATH_HINTS = ("paper", "papers", "report", "tech-report", "technical-report")
COMMUNITY_DOMAINS = {
    "GeekNews": "news.hada.io",
    "Hacker News": "news.ycombinator.com",
}
DISCUSSION_TRIM_TOKENS = FORMAT_TOKENS | {
    "base",
    "chat",
    "distill",
    "instruct",
    "instruction",
    "it",
    "mlx",
    "onnx",
    "preview",
    "reasoning",
}
def request(url: str) -> Request:
    return Request(url, headers={"User-Agent": USER_AGENT})


def fetch_bytes(url: str, limit: int = MAX_TEXT_BYTES) -> tuple[bytes, bool]:
    with urlopen(request(url), timeout=TIMEOUT_SECONDS) as response:
        payload = response.read(limit + 1)
    truncated = len(payload) > limit
    return payload[:limit], truncated


def fetch_text(url: str, limit: int = MAX_TEXT_BYTES) -> tuple[str | None, str | None]:
    try:
        payload, truncated = fetch_bytes(url, limit=limit)
    except (HTTPError, URLError, TimeoutError) as exc:
        return None, str(exc)
    text = payload.decode("utf-8", "replace")
    if truncated:
        text += "\n...[truncated]"
    return text, None


def fetch_json(url: str) -> tuple[dict[str, Any] | list[Any] | None, str | None]:
    text, error = fetch_text(url)
    if error:
        return None, error
    try:
        return json.loads(text), None
    except json.JSONDecodeError as exc:
        return None, f"JSON decode error: {exc}"


def normalize_repo_id(raw: str) -> str:
    raw = raw.strip()
    if not raw:
        raise ValueError("empty input")
    if "://" not in raw:
        cleaned = raw.strip("/")
        parts = [part for part in cleaned.split("/") if part]
        if len(parts) != 2:
            raise ValueError("expected org/model repo id")
        return "/".join(parts)
    parsed = urlparse(raw)
    if parsed.netloc not in HF_HOSTS:
        raise ValueError("expected a Hugging Face URL")
    parts = [part for part in parsed.path.split("/") if part]
    if not parts:
        raise ValueError("missing repo path")
    if parts[0] in {"models"}:
        parts = parts[1:]
    if parts and parts[0] in {"datasets", "spaces"}:
        raise ValueError("expected a model URL, not a dataset or space URL")
    if len(parts) < 2:
        raise ValueError("expected owner and repo in the URL path")
    return f"{parts[0]}/{parts[1]}"


def api_model_url(repo_id: str) -> str:
    return f"https://huggingface.co/api/models/{quote(repo_id, safe='/')}"


def raw_file_url(repo_id: str, filename: str) -> str:
    return f"https://huggingface.co/{repo_id}/raw/main/{filename}"


def strip_frontmatter(text: str) -> str:
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            return text[end + 5 :]
    return text


def visible_markdown_lines(text: str) -> list[str]:
    lines: list[str] = []
    in_code_block = False
    for raw_line in text.splitlines():
        stripped = raw_line.strip()
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue
        if stripped.startswith("<") and stripped.endswith(">"):
            continue
        lines.append(raw_line)
    return lines


def clean_inline_markdown(text: str) -> str:
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    text = re.sub(r"\*([^*]+)\*", r"\1", text)
    text = re.sub(r"<[^>]+>", "", text)
    return re.sub(r"\s+", " ", text).strip()


def extract_title(readme_body: str, fallback: str) -> str:
    for line in visible_markdown_lines(readme_body):
        if line.startswith("# "):
            title = clean_inline_markdown(line[2:])
            if title:
                return title
    return fallback


def extract_headings(readme_body: str) -> list[str]:
    headings: list[str] = []
    for line in visible_markdown_lines(readme_body):
        match = re.match(r"^(#{2,3})\s+(.+?)\s*$", line)
        if match:
            headings.append(clean_inline_markdown(match.group(2)))
    return headings[:12]


def extract_intro(readme_body: str) -> list[str]:
    lines = visible_markdown_lines(readme_body)
    intro: list[str] = []
    saw_h1 = any(line.startswith("# ") for line in lines)
    started = not saw_h1
    current: list[str] = []
    for line in lines:
        stripped = line.strip()
        if line.startswith("# "):
            started = True
            continue
        if not started:
            continue
        if line.startswith("## "):
            break
        if not stripped:
            if current:
                intro.append(clean_inline_markdown(" ".join(current)))
                current = []
            continue
        if stripped.startswith("---"):
            continue
        if stripped.startswith("<"):
            continue
        current.append(stripped)
    if current:
        intro.append(clean_inline_markdown(" ".join(current)))
    return [item for item in intro if item][:3]


def unique(items: list[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            ordered.append(item)
    return ordered


def extract_links(text: str) -> list[str]:
    links = re.findall(r"\[[^\]]+\]\((https?://[^)]+)\)", text)
    links.extend(re.findall(r"https?://[^\s)>]+", text))
    cleaned = [item.rstrip('.,)"\'') for item in links]
    return unique(cleaned)


def host_for(url: str) -> str:
    return urlparse(url).netloc.lower()


def normalize_paper_url(url: str) -> str:
    parsed = urlparse(url)
    host = parsed.netloc.lower()
    path = parsed.path
    if host.endswith("arxiv.org") and path.startswith("/pdf/"):
        paper_id = path.removeprefix("/pdf/").removesuffix(".pdf")
        return f"https://arxiv.org/abs/{paper_id}"
    return url


def is_probable_paper_url(url: str) -> bool:
    parsed = urlparse(url)
    host = parsed.netloc.lower()
    path = parsed.path.lower()
    query = parsed.query.lower()
    if any(path.endswith(suffix) for suffix in NON_PAPER_SUFFIXES):
        return False
    if host in HF_HOSTS and path.startswith("/papers/"):
        return True
    if host.endswith("arxiv.org") and (path.startswith("/abs/") or path.startswith("/pdf/")):
        return True
    if host.endswith("openreview.net") and path.startswith("/forum"):
        return True
    if host.endswith("aclanthology.org"):
        return True
    if host in PAPER_HOSTS:
        return True
    if any(hint in f"{path}?{query}" for hint in PAPER_PATH_HINTS):
        return True
    return False


def extract_paper_links(links: list[str]) -> list[str]:
    normalized = [normalize_paper_url(url) for url in links if is_probable_paper_url(url)]
    return unique(normalized)


def derive_discussion_query(repo_name: str) -> str:
    tokens = [token for token in repo_name.split("-") if token]
    while len(tokens) > 1:
        tail = tokens[-1].lower()
        if (
            re.fullmatch(r"\d+k", tail)
            or re.fullmatch(r"v\d+(\.\d+)*", tail)
            or tail in DISCUSSION_TRIM_TOKENS
        ):
            tokens.pop()
            continue
        break
    return "-".join(tokens) or repo_name


def build_discussion_terms(
    repo_id: str,
    readme_title: str | None,
    base_contexts: list[dict[str, Any]],
) -> list[str]:
    repo_name = repo_id.split("/", 1)[1]
    family = derive_discussion_query(repo_name)
    terms: list[str] = [repo_id, repo_name, repo_name.replace("-", " ")]
    if family and family != repo_name:
        terms.extend([family, family.replace("-", " ")])
    if readme_title and readme_title != repo_id:
        terms.append(readme_title)
    for base in base_contexts[:1]:
        base_name = base["repo_id"].split("/", 1)[1]
        terms.extend([base_name, base_name.replace("-", " ")])
    cleaned = [term.strip() for term in terms if term and len(term.strip()) >= 3]
    return unique(cleaned)[:6]


def search_domain_candidates(domain: str, terms: list[str], suffix: str = "") -> list[str]:
    candidates: list[str] = []
    for term in terms[:4]:
        query = f'site:{domain} "{term}" {suffix}'.strip()
        url = "https://duckduckgo.com/html/?q=" + quote(query)
        text, error = fetch_text(url, limit=120_000)
        if error:
            continue
        links = [
            item
            for item in parse_duckduckgo_links(text)
            if host_for(item).endswith(domain)
        ]
        candidates.extend(links[:3])
        if len(unique(candidates)) >= 3:
            break
    return unique(candidates)[:3]


def summarize_section(text: str) -> str | None:
    for line in visible_markdown_lines(text):
        stripped = clean_inline_markdown(line)
        if stripped and not stripped.startswith("#"):
            return stripped[:240]
    return None


def categorize_files(file_names: list[str]) -> tuple[list[str], list[str]]:
    benchmarks = [
        name
        for name in file_names
        if any(token in name.lower() for token in BENCHMARK_HINTS)
    ]
    serving = [
        name
        for name in file_names
        if any(token in name.lower() for token in SERVING_HINTS)
        and name.lower().endswith((".md", ".txt"))
    ]
    return benchmarks[:8], serving[:8]


def summarize_benchmark_payload(filename: str, payload: Any) -> dict[str, Any]:
    summary: dict[str, Any] = {"filename": filename}
    if isinstance(payload, dict) and isinstance(payload.get("summary"), dict):
        src = payload["summary"]
        summary["type"] = "summary"
        for key in (
            "prompt_count",
            "overall_pct",
            "overall_avg_score",
            "avg_generation_tps",
            "avg_latency_sec",
            "median_latency_sec",
            "errors",
        ):
            if key in src:
                summary[key] = src[key]
        if isinstance(src.get("category_averages"), dict):
            summary["category_averages"] = src["category_averages"]
        return summary
    if isinstance(payload, dict):
        summary["type"] = "dict"
        summary["top_level_keys"] = list(payload.keys())[:12]
        return summary
    if isinstance(payload, list):
        summary["type"] = "list"
        summary["item_count"] = len(payload)
        return summary
    summary["type"] = type(payload).__name__
    return summary


def collect_benchmark_summaries(repo_id: str, benchmark_files: list[str]) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for filename in benchmark_files[:3]:
        if not filename.lower().endswith(".json"):
            results.append({"filename": filename, "type": "unparsed"})
            continue
        payload, error = fetch_json(raw_file_url(repo_id, filename))
        if error:
            results.append({"filename": filename, "error": error})
            continue
        results.append(summarize_benchmark_payload(filename, payload))
    return results


def collect_serving_notes(repo_id: str, serving_files: list[str]) -> list[dict[str, Any]]:
    notes: list[dict[str, Any]] = []
    for filename in serving_files[:3]:
        text, error = fetch_text(raw_file_url(repo_id, filename), limit=80_000)
        if error:
            notes.append({"filename": filename, "error": error})
            continue
        body = strip_frontmatter(text)
        notes.append(
            {
                "filename": filename,
                "title": extract_title(body, filename),
                "summary": summarize_section(body),
            }
        )
    return notes


def derive_variant_query(repo_name: str) -> str:
    tokens = [token for token in repo_name.split("-") if token]
    while len(tokens) > 2:
        tail = tokens[-1].lower()
        if re.fullmatch(r"v\d+", tail) or tail in FORMAT_TOKENS:
            tokens.pop()
            continue
        break
    if len(tokens) >= 3:
        return "-".join(tokens)
    return repo_name


def collect_related_variants(repo_id: str) -> list[dict[str, Any]]:
    owner, repo_name = repo_id.split("/", 1)
    query = derive_variant_query(repo_name)
    url = (
        "https://huggingface.co/api/models"
        f"?author={quote(owner)}&search={quote(query)}&limit=12"
    )
    payload, error = fetch_json(url)
    if error or not isinstance(payload, list):
        return []
    variants: list[dict[str, Any]] = []
    for item in payload:
        candidate = item.get("id")
        if not candidate or candidate == repo_id:
            continue
        variants.append(
            {
                "repo_id": candidate,
                "pipeline_tag": item.get("pipeline_tag"),
                "last_modified": item.get("lastModified"),
            }
        )
    return variants


def collect_readme(repo_id: str) -> dict[str, Any]:
    text, error = fetch_text(raw_file_url(repo_id, "README.md"))
    if error:
        return {"error": error}
    body = strip_frontmatter(text)
    title = extract_title(body, repo_id)
    links = extract_links(body)
    paper_links = extract_paper_links(links)
    external_links = [url for url in links if host_for(url) not in HF_HOSTS]
    return {
        "title": title,
        "intro": extract_intro(body),
        "headings": extract_headings(body),
        "links": links[:20],
        "paper_links": paper_links[:8],
        "external_links": external_links[:12],
        "body_excerpt": body[:2000],
    }


def collect_base_model_context(base_model: str | list[str] | None) -> list[dict[str, Any]]:
    if not base_model:
        return []
    repo_ids = [base_model] if isinstance(base_model, str) else list(base_model)
    contexts: list[dict[str, Any]] = []
    for repo_id in repo_ids[:3]:
        payload, error = fetch_json(api_model_url(repo_id))
        if error or not isinstance(payload, dict):
            contexts.append({"repo_id": repo_id, "error": error or "unknown error"})
            continue
        readme = collect_readme(repo_id)
        contexts.append(
            {
                "repo_id": repo_id,
                "pipeline_tag": payload.get("pipeline_tag"),
                "library_name": payload.get("library_name"),
                "license": payload.get("cardData", {}).get("license") or payload.get("license"),
                "created_at": payload.get("createdAt"),
                "last_modified": payload.get("lastModified"),
                "title": readme.get("title"),
                "intro": readme.get("intro", []),
                "headings": readme.get("headings", []),
                "links": readme.get("links", [])[:10],
                "paper_links": readme.get("paper_links", [])[:6],
            }
        )
    return contexts


def parse_duckduckgo_links(html: str) -> list[str]:
    matches = re.findall(r'class="result__a"[^>]*href="([^"]+)"', html)
    decoded: list[str] = []
    for candidate in matches:
        if candidate.startswith("//"):
            candidate = "https:" + candidate
        parsed = urlparse(candidate)
        if parsed.netloc.endswith("duckduckgo.com") and parsed.path.startswith("/l/"):
            target = parse_qs(parsed.query).get("uddg", [""])[0]
            if target:
                decoded.append(unquote(target))
                continue
        decoded.append(candidate)
    return unique([item for item in decoded if item.startswith("http")])


def collect_third_party_candidates(repo_id: str, readme_title: str | None) -> dict[str, Any]:
    query_bits = [f'"{repo_id}"', "benchmark", "review"]
    if readme_title:
        query_bits.insert(1, f'"{readme_title}"')
    query = " ".join(query_bits)
    url = "https://duckduckgo.com/html/?q=" + quote(query)
    text, error = fetch_text(url, limit=150_000)
    if error:
        return {"status": "error", "reason": error, "results": []}
    links = [
        item
        for item in parse_duckduckgo_links(text)
        if host_for(item) not in HF_HOSTS
    ]
    return {"status": "ok", "query": query, "results": links[:5]}


def collect_community_discussions(
    repo_id: str,
    readme_title: str | None,
    base_contexts: list[dict[str, Any]],
) -> dict[str, Any]:
    terms = build_discussion_terms(repo_id, readme_title, base_contexts)
    results: dict[str, list[str]] = {}
    for label, domain in COMMUNITY_DOMAINS.items():
        site_results = search_domain_candidates(domain, terms, suffix="model OR Hugging Face")
        results[label] = site_results
    found_any = any(results.values())
    return {
        "status": "ok" if found_any else "no_results",
        "terms": terms,
        "results": results,
    }


def hf_cache_path(repo_id: str) -> Path:
    return Path.home() / ".cache" / "huggingface" / "hub" / f"models--{repo_id.replace('/', '--')}"


def collect_local_smoke(repo_id: str, model_info: dict[str, Any], enabled: bool) -> dict[str, Any]:
    if not enabled:
        return {"status": "not_requested", "reason": "--with-local-smoke not set"}
    library_name = (model_info.get("library_name") or "").lower()
    cache_path = hf_cache_path(repo_id)
    if library_name != "mlx":
        return {
            "status": "skipped",
            "reason": f"no safe local runner configured for library `{library_name or 'unknown'}`",
        }
    if not cache_path.exists():
        return {
            "status": "skipped",
            "reason": "safe local smoke skipped because the model is not cached locally and download would be required",
        }
    import_check = subprocess.run(
        [sys.executable, "-c", "import mlx_lm"],
        capture_output=True,
        text=True,
        timeout=20,
    )
    if import_check.returncode != 0:
        return {
            "status": "skipped",
            "reason": "mlx_lm runtime is not available in the local Python environment",
        }
    command = [
        sys.executable,
        "-m",
        "mlx_lm.generate",
        "--model",
        repo_id,
        "--prompt",
        "Say hello in one short sentence.",
        "--max-tokens",
        "32",
    ]
    env = os.environ.copy()
    env["HF_HUB_OFFLINE"] = "1"
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=120,
            env=env,
        )
    except subprocess.TimeoutExpired:
        return {"status": "error", "reason": "local smoke command timed out"}
    output = (result.stdout or result.stderr).strip()
    if result.returncode != 0:
        return {
            "status": "error",
            "reason": "local smoke command failed",
            "command": " ".join(command),
            "output_excerpt": output[:400],
        }
    return {
        "status": "ok",
        "command": " ".join(command),
        "output_excerpt": output[:400],
    }


def optional_hf_client_available() -> bool:
    try:
        __import__("huggingface_hub")
        return True
    except ImportError:
        return False


def infer_packaging_variant(repo_id: str, model_info: dict[str, Any], base_contexts: list[dict[str, Any]]) -> bool:
    repo_name = repo_id.split("/", 1)[1].lower()
    library_name = (model_info.get("library_name") or "").lower()
    base_present = bool(base_contexts)
    token_hit = any(token in repo_name for token in FORMAT_TOKENS) or bool(
        re.search(r"-v\d+$", repo_name)
    )
    return base_present and (token_hit or library_name in {"mlx", "gguf"})


def make_title(snapshot: dict[str, Any]) -> str:
    display_title = snapshot["readme"].get("title") or snapshot["repo_id"]
    if snapshot["positioning"]["is_packaging_variant"] and snapshot["base_models"]:
        base_repo = snapshot["base_models"][0]["repo_id"]
        base_name = base_repo.split("/", 1)[1]
        focus = snapshot["library_name"] or snapshot["pipeline_tag"] or "deployment variant"
        return f"{display_title} = {base_name}의 {focus} 기반 파생 배포 변형"
    if snapshot["pipeline_tag"] == "image-text-to-text":
        return f"{display_title} = 멀티모달 입력 중심 모델"
    if snapshot["pipeline_tag"] in {"feature-extraction", "sentence-similarity"}:
        return f"{display_title} = 임베딩/유사도 특화 모델"
    if snapshot["pipeline_tag"] == "text-classification":
        return f"{display_title} = 분류 태스크 특화 모델"
    return display_title


def make_tldr(snapshot: dict[str, Any]) -> list[str]:
    bullets: list[str] = []
    repo_id = snapshot["repo_id"]
    pipeline = snapshot["pipeline_tag"] or "unknown"
    library = snapshot["library_name"] or "unknown"
    bullets.append(f"[공식 자료] `{repo_id}` 는 HF API 기준 `{pipeline}` 파이프라인과 `{library}` 라이브러리로 표기된다.")
    if snapshot["base_models"]:
        base_repo = snapshot["base_models"][0]["repo_id"]
        bullets.append(f"[공식 자료] `base_model` 로 `{base_repo}` 가 선언되어 있어 파생 repo로 해석할 수 있다.")
    else:
        bullets.append("[공식 자료] `base_model` 선언이 없어 공개 메타데이터만으로는 upstream lineage를 확정하기 어렵다.")
    current_papers = snapshot["readme"].get("paper_links", [])
    base_papers = [
        url
        for base in snapshot["base_models"]
        for url in base.get("paper_links", [])
    ]
    if current_papers:
        bullets.append("[공식 자료] 현재 repo가 직접 연결한 논문/공식 문헌이 있어 구조 설명을 README 요약보다 강한 근거로 확인할 수 있다.")
    elif base_papers:
        bullets.append("[공식 자료] 현재 repo 자체 논문 링크는 미확인이나, base model 공식 문헌 링크는 확인되어 upstream 구조 설명의 근거로 활용 가능하다.")
    else:
        bullets.append("[공식 자료] 미확인: 현재 repo 또는 base model에서 직접 연결된 논문/기술문서를 자동 수집하지 못했다.")
    bench = snapshot["benchmarks"][0] if snapshot["benchmarks"] else None
    if bench and bench.get("overall_pct") is not None:
        bullets.append(
            f"[모델 카드 자기주장] repo 포함 benchmark 파일은 overall `{bench['overall_pct']}` 와 avg generation `{bench.get('avg_generation_tps', 'n/a')}` tok/s를 제시한다."
        )
    else:
        bullets.append("[모델 카드 자기주장] 독립 재현이 아닌 repo 자체 benchmark 외에는 자동 수집된 성능 수치가 제한적이다.")
    if snapshot["positioning"]["is_packaging_variant"]:
        bullets.append("[추정] 공개 자료 기준 이 repo의 차별점은 신규 아키텍처보다는 포맷 변환, 후속 튜닝, 배포 최적화에 가깝다.")
    else:
        bullets.append("[추정] 공개 자료만으로는 구조적 novelty와 후처리/패키징 차이를 완전히 분리하기 어렵다.")
    return bullets[:5]


def markdown_escape(value: Any) -> str:
    text = str(value) if value is not None else "-"
    return text.replace("|", "\\|").replace("\n", "<br>")


def render_basic_info_table(snapshot: dict[str, Any]) -> str:
    base_value = ", ".join(item["repo_id"] for item in snapshot["base_models"]) or "-"
    related = ", ".join(item["repo_id"] for item in snapshot["related_variants"]) or "-"
    rows = [
        ("Repo", f"`{snapshot['repo_id']}`", "[공식 자료] HF API"),
        ("파이프라인", f"`{snapshot['pipeline_tag'] or 'unknown'}`", "[공식 자료] HF API"),
        ("라이브러리/포맷", f"`{snapshot['library_name'] or 'unknown'}`", "[공식 자료] HF API"),
        ("라이선스", f"`{snapshot['license'] or 'unknown'}`", "[공식 자료] HF metadata"),
        ("베이스 모델", base_value, "[공식 자료] HF metadata"),
        ("생성일", snapshot["created_at"] or "-", "[공식 자료] HF API"),
        ("최종 수정일", snapshot["last_modified"] or "-", "[공식 자료] HF API"),
        ("관련 변형", related, "[공식 자료] HF API search"),
    ]
    lines = ["| 항목 | 값 | 근거 |", "| --- | --- | --- |"]
    for key, value, evidence in rows:
        lines.append(
            f"| {markdown_escape(key)} | {markdown_escape(value)} | {markdown_escape(evidence)} |"
        )
    return "\n".join(lines)


def render_core_differentiators(snapshot: dict[str, Any]) -> list[str]:
    lines: list[str] = []
    intro = snapshot["readme"].get("intro", [])
    if intro:
        lines.append(f"- [모델 카드 자기주장] {intro[0]}")
    if snapshot["base_models"]:
        base = snapshot["base_models"][0]
        lines.append(
            f"- [공식 자료] 베이스 모델 `{base['repo_id']}` 는 `{base.get('pipeline_tag') or 'unknown'}` 파이프라인으로 표기되며, 현재 repo는 `{snapshot['pipeline_tag'] or 'unknown'}` 로 노출된다."
        )
    if snapshot["related_variants"]:
        siblings = ", ".join(item["repo_id"] for item in snapshot["related_variants"][:4])
        lines.append(f"- [공식 자료] 동일 owner 검색 기준 관련 변형 repo로 {siblings} 가 함께 보인다.")
    if snapshot["positioning"]["is_packaging_variant"]:
        lines.append(
            "- [추정] repo 이름, 라이브러리 표기, 파일 구성 기준으로 보면 차별점의 중심은 아키텍처 변경보다 포맷/튜닝/서빙 패키징이다."
        )
    else:
        lines.append(
            "- [추정] 공개 자료 기준 차별점이 구조적 변경인지 후속 튜닝인지 완전히 분리되지는 않으므로, 과도한 architecture claim은 피하는 편이 안전하다."
        )
    return lines


def render_literature_section(snapshot: dict[str, Any]) -> list[str]:
    lines: list[str] = []
    current_papers = snapshot["readme"].get("paper_links", [])
    base_models_with_papers = [
        base for base in snapshot["base_models"] if base.get("paper_links")
    ]
    if current_papers:
        urls = ", ".join(current_papers[:4])
        lines.append(f"- [공식 자료] 현재 repo가 직접 연결한 논문/공식 문헌: {urls}")
    else:
        lines.append(
            "- [공식 자료] 미확인: 현재 repo README/HF 링크에서 직접 연결된 논문 또는 technical report를 자동 수집하지 못했다."
        )
    if base_models_with_papers:
        for base in base_models_with_papers[:2]:
            urls = ", ".join(base["paper_links"][:3])
            lines.append(f"- [공식 자료] 베이스 모델 `{base['repo_id']}` 관련 공식 문헌: {urls}")
    elif snapshot["base_models"]:
        repo_ids = ", ".join(base["repo_id"] for base in snapshot["base_models"][:3])
        lines.append(
            f"- [공식 자료] 미확인: 베이스 모델 {repo_ids} 에서도 자동 수집 가능한 직접 논문 링크는 확인하지 못했다."
        )
    else:
        lines.append("- [공식 자료] `base_model` 선언이 없어 upstream 논문 추적 범위도 제한적이다.")
    if snapshot["positioning"]["is_packaging_variant"]:
        if base_models_with_papers:
            lines.append(
                "- [추정] 현재 repo는 파생 배포/튜닝 성격이 강하므로, 아키텍처·학습 배경 설명은 base model 공식 문헌을 기준으로 해석하는 편이 안전하다."
            )
        else:
            lines.append(
                "- [추정] 파생 배포/튜닝 repo로 보이므로, 논문 부재 상태에서 구조적 novelty를 현재 repo에 직접 귀속하면 과장될 수 있다."
            )
    elif current_papers:
        lines.append(
            "- [공식 자료] 구조·학습 설명은 README 요약보다 위 문헌의 표현을 우선 근거로 사용하는 편이 안전하다."
        )
    else:
        lines.append(
            "- [공식 자료] 미확인: 구조·학습·모달리티 설명을 직접 뒷받침하는 공식 문헌이 없어 README 서술만으로는 확정이 어렵다."
        )
    return lines


def render_benchmark_section(snapshot: dict[str, Any]) -> list[str]:
    lines: list[str] = []
    if snapshot["benchmarks"]:
        for bench in snapshot["benchmarks"]:
            if bench.get("overall_pct") is not None:
                details = [f"overall `{bench['overall_pct']}`"]
                if bench.get("avg_generation_tps") is not None:
                    details.append(f"avg generation `{bench['avg_generation_tps']}` tok/s")
                if bench.get("avg_latency_sec") is not None:
                    details.append(f"avg latency `{bench['avg_latency_sec']}` sec")
                lines.append(
                    f"- [모델 카드 자기주장] `{bench['filename']}` 는 {', '.join(details)} 를 제시한다."
                )
                if bench.get("category_averages"):
                    category_bits = [
                        f"{key} `{value}`"
                        for key, value in list(bench["category_averages"].items())[:5]
                    ]
                    lines.append(
                        f"- [모델 카드 자기주장] 카테고리 평균은 {', '.join(category_bits)} 로 정리되어 있다."
                    )
            else:
                lines.append(
                    f"- [모델 카드 자기주장] `{bench['filename']}` 는 존재하지만 자동 요약 가능한 공통 summary 형식은 확인하지 못했다."
                )
    else:
        lines.append("- [모델 카드 자기주장] 자동 수집 가능한 구조화 benchmark 파일은 확인하지 못했다.")
    if snapshot["with_third_party"]:
        third_party = snapshot["third_party"]
        if third_party.get("results"):
            urls = ", ".join(third_party["results"])
            lines.append(f"- [제3자 자료] 추가 검토 후보 URL: {urls}")
        else:
            lines.append(
                f"- [제3자 자료] 미확인: 자동 검색에서 신뢰할 만한 외부 benchmark/review 후보를 확보하지 못했다 ({third_party.get('reason', 'no results')})."
            )
    else:
        lines.append("- [제3자 자료] 미확인: `--with-third-party` 옵션 없이 실행했다.")
    local = snapshot["local_smoke"]
    if local["status"] == "ok":
        lines.append(f"- [로컬 검증] `{local['command']}` 실행이 성공했고 출력 일부는 `{local['output_excerpt']}` 이다.")
    else:
        lines.append(f"- [로컬 검증] 미수행: {local.get('reason', local['status'])}.")
    return lines


def render_community_section(snapshot: dict[str, Any]) -> list[str]:
    discussions = snapshot["community_discussions"]
    lines: list[str] = []
    for label, urls in discussions.get("results", {}).items():
        if urls:
            joined = ", ".join(urls)
            lines.append(f"- [제3자 자료] {label} 관련 토론 후보: {joined}")
        else:
            lines.append(f"- [제3자 자료] 미확인: {label} 에서 자동 검색으로 관련 토론을 찾지 못했다.")
    if any(discussions.get("results", {}).values()):
        lines.append(
            "- [제3자 자료] 커뮤니티 토론은 실사용 pain point와 배포 이슈 파악에는 유용하지만, 성능·아키텍처 사실을 단독 확정하는 근거로 쓰면 안 된다."
        )
    else:
        terms = ", ".join(discussions.get("terms", [])[:4]) or "search terms unavailable"
        lines.append(
            f"- [제3자 자료] 미확인: 자동 검색어 `{terms}` 기준으로 GeekNews/Hacker News 관련 토론을 찾지 못했다."
        )
    return lines


def render_architecture_section(snapshot: dict[str, Any]) -> list[str]:
    lines: list[str] = []
    if snapshot["base_models"]:
        base = snapshot["base_models"][0]
        intro = base.get("intro") or []
        lines.append(
            f"- [공식 자료] upstream `{base['repo_id']}` 는 `{base.get('pipeline_tag') or 'unknown'}` / `{base.get('library_name') or 'unknown'}` 로 표기된다."
        )
        if intro:
            lines.append(f"- [공식 자료] upstream 소개 문구 요약: {intro[0]}")
    if snapshot["serving_notes"]:
        for note in snapshot["serving_notes"][:2]:
            if note.get("summary"):
                lines.append(
                    f"- [공식 자료] `{note['filename']}` 는 서빙 관련 포인트로 `{note['summary']}` 를 담고 있다."
                )
    else:
        lines.append("- [공식 자료] 별도 serving note는 자동 수집 범위에서 확인되지 않았다.")
    if snapshot["readme"].get("headings"):
        headings = ", ".join(snapshot["readme"]["headings"][:6])
        lines.append(f"- [모델 카드 자기주장] README 주요 섹션은 {headings} 순으로 구성되어 있다.")
    if snapshot["positioning"]["is_packaging_variant"]:
        lines.append(
            "- [추정] 공개 자료 기준 현재 repo는 베이스 모델 위에 포맷 전환, 후속 튜닝, chat template/serving 조정이 얹힌 배포 변형으로 읽는 편이 안전하다."
        )
    else:
        lines.append(
            "- [추정] 공개 README만으로는 아키텍처 변경과 post-training/패키징 변경의 경계를 확정하기 어렵다."
        )
    return lines


def render_risk_section(snapshot: dict[str, Any]) -> list[str]:
    tags = {tag.lower() for tag in snapshot["tags"]}
    lines = [
        "- [추정] repo 자체 benchmark는 독립 재현이 아니므로 의사결정에는 추가 검증이 필요하다.",
    ]
    if "uncensored" in tags or "abliterated" in tags:
        lines.append("- [모델 카드 자기주장] 안전성/거절 억제 계열 positioning이 보여 운영 정책과 충돌할 수 있다.")
    if snapshot["license"]:
        lines.append(f"- [공식 자료] 라이선스는 `{snapshot['license']}` 로 표기되어 있어 파생 사용 조건을 별도로 확인해야 한다.")
    if snapshot["local_smoke"]["status"] != "ok":
        lines.append(f"- [로컬 검증] 미수행 또는 제한: {snapshot['local_smoke'].get('reason', snapshot['local_smoke']['status'])}.")
    if snapshot["with_third_party"] and not snapshot["third_party"].get("results"):
        lines.append("- [제3자 자료] 외부 독립 검증을 아직 확보하지 못했다.")
    if not any(snapshot["community_discussions"].get("results", {}).values()):
        lines.append("- [제3자 자료] GeekNews/Hacker News 실사용 토론을 확보하지 못해 현장 pain point 관측은 제한적이다.")
    return lines


def render_use_case_section(snapshot: dict[str, Any]) -> list[str]:
    pipeline = snapshot["pipeline_tag"] or ""
    tags = {tag.lower() for tag in snapshot["tags"]}
    lines: list[str] = []
    if pipeline == "text-generation":
        lines.append("- 적합: 로컬 agent, 코딩, tool-use, 한국어 기술 대화처럼 텍스트 추론 중심 워크로드")
        lines.append("- 부적합: 엄격한 안전 정책, 공식 재현 벤치가 필수인 비교 평가, 멀티모달 입력이 필요한 업무")
    elif pipeline == "image-text-to-text":
        lines.append("- 적합: 문서/OCR/UI 이해, 멀티모달 질의응답, 이미지와 텍스트를 함께 쓰는 분석")
        lines.append("- 부적합: 텍스트 전용 최소 지연 환경, 단순 분류/임베딩처럼 더 가벼운 모델이 적합한 업무")
    elif pipeline in {"feature-extraction", "sentence-similarity"}:
        lines.append("- 적합: 검색, 임베딩, 유사도, RAG 인덱싱 파이프라인")
        lines.append("- 부적합: 직접 생성형 응답이 필요한 채팅 업무")
    elif pipeline == "text-classification":
        lines.append("- 적합: 라벨 예측, 문장 분류, 도메인별 라우팅")
        lines.append("- 부적합: 자유 생성, 장문 reasoning, 도구 사용 중심 업무")
    else:
        lines.append("- 적합: repo가 명시하는 주 파이프라인에 맞는 업무")
        lines.append("- 부적합: 공개 자료로 확인되지 않은 확장 사용처")
    if "uncensored" in tags:
        lines.append("- 주의: uncensored positioning 때문에 안전성 가드레일이 필요한 환경에는 추가 정책 계층이 필요할 수 있다.")
    return lines


def render_sources(snapshot: dict[str, Any]) -> list[str]:
    lines = [
        f"- HF API: https://huggingface.co/api/models/{snapshot['repo_id']}",
        f"- README: https://huggingface.co/{snapshot['repo_id']}",
    ]
    for base in snapshot["base_models"]:
        lines.append(f"- Base model: https://huggingface.co/{base['repo_id']}")
    for url in snapshot["readme"].get("paper_links", [])[:4]:
        lines.append(f"- Paper: {url}")
    for base in snapshot["base_models"]:
        for url in base.get("paper_links", [])[:2]:
            lines.append(f"- Base paper ({base['repo_id']}): {url}")
    for label, urls in snapshot["community_discussions"].get("results", {}).items():
        for url in urls[:2]:
            lines.append(f"- Community ({label}): {url}")
    for url in snapshot["readme"].get("links", [])[:8]:
        lines.append(f"- Linked source: {url}")
    return lines


def render_markdown(snapshot: dict[str, Any]) -> str:
    sections = [
        f"# {make_title(snapshot)}",
        "",
        "## TL;DR 3-5줄",
        *make_tldr(snapshot),
        "",
        "## 기본 정보 표",
        render_basic_info_table(snapshot),
        "",
        "## 관련 논문/공식 문헌",
        *render_literature_section(snapshot),
        "",
        "## 핵심 차별점",
        *render_core_differentiators(snapshot),
        "",
        "## 성능/벤치마크",
        *render_benchmark_section(snapshot),
        "",
        "## 커뮤니티 반응/실사용 코멘트",
        *render_community_section(snapshot),
        "",
        "## 아키텍처·학습·서빙 포인트",
        *render_architecture_section(snapshot),
        "",
        "## 리스크/한계",
        *render_risk_section(snapshot),
        "",
        "## 적합/부적합 용도",
        *render_use_case_section(snapshot),
        "",
        "## 출처",
        *render_sources(snapshot),
    ]
    return "\n".join(sections).strip() + "\n"


def collect_snapshot(raw_input: str, with_third_party: bool, with_local_smoke: bool) -> dict[str, Any]:
    repo_id = normalize_repo_id(raw_input)
    model_info, error = fetch_json(api_model_url(repo_id))
    if error or not isinstance(model_info, dict):
        raise RuntimeError(f"failed to fetch HF model info: {error or 'unknown error'}")

    file_names = [item.get("rfilename") for item in model_info.get("siblings", []) if item.get("rfilename")]
    benchmark_files, serving_files = categorize_files(file_names)
    readme = collect_readme(repo_id)
    base_model = model_info.get("cardData", {}).get("base_model") or model_info.get("base_model")
    base_contexts = collect_base_model_context(base_model)
    third_party = (
        collect_third_party_candidates(repo_id, readme.get("title"))
        if with_third_party
        else {"status": "not_requested", "results": []}
    )
    community_discussions = (
        collect_community_discussions(repo_id, readme.get("title"), base_contexts)
        if with_third_party
        else {
            "status": "not_requested",
            "terms": build_discussion_terms(repo_id, readme.get("title"), base_contexts),
            "results": {label: [] for label in COMMUNITY_DOMAINS},
        }
    )
    snapshot = {
        "input": raw_input,
        "repo_id": repo_id,
        "model_url": f"https://huggingface.co/{repo_id}",
        "pipeline_tag": model_info.get("pipeline_tag"),
        "library_name": model_info.get("library_name") or model_info.get("cardData", {}).get("library_name"),
        "license": model_info.get("cardData", {}).get("license") or model_info.get("license"),
        "tags": model_info.get("tags", []),
        "downloads": model_info.get("downloads"),
        "likes": model_info.get("likes"),
        "created_at": model_info.get("createdAt"),
        "last_modified": model_info.get("lastModified"),
        "readme": readme,
        "file_names": file_names,
        "benchmark_files": benchmark_files,
        "benchmarks": collect_benchmark_summaries(repo_id, benchmark_files),
        "serving_files": serving_files,
        "serving_notes": collect_serving_notes(repo_id, serving_files),
        "base_models": base_contexts,
        "related_variants": collect_related_variants(repo_id),
        "with_third_party": with_third_party,
        "third_party": third_party,
        "community_discussions": community_discussions,
        "local_smoke": collect_local_smoke(repo_id, model_info, with_local_smoke),
        "optional_huggingface_hub_available": optional_hf_client_available(),
    }
    snapshot["positioning"] = {
        "is_packaging_variant": infer_packaging_variant(repo_id, model_info, base_contexts)
    }
    return snapshot


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Collect Hugging Face model metadata and draft a Korean internal briefing.",
    )
    parser.add_argument("repo", help="Hugging Face model URL or org/model repo id")
    parser.add_argument(
        "--with-third-party",
        action="store_true",
        help="Collect third-party review candidates via best-effort web search",
    )
    parser.add_argument(
        "--with-local-smoke",
        action="store_true",
        help="Attempt a safe local smoke test when a supported runtime and local cache exist",
    )
    parser.add_argument(
        "--output",
        choices=("markdown", "json"),
        default="markdown",
        help="Output format",
    )
    args = parser.parse_args()

    try:
        snapshot = collect_snapshot(
            args.repo,
            with_third_party=args.with_third_party,
            with_local_smoke=args.with_local_smoke,
        )
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if args.output == "json":
        print(json.dumps(snapshot, ensure_ascii=False, indent=2))
    else:
        print(render_markdown(snapshot))
    return 0


if __name__ == "__main__":
    sys.exit(main())
