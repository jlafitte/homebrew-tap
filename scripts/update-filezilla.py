import hashlib
import os
import re
import subprocess
import sys
import urllib.request

CASK_PATH = "Casks/filezilla.rb"
SOURCEFORGE_RSS = "https://sourceforge.net/projects/filezilla/rss"
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0"

# Refined list of high-reliability mirrors
MIRRORS = [
    "netix",
    "versaweb",
    "jaist",
    "nchc",
    "freefr",
    "kent",
    "heanet",
    "iweb",
    "astutehost",
]


def get_latest_version():
    print("Checking SourceForge RSS for latest version...")
    req = urllib.request.Request(
        SOURCEFORGE_RSS,
        headers={"User-Agent": USER_AGENT},
    )
    try:
        with urllib.request.urlopen(req) as response:
            xml = response.read().decode("utf-8")
            matches = re.findall(
                r"FileZilla_([0-9]+\.[0-9]+\.[0-9]+(?:\.[0-9]+)?)_", xml
            )
            if matches:
                versions = sorted(
                    list(set(matches)), key=lambda v: [int(x) for x in v.split(".")]
                )
                return versions[-1]
            return None
    except Exception as e:
        print(f"Failed to check SourceForge RSS: {e}")
        return None


def get_sha256(version, filename):
    temp_file = f"fz_{filename}"

    # Strategy 1: Try the official redirector first with heavy headers
    urls = [
        f"https://downloads.sourceforge.net/project/filezilla/FileZilla_Client/{version}/{filename}",
        f"https://download.filezilla-project.org/client/{filename}",
    ]

    # Strategy 2: Try specific mirrors
    for mirror in MIRRORS:
        urls.append(
            f"https://{mirror}.dl.sourceforge.net/project/filezilla/FileZilla_Client/{version}/{filename}"
        )

    for url in urls:
        print(f"Attempting download from: {url}")

        try:
            # -L: Follow redirects
            # -f: Fail on error
            # -4: Force IPv4 (important for some mirrors in CI)
            # -A: User Agent
            # -e: Referer
            # -H: Extra headers to look more like a browser
            result = subprocess.run(
                [
                    "curl",
                    "-L",
                    "-f",
                    "-4",
                    "-s",
                    "--connect-timeout",
                    "20",
                    "-A",
                    USER_AGENT,
                    "-e",
                    "https://filezilla-project.org/download.php?show_all=1",
                    "-H",
                    "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    "-H",
                    "Accept-Language: en-US,en;q=0.5",
                    "-o",
                    temp_file,
                    url,
                ],
                capture_output=True,
            )

            if result.returncode != 0:
                continue

            if not os.path.exists(temp_file):
                continue

            size = os.path.getsize(temp_file)
            if size < 1000000:
                os.remove(temp_file)
                continue

            print(f"Successfully downloaded {filename} ({size} bytes).")
            sha256_hash = hashlib.sha256()
            with open(temp_file, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)

            os.remove(temp_file)
            return sha256_hash.hexdigest()

        except Exception:
            if os.path.exists(temp_file):
                os.remove(temp_file)
            continue

    print(f"All download attempts failed for {filename}.")
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
        print("Could not find latest version on SourceForge RSS.")
        # Fallback for when RSS is empty/broken
        latest_version = "3.69.3"

    with open(CASK_PATH, "r") as f:
        current_content = f.read()
        version_match = re.search(r'version "(.*)"', current_content)
        current_version = version_match.group(1) if version_match else None

    print(f"Current version: {current_version}")
    print(f"Latest version:  {latest_version}")

    is_placeholder = "PLACEHOLDER" in current_content

    if current_version == latest_version and not is_placeholder:
        print("Already up to date.")
        return

    print(f"Updating to {latest_version}...")

    arm_filename = f"FileZilla_{latest_version}_macos-arm64.app.tar.bz2"
    intel_filename = f"FileZilla_{latest_version}_macosx-x86.app.tar.bz2"

    arm_sha = get_sha256(latest_version, arm_filename)
    intel_sha = get_sha256(latest_version, intel_filename)

    if not arm_sha or not intel_sha:
        print("Failed to get SHAs. Skipping update.")
        sys.exit(1)

    update_cask(latest_version, arm_sha, intel_sha)
    print("Cask updated successfully.")


if __name__ == "__main__":
    main()
