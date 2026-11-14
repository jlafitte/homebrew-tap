cask "filezilla" do
  arch arm: "macos-arm64", intel: "macos-x86"

  version "3.72.0"
  sha256 arm:   "9a711a36c01860d5292884a78ad0981b5b68a2504bd3698f4c5e1af19a9dddcd",
         intel: "e4266c125ffe3f242dc1324e48ea2ed44cd4e5c07dad71d3155a2c5652f85ee4"

  url "https://download.filezilla-project.org/client/FileZilla_#{version}_#{arch}.app.tar.bz2",
      user_agent: "FileZilla/#{version}"
  name "FileZilla"
  desc "FTP, FTPS and SFTP client"
  homepage "https://filezilla-project.org/"

  app "FileZilla.app"

  zap trash: [
    "~/.config/filezilla",
    "~/Library/Application Support/com.apple.sharedfilelist/com.apple.LSSharedFileList.ApplicationRecentDocuments/de.filezilla.sfl*",
    "~/Library/Preferences/de.filezilla.plist",
    "~/Library/Saved Application State/de.filezilla.savedState",
  ]
end
