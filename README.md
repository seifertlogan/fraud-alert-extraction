# Fraud Alert Extraction — Fine-Tuned LLM Pipeline

A complete fine-tuning pipeline that trains GPT-3.5 Turbo to extract
structured JSON from unstructured banking transaction narratives and
fraud alerts.

## What It Does

Takes raw fraud narrative text like this:

> "ACH debit of $4,872.00 posted 06/02/2026 to checking account
> ending 4491. Customer did not authorize. Recommend SAR filing."

And returns structured JSON like this:

```json
{
  "transaction_type": "ACH debit",
  "amount": 4872.00,
  "account_last4": "4491",
  "fraud_indicators": ["customer denial"],
  "risk_level": "high",
  "sar_required": true
}
```

## Why I Built This

Manual fraud alert review is time-consuming and inconsistent. This
pipeline demonstrates how fine-tuned LLMs can standardize extraction
from unstructured banking text — enabling downstream automation like
case management routing, SAR filing triggers, and risk scoring.

## Design Decisions

**Fine-tuning over few-shot prompting.** At meaningful volume (5K+
narratives/month), fine-tuning amortizes the upfront cost within a
quarter while reducing per-request tokens by roughly 60% and
improving output consistency.

**Single-shot extraction over multi-step.** The input is bounded
and the output schema is fixed, so single-shot is correct. A
multi-step pipeline (extract → validate → enrich with customer
history) would be appropriate if extractions needed to reference
external context.

**Synthetic training data, no PII.** All 25 examples are synthetic
narratives modeled on real fraud typologies. In a real deployment,
training data would require either tokenized PII or full PII
handling controls and a model deployed in a SOC 2 / FFIEC-aligned
environment.

**Null-tolerant schema.** Every field appears in every output, with
explicit `null` values when unknown. This makes downstream systems
trivially parseable — no field-existence checks, no `KeyError`
handling.

**Eleven fields, not three.** A minimal schema (amount, type, risk)
would have been easier to train but less useful. I built the schema
to cover everything an actual fraud case file would need so the
output is directly consumable by case management, not just a demo.

## Production Considerations

This is a portfolio project, not a deployed system. Production
deployment would require:

- **Monitoring**: daily sampling of model outputs against analyst
  decisions to detect drift
- **Retraining cadence**: quarterly, or after material FinCEN
  guidance changes or new fraud typology emergence
- **Audit trail**: every classification logged with model version,
  input hash, output, and timestamp for examiner review
- **Human in the loop**: model output never auto-files a SAR.
  Output routes to an analyst with the model's reasoning as
  decision support, not decision authority
- **PII handling**: real narratives require encryption in transit
  and at rest, plus role-based access on extracted fields

## Project Structure

| File | Purpose |
|---|---|
| `training_data.jsonl` | 25 hand-curated training examples covering ACH, wire, card, check, and other fraud scenarios |
| `validate_data.py` | Pre-flight validation — checks schema completeness, JSON validity, and enum values |
| `finetune.py` | Submits the fine-tuning job to OpenAI's API and polls for completion |
| `test_model.py` | Evaluates the fine-tuned model against unseen test cases |

## Usage

```bash
python validate_data.py training_data.jsonl
export OPENAI_API_KEY="sk-..."
python finetune.py
python test_model.py ft:gpt-3.5-turbo:your-org:custom:abc123
```

## Project Status

✅ Schema designed, dataset built, scripts complete
⏸️ Fine-tuning job not yet executed — pipeline is ready to run
when sponsored by a real use case

## Background

Built as part of an AI engineering portfolio focused on financial
services automation. Domain background includes BSA/AML compliance,
payments processing, fraud operations, and banking core systems.
