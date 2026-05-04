import hashlib
import os
import re
import subprocess
import sys
import urllib.request

CASK_PATH = "Casks/filezilla.rb"
# SourceForge RSS is the most reliable way to find versions that actually exist on mirrors
SOURCEFORGE_RSS = (
    "https://sourceforge.net/projects/filezilla/rss?path=/FileZilla_Client"
)
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# A list of known SourceForge mirrors
MIRRORS = [
    "netix",
    "versaweb",
    "ayera",
    "nchc",
    "jaist",
    "freefr",
    "kumasan",
    "cfhcable",
    "iweb",
    "phoenixnap",
    "superb-sea2",
    "tenet",
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
            # Look for version numbers in the RSS feed
            # Pattern matches things like /FileZilla_Client/3.69.3/
            matches = re.findall(
                r"/FileZilla_Client/([0-9]+\.[0-9]+\.[0-9]+(?:\.[0-9]+)?)/", xml
            )
            if matches:
                # Get the most recent one (usually the first)
                return sorted(
                    list(set(matches)), key=lambda v: [int(x) for x in v.split(".")]
                )[-1]
            return None
    except Exception as e:
        print(f"Failed to check SourceForge RSS: {e}")
        return None


def get_sha256(version, filename):
    temp_file = f"fz_{filename}"

    # Try multiple mirrors
    for mirror in MIRRORS:
        url = f"https://{mirror}.dl.sourceforge.net/project/filezilla/FileZilla_Client/{version}/{filename}"

        print(f"Trying mirror {mirror}: {url}")

        try:
            result = subprocess.run(
                [
                    "curl",
                    "-L",
                    "-f",
                    "-A",
                    USER_AGENT,
                    "--connect-timeout",
                    "15",
                    "-e",
                    "https://filezilla-project.org/",
                    "-o",
                    temp_file,
                    url,
                ],
                capture_output=True,
            )

            if result.returncode != 0:
                print(f"Mirror {mirror} failed or timed out.")
                continue

            if not os.path.exists(temp_file):
                continue

            size = os.path.getsize(temp_file)
            if size < 1000000:
                print(
                    f"Mirror {mirror} returned a file that is too small ({size} bytes)."
                )
                os.remove(temp_file)
                continue

            print(f"Successfully downloaded {filename} from {mirror} ({size} bytes).")
            sha256_hash = hashlib.sha256()
            with open(temp_file, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)

            os.remove(temp_file)
            return sha256_hash.hexdigest()

        except Exception as e:
            print(f"Exception during mirror {mirror} attempt: {e}")
            if os.path.exists(temp_file):
                os.remove(temp_file)
            continue

    print(f"All mirrors failed for {filename}.")
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
        print("Could not find latest version on SourceForge.")
        sys.exit(1)

    with open(CASK_PATH, "r") as f:
        current_content = f.read()
        version_match = re.search(r'version "(.*)"', current_content)
        current_version = version_match.group(1) if version_match else None

    print(f"Current version: {current_version}")
    print(f"Latest version (on SourceForge): {latest_version}")

    # If the version in the Cask is actually NEWER than SourceForge (manual update),
    # we don't want to "downgrade" it. But we DO want to fix PLACEHOLDERs.
    is_placeholder = "PLACEHOLDER" in current_content

    if current_version == latest_version and not is_placeholder:
        print("Already up to date.")
        return

    # Simple version comparison
    def version_tuple(v):
        return tuple(map(int, (v.split("."))))

    if (
        not is_placeholder
        and current_version
        and version_tuple(current_version) > version_tuple(latest_version)
    ):
        print(
            f"Cask version ({current_version}) is newer than SourceForge ({latest_version}). Waiting for mirrors."
        )
        return

    print(f"Updating to {latest_version}...")

    arm_filename = f"FileZilla_{latest_version}_macos-arm64.app.tar.bz2"
    intel_filename = f"FileZilla_{latest_version}_macosx-x86.app.tar.bz2"

    arm_sha = get_sha256(latest_version, arm_filename)
    intel_sha = get_sha256(latest_version, intel_filename)

    if not arm_sha or not intel_sha:
        print("Failed to get SHAs from any mirror. Skipping update.")
        sys.exit(1)

    update_cask(latest_version, arm_sha, intel_sha)
    print("Cask updated successfully.")


if __name__ == "__main__":
    main()
