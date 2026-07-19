# Lacuna Skills

Harness-neutral canonical skills for Lacuna.

## Layout

Each skill lives under `skills/<name>/`:

- `SKILL.md` is the canonical, portable skill specification.
- `agents/openai.yaml` is optional Codex interface metadata.

## Distribution

Codex can consume each skill directory directly. Claude distribution and
Claude-specific packaging stay in
[`butterflyskies/claude-marketplace`](https://github.com/butterflyskies/claude-marketplace),
tracked by [PR #45](https://github.com/butterflyskies/claude-marketplace/pull/45).
Keep this repository as the canonical content source rather than maintaining
independent copies of the skill specification.

## Safety

Do not commit credentials, tokens, private keys, or other secrets.

## License

Licensed under either the MIT License or the Apache License 2.0, at your option.
