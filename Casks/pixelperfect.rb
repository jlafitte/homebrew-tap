cask "pixelperfect" do
  version "1.5"
  sha256 "94c2fbb35850b3703e1677959421c761b4ad9860a8d17f383c07900fbd89c99a"

  url "https://github.com/cormiertyshawn895/PixelPerfect/releases/download/#{version}/PixelPerfect.#{version}.zip"
  name "Pixel Perfect"
  desc "Increase the text size of iPhone and iPad apps on Mac"
  homepage "https://github.com/cormiertyshawn895/PixelPerfect"

  livecheck do
    url :url
    strategy :github_latest
  end

  app "Pixel Perfect.app"

  zap trash: [
    "~/Library/Application Support/PixelPerfect",
    "~/Library/Preferences/com.cormiertyshawn895.PixelPerfect.plist",
  ]
end
