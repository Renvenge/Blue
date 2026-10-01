#!/bin/bash
set -euo pipefail
if [ "$(id -u)" -ne 0 ]; then echo "Execute com sudo: sudo bash build-blue.sh" >&2; exit 1; fi
if [ "$(uname -m)" != x86_64 ]; then echo "Use Linux x86_64 para gerar esta edição." >&2; exit 1; fi
for tool in lb debootstrap xorriso python3 unsquashfs; do
 command -v "$tool" >/dev/null 2>&1 || { echo "Falta $tool. Instale as dependências indicadas no LEIA-ME.md." >&2; exit 1; }
done
PROJECT=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
if [ ! -f "$PROJECT/config/includes.chroot/usr/lib/blue-vbox/VBoxClient" ]; then
 echo "Prepare a integração com scripts/prepare-vbox-tools.sh antes de compilar." >&2
 exit 1
fi
mkdir -p "$PROJECT/build"
WORK=$(mktemp -d "$PROJECT/build/iso-XXXXXXXX")
cp -R "$PROJECT/config" "$WORK/config"
chmod 0755 "$WORK/config/includes.chroot/usr/lib/blue-vbox/VBoxClient" "$WORK/config/includes.chroot/usr/lib/blue-vbox/VBoxService"
mkdir -p "$WORK/config/includes.chroot/usr/lib/blue-assistant"
cp "$PROJECT/assistant/blue_assistant.py" "$WORK/config/includes.chroot/usr/lib/blue-assistant/blue_assistant.py"
cp "$PROJECT/LICENSE" "$WORK/config/includes.chroot/usr/lib/blue-assistant/LICENSE"
cd "$WORK"
lb config --mode debian --distribution trixie --architectures amd64 \
 --binary-images iso-hybrid --archive-areas "main" \
 --apt-recommends false --debian-installer none --mksquashfs-options "-comp zstd -Xcompression-level 10" \
 --bootloaders "syslinux grub-efi" --firmware-chroot false --firmware-binary false \
 --iso-application "Blue Linux" --iso-volume "BLUE_LIVE" \
 --bootappend-live "boot=live components persistence persistence-label=blue-data username=blue hostname=blue locales=pt_BR.UTF-8 keyboard-layouts=br timezone=America/Fortaleza"
chmod +x config/hooks/live/*.hook.chroot
lb build 2>&1 | tee build.log
# Confirma que uma imagem foi produzida e ajusta o boot ao snapshot compactado.
test -s live-image-amd64.hybrid.iso || { echo "A ISO não foi gerada. Consulte $WORK/build.log" >&2; exit 1; }
python3 "$PROJECT/finalize-image.py" "$WORK"
cp live-image-amd64.hybrid.iso "$PROJECT/Blue-0.3-amd64.iso"
cp Blue-0.3-amd64.packages "$PROJECT/Blue-0.3-amd64.packages"
cd "$PROJECT"
sha256sum Blue-0.3-amd64.iso > Blue-0.3-amd64.iso.sha256
printf '\nImagem criada: %s/Blue-0.3-amd64.iso\n' "$PROJECT"
