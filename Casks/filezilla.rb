cask "filezilla" do
  arch arm: "macos-arm64", intel: "macos-x86"

  version "3.71.0"
  sha256 arm:   "3dc5ced57173353ebd92b98b345324327d99827388aa0e2646108bf584779211",
         intel: "47d1e6c5902f45065744db0922d1968bcf7f197a68eb1fbd387cb1d2601b256c"

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
