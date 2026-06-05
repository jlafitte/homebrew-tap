cask "filezilla" do
  arch arm: "macos-arm64", intel: "macos-x86"

  version "3.70.6"
  sha256 arm:   "f2a2c13361e1037bab9729a4d738f6ce6b489f04fd82572ca1b0235b602bdfca",
         intel: "c0e6c85af1cc71a19a31b35205579fe51b499bd31b27afa3f6fb30cabf5e070a"

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
