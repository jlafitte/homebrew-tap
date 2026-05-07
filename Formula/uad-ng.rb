class UadNg < Formula
  desc "Cross-platform GUI written in Rust to debloat Android devices"
  homepage "https://github.com/Universal-Debloater-Alliance/universal-android-debloater-next-generation"

  livecheck do
    url :stable
    strategy :github_latest
  end

  if Hardware::CPU.intel?
    url "https://github.com/Universal-Debloater-Alliance/universal-android-debloater-next-generation/releases/download/v1.2.0/uad-ng-noselfupdate-macos-intel"
    sha256 "f2bc122975a8a1474ed41e058e4063019d07b637e85d97219a5d48b15a818a73"
  else
    url "https://github.com/Universal-Debloater-Alliance/universal-android-debloater-next-generation/releases/download/v1.2.0/uad-ng-noselfupdate-macos"
    sha256 "9e6d227ddbead08cca5ec3e875784c7100896f7e7be1ed177631d771173b6deb"
  end

  def install
    bin_name = Hardware::CPU.intel? ? "uad-ng-noselfupdate-macos-intel" : "uad-ng-noselfupdate-macos"
    bin.install bin_name => "uad-ng"
  end

  test do
    assert_match "uad-ng", shell_output("file #{bin/"uad-ng"}")
  end
end
