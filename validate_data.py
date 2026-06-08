"""
validate_data.py

Validates the training_data.jsonl file before submitting to OpenAI's
fine-tuning API. Catches schema errors, malformed JSON, and inconsistent
field structures that would otherwise fail the fine-tuning job.

Usage:
    python validate_data.py training_data.jsonl
"""

import json
import sys
from collections import Counter

REQUIRED_FIELDS = {
    "transaction_type",
    "amount",
    "currency",
    "account_last4",
    "transaction_date",
    "originator",
    "fraud_indicators",
    "customer_reported",
    "recommended_action",
    "risk_level",
    "sar_required",
}

VALID_RISK_LEVELS = {"low", "medium", "high", "critical"}
VALID_TRANSACTION_TYPES = {"ACH debit", "ACH credit", "wire", "card", "check", "other"}


def validate(filepath):
    errors = []
    risk_counts = Counter()
    type_counts = Counter()
    total = 0

    with open(filepath) as f:
        for i, line in enumerate(f, start=1):
            total += 1
            try:
                obj = json.loads(line)
            except json.JSONDecodeError as e:
                errors.append(f"Line {i}: invalid JSON — {e}")
                continue

            # Check message structure
            if "messages" not in obj:
                errors.append(f"Line {i}: missing 'messages' key")
                continue

            roles = [m["role"] for m in obj["messages"]]
            if roles != ["system", "user", "assistant"]:
                errors.append(f"Line {i}: roles must be [system, user, assistant], got {roles}")
                continue

            # Parse assistant output as JSON
            try:
                output = json.loads(obj["messages"][2]["content"])
            except json.JSONDecodeError:
                errors.append(f"Line {i}: assistant content is not valid JSON")
                continue

            # Check schema completeness
            missing = REQUIRED_FIELDS - set(output.keys())
            if missing:
                errors.append(f"Line {i}: missing fields {missing}")

            # Check enum values
            if output.get("risk_level") not in VALID_RISK_LEVELS:
                errors.append(f"Line {i}: invalid risk_level '{output.get('risk_level')}'")
            if output.get("transaction_type") not in VALID_TRANSACTION_TYPES:
                errors.append(f"Line {i}: invalid transaction_type '{output.get('transaction_type')}'")

            # Collect stats
            risk_counts[output.get("risk_level")] += 1
            type_counts[output.get("transaction_type")] += 1

    # Report
    print(f"Total examples: {total}")
    print(f"Errors found: {len(errors)}")
    print()

    if errors:
        print("ERRORS:")
        for e in errors:
            print(f"  {e}")
        print()

    print("Risk level distribution:")
    for level, count in sorted(risk_counts.items()):
        print(f"  {level}: {count}")
    print()

    print("Transaction type distribution:")
    for ttype, count in sorted(type_counts.items()):
        print(f"  {ttype}: {count}")

    return len(errors) == 0


if __name__ == "__main__":
    filepath = sys.argv[1] if len(sys.argv) > 1 else "training_data.jsonl"
    success = validate(filepath)
    sys.exit(0 if success else 1)
