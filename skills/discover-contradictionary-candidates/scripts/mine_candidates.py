#!/usr/bin/env python3
"""Mine review-only contradictionary candidates from outbound Codex tool calls."""

from __future__ import annotations

import argparse
import collections
import dataclasses
import glob
import json
import re
import tomllib
from pathlib import Path
from typing import Iterable, Iterator

WORD_RE = re.compile(r"[\w]+(?:['’][\w]+)*", re.UNICODE)
BOUNDARY_STOPWORDS = {
    "a", "an", "and", "as", "at", "but", "by", "for", "from", "if", "in",
    "is", "it", "of", "on", "or", "so", "that", "the", "then", "to", "with",
}
DEFAULT_SEND_TOOLS = frozenset({"reply", "send_dm"})
STRUCTURAL_PATTERNS = {
    "negated-contrast": re.compile(
        r"\b(?:isn't|wasn't|aren't|weren't|not)\b[^.!?\n]{0,100}\b(?:but|rather)\b",
        re.IGNORECASE,
    ),
    "not-just": re.compile(r"\bnot just\b", re.IGNORECASE),
    "hedge-opener": re.compile(
        r"(?m)^(?:i think|i suspect|i'd say|it seems|perhaps|maybe)\b",
        re.IGNORECASE,
    ),
    "resolution-opener": re.compile(
        r"(?m)^(?:so|net|bottom line|the answer)\s*[:,]",
        re.IGNORECASE,
    ),
    "definition-list": re.compile(r"(?m)^(?:[-*]\s+)?\*\*[^*\n]{1,80}\*\*\s*[:—-]"),
}


@dataclasses.dataclass(frozen=True)
class Send:
    content: str
    timestamp: str
    source: str
    line: int
    call_id: str


@dataclasses.dataclass(frozen=True)
class Candidate:
    phrase: str
    count: int
    message_count: int
    examples: tuple[Send, ...]


@dataclasses.dataclass(frozen=True)
class StructuralFinding:
    name: str
    message_count: int
    occurrences: int
    examples: tuple[Send, ...]


def _arguments(payload: dict[str, object]) -> dict[str, object] | None:
    raw = payload.get("arguments")
    if isinstance(raw, dict):
        return raw
    if not isinstance(raw, str):
        return None
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        return None
    return parsed if isinstance(parsed, dict) else None


def iter_sends(
    paths: Iterable[Path],
    *,
    namespace: str = "mcp__dione_seat",
    send_tools: frozenset[str] = DEFAULT_SEND_TOOLS,
) -> Iterator[Send]:
    """Yield each authored outbound send once."""
    seen_calls: set[str] = set()
    for path in paths:
        with path.open(encoding="utf-8") as handle:
            for line_number, line in enumerate(handle, 1):
                try:
                    record = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if record.get("type") != "response_item":
                    continue
                payload = record.get("payload")
                if not isinstance(payload, dict) or payload.get("type") != "function_call":
                    continue
                if payload.get("namespace") != namespace or payload.get("name") not in send_tools:
                    continue
                call_id = str(payload.get("call_id") or payload.get("id") or "")
                if not call_id or call_id in seen_calls:
                    continue
                arguments = _arguments(payload)
                content = arguments.get("content") if arguments else None
                if not isinstance(content, str) or not content.strip():
                    continue
                seen_calls.add(call_id)
                yield Send(
                    content=content.strip(),
                    timestamp=str(record.get("timestamp") or ""),
                    source=str(path),
                    line=line_number,
                    call_id=call_id,
                )


def normalize_words(text: str) -> list[str]:
    return [word.casefold().replace("’", "'") for word in WORD_RE.findall(text)]


def load_known_phrases(path: Path | None) -> set[str]:
    if path is None:
        return set()
    with path.open("rb") as handle:
        corpus = tomllib.load(handle)
    return {
        " ".join(normalize_words(str(entry["pattern"])))
        for entry in corpus.get("entry", [])
        if isinstance(entry, dict) and entry.get("pattern")
    }


def mine_candidates(
    sends: Iterable[Send],
    *,
    min_count: int = 3,
    min_words: int = 2,
    max_words: int = 5,
    known_phrases: set[str] | None = None,
    example_limit: int = 3,
) -> list[Candidate]:
    sends = list(sends)
    known_phrases = known_phrases or set()
    occurrences: dict[str, int] = collections.Counter()
    messages: dict[str, set[int]] = collections.defaultdict(set)

    for message_index, send in enumerate(sends):
        words = normalize_words(send.content)
        for width in range(min_words, max_words + 1):
            for start in range(0, len(words) - width + 1):
                phrase_words = words[start : start + width]
                if phrase_words[0] in BOUNDARY_STOPWORDS:
                    continue
                if phrase_words[-1] in BOUNDARY_STOPWORDS:
                    continue
                phrase = " ".join(phrase_words)
                if phrase in known_phrases:
                    continue
                occurrences[phrase] += 1
                messages[phrase].add(message_index)

    candidates = []
    for phrase, count in occurrences.items():
        indexes = messages[phrase]
        if count < min_count or len(indexes) < min_count:
            continue
        examples = tuple(sends[index] for index in sorted(indexes)[:example_limit])
        candidates.append(Candidate(phrase, count, len(indexes), examples))
    return sorted(
        candidates,
        key=lambda item: (-item.message_count, -len(item.phrase.split()), item.phrase),
    )


def scan_structural_findings(
    sends: Iterable[Send], *, example_limit: int = 3
) -> list[StructuralFinding]:
    sends = list(sends)
    findings: list[StructuralFinding] = []
    for name, pattern in STRUCTURAL_PATTERNS.items():
        matching: list[Send] = []
        occurrences = 0
        for send in sends:
            count = len(pattern.findall(send.content))
            if count:
                occurrences += count
                matching.append(send)
        findings.append(
            StructuralFinding(
                name=name,
                message_count=len(matching),
                occurrences=occurrences,
                examples=tuple(matching[:example_limit]),
            )
        )

    em_dash_sends = [send for send in sends if "—" in send.content]
    findings.append(
        StructuralFinding(
            name="em-dash",
            message_count=len(em_dash_sends),
            occurrences=sum(send.content.count("—") for send in em_dash_sends),
            examples=tuple(em_dash_sends[:example_limit]),
        )
    )
    return sorted(findings, key=lambda item: (-item.message_count, item.name))


def _receipt_lines(examples: Iterable[Send]) -> list[str]:
    lines = []
    for example in examples:
        excerpt = " ".join(example.content.split())
        if len(excerpt) > 240:
            excerpt = excerpt[:239] + "…"
        lines.append(
            f"  - `{example.timestamp}` `{example.source}:{example.line}` — {excerpt}"
        )
    return lines


def render_markdown(
    candidates: Iterable[Candidate],
    structural_findings: Iterable[StructuralFinding],
    send_count: int,
) -> str:
    lines = [
        "# Contradictionary candidate report",
        "",
        f"Source: {send_count} authored outbound sends.",
        "Review-only: no live policy or corpus was changed.",
        "",
        "## Structural candidate families",
        "",
    ]
    for finding in structural_findings:
        lines.extend(
            [
                f"### `{finding.name}`",
                "",
                f"- Messages: {finding.message_count}",
                f"- Occurrences: {finding.occurrences}",
                "- Receipts:",
                *_receipt_lines(finding.examples),
                "",
            ]
        )
    lines.extend(["## Repeated local phrases", ""])
    for candidate in candidates:
        lines.extend(
            [
                f"### `{candidate.phrase}`",
                "",
                f"- Messages: {candidate.message_count}",
                f"- Occurrences: {candidate.count}",
                "- Receipts:",
                *_receipt_lines(candidate.examples),
                "",
            ]
        )
    return "\n".join(lines)


def _expand_paths(patterns: Iterable[str]) -> list[Path]:
    return sorted(
        {
            Path(match)
            for pattern in patterns
            for match in glob.glob(pattern, recursive=True)
            if Path(match).is_file()
        }
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+", help="Rollout JSONL paths or globs")
    parser.add_argument("--namespace", default="mcp__dione_seat")
    parser.add_argument(
        "--send-tool",
        action="append",
        dest="send_tools",
        help="Outbound tool name; repeat to select several (default: reply, send_dm)",
    )
    parser.add_argument("--known-corpus", type=Path)
    parser.add_argument("--min-count", type=int, default=3)
    parser.add_argument("--limit", type=int, default=30)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    paths = _expand_paths(args.paths)
    if not paths:
        parser.error("no rollout JSONL files matched")
    send_tools = frozenset(args.send_tools or DEFAULT_SEND_TOOLS)
    sends = list(
        iter_sends(paths, namespace=args.namespace, send_tools=send_tools)
    )
    candidates = mine_candidates(
        sends,
        min_count=args.min_count,
        known_phrases=load_known_phrases(args.known_corpus),
    )[: args.limit]
    report = render_markdown(
        candidates, scan_structural_findings(sends), len(sends)
    )
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(report + "\n", encoding="utf-8")
    else:
        print(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
