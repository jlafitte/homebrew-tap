import hashlib
import os
import re
import subprocess
import sys
import urllib.request

CASK_PATH = "Casks/filezilla.rb"
UPTODOWN_URL = "https://filezilla.en.uptodown.com/mac/versions"
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"


def get_latest_version():
    req = urllib.request.Request(
        UPTODOWN_URL,
        headers={
            "User-Agent": USER_AGENT,
            "Referer": "https://filezilla.en.uptodown.com/mac",
        },
    )
    with urllib.request.urlopen(req) as response:
        html = response.read().decode("utf-8")
        matches = re.findall(r"3\.[0-9]+\.[0-9]+(?:\.[0-9]+)?", html)
        return matches[0] if matches else None


def get_sha256(url):
    print(f"Downloading from {url}...")
    temp_file = "fz_temp.tar.bz2"
    try:
        # Using curl to handle the SourceForge redirect mess
        # -L follows redirects
        # -A sets user agent
        # -e sets referer
        result = subprocess.run(
            [
                "curl",
                "-L",
                "-A",
                USER_AGENT,
                "-e",
                "https://filezilla-project.org/",
                "-o",
                temp_file,
                url,
            ],
            capture_output=True,
        )

        if result.returncode != 0:
            print(f"Curl failed: {result.stderr.decode()}")
            return None

        if not os.path.exists(temp_file) or os.path.getsize(temp_file) < 1000000:
            print("Error: Downloaded file too small or missing. Likely blocked.")
            # If it's small, it might be an error page. Let's see what's in it.
            if os.path.exists(temp_file):
                with open(temp_file, "r", errors="ignore") as f:
                    print(f"File content start: {f.read(100)}")
                os.remove(temp_file)
            return None

        sha256_hash = hashlib.sha256()
        with open(temp_file, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)

        os.remove(temp_file)
        return sha256_hash.hexdigest()
    except Exception as e:
        print(f"Download failed: {e}")
        return None


def update_cask(version, arm_sha, intel_sha):
    with open(CASK_PATH, "r") as f:
        content = f.read()

    content = re.sub(r'version ".*"', f'version "{version}"', content)
    content = re.sub(r'sha256 arm:\s+".*"', f'sha256 arm:   "{arm_sha}"', content)
    content = re.sub(r'intel:\s+".*"', f'intel: "{intel_sha}"', content)

    with open(CASK_PATH, "w") as f:
        f.write(content)


def main():
    latest_version = get_latest_version()
    if not latest_version:
        print("Could not find latest version.")
        sys.exit(1)

    with open(CASK_PATH, "r") as f:
        current_content = f.read()
        version_match = re.search(r'version "(.*)"', current_content)
        current_version = version_match.group(1) if version_match else None

    print(f"Current version: {current_version}")
    print(f"Latest version:  {latest_version}")

    if current_version == latest_version and "PLACEHOLDER" not in current_content:
        print("Already up to date.")
        return

    print(f"Updating to {latest_version}...")

    # Try SourceForge
    arm_url = f"https://downloads.sourceforge.net/project/filezilla/FileZilla_Client/{latest_version}/FileZilla_{latest_version}_macos-arm64.app.tar.bz2"
    intel_url = f"https://downloads.sourceforge.net/project/filezilla/FileZilla_Client/{latest_version}/FileZilla_{latest_version}_macosx-x86.app.tar.bz2"

    arm_sha = get_sha256(arm_url)
    intel_sha = get_sha256(intel_url)

    if not arm_sha or not intel_sha:
        print("Failed to get SHAs. Skipping update.")
        sys.exit(1)

    update_cask(latest_version, arm_sha, intel_sha)
    print("Cask updated successfully.")


if __name__ == "__main__":
    main()
