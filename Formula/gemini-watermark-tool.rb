class GeminiWatermarkTool < Formula
  desc "Tool to remove watermarks using reverse alpha blending"
  homepage "https://github.com/allenk/GeminiWatermarkTool"
  url "https://github.com/allenk/GeminiWatermarkTool/releases/download/v0.3.1/GeminiWatermarkTool-macOS-Universal.zip"
  sha256 "5d425d49d74c74449a9d5fe267b2587ae036c7931b66c5a9c13db568a72f45d8"
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
