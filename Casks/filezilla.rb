cask "filezilla" do
  arch arm: "macos-arm64", intel: "macosx-x86"

  version "3.70.4"
  sha256 arm:   "ARM_SHA256_PLACEHOLDER",
         intel: "INTEL_SHA256_PLACEHOLDER"

  url "https://downloads.sourceforge.net/project/filezilla/FileZilla_Client/#{version}/FileZilla_#{version}_#{arch}.app.tar.bz2"
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
