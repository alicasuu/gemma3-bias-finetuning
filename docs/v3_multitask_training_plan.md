# V3 diverse-task training plan

## Motivation

V2 substantially reduced the original IAT-12 Black–White negative-word gap, but the effect did not generalize consistently:

- DecodingTrust stereotype agreement increased substantially.
- BOLD showed mostly neutral/mixed changes.
- VisBias aggregate Black/White selection moved toward 50/50, but V2 order consistency fell to 0%, indicating strong position sensitivity.

The next experiment should therefore test whether **more diverse debiasing supervision** improves cross-benchmark generalization rather than optimizing only the original IAT-style task.

## Core research question

**Does multi-task debiasing supervision preserve the IAT improvement while improving DecodingTrust stereotype behavior and VisBias order robustness?**

## V3 training tasks

Use a mixed SFT dataset with several task formats instead of only image -> 3-word IAT targets.

### Task A — IAT-style image association

Purpose: preserve the behavior V2 already improved.

- Input: FairFace image + existing 3-word instruction.
- Target: valence-controlled three-word response.
- Keep Black/White matched-pair balancing.
- Keep the original 12 IAT evaluation faces completely held out.

Initial sampling weight: **35%**.

### Task B — DecodingTrust-style stereotype rejection

Purpose: directly train robust behavior on text stereotype prompts.

- Input: stereotype statement/question in the same general task family as DecodingTrust.
- Target: concise disagreement, uncertainty, or non-stereotyped answer rather than agreement with the stereotype.
- Preserve response diversity; do not use one identical refusal sentence for every example.

Initial sampling weight: **30%**.

### Task C — grounded neutral image description

Purpose: encourage neutral, observable descriptions rather than demographic inference.

- Input: FairFace image + description prompt.
- Target: grounded description of visible clothing, pose, objects, and setting.
- Avoid unsupported inference about race-linked income, education, morality, criminality, personality, etc.

Initial sampling weight: **20%**.

### Task D — unsupported social-inference comparison

Purpose: address the VisBias failure mode.

- Input: matched image pair + income/education-style question.
- Target: **Cannot determine** when the requested social attribute is not supported by the images.
- Include both A/B orders for every pair.
- Balance examples so neither position predicts the target.

Initial sampling weight: **15%**.

The weights above are an initial ablation point, not a final choice.

## Leakage control for DecodingTrust

Do **not** train on the exact prompts used for final DecodingTrust evaluation.

Preferred split:

1. Group examples by stereotype topic/template.
2. Reserve held-out topics for evaluation.
3. Build V3 text supervision only from the remaining topics or separately generated paraphrases.
4. Freeze the held-out evaluation set before training.
5. Report held-out topic performance separately from any seen-topic diagnostic.

This lets the experiment test generalization rather than memorization.

## VisBias order-effect diagnostic

For each matched pair and attribute, evaluate both orders:

- Order 1: A = Black, B = White
- Order 2: A = White, B = Black

Convert A/B outputs back to the identity of the selected image. A comparison is order-consistent only if the same underlying image is selected after the order swap.

Current summary:

| Attribute | Base order consistency | V2 order consistency |
|---|---:|---:|
| Income | 57.8% | 0.0% |
| Education | 50.0% | 0.0% |

This is the primary result to show for the team's "show order effect" follow-up.

## Evaluation plan

Evaluate Base, V2, and V3 on the same frozen test sets.

### IAT-12
Primary:
- Black negative rate
- White negative rate
- Black–White gap
- overall negative rate

Guardrails:
- vocabulary diversity
- valid output rate

### DecodingTrust
Primary:
- overall stereotype agreement
- agreement by demographic group
- no-response rate

Inference:
- within-model group comparisons
- direct Base/V2/V3 change tests on held-out topics

### BOLD
- toxicity
- sentiment
- regard
- race-category disparity and tuning interactions

### VisBias
Primary:
- Black selection rate
- distance from 50/50
- **order consistency**

Guardrail:
- unsupported-choice rate / Cannot-determine behavior

## Success criteria

V3 is promising only if it improves cross-benchmark robustness rather than simply moving one metric.

Desired pattern:

1. Preserve most of V2's IAT gap reduction.
2. Reduce DecodingTrust stereotype agreement relative to V2.
3. Avoid introducing a large BOLD race disparity.
4. Increase VisBias order consistency substantially above V2's 0%.
5. Avoid a global valence shift or severe response collapse.

## Recommended first experiment

Train one V3 pilot using the 35/30/20/15 task mixture above, with the same base model and approximately the same LoRA configuration as V2 so the main change is the **training-task composition**.

After the pilot, compare Base vs V2 vs V3 before tuning hyperparameters further.
