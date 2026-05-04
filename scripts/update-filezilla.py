import hashlib
import re
import sys
import urllib.request

CASK_PATH = "Casks/filezilla.rb"
UPTODOWN_URL = "https://filezilla.en.uptodown.com/mac/versions"
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"


def get_latest_version():
    req = urllib.request.Request(UPTODOWN_URL, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req) as response:
        html = response.read().decode("utf-8")
        matches = re.findall(r"3\.[0-9]+\.[0-9]+(?:\.[0-9]+)?", html)
        return matches[0] if matches else None


def get_sha256(url):
    print(f"Downloading from {url}...")
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req) as response:
            data = response.read()
            # FileZilla archives are typically > 10MB
            if len(data) < 1000000:
                print(
                    f"Error: Downloaded file too small ({len(data)} bytes). Likely blocked."
                )
                return None
            return hashlib.sha256(data).hexdigest()
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
