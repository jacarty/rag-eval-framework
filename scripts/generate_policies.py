"""Generate synthetic bank policy documents for Crest Bank using Claude via Bedrock.

Usage:
    uv run python scripts/generate_policies.py              # Generate all policies
    uv run python scripts/generate_policies.py --policy "Anti-Money Laundering Policy"  # Single policy
    uv run python scripts/generate_policies.py --dry-run     # Preview what would be generated
    uv run python scripts/generate_policies.py --skip-upload  # Generate locally, don't push to S3
"""

import argparse
import json
import logging
import os
import re
from datetime import UTC, datetime
from pathlib import Path

import boto3
from botocore.config import Config
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

# --- Policy catalogue ---
# Each entry: (policy name, brief instruction to guide generation)
POLICIES = [
    (
        "Anti-Money Laundering Policy",
        "Cover customer due diligence (CDD), enhanced due diligence (EDD), suspicious activity "
        "reporting (SARs), ongoing monitoring, and PEP screening. Reference the Money Laundering "
        "Regulations 2017 alongside FCA requirements.",
    ),
    (
        "Customer Complaints Handling Procedure",
        "Cover complaint receipt, acknowledgement timescales, investigation process, final response "
        "letters, FOS referral rights, root cause analysis, and complaint MI reporting.",
    ),
    (
        "Treating Customers Fairly Policy",
        "Cover the six TCF outcomes, product design, communications clarity, vulnerable customer "
        "identification, and post-sale service standards.",
    ),
    (
        "Conflicts of Interest Policy",
        "Cover identification, recording, management, and disclosure of conflicts. Include personal "
        "account dealing, gifts and hospitality, and outside business interests.",
    ),
    (
        "Data Protection and GDPR Compliance Policy",
        "Cover lawful bases for processing, data subject rights, data retention, breach notification "
        "procedures, DPIAs, and international transfers. Reference UK GDPR and DPA 2018.",
    ),
    (
        "Vulnerable Customers Policy",
        "Cover identification of vulnerability indicators (health, life events, resilience, "
        "capability), staff training, reasonable adjustments, product suitability, and recording "
        "vulnerability flags.",
    ),
    (
        "Product Governance Framework",
        "Cover target market identification, product approval process, distribution strategy, "
        "value assessment, ongoing review, and product lifecycle management.",
    ),
    (
        "Operational Resilience Policy",
        "Cover important business services, impact tolerances, scenario testing, third-party "
        "dependencies, incident response, and recovery planning. Reference the PRA/FCA operational "
        "resilience requirements.",
    ),
    (
        "Outsourcing and Third-Party Risk Policy",
        "Cover due diligence on providers, contractual requirements, ongoing monitoring, exit "
        "strategies, concentration risk, and critical/important outsourcing classification.",
    ),
    (
        "Financial Crime Prevention Policy",
        "Cover fraud detection and prevention, sanctions screening, terrorist financing, bribery "
        "and corruption, and the three lines of defence model.",
    ),
    (
        "Information Security Policy",
        "Cover access controls, data classification, encryption standards, incident response, "
        "penetration testing, and security awareness training. Reference SYSC requirements for "
        "systems and controls.",
    ),
    (
        "Business Continuity Policy",
        "Cover business impact analysis, recovery time objectives, disaster recovery for digital "
        "banking services, crisis communication, and testing frequency.",
    ),
    (
        "Senior Managers and Certification Regime Policy",
        "Cover SM&CR scope, statements of responsibilities, duty of responsibility, fitness and "
        "propriety assessments, conduct rules, and certification regime annual assessments.",
    ),
    (
        "Consumer Duty Implementation Policy",
        "Cover the four outcomes (products and services, price and value, consumer understanding, "
        "consumer support), fair value assessments, outcomes monitoring, and board reporting. "
        "Reference FCA PS22/9 and the PRIN 2A rules.",
    ),
    (
        "Record Keeping and Document Retention Policy",
        "Cover retention periods by document type, storage requirements, disposal procedures, "
        "legal hold processes, and regulatory record-keeping obligations.",
    ),
    (
        "Whistleblowing Policy",
        "Cover reporting channels, whistleblower protections, investigation procedures, the role "
        "of the Whistleblowing Champion, and FCA reporting obligations.",
    ),
    (
        "Credit Risk Management Policy",
        "Cover creditworthiness assessments, affordability checks, credit scoring methodology, "
        "arrears management, forbearance, and provisioning. Reference CONC requirements for "
        "consumer credit.",
    ),
    (
        "Market Abuse and Inside Information Policy",
        "Cover identification of inside information, insider lists, wall-crossing procedures, "
        "personal account dealing restrictions, and suspicious transaction reporting.",
    ),
    (
        "Client Money and Assets Policy",
        "Cover CASS requirements for client money segregation, reconciliation, record keeping, "
        "and the CASS resolution pack.",
    ),
    (
        "Change Management Policy",
        "Cover change risk assessment, regulatory impact analysis, testing and approval gates, "
        "rollback procedures, and post-implementation review. Focus on digital-first context "
        "where all customer interaction is via the app and API.",
    ),
]

PROMPT_PATH = Path("data/prompts/policy_generation_prompt.txt")
OUTPUT_DIR = Path("data/synthetic/policies")

# Matches patterns like PRIN 2, SYSC 6.1.1R, COBS 2.1.1R, MCOB 3A, CONC 5.2, CASS 7.13.8R
FCA_REF_PATTERN = re.compile(
    r"\b(PRIN|SYSC|COBS|ICOBS|MCOB|BCOBS|CASS|MAR|PROD|ESG|TC|GEN|FEES|CONC|COCON|COND|APER|FIT"
    r"|FINMAR|DISP|SUP|DEPP|EG|ENF|AUTH|PERG|COMP|FUND|IPRU-INV|GENPRU|BIPRU|IFPRU|MIPRU|FCG)"
    r"(?:\s+(\d[\w.]*(?:[RGDE])?))?\b"
)


def slugify(name: str) -> str:
    """Convert a policy name to a filename-safe slug."""
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def load_system_prompt() -> str:
    """Load the system prompt from the repo."""
    if not PROMPT_PATH.exists():
        raise FileNotFoundError(f"System prompt not found at {PROMPT_PATH}")
    return PROMPT_PATH.read_text()


def extract_fca_references(text: str) -> list[str]:
    """Extract unique FCA module references from generated markdown."""
    matches = FCA_REF_PATTERN.findall(text)
    refs = sorted({f"{module} {provision}".strip() for module, provision in matches})
    return refs


def get_bedrock_client() -> boto3.client:
    """Create a Bedrock Runtime client."""
    return boto3.Session(
        profile_name=os.getenv("AWS_PROFILE"),
        region_name=os.getenv("AWS_REGION", "eu-west-1"),
    ).client(
        "bedrock-runtime",
        config=Config(read_timeout=600),
    )


def generate_policy(
    client: boto3.client,
    system_prompt: str,
    policy_name: str,
    policy_instructions: str,
    model_id: str,
) -> str:
    """Call Bedrock converse API to generate a single policy document."""
    user_message = (
        f"Generate the {policy_name} for Crest Bank.\n\n"
        f"Specific guidance for this policy:\n{policy_instructions}"
    )

    response = client.converse(
        modelId=model_id,
        system=[{"text": system_prompt}],
        messages=[{"role": "user", "content": [{"text": user_message}]}],
        inferenceConfig={
            "maxTokens": 4096,
            "temperature": 0.4,
        },
    )

    output_message = response["output"]["message"]
    text_parts = [block["text"] for block in output_message["content"] if "text" in block]
    return "\n".join(text_parts)


def save_policy(policy_name: str, content: str, model_id: str) -> tuple[Path, Path]:
    """Save markdown and metadata sidecar. Returns (md_path, meta_path)."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    slug = slugify(policy_name)
    md_path = OUTPUT_DIR / f"{slug}.md"
    meta_path = OUTPUT_DIR / f"{slug}.metadata.json"

    md_path.write_text(content)

    fca_refs = extract_fca_references(content)
    metadata = {
        "document_title": policy_name,
        "document_type": "internal_policy",
        "source": "synthetic",
        "synthetic": True,
        "organisation": "Crest Bank Ltd",
        "fca_modules_referenced": fca_refs,
        "generation_timestamp": datetime.now(UTC).isoformat(),
        "model_id": model_id,
        "word_count": len(content.split()),
    }
    meta_path.write_text(json.dumps(metadata, indent=2))

    return md_path, meta_path


def upload_to_s3(session: boto3.Session, bucket: str, prefix: str) -> None:
    """Upload all generated policies and metadata to S3."""
    s3 = session.client("s3")
    files = list(OUTPUT_DIR.glob("*"))
    for file_path in sorted(files):
        key = f"{prefix}/{file_path.name}"
        logger.info(f"Uploading {file_path.name} → s3://{bucket}/{key}")
        s3.upload_file(str(file_path), bucket, key)
    logger.info(f"Uploaded {len(files)} files to s3://{bucket}/{prefix}/")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate synthetic Crest Bank policy documents")
    parser.add_argument(
        "--policy",
        type=str,
        help="Generate a single policy by name (must match a name in the catalogue)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="List policies that would be generated without calling Bedrock",
    )
    parser.add_argument(
        "--skip-upload",
        action="store_true",
        help="Generate locally without uploading to S3",
    )
    parser.add_argument(
        "--model-id",
        type=str,
        default=os.getenv("BEDROCK_GENERATION_MODEL", "eu.anthropic.claude-sonnet-4-6"),
        help="Bedrock model ID for generation",
    )
    args = parser.parse_args()

    load_dotenv()

    # Filter to a single policy if requested
    if args.policy:
        policies = [(name, instr) for name, instr in POLICIES if name == args.policy]
        if not policies:
            available = "\n".join(f"  - {name}" for name, _ in POLICIES)
            logger.error(f"Policy '{args.policy}' not found. Available:\n{available}")
            raise SystemExit(1)
    else:
        policies = POLICIES

    if args.dry_run:
        print(f"\nWould generate {len(policies)} policies:\n")
        for name, _instructions in policies:
            slug = slugify(name)
            print(f"  {slug}.md — {name}")
        print(f"\nModel: {args.model_id}")
        print(f"Output: {OUTPUT_DIR}/")
        return

    system_prompt = load_system_prompt()
    client = get_bedrock_client()

    total = len(policies)
    generated = 0
    failed = []

    for i, (policy_name, instructions) in enumerate(policies, start=1):
        logger.info(f"[{i}/{total}] Generating: {policy_name}")
        try:
            content = generate_policy(
                client, system_prompt, policy_name, instructions, args.model_id
            )
            md_path, meta_path = save_policy(policy_name, content, args.model_id)

            fca_refs = extract_fca_references(content)
            word_count = len(content.split())
            logger.info(f"  Saved: {md_path.name} ({word_count} words, {len(fca_refs)} FCA refs)")
            generated += 1

        except Exception as e:
            logger.error(f"  FAILED: {policy_name} — {e}")
            failed.append(policy_name)

    # Summary
    print(f"\n{'=' * 60}")
    print(f"Generation complete: {generated}/{total} succeeded")
    if failed:
        print(f"Failed ({len(failed)}):")
        for name in failed:
            print(f"  - {name}")
    print(f"Output directory: {OUTPUT_DIR}/")
    print(f"{'=' * 60}\n")

    # S3 upload
    if not args.skip_upload and generated > 0:
        bucket = os.getenv("S3_BUCKET")
        prefix = os.getenv("S3_SYNTHETIC_PREFIX", "synthetic/policies")
        if bucket:
            session = boto3.Session(
                profile_name=os.getenv("AWS_PROFILE"),
                region_name=os.getenv("AWS_REGION", "eu-west-1"),
            )
            upload_to_s3(session, bucket, prefix)
        else:
            logger.warning("S3_BUCKET not set in .env — skipping upload")


if __name__ == "__main__":
    main()
