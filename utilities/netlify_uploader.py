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
    Extracts a clean Netlify URL from CLI output.
    Removes Unicode borders and trailing junk characters.
    """

    for line in output.splitlines():
        line = line.strip()

        if "http" in line:
            # Isolate starting from the first "http"
            url = "http" + line.split("http", 1)[1]

            # Remove trailing box characters (│ ╯ ╰ etc.)
            url = url.rstrip("│║╚╝╔╗─— ")

            # Remove surrounding whitespace
            return url.strip()

    return None


