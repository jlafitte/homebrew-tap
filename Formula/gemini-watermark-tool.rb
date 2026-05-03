class GeminiWatermarkTool < Formula
  desc "Tool to remove watermarks using reverse alpha blending"
  homepage "https://github.com/allenk/GeminiWatermarkTool"
  url "https://github.com/allenk/GeminiWatermarkTool/releases/download/v0.2.8/GeminiWatermarkTool-macOS-Universal.zip"
  sha256 "dc693e64680886361cf5a20ccef2947d1d04004df815cd21944f38813b819e3a"
  license "MIT"

  livecheck do
    url "https://github.com/allenk/GeminiWatermarkTool/releases"
    strategy :github_latest
  end

  def install
    bin.install "GeminiWatermarkTool"
  end

  test do
    system "#{bin}/GeminiWatermarkTool", "--version"
  end
end
