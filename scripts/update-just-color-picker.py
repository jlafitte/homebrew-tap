import hashlib
import os
import re
import subprocess
import sys

CASK_PATH = "Casks/just-color-picker.rb"
HOMEPAGE_URL = "https://annystudio.com/software/colorpicker/"
DMG_URL = "https://annystudio.com/software/colorpicker/jcpicker.dmg"


def get_latest_version():
    print(f"Checking {HOMEPAGE_URL} for latest version...")
    try:
        result = subprocess.run(
            ["curl", "-L", "-s", HOMEPAGE_URL], capture_output=True, text=True
        )
        if result.returncode != 0:
            print(f"Failed to fetch homepage. Error: {result.stderr}")
            return None

        # Regex based on the livecheck pattern: Download free Just Color Picker v?(\d+(?:\.\d+)+)
        match = re.search(
            r"Download\s+free\s+Just\s+Color\s+Picker\s+v?(\d+(?:\.\d+)+)",
            result.stdout,
            re.IGNORECASE,
        )
        if match:
            return match.group(1)

        print("Could not find version match on the homepage.")
        return None
    except Exception as e:
        print(f"Exception during version check: {e}")
        return None


def get_sha256():
    print(f"Downloading DMG from {DMG_URL}...")
    temp_file = "jcpicker.dmg"
    try:
        result = subprocess.run(
            ["curl", "-L", "-s", "-o", temp_file, DMG_URL], capture_output=True
        )
        if result.returncode != 0:
            print(f"Download failed. Error: {result.stderr.decode()}")
            return None

        sha256_hash = hashlib.sha256()
        with open(temp_file, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)

        os.remove(temp_file)
        return sha256_hash.hexdigest()
    except Exception as e:
        print(f"Exception during download/hash calculation: {e}")
        return None


def update_cask(version, sha256):
    with open(CASK_PATH, "r") as f:
        content = f.read()

    content = re.sub(r'version ".*"', f'version "{version}"', content)
    content = re.sub(r'sha256 ".*"', f'sha256 "{sha256}"', content)

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

    if current_version == latest_version:
        print("✅ Just Color Picker is up to date.")
        return

    print(f"🚀 Updating to {latest_version}...")
    new_sha = get_sha256()
    if not new_sha:
        print("❌ Failed to get SHA256.")
        sys.exit(1)

    update_cask(latest_version, new_sha)
    print("✨ Cask updated successfully.")


if __name__ == "__main__":
    main()
