import os
import sys
import subprocess
from datetime import datetime

from utilities.report_reader import read_pytest_json
from utilities.allure_zipper import zip_allure_report
from utilities.email_configuration import send_report_email
from utilities.email_html_builder import build_email_body
from utilities.drive_uploader import upload_file_to_drive


def main():

    # STEP 1 — Create timestamped results folder
    time_stamp = datetime.now().strftime("%Y-%m-%d__%H-%M-%S")
    results_dir = os.path.join("allure-results", time_stamp)
    os.makedirs(results_dir, exist_ok=True)

    # JSON summary path
    json_report_path = os.path.join(results_dir, "report.json")

    args = sys.argv[1:]

    # STEP 2 — Run Pytest with Allure + JSON Report
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
    html_report_dir = "allure-report"  # overwrite cleanly
    subprocess.run(["allure", "generate", results_dir, "-o", html_report_dir, "--clean"])
    print("HTML report generated at:", html_report_dir)

    # STEP 4 — Get test summary
    total, passed, failed, skipped, duration = read_pytest_json(json_report_path)

    # STEP 5 — ZIP the Allure HTML report
    zip_path = zip_allure_report(html_report_dir)
    print("Zipped report:", zip_path)

    # STEP 6 — Upload ZIP to Google Drive
    drive_link = upload_file_to_drive(zip_path)
    print("Uploaded report link:", drive_link)

    # STEP 7 — Build email HTML with link
    summary_html = build_email_body(total, passed, failed, skipped, duration, drive_link)

    # STEP 9 — Send Email (HTML)
    send_report_email(summary_html)

    print("\nAllure Report Uploaded & Email Sent Successfully!\n")


if __name__ == "__main__":
    main()
