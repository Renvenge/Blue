#!/bin/bash
# Usa os clientes livres do VirtualBox e os drivers do kernel Debian.
set -euo pipefail
project=$(cd -- "$(dirname -- "$0")/.." && pwd)
image=${1:?Informe o caminho de VBoxGuestAdditions_7.0.8.iso}
checksum=8d73e2361afbf696e6128ffa5e96d9f6a78ff32cb2cb54c727a5be7992be0b31
actual=$(sha256sum "$image" | cut -d ' ' -f 1)
if [ "$actual" != "$checksum" ]; then
    echo 'A imagem não corresponde aos Guest Additions 7.0.8 oficiais.' >&2
    exit 1
fi
work=$(mktemp -d)
trap 'rm -rf -- "$work"' EXIT
mkdir "$work/iso" "$work/installer" "$work/files"
xorriso -osirrox on -indev "$image" -extract /VBoxLinuxAdditions.run "$work/iso/installer.run"
bash "$work/iso/installer.run" --noexec --target "$work/installer"
tar -xjf "$work/installer/VBoxGuestAdditions-amd64.tar.bz2" -C "$work/files"
destination="$project/config/includes.chroot/usr/lib/blue-vbox"
mkdir -p "$destination"
install -m 0755 "$work/files/bin/VBoxClient" "$destination/VBoxClient"
install -m 0755 "$work/files/sbin/VBoxService" "$destination/VBoxService"
install -m 0644 "$work/files/LICENSE" "$destination/LICENSE"
printf 'VirtualBox Guest Additions 7.0.8\nSource: https://download.virtualbox.org/virtualbox/7.0.8/VirtualBox-7.0.8.tar.bz2\n' > "$destination/SOURCE.txt"
