cask "stremio-native" do
  version "2.1.2,27-213-1-9ec534dc9673"
  sha256 "dcb641b5dc63d7b0c282844c0087d0566cfb6864b623c3a06dfb295a06f7ad02"

  url "https://dl.strem.io/apple/macos/release/Stremio-#{version.csv.first}-#{version.csv.second}.zip"
  name "Stremio Native"
  desc "Open-source media center (native macOS client)"
  homepage "https://www.stremio.com/"

  livecheck do
    url "https://dl.strem.io/apple/macos/source.xml"
    strategy :sparkle do |item|
      match = item.url.match(/Stremio[._-]v?(\d+(?:\.\d+)+)[._-](\d+.*?)\.zip/i)
      next if match.blank?

      "#{match[1]},#{match[2]}"
    end
  end

  auto_updates true
  conflicts_with cask: "stremio"
  depends_on macos: :monterey

  app "Stremio.app"

  zap trash: [
    "~/Library/Application Support/com.stremio.pal",
    "~/Library/Application Support/stremio-server",
    "~/Library/Caches/com.stremio.pal",
    "~/Library/HTTPStorages/com.stremio.pal",
    "~/Library/Preferences/com.stremio.pal.plist",
    "~/Library/Saved Application State/com.stremio.pal.savedState",
    "~/Library/WebKit/com.stremio.pal",
  ]
end
