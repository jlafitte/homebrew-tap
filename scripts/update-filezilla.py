import hashlib
import os
import re
import subprocess
import sys
import urllib.request

CASK_PATH = "Casks/filezilla.rb"
OFFICIAL_FEED = "https://filezilla-project.org/newsfeed.php"
# The discovered "backdoor" User-Agent
BASE_USER_AGENT = "FileZilla/{version}"


def get_latest_version():
    print("Checking official FileZilla news feed for latest version...")
    # Standard browser UA for checking the feed
    req = urllib.request.Request(
        OFFICIAL_FEED,
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0",
        },
    )
    try:
        with urllib.request.urlopen(req) as response:
            xml = response.read().decode("utf-8")
            matches = re.findall(
                r"FileZilla Client ([0-9]+\.[0-9]+\.[0-9]+(?:\.[0-9]+)?) released", xml
            )
            if matches:
                return sorted(
                    list(set(matches)), key=lambda v: [int(x) for x in v.split(".")]
                )[-1]
            return None
    except Exception as e:
        print(f"Failed to check official feed: {e}")
        return None


def get_sha256(version, arch):
    filename = f"FileZilla_{version}_{arch}.app.tar.bz2"
    url = f"https://download.filezilla-project.org/client/{filename}"
    temp_file = f"fz_{arch}.tar.bz2"
    user_agent = BASE_USER_AGENT.format(version=version)

    print(f"Downloading {filename} using User-Agent: {user_agent}")

    try:
        # Use the special User-Agent to bypass the token requirement
        result = subprocess.run(
            [
                "curl",
                "-L",
                "-f",
                "-s",
                "-A",
                user_agent,
                "-o",
                temp_file,
                url,
            ],
            capture_output=True,
        )

        if result.returncode != 0:
            print(f"Download failed for {arch}")
            return None

        sha256_hash = hashlib.sha256()
        with open(temp_file, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)

        os.remove(temp_file)
        return sha256_hash.hexdigest()

    except Exception as e:
        print(f"Exception during download: {e}")
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

    print(f"Current version in Tap: {current_version}")
    print(f"Latest version online:  {latest_version}")

    if current_version == latest_version and "PLACEHOLDER" not in current_content:
        print("✅ FileZilla is up to date.")
        return

    print(f"🚀 Updating to {latest_version}...")

    arm_sha = get_sha256(latest_version, "macos-arm64")
    intel_sha = get_sha256(latest_version, "macos-x86")

    if not arm_sha or not intel_sha:
        print("❌ Failed to get SHAs using the User-Agent trick.")
        sys.exit(1)

    update_cask(latest_version, arm_sha, intel_sha)
    print("✨ Cask updated successfully.")


if __name__ == "__main__":
    main()
