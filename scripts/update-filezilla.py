import hashlib
import os
import re
import subprocess
import sys
import urllib.request

CASK_PATH = "Casks/filezilla.rb"
UPTODOWN_URL = "https://filezilla.en.uptodown.com/mac/versions"
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# A list of known SourceForge mirrors that often bypass the Cloudflare landing page
MIRRORS = [
    "netix",
    "versaweb",
    "ayera",
    "nchc",
    "jaist",
    "master.dl",
    "freefr",
    "kumasan",
]


def get_latest_version():
    print("Checking for latest version...")
    req = urllib.request.Request(
        UPTODOWN_URL,
        headers={
            "User-Agent": USER_AGENT,
            "Referer": "https://filezilla.en.uptodown.com/mac",
        },
    )
    try:
        with urllib.request.urlopen(req) as response:
            html = response.read().decode("utf-8")
            matches = re.findall(r"3\.[0-9]+\.[0-9]+(?:\.[0-9]+)?", html)
            return matches[0] if matches else None
    except Exception as e:
        print(f"Failed to check Uptodown: {e}")
        return None


def get_sha256(version, filename):
    temp_file = f"fz_{filename}"

    # Try multiple mirrors
    for mirror in MIRRORS:
        url = f"https://{mirror}.sourceforge.net/project/filezilla/FileZilla_Client/{version}/{filename}"
        # Some mirrors use a slightly different path
        if mirror == "master.dl":
            url = f"https://master.dl.sourceforge.net/project/filezilla/FileZilla_Client/{version}/{filename}"

        print(f"Trying mirror {mirror}: {url}")

        try:
            # -L follows redirects
            # -f fails on 404/500
            # -s is silent but we want error info if it fails
            result = subprocess.run(
                [
                    "curl",
                    "-L",
                    "-f",
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
                print(f"Mirror {mirror} failed (HTTP error or connection issue).")
                continue

            # Check if we actually got a file and not an HTML error page
            if not os.path.exists(temp_file):
                continue

            size = os.path.getsize(temp_file)
            if size < 1000000:
                print(
                    f"Mirror {mirror} returned a file that is too small ({size} bytes). Likely a redirect or error page."
                )
                with open(temp_file, "r", errors="ignore") as f:
                    print(f"Preview: {f.read(100)}")
                os.remove(temp_file)
                continue

            # Success! Calculate hash
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
    # The intel line might be harder to match if it's not the first sha256 line
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

    needs_update = (current_version != latest_version) or (
        "PLACEHOLDER" in current_content
    )

    if not needs_update:
        print("Already up to date.")
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
