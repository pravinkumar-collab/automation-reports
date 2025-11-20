import json

def read_pytest_json(path):
    """Reads pytest JSON summary file and extracts test statistics."""
    with open(path, "r") as f:
        data = json.load(f)

    total = data["summary"]["total"]
    passed = data["summary"].get("passed", 0)
    failed = data["summary"].get("failed", 0)
    skipped = data["summary"].get("skipped", 0)
    duration = data["duration"]

    return total, passed, failed, skipped, duration
