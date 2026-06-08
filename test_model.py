"""
test_model.py

Tests the fine-tuned model against new fraud narratives the model has
never seen during training. Compares outputs to expected JSON to gauge
real-world performance.

Requires:
    pip install openai
    export OPENAI_API_KEY="sk-..."

Usage:
    python test_model.py ft:gpt-3.5-turbo:your-org:custom:abc123
"""

import json
import sys
from openai import OpenAI

SYSTEM_PROMPT = (
    "You are a banking fraud analyst. Extract structured data from "
    "transaction narratives and return only valid JSON matching the "
    "required schema. Never include explanation or markdown."
)

# Test cases the model has NOT seen during training
TEST_CASES = [
    {
        "name": "Skimmer fraud at gas station",
        "narrative": (
            "Debit card transaction of $89.40 at SHELLGASSTATION on "
            "06/05/2026 to account ending 4488 followed by $1,247.00 "
            "card-not-present transaction to OFFSHOREVPN.COM 18 minutes "
            "later. Card skimmer suspected at the gas station based on "
            "fraud pattern alerts for that ZIP code."
        ),
    },
    {
        "name": "Business email compromise wire",
        "narrative": (
            "Outbound wire of $48,200 sent 06/04/2026 from business "
            "checking account ending 7790 to vendor account in Texas. "
            "Customer later reported the vendor's email was compromised "
            "and the wire instructions were fraudulent. Real vendor uses "
            "a different account. Wire already settled."
        ),
    },
    {
        "name": "Legitimate large purchase",
        "narrative": (
            "Card transaction of $3,400 at HOMEDEPOT on 06/05/2026 to "
            "account ending 1102. Flagged by fraud system due to amount. "
            "Customer reached and confirmed they are remodeling a kitchen "
            "and authorized the purchase."
        ),
    },
]


def extract(client, model, narrative):
    """Run the fine-tuned model against a single narrative."""
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": narrative},
        ],
        temperature=0,
    )
    return response.choices[0].message.content


def main():
    if len(sys.argv) < 2:
        raise SystemExit("Usage: python test_model.py <fine-tuned-model-id>")

    model = sys.argv[1]
    client = OpenAI()

    for case in TEST_CASES:
        print("=" * 70)
        print(f"TEST: {case['name']}")
        print("=" * 70)
        print(f"INPUT:\n{case['narrative']}\n")

        output = extract(client, model, case["narrative"])
        print(f"MODEL OUTPUT:\n{output}\n")

        # Verify it returned valid JSON
        try:
            parsed = json.loads(output)
            print(f"✓ Valid JSON. risk_level={parsed.get('risk_level')}, "
                  f"sar_required={parsed.get('sar_required')}")
        except json.JSONDecodeError:
            print("✗ Invalid JSON returned")

        print()


if __name__ == "__main__":
    main()
