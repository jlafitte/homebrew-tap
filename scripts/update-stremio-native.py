import hashlib
import os
import re
import subprocess
import sys
import xml.etree.ElementTree as ET

CASK_PATH = "Casks/stremio-native.rb"
FEED_URL = "https://dl.strem.io/apple/macos/source.xml"


def get_latest_release():
    print(f"Checking Sparkle feed at {FEED_URL} for latest version...")
    try:
        result = subprocess.run(
            ["curl", "-L", "-s", FEED_URL], capture_output=True, text=True
        )
        if result.returncode != 0:
            print(f"Failed to fetch feed. Error: {result.stderr}")
            return None, None

        root = ET.fromstring(result.stdout)
        channel = root.find("channel")
        items = channel.findall("item") if channel is not None else []
        if not items:
            print("No items found in feed.")
            return None, None

        latest_item = items[0]
        enclosure = latest_item.find("enclosure")
        if enclosure is None:
            print("No enclosure found in latest item.")
            return None, None

        url = enclosure.get("url")
        if not url:
            print("Enclosure has no URL attribute.")
            return None, None

        match = re.search(
            r"Stremio[._-]v?(\d+(?:\.\d+)+)[._-](\d+.*?)\.zip", url, re.IGNORECASE
        )
        if not match:
            print(f"Could not parse version from URL: {url}")
            return None, None

        version = f"{match.group(1)},{match.group(2)}"
        return version, url
    except Exception as e:
        print(f"Exception during version check: {e}")
        return None, None


def get_sha256(url):
    print(f"Downloading release archive from {url}...")
    temp_file = "stremio-native.zip"
    try:
        result = subprocess.run(
            ["curl", "-L", "-s", "-o", temp_file, url], capture_output=True
        )
        if result.returncode != 0:
            print(f"Download failed. Error: {result.stderr.decode()}")
            return None

        sha256_hash = hashlib.sha256()
        with open(temp_file, "rb") as f:
            for byte_block in iter(lambda: f.read(65536), b""):
                sha256_hash.update(byte_block)

        os.remove(temp_file)
        return sha256_hash.hexdigest()
    except Exception as e:
        print(f"Exception during download/hash calculation: {e}")
        if os.path.exists(temp_file):
            os.remove(temp_file)
        return None


def update_cask(version, sha256):
    with open(CASK_PATH, "r") as f:
        content = f.read()

    content = re.sub(r'version ".*"', f'version "{version}"', content)
    content = re.sub(r'sha256 ".*"', f'sha256 "{sha256}"', content)

    with open(CASK_PATH, "w") as f:
        f.write(content)


def main():
    latest_version, download_url = get_latest_release()
    if not latest_version or not download_url:
        print("Could not find latest release information.")
        sys.exit(1)

    with open(CASK_PATH, "r") as f:
        current_content = f.read()
        version_match = re.search(r'version "(.*)"', current_content)
        current_version = version_match.group(1) if version_match else None

    print(f"Current version in Tap: {current_version}")
    print(f"Latest version online:  {latest_version}")

    if current_version == latest_version:
        print("✅ Stremio Native is up to date.")
        return

    print(f"🚀 Updating to {latest_version}...")
    new_sha = get_sha256(download_url)
    if not new_sha:
        print("❌ Failed to calculate SHA256.")
        sys.exit(1)

    update_cask(latest_version, new_sha)
    print("✨ Cask updated successfully.")


if __name__ == "__main__":
    main()
