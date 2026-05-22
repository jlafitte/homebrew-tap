class GeminiWatermarkTool < Formula
  desc "Tool to remove watermarks using reverse alpha blending"
  homepage "https://github.com/allenk/GeminiWatermarkTool"
  url "https://github.com/allenk/GeminiWatermarkTool/releases/download/v0.3.0/GeminiWatermarkTool-macOS-Universal.zip"
  sha256 "8740fe924aeef5bf63acbd665334914a4eac61dc5aaf9bff6fc68c9c3a4793f9"
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
