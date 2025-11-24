import os
import subprocess
from utilities.config_reader import get_config


def deploy_to_netlify(folder_path):
    token = get_config("Netlify", "auth_token")
    site_id = get_config("Netlify", "site_id")

    cmd = [
        "netlify",
        "deploy",
        "--dir", folder_path,
        "--prod",
        "--auth", token,
        "--site", site_id
    ]

    print("Running Netlify deployment...")
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print("❌ Netlify Upload Failed")
        print(result.stderr)
        raise Exception("Netlify deploy failed")

    print("✅ Netlify Upload Successful")
    print(result.stdout)

    # Extract final URL from CLI output
    link = extract_final_url(result.stdout)

    if not link:
        raise Exception("❌ Could not extract website URL from Netlify output")

    return link


def extract_final_url(output):
    """
    Extracts the production URL ONLY.
    """

    for line in output.splitlines():
        line = line.strip()

        if "Deployed to production URL:" in line:
            url = "http" + line.split("http", 1)[1]
            return url.rstrip("│║╚╝╔╗─— ").strip()

    # fallback in case format changes
    for line in output.splitlines():
        line = line.strip()
        if "http" in line:
            url = "http" + line.split("http", 1)[1]
            return url.rstrip("│║╚╝╔╗─— ").strip()

    return None



