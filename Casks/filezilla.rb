cask "filezilla" do
  arch arm: "macos-arm64", intel: "cce3d24c6affcecb01799c249f1da5646004dec5c2417f27449b483103b33c24"

  version "3.70.5"
  sha256 arm:   "9aefcc4343c90e62a0afb9f0abb715a21fa3afc11ab0b8980afc395872908525",
         intel: "cce3d24c6affcecb01799c249f1da5646004dec5c2417f27449b483103b33c24"

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
