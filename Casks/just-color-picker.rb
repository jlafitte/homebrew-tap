cask "just-color-picker" do
  version "6.3"
  sha256 "6693aa0efbce21885afc7f56429239d54ff27c64e1149f2d28a5852b80f46550"

  url "https://annystudio.com/software/colorpicker/jcpicker.dmg"
  name "Just Color Picker"
  desc "Offline color picker and color editing tool"
  homepage "https://annystudio.com/software/colorpicker/"

  livecheck do
    url :homepage
    regex(/Download\s+free\s+Just\s+Color\s+Picker\s+v?(\d+(?:\.\d+)+)/i)
  end

  app "Just Color Picker.app"

  zap trash: [
    "~/.config/Just Color Picker.cfg*",
    "~/Library/Preferences/com.annystudio.colorpicker.plist",
    "~/Library/Saved Application State/com.annystudio.colorpicker.savedState",
  ]
end
