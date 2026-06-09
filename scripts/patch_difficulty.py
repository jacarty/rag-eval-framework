"""Patch qa_pairs.json: re-admit difficulty-only failures with corrected difficulty.

Reads qa_failed.json, identifies pairs where correctness=pass AND
source_completeness=pass (i.e. only failed on difficulty), applies
the critic's suggested_difficulty, and appends them to qa_pairs.json.
"""

import json
from pathlib import Path

QA_DIR = Path("data/qa")

failed = json.loads((QA_DIR / "qa_failed.json").read_text())
passed = json.loads((QA_DIR / "qa_pairs.json").read_text())

recovered = []
still_failed = []

for pair in failed:
    cr = pair.get("critic_result", {})
    correctness_ok = cr.get("correctness") == "pass"
    source_ok = cr.get("source_completeness") == "pass"
    difficulty_bad = not cr.get("difficulty_reasonable", True)

    if correctness_ok and source_ok and difficulty_bad:
        # Re-admit with corrected difficulty
        clean = {
            "question_id": "",  # will be renumbered
            "question": pair["question"],
            "answer": pair["answer"],
            "source_sections": pair["source_sections"],
            "difficulty": cr.get("suggested_difficulty", pair.get("difficulty", "medium")),
            "type": pair["type"],
            "difficulty_original": pair.get("difficulty"),
        }
        recovered.append(clean)
    else:
        still_failed.append(pair)

# Append recovered to passed and renumber all
all_pairs = passed + recovered
for i, pair in enumerate(all_pairs):
    pair["question_id"] = f"q{i + 1:03d}"

(QA_DIR / "qa_pairs.json").write_text(json.dumps(all_pairs, indent=2))
(QA_DIR / "qa_failed.json").write_text(json.dumps(still_failed, indent=2))

# Stats
type_counts = {}
diff_counts = {}
for p in all_pairs:
    type_counts[p["type"]] = type_counts.get(p["type"], 0) + 1
    diff_counts[p["difficulty"]] = diff_counts.get(p["difficulty"], 0) + 1

print(f"Recovered {len(recovered)} pairs, {len(still_failed)} still failed")
print(f"Total Q&A pairs: {len(all_pairs)}")
print("\nBy type:")
for t, c in sorted(type_counts.items()):
    print(f"  {t:25s} {c:4d}")
print("\nBy difficulty:")
for d, c in sorted(diff_counts.items()):
    print(f"  {d:25s} {c:4d}")
