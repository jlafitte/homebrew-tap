class GwtMini < Formula
  desc "Minimal CLI-only version of GeminiWatermarkTool"
  homepage "https://github.com/allenk/GeminiWatermarkTool"
  url "https://github.com/allenk/GeminiWatermarkTool/releases/download/v0.3.1/gwt-mini-macos-universal.zip"
  sha256 "a55f458250adfa74559366eaa4b9e52ec6e6eb4df72a5f9d8dc392994721e911"
  license "MIT"

  livecheck do
    url "https://github.com/allenk/GeminiWatermarkTool/releases"
    strategy :github_latest
  end

  def install
    # The binary inside the zip is named 'gwt-mini'
    bin.install "gwt-mini"
  end

  test do
    system "#{bin}/gwt-mini", "--version"
  end
end
