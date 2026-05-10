class GwtMini < Formula
  desc "Minimal CLI-only version of GeminiWatermarkTool"
  homepage "https://github.com/allenk/GeminiWatermarkTool"
  url "https://github.com/allenk/GeminiWatermarkTool/releases/download/v0.2.9/gwt-mini-macos-universal.zip"
  sha256 "d7a4020ec81daa731295b3cb37245157bb032756c7d5fc5f3623458ab4122057"
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
