cask "filezilla" do
  arch arm: "macos-arm64", intel: "macos-x86"

  version "3.72.1"
  sha256 arm:   "d2830c8c5167faf3d5f94f9eadb558bc589c6015b2febcdc4514736561f6363e",
         intel: "6d41b25efe41755d8378f8973c24d46e1242fed03030190e2422864af610e803"

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
