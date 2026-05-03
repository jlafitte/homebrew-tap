class GwtMini < Formula
  desc "Minimal CLI-only version of GeminiWatermarkTool"
  homepage "https://github.com/allenk/GeminiWatermarkTool"
  url "https://github.com/allenk/GeminiWatermarkTool/releases/download/v0.2.8/gwt-mini-macos-universal.zip"
  sha256 "59b2145405a9a3814c716b97284dff133f7a62b1d86efc164c320cd00fc5c87a"
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
