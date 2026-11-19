"""Check that contract examples match their schemas, and that data/vocabulary.csv follows C1.

Run: pip install jsonschema && python scripts/validate_contracts.py
Exit code 1 if anything is wrong (used by CI on every pull request).
"""
import csv
import json
import re
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parent.parent
CONTRACTS = ROOT / "docs" / "contracts"
VOCAB = ROOT / "data" / "vocabulary.csv"
VOCAB_COLUMNS = ["sign_id", "ar_eg", "ar_msa", "en", "category", "source", "esl_verified", "urgent", "video_file", "has_animation"]
CATEGORIES = {"basics", "people", "places", "appointments", "time", "symptoms", "body", "tests", "payment", "numbers", "letters"}

errors = []


def check_schemas():
    schemas = sorted((CONTRACTS / "schemas").glob("*.schema.json"))
    for schema_file in schemas:
        schema = json.loads(schema_file.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
        name = schema_file.name.replace(".schema.json", "")
        example = CONTRACTS / "examples" / f"{name}.json"
        if not example.exists():
            errors.append(f"{name}: missing example {example.relative_to(ROOT)}")
            continue
        for err in Draft202012Validator(schema).iter_errors(json.loads(example.read_text(encoding="utf-8"))):
            errors.append(f"{name}: example does not match schema at {list(err.path)}: {err.message}")
    print(f"checked {len(schemas)} schemas")


def check_vocabulary():
    if not VOCAB.exists():
        print("data/vocabulary.csv not created yet (role 1, week 2): skipped")
        return
    with VOCAB.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != VOCAB_COLUMNS:
            errors.append(f"vocabulary.csv columns must be exactly: {','.join(VOCAB_COLUMNS)}")
            return
        seen = set()
        rows = 0
        for i, row in enumerate(reader, start=2):
            rows += 1
            sid = row["sign_id"]
            if not re.fullmatch(r"S\d{3}", sid):
                errors.append(f"vocabulary.csv line {i}: bad sign_id {sid!r}")
            if sid in seen:
                errors.append(f"vocabulary.csv line {i}: duplicate sign_id {sid}")
            seen.add(sid)
            if row["category"] not in CATEGORIES:
                errors.append(f"vocabulary.csv line {i}: unknown category {row['category']!r}")
            for col in ("esl_verified", "urgent", "has_animation"):
                if row[col] not in ("yes", "no"):
                    errors.append(f"vocabulary.csv line {i}: {col} must be yes or no")
            if not row["ar_eg"].strip() or not row["en"].strip():
                errors.append(f"vocabulary.csv line {i}: ar_eg and en are required")
    print(f"checked vocabulary.csv: {rows} signs")


check_schemas()
check_vocabulary()
if errors:
    print("\nCONTRACT PROBLEMS:")
    for e in errors:
        print(" -", e)
    sys.exit(1)
print("all contracts OK")
