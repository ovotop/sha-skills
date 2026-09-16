# English controlled writing (condensed STE-aligned rules)

Scope: directional rules for English technical documents. This is **not** the full ASD-STE100
dictionary (≈900 approved words, 53 rules). Long-output tasks drift, so keep the rules visible.

## Sentence rules

- One instruction per sentence. Keep sentences ≤ 25 words; prefer ≤ 20.
- Use active voice and name the actor: 「The service writes the log」, not 「the log is written」.
- Put the condition before the action. Put a warning before the step that can cause harm.
- Do not stack several conditions, actions and exceptions in one sentence.

## Words

- One term per concept. Do not rotate synonyms for the same object or action.
- Expand an abbreviation at first use; keep the same form afterwards.
- No vague adverbs: basically, very, really, quite, fairly, significantly (unless you give the value).
- No marketing jargon: leverage, empower, seamless, robust, cutting-edge, best-in-class, holistic,
  synergy, ecosystem, north star.
- No mechanical status words: a bare 「Success」/「Invalid」 label tells the reader nothing. Say what
  happened and what to do next.

## Modality and sources (confidence ladder — identical to the Chinese rules)

- A claim with a checkable source MAY use strong modality; put the source in the sentence.
- A claim with no source but identifiable as inference MUST use weak modality (may, appears to,
  based on …) and be marked as inference.
- A claim with no source and unclear status MUST be deleted.
- Warnings, limits and exceptions are a protected category: keep them even without a source. You may
  soften the modality; never delete them.
- Never add numbers, dates, conditions or conclusions that the source material does not contain.

## Structure guardrails

- Lead with the conclusion; give ≤ 3 supporting points; put details and exceptions last.
- A heading is a claim, not a label: 「Retries stop after three failures」, not 「Retries」.
- Prefer induction inside a group; do not mix induction and deduction in the same group.
- No empty shells: never write 「There are three problems:」 followed by items that carry no claim.
- Steps: preconditions → risks/limits → numbered steps → expected result per step → stop condition
  and recovery.

## Upgrade threshold (design D8)

This file carries directional rules only. When the share of long English documentation tasks exceeds
30%, expand it into a fuller STE mapping (condensed 53-rule mapping + approved-word subset). Track
the threshold in the change tasks; do not expand preemptively.
