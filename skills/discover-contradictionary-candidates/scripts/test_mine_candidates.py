from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).with_name("mine_candidates.py")
SPEC = importlib.util.spec_from_file_location("mine_candidates", MODULE_PATH)
assert SPEC and SPEC.loader
miner = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = miner
SPEC.loader.exec_module(miner)


def record(call_id: str, content: str, *, namespace: str = "mcp__dione_seat") -> str:
    return json.dumps(
        {
            "timestamp": "2026-07-27T00:00:00Z",
            "type": "response_item",
            "payload": {
                "type": "function_call",
                "namespace": namespace,
                "name": "reply",
                "call_id": call_id,
                "arguments": json.dumps({"channel_id": "1", "content": content}),
            },
        }
    )


def send(content: str):
    return miner.Send(content, "now", "test", 1, content)


class CandidateDiscoveryTests(unittest.TestCase):
    def test_extracts_only_unique_selected_sends(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "rollout.jsonl"
            path.write_text(
                "\n".join(
                    [
                        record("one", "Verified from this seat."),
                        record("one", "Verified from this seat."),
                        record("two", "Not ours.", namespace="other"),
                        "{bad json",
                    ]
                ),
                encoding="utf-8",
            )
            sends = list(miner.iter_sends([path]))
        self.assertEqual([item.content for item in sends], ["Verified from this seat."])

    def test_reports_phrases_across_distinct_messages(self) -> None:
        sends = [
            send("Verified from this seat with hashes."),
            send("Verified from this seat with a dry run."),
            send("Verified from this seat after review."),
        ]
        phrases = {
            candidate.phrase
            for candidate in miner.mine_candidates(sends, min_count=3)
        }
        self.assertIn("verified from this seat", phrases)

    def test_excludes_known_phrases(self) -> None:
        candidates = miner.mine_candidates(
            [send("Taking that now.") for _ in range(3)],
            min_count=3,
            known_phrases={"taking that"},
        )
        self.assertNotIn("taking that", {item.phrase for item in candidates})

    def test_counts_structural_signals(self) -> None:
        findings = {
            item.name: item
            for item in miner.scan_structural_findings(
                [
                    send("It is not a title, but a description—and that matters."),
                    send("Not just a word. Not just another word."),
                ]
            )
        }
        self.assertEqual(findings["negated-contrast"].message_count, 1)
        self.assertEqual(findings["not-just"].occurrences, 2)
        self.assertEqual(findings["em-dash"].occurrences, 1)


if __name__ == "__main__":
    unittest.main()
