class GeminiWatermarkTool < Formula
  desc "Tool to remove watermarks using reverse alpha blending"
  homepage "https://github.com/allenk/GeminiWatermarkTool"
  url "https://github.com/allenk/GeminiWatermarkTool/releases/download/v0.3.2/GeminiWatermarkTool-macOS-Universal.zip"
  sha256 "2c32078282b08587eef6c7a0c32dd4464dd234d0df3d9a03939b43388e5875e7"
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
