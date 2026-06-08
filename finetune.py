"""
finetune.py

Submits a fine-tuning job to OpenAI's API using the validated training
data. Uploads the JSONL file, launches the fine-tuning job, and polls
for status until completion.

Requires:
    pip install openai
    export OPENAI_API_KEY="sk-..."

Usage:
    python finetune.py
"""

import os
import time
from openai import OpenAI

TRAINING_FILE = "training_data.jsonl"
BASE_MODEL = "gpt-3.5-turbo"
POLL_INTERVAL_SECONDS = 30


def upload_training_file(client):
    """Upload JSONL file to OpenAI and return the file ID."""
    print(f"Uploading {TRAINING_FILE}...")
    with open(TRAINING_FILE, "rb") as f:
        upload = client.files.create(file=f, purpose="fine-tune")
    print(f"  File ID: {upload.id}")
    return upload.id


def launch_finetune_job(client, file_id):
    """Submit the fine-tuning job."""
    print(f"Launching fine-tuning job on base model {BASE_MODEL}...")
    job = client.fine_tuning.jobs.create(
        training_file=file_id,
        model=BASE_MODEL,
    )
    print(f"  Job ID: {job.id}")
    return job.id


def poll_until_complete(client, job_id):
    """Poll the job status until it succeeds or fails."""
    print("Polling job status (this can take 10-30+ minutes)...")
    while True:
        job = client.fine_tuning.jobs.retrieve(job_id)
        print(f"  Status: {job.status}")
        if job.status in {"succeeded", "failed", "cancelled"}:
            return job
        time.sleep(POLL_INTERVAL_SECONDS)


def main():
    if not os.environ.get("OPENAI_API_KEY"):
        raise SystemExit("OPENAI_API_KEY environment variable not set")

    client = OpenAI()

    file_id = upload_training_file(client)
    job_id = launch_finetune_job(client, file_id)
    job = poll_until_complete(client, job_id)

    if job.status == "succeeded":
        print()
        print("Fine-tuning complete.")
        print(f"  Fine-tuned model: {job.fine_tuned_model}")
        print()
        print("Save this model name — you'll use it in test_model.py")
    else:
        print(f"Job ended with status: {job.status}")


if __name__ == "__main__":
    main()














