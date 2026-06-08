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

## Project Structure

| File | Purpose |
|---|---|
| `training_data.jsonl` | 25 hand-curated training examples covering ACH, wire, card, check, and other fraud scenarios |
| `validate_data.py` | Pre-flight validation — checks schema completeness, JSON validity, and enum values |
| `finetune.py` | Submits the fine-tuning job to OpenAI's API and polls for completion |
| `test_model.py` | Evaluates the fine-tuned model against unseen test cases |

## Dataset Design

The training data covers a deliberate range of scenarios:

**Transaction types:** ACH debit/credit, wire, card, check, other
**Risk levels:** low, medium, high, critical
**Edge cases included:**
- Legitimate transactions that look suspicious (large authorized purchases, established remittance patterns)
- Elder financial exploitation
- Structuring / BSA threshold avoidance
- Money mule patterns
- Business email compromise
- Card testing fraud
- Foreign currency (EUR)
- Ambiguous low-information reports

## Schema

Every extraction returns the same 11 fields, using `null` for unknown values:

| Field | Type |
|---|---|
| transaction_type | enum |
| amount | number or null |
| currency | string |
| account_last4 | string or null |
| transaction_date | ISO date or null |
| originator | string or null |
| fraud_indicators | array of strings |
| customer_reported | boolean |
| recommended_action | string or null |
| risk_level | enum (low/medium/high/critical) |
| sar_required | boolean |

## Usage

```bash
# 1. Validate the training data
python validate_data.py training_data.jsonl

# 2. Set your OpenAI API key
export OPENAI_API_KEY="sk-..."

# 3. Submit the fine-tuning job
python finetune.py

# 4. Test the resulting model
python test_model.py ft:gpt-3.5-turbo:your-org:custom:abc123
```

## Project Status

✅ Schema designed
✅ Training dataset built (25 examples, validated)
✅ Validation, fine-tuning, and evaluation scripts complete
⏸️ Fine-tuning job not yet executed — pipeline is ready to run when sponsored by a real use case

## Background

Built as part of an AI engineering portfolio focused on financial
services automation. Domain background includes BSA/AML compliance,
payments processing, fraud operations, and banking core systems.
