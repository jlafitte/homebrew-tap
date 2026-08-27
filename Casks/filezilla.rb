cask "filezilla" do
  arch arm: "macos-arm64", intel: "macos-x86"

  version "3.71.1"
  sha256 arm:   "73f081493dc528429d601cc0860900b9e9ded60b6a12fadee027d18939939238",
         intel: "cd68b730fbbd6e9617dc94f166ea75c8b9da098b520c5dff6c8f6935655e6683"

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
