class GwtMini < Formula
  desc "Minimal CLI-only version of GeminiWatermarkTool"
  homepage "https://github.com/allenk/GeminiWatermarkTool"
  url "https://github.com/allenk/GeminiWatermarkTool/releases/download/v0.3.0/gwt-mini-macos-universal.zip"
  sha256 "2d2ba3bd15b1a91c8871962bc8ab4b9725a4fcbbe0bb1a0a168a6154393203a7"
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
