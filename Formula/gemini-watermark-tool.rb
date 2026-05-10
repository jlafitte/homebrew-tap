class GeminiWatermarkTool < Formula
  desc "Tool to remove watermarks using reverse alpha blending"
  homepage "https://github.com/allenk/GeminiWatermarkTool"
  url "https://github.com/allenk/GeminiWatermarkTool/releases/download/v0.2.9/GeminiWatermarkTool-macOS-Universal.zip"
  sha256 "2cbc76649d86177eed65aa12225d0ac2f51a452db49db2dff1bb20d13402bab1"
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
