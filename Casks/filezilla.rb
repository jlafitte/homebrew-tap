cask "filezilla" do
  arch arm: "macos-arm64", intel: "macos-x86"

  version "3.70.4"
  sha256 arm:   "13b1d55dbd2081aa6888aa7dc5cba5bb1bccb01f5edc934f36905a7ac00b7167",
         intel: "6dfa6641ad338f339400441482b3696b3d647a50b634aad6488ba81df51b3ccf"

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
