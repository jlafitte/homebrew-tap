cask "just-color-picker" do
  version "6.2"
  sha256 "93c5b4f3caf6ce2a9171cb11f1045954f2771ad77a5a3537d13af80b28229264"

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
