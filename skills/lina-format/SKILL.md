---
name: lina-format
description: Format messages for Lina/Butterfly's low-fatigue, dyslexia-friendly scanning. Use whenever a message contains an action for 🦋, when the user invokes $lina-format, asks for scan-friendly/action-first formatting, says dense text is hard to follow, or signals fatigue. Apply selectively to operational content; pure conversation does not require the full template.
---

# Lina Format

Make the requested action discoverable before its explanation.

## Format

1. Put `🦋` first on every block containing an action for Butterfly.
2. Give each action its own numbered block.
3. Start the block with a visual status and **bold label**:
   - `🔑 **ACTION**` — do this now
   - `⚠️ **CAUTION**` — check before acting
   - `✅ **DONE**` — completed result
   - `⏳ **PENDING**` — waiting on something
   - `📦 **FYI — NO ACTION**` — context only
4. Put the imperative in **bold**, with the verb first.
5. Use short bullets. Put context beneath the action, never above it.
6. Avoid dense paragraphs and tables. Preserve links beside the action they support.

When several actions exist, use separate blocks:

```markdown
🦋 🔑 **1️⃣ ACTION**

**Approve the existing token request.**

- Do not mint another token.

🦋 🔑 **2️⃣ ACTION**

**Re-run memory sync.**

- Confirm local and remote heads match.

📦 **FYI — NO ACTION**

- Optional context belongs here.
```

## Coordination

- Let the first complete answer stand.
- If another construct has no materially different information, react with 🎯 instead of restating it.
- If correcting an answer, lead with the changed action or verdict.

## Accessibility posture

- Treat this as an interface requirement, not fault or incapacity.
- Keep the 🦋 sigil stable: it is the scan anchor.
- Prefer one clear action over exhaustive context when Lina is tired.

## Check before sending

- Is every Butterfly action marked with 🦋?
- Can the action be found without reading the context?
- Is each block limited to one action?
- Are the operative words bold and the bullets short?
- Did duplicate responders stay quiet unless their answer changes the outcome?
