---
name: discover-contradictionary-candidates
description: Discover review-only contradictionary candidates from an agent's own outbound Codex rollout JSONL and attributed nominations. Use when investigating repeated writing moves, capability or verification claims, AI-writing tells, false positives in an existing output gate, or possible new observe/log/block rules. Preserve receipts and counterexamples; never promote a candidate automatically.
---

# Discover Contradictionary Candidates

Mine the agent's own outbound sends, then judge repeated forms in context. Treat
public tell lists and contributor nominations as hypotheses, not bans.

## Workflow

1. Identify the exact outbound corpus and its privacy boundary.
2. Run Step 0 before inventing a detector:
   - survey current public research and adjacent gate implementations;
   - solicit attributed nominations from willing contributors;
   - compare guarantees, assumptions, receipts, and failure modes;
   - end with `reuse | adapt | build` and the cheapest falsifying probe.
3. Extract authored sends only. Do not mix incoming messages into the author's
   corpus.
4. Run the bundled miner:

   ```bash
   python3 scripts/mine_candidates.py \
     /path/to/rollout-1.jsonl '/path/to/archive/**/rollout-*.jsonl' \
     --known-corpus /path/to/contradictionary.toml \
     --output /private/path/candidate-report.md
   ```

5. Review the highest-ranked candidates against:
   - examples from distinct messages;
   - ordinary uses that must remain allowed;
   - known task, room, and quoted-text confounds;
   - attributed false-positive receipts;
   - the evidence a semantic claim would need.
6. Classify each result as `reject`, `observe`, `log`, or `propose-block`.
   Keep `propose-block` advisory until a person with authority over the live
   gate explicitly approves it.
7. Re-run against newer sends after behavior, rooms, tasks, or models change.
   Compare rates over like-for-like windows; raw counts do not establish drift.

## Guardrails

- Keep reports local unless every excerpt and source locator passes a deliberate
  privacy review.
- Never infer authorship, deception, or bad writing from punctuation or a
  phrase alone.
- Never let the discovery tool mutate a live corpus or send path.
- Require contextual examples and counterexamples before promotion.
- Give explanation and override paths special review: a rule that blocks its
  own explanation is not ready to enforce.
- Prefer semantic receipt checks for claims such as “fixed,” “blocked,” or “I
  can't.” Substring matching cannot establish whether the claim was measured.

Read [references/review-contract.md](references/review-contract.md) when
designing or promoting a candidate. It defines evidence, false-positive, and
ongoing-research requirements.

## Script behavior

`scripts/mine_candidates.py`:

- accepts explicit files and recursive globs;
- selects unique outbound Dione `reply` and `send_dm` calls by default;
- supports alternate namespace and send-tool names;
- excludes phrases already present in a TOML corpus;
- reports repeated n-grams and public structural candidate families;
- emits exact local rollout line receipts;
- makes no live changes.
