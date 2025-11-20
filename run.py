import os
import sys
import subprocess
from datetime import datetime

from utilities.report_reader import read_pytest_json
from utilities.allure_zipper import zip_allure_report
from utilities.email_configuration import send_report_email
from utilities.email_html_builder import build_email_body


def main():
    # STEP 1 — Create timestamped results folder
    time_stamp = datetime.now().strftime("%Y-%m-%d__%H-%M-%S")
    results_dir = os.path.join("allure-results", time_stamp)
    os.makedirs(results_dir, exist_ok=True)

    # Pytest JSON summary file will be placed here
    json_report_path = os.path.join(results_dir, "report.json")

    # Accept pytest arguments from CLI
    args = sys.argv[1:]

    # STEP 2 — Build pytest command
    pytest_cmd = [
        "pytest",
        "-vs",
        f"--alluredir={results_dir}",
        "--json-report",
        f"--json-report-file={json_report_path}"
    ] + args

    print("\nRunning:", " ".join(pytest_cmd))

    # STEP 3 — Run tests
    subprocess.run(pytest_cmd)

    # STEP 4 — Generate HTML Allure report
    html_report_dir = "allure-report"   # always overwrite old one safely
    subprocess.run(["allure", "generate", results_dir, "-o", html_report_dir, "--clean"])

    # STEP 5 — Read test summary from pytest JSON
    total, passed, failed, skipped, duration = read_pytest_json(json_report_path)

    # STEP 6 — Build HTML email summary
    summary_html = build_email_body(total, passed, failed, skipped, duration)

    # STEP 7 — ZIP Allure HTML report
    zip_path = zip_allure_report(html_report_dir)

    # STEP 8 — Send Email
    send_report_email(summary_html, zip_path)

    print("\nAllure Report & Email Completed Successfully!\n")


if __name__ == "__main__":
    main()
