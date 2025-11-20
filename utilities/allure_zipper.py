import os
import pyminizip

def zip_allure_report(report_dir, zip_name="allure-report", password="FatakPay123"):
    zip_path = f"{zip_name}.zip"

    # Remove old file
    if os.path.exists(zip_path):
        os.remove(zip_path)

    # Compress (level 5)
    pyminizip.compress_multiple([report_dir], [], zip_path, password, 5)

    return zip_path