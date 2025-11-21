import shutil
import os

def zip_allure_report(report_dir, zip_name="allure-report"):
    zip_path = f"{zip_name}.zip"

    if os.path.exists(zip_path):
        os.remove(zip_path)

    shutil.make_archive(zip_name, "zip", report_dir)
    return zip_path
