class RomConverto < Formula
  desc "Suite for converting, compressing, and decrypting ROMs"
  homepage "https://github.com/DevYukine/rom-converto"
  license "MIT"

  livecheck do
    url :stable
    strategy :github_latest
  end

  on_macos do
    on_arm do
      url "https://github.com/DevYukine/rom-converto/releases/download/v0.24.0/rom-converto-cli-macos-arm64"
      sha256 "4de8bbc96ddef23d8ed823ce42efcd64425c7885c4fe25058a2376ab42053aee"
    end
    on_intel do
      url "https://github.com/DevYukine/rom-converto/releases/download/v0.24.0/rom-converto-cli-macos-x64"
      sha256 "8bf11dd14c920db3ed9d00782a0ab018cc3d1e316b63d0deb2ff7b50d19e85f9"
    end
  end

  on_linux do
    on_arm do
      url "https://github.com/DevYukine/rom-converto/releases/download/v0.24.0/rom-converto-cli-linux-arm64"
      sha256 "990286bc3367342b0e04ab6dd0d28d8e95c3133ac2b4c5d6440a119e541b0b43"
    end
    on_intel do
      url "https://github.com/DevYukine/rom-converto/releases/download/v0.24.0/rom-converto-cli-linux-x64"
      sha256 "0d4abd56cfec477ff447f68b656d45ca48f670f464363bca2d895b1eee2c356d"
    end
  end

  def install
    binary_name = if OS.mac?
      Hardware::CPU.arm? ? "rom-converto-cli-macos-arm64" : "rom-converto-cli-macos-x64"
    else
      Hardware::CPU.arm? ? "rom-converto-cli-linux-arm64" : "rom-converto-cli-linux-x64"
    end

    bin.install binary_name => "rom-converto"
    chmod 0755, bin/"rom-converto"
    generate_completions_from_executable(bin/"rom-converto", "shell-completions")
  end

  test do
    assert_match version.to_s, shell_output("#{bin}/rom-converto --version")
  end
end
