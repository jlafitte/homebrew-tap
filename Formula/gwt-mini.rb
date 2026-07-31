class GwtMini < Formula
  desc "Minimal CLI-only version of GeminiWatermarkTool"
  homepage "https://github.com/allenk/GeminiWatermarkTool"
  url "https://github.com/allenk/GeminiWatermarkTool/releases/download/v0.3.2/gwt-mini-macos-universal.zip"
  sha256 "da56b0537b54f9921498da6cfad48d92aa9795bd09ebbb2e0ac24edcbbd1db0f"
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
