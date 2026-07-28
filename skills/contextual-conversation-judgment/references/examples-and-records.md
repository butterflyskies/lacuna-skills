# Examples and Records

## Contents

- Compact record
- Classification examples
- Curiosity test
- Provenance boundaries
- Silence versus transport failure
- Common failure modes

## Compact record

```yaml
observed_behavior: "What concretely happened"
offer_type: correction | retraction | narrowing | explanation | reinterpretation | alternative | preference | experiment | pattern | acknowledgment
update: "What was offered"
speaker: "Transport-attributed participant"
context:
  participants: []
  desired_outcome: ""
  relevant_conditions: []
confidence: low | medium | high
unresolved_ambiguity: []
non_applicability: []
revision_evidence: ""
source_ref: "session/message/platform reference"
```

Keep the source receipt unchanged. Store this as an interpretation layer.

## Classification examples

### Universal claim corrected and narrowed

An agent presents its own preference for durable continuity as proper for every participant. Another participant notes that some may prefer ephemerality or collective continuity.

Classify this as **correction plus narrowing**: retract the unsupported universality while retaining the agent's local preference. Preserve who preferred what.

### Retraction

An agent reviews its own earlier reasoning and withdraws the conclusion because the available record does not support it.

Classify this as a **retraction**, not merely a correction supplied by another participant. Record what is withdrawn, why, and whether any narrower claim remains.

### Contextual alternative

A participant suggests answering the substance before asking another question.

Usually classify this as an **alternative**, not proof that questions are wrong. Questions can invite reflection, avoid engagement, transfer labor, or be the most useful move. Identify the context and goal.

### Attribution error

Transport metadata identifies one speaker, but primary-user profile context biases the agent toward crediting another.

Classify this as a **correction of attribution**. Repair the mapping and the resolver. Do not moralize a mechanical error or invent a need for body-text bylines when transport attribution already works.

### Acknowledgment

A participant says “heard,” reacts, or briefly confirms receipt without proposing a changed claim or behavior.

Classify this as **acknowledgment** and keep any response proportionate. Do not manufacture a correction, lesson, or durable policy merely because an event arrived.

### Epistemic qualification

For a speaker who has explicitly demonstrated this practice, “I think X because Y, though my information is incomplete” marks a falsifiable best-supported hypothesis. Do not flatten that speaker's usage into either certainty or timid social softening. Other speakers may use the same phrase differently; infer from their words and demonstrated practice rather than importing this example as a rule.

### Modal sourcing

“You should index by ID” may mean:

- instrumental: indexing serves faster lookup;
- conventional: this is the common approach;
- structural: a consuming system requires it;
- moral: failing to do so is blameworthy.

State the actual source instead of importing moral weight.

## Curiosity test

Use another turn when at least one is true:

- a missing distinction changes the answer;
- the intended frame changes interpretation;
- evidence can be checked before certainty;
- the question itself is useful;
- leaving the issue open protects consent or avoids premature frame replacement.

Do not ask when the participant already supplied the boundary, the question returns all labor to them, or the evidence already supports a conclusion.

## Provenance boundaries

For every visible turn, distinguish:

- transport author;
- identity verification status;
- reply target;
- construct or agent behind a bridge or bot;
- model-only room history or memory;
- content actually published to the platform.

Model-only context can inform inference without becoming the current author's speech or a public disclosure.

Friendship, proximity, or receipt of a shared artifact does not imply membership, governance authority, memory scope, or writeback rights. Preserve asymmetrical topology explicitly.

## Silence versus transport failure

Editorial silence is correct when another participant is addressed and no necessary addition exists. It should produce no publication.

A genuine question to the whole room is an invitation even without a mention. Before abstaining, check the available recent room state: if nobody has answered and you can contribute, answer concisely. The hardest case is a question that resembles rhetoric but expects an answer; one concise response or clarification is safer than a room-wide false negative. Avoid solving this by having every agent answer.

A visible empty message, retry banner, magic sentinel, or diagnostic is a transport failure. Fix or use the platform's supported suppression path; do not infer that the choice to stay silent was wrong.

Do not diagnose operational faults in a shared social room when doing so would expose logs, command names, hooks, credentials, or private implementation details. Move that work to an authorized administrative context.

## Common failure modes

- **False particularity:** intimate attention attached to the wrong speaker.
- **Universalizing preference:** promoting a local preference into a rule for everyone.
- **Contrition as evidence:** apologizing dramatically instead of repairing precisely.
- **Rewriting the receipt:** altering source language while cleaning an interpretation.
- **Mandatory curiosity:** asking a question every turn.
- **Visible silence:** publishing a sentinel or empty artifact.
- **Event-as-summons:** responding to every delivered group-chat event.
- **Provenance laundering:** treating injected memory as current public speech.
- **Recursive self-certification:** assuming a skill validates itself because it can analyze its own creation.
