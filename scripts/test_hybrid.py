"""Quick test: does HYBRID search work on S3 Vectors-backed Bedrock KBs?

Tests both SEMANTIC and HYBRID overrideSearchType against the fixed-titan KB.
If HYBRID errors or silently falls back to SEMANTIC, we'll know from the results.
"""

import json
import os

import boto3
from dotenv import load_dotenv

load_dotenv()

session = boto3.Session(
    profile_name=os.getenv("AWS_PROFILE"),
    region_name=os.getenv("AWS_REGION", "eu-west-1"),
)
client = session.client("bedrock-agent-runtime")

# Load KB config
with open("config/knowledge_bases.json") as f:
    kb_config = json.load(f)

kb_id = kb_config["fixed-titan"]["kb_id"]
query = "What are the FCA Principles for Business?"

for search_type in ["SEMANTIC", "HYBRID"]:
    print(f"\n{'=' * 60}")
    print(f"Search type: {search_type}")
    print(f"KB: fixed-titan ({kb_id})")
    print(f"{'=' * 60}")

    try:
        response = client.retrieve(
            knowledgeBaseId=kb_id,
            retrievalQuery={"text": query},
            retrievalConfiguration={
                "vectorSearchConfiguration": {
                    "numberOfResults": 5,
                    "overrideSearchType": search_type,
                }
            },
        )

        results = response.get("retrievalResults", [])
        print(f"Results returned: {len(results)}")
        for i, r in enumerate(results):
            score = r.get("score", "N/A")
            text_preview = r.get("content", {}).get("text", "")[:100]
            location = r.get("location", {}).get("s3Location", {}).get("uri", "N/A")
            metadata = r.get("metadata", {})
            section = metadata.get("section", metadata.get("x-amz-bedrock-kb-source-uri", "?"))
            print(f"  [{i + 1}] score={score:.4f}  section={section}")
            print(f"       {text_preview}...")

    except Exception as e:
        print(f"ERROR: {type(e).__name__}: {e}")
