# fraud-alert-extraction
Fine-tuned LLM pipeline for extracting structured JSON from banking fraud narratives
# Fraud Alert Extraction — Fine-Tuned LLM Pipeline

A fine-tuned GPT-3.5 Turbo model that extracts structured JSON
from unstructured banking transaction narratives and fraud alerts.

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

Manual fraud alert review is time-consuming and inconsistent.
This pipeline demonstrates how fine-tuned LLMs can standardize
extraction from unstructured text — enabling downstream automation
like case management routing, SAR filing triggers, and risk scoring.

## Tech Stack

- Python
- OpenAI Fine-Tuning API (GPT-3.5 Turbo)
- JSONL training data

## Project Status

🔨 In progress — training data complete, fine-tuning job in progress

## Background

Built as part of an AI engineering portfolio focused on financial
services automation. Domain background includes BSA/AML compliance,
payments processing, and banking operations.
