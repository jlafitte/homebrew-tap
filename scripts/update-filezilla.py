import hashlib
import os
import re
import subprocess
import sys

CASK_PATH = "Casks/filezilla.rb"
OFFICIAL_FEED = "https://filezilla-project.org/newsfeed.php"
# The "backdoor" User-Agent that FileZilla's servers trust
BASE_USER_AGENT = "FileZilla/{version}"


def get_latest_version():
    print("Checking official FileZilla news feed for latest version...")
    # Use an older but valid FileZilla UA to check the feed
    try:
        result = subprocess.run(
            [
                "curl",
                "-L",
                "-f",
                "-s",
                "-A",
                "FileZilla/3.67.0",
                OFFICIAL_FEED,
            ],
            capture_output=True,
        )

        if result.returncode != 0:
            print(f"Failed to fetch news feed. Curl error: {result.stderr.decode()}")
            return None

        xml = result.stdout.decode("utf-8")
        matches = re.findall(
            r"FileZilla Client ([0-9]+\.[0-9]+\.[0-9]+(?:\.[0-9]+)?) released", xml
        )
        if matches:
            return sorted(
                list(set(matches)), key=lambda v: [int(x) for x in v.split(".")]
            )[-1]

        print("Could not find version matches in the feed content.")
        print(f"Content preview: {xml[:200]}")
        return None
    except Exception as e:
        print(f"Exception during version check: {e}")
        return None


def get_sha256(version, arch):
    filename = f"FileZilla_{version}_{arch}.app.tar.bz2"
    url = f"https://download.filezilla-project.org/client/{filename}"
    temp_file = f"fz_{arch}.tar.bz2"
    user_agent = BASE_USER_AGENT.format(version=version)

    print(f"Downloading {filename} using User-Agent: {user_agent}")

    try:
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

    is_placeholder = "PLACEHOLDER" in current_content

    if current_version == latest_version and not is_placeholder:
        print("✅ FileZilla is up to date.")
        return

    print(f"🚀 Updating to {latest_version}...")

    arm_sha = get_sha256(latest_version, "macos-arm64")
    intel_sha = get_sha256(latest_version, "macos-x86")

    if not arm_sha or not intel_sha:
        print("❌ Failed to get SHAs.")
        sys.exit(1)

    update_cask(latest_version, arm_sha, intel_sha)
    print("✨ Cask updated successfully.")


if __name__ == "__main__":
    main()
