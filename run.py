import os
import sys
import subprocess
from datetime import datetime

from utilities.netlify_uploader import deploy_to_netlify
from utilities.report_reader import read_pytest_json
from utilities.email_configuration import send_report_email
from utilities.email_html_builder import build_email_body


def main():

    # STEP 1 — Create timestamped allure-results folder
    time_stamp = datetime.now().strftime("%Y-%m-%d__%H-%M-%S")
    results_dir = os.path.join("allure-results", time_stamp)
    os.makedirs(results_dir, exist_ok=True)

    # JSON summary path
    json_report_path = os.path.join(results_dir, "report.json")

    # Collect pytest args
    args = sys.argv[1:]

    # STEP 2 — Run pytest with Allure + JSON report enabled
    pytest_cmd = [
        "pytest",
        "-vs",
        f"--alluredir={results_dir}",
        "--json-report",
        f"--json-report-file={json_report_path}",
    ] + args

    print("\nRunning:", " ".join(pytest_cmd))
    subprocess.run(pytest_cmd)

    # STEP 3 — Generate Allure HTML report
    html_report_dir = "allure-report"
    subprocess.run(["allure", "generate", results_dir, "-o", html_report_dir, "--clean"])
    print("HTML report generated at:", html_report_dir)

    # STEP 4 — Get test summary
    total, passed, failed, skipped, duration = read_pytest_json(json_report_path)

    # STEP 5 — Upload to Netlify
    print("\nUploading Allure report to Netlify...")
    website_link = deploy_to_netlify(html_report_dir)

    print("✅ Uploaded to Netlify:", website_link)

    # STEP 6 — Build the email HTML body
    summary_html = build_email_body(total, passed, failed, skipped, duration, website_link)

    # STEP 7 — Send email
    send_report_email(summary_html)

    print("\n Allure Report Uploaded & Email Sent Successfully!\n")


if __name__ == "__main__":
    main()
