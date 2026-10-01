#!/usr/bin/env python3
"""Mantém o boot coerente com o snapshot compactado, mesmo após updates do mirror."""
import hashlib
from pathlib import Path
import re
import shutil
import shlex
import os
import subprocess
import sys
import tempfile

work = Path(sys.argv[1]).resolve()
binary = work / 'binary'
live = binary / 'live'
image = live / 'filesystem.squashfs'
iso = work / 'live-image-amd64.hybrid.iso'
# live-build pode deixar o auxiliar do dpkg ausente após desfazer o desvio
# temporário usado durante o chroot. Recuperamos o arquivo do mesmo pacote.
checksums = subprocess.check_output(['unsquashfs', '-cat', str(image),
                                     'var/lib/dpkg/info/dpkg.md5sums'], text=True)
expected = re.search(r'^([0-9a-f]{32})\s+usr/sbin/start-stop-daemon$', checksums, re.M)
if not expected:
    raise RuntimeError('Checksum do auxiliar dpkg ausente no pacote instalado.')
original = subprocess.run(['unsquashfs', '-cat', str(image), 'usr/sbin/start-stop-daemon'],
                          stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
fix_root = live / 'zz-blue-fixes.dir'
# Recria a camada para que painéis removidos da fonte não sobrevivam a updates.
if fix_root.is_dir():
    shutil.rmtree(fix_root)
if original.returncode or hashlib.md5(original.stdout).hexdigest() != expected[1]:
    candidates = [work / 'chroot/usr/sbin/start-stop-daemon', Path('/usr/sbin/start-stop-daemon')]
    chosen = next((path for path in candidates if path.is_file()
                   and hashlib.md5(path.read_bytes()).hexdigest() == expected[1]), None)
    if chosen is None:
        raise RuntimeError('Auxiliar dpkg original não encontrado; use Debian com a mesma versão de dpkg da imagem.')
    target = fix_root / 'usr/sbin/start-stop-daemon'
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(chosen, target)
    target.chmod(0o755)
    print('Auxiliar dpkg original recuperado.', flush=True)
issue = fix_root / 'etc/issue'
issue.parent.mkdir(parents=True, exist_ok=True)
issue.write_text('Blue 0.3 - Linux para programacao\n', encoding='ascii')
# Aplica os arquivos do projeto à imagem, preservando os pacotes Debian.
project = Path(__file__).resolve().parent
includes = project / 'config/includes.chroot'
if includes.is_dir():
    shutil.copytree(includes, fix_root, dirs_exist_ok=True)
service = fix_root / 'etc/systemd/system/multi-user.target.wants/blue-vbox.service'
service.parent.mkdir(parents=True, exist_ok=True)
service.symlink_to('../blue-vbox.service')
assistant = project / 'assistant/blue_assistant.py'
if assistant.exists():
    target = fix_root / 'usr/lib/blue-assistant/blue_assistant.py'
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(assistant, target)
for path in (fix_root / 'usr/local/bin').glob('*'):
    if path.is_file():
        path.chmod(0o755)
# Uma única imagem evita diferenças na ordem das camadas com persistência.
with tempfile.TemporaryDirectory(prefix='blue-root-', dir=work) as folder:
    root = Path(folder) / 'root'
    subprocess.run(['unsquashfs', '-no-progress', '-d', str(root), str(image)], check=True)
    # copytree não substitui links que já existem em uma imagem atualizada.
    for source in fix_root.rglob('*'):
        if source.is_symlink():
            target = root / source.relative_to(fix_root)
            if target.is_symlink() or target.is_file():
                target.unlink()
    shutil.copytree(fix_root, root, dirs_exist_ok=True, symlinks=True)
    replacement = Path(folder) / 'filesystem.squashfs'
    subprocess.run(['mksquashfs', str(root), str(replacement), '-noappend', '-comp', 'zstd', '-Xcompression-level', '5',
                    '-processors', '2', '-no-progress'], check=True)
    replacement.replace(image)
shutil.rmtree(fix_root)
(live / 'zz-blue-fixes.squashfs').unlink(missing_ok=True)
(live / 'filesystem.module').write_text('filesystem.squashfs\n')
listing = subprocess.check_output(['unsquashfs', '-ls', str(image), 'boot'], text=True)
kernels = re.findall(r'^squashfs-root/boot/vmlinuz-([^\n/]+)$', listing, re.M)
if not kernels:
    raise RuntimeError('Não há kernel no sistema compactado.')
# Utiliza a mesma ordenação de versões GNU empregada pelas ferramentas Debian.
selected = subprocess.check_output(['sort', '-V'], input='\n'.join(kernels) + '\n', text=True).splitlines()[-1]
valid = set(kernels)
print('Kernel de referência:', selected, flush=True)
for stem in ('vmlinuz', 'initrd.img'):
    target = live / stem
    temp = live / ('.' + stem + '.blue')
    with temp.open('wb') as output:
        subprocess.run(['unsquashfs', '-cat', str(image), 'boot/' + stem + '-' + selected],
                       stdout=output, check=True)
    temp.replace(target)
    # Os arquivos com versão e os aliases devem conter os mesmos bytes.
    versioned = live / (stem + '-' + selected)
    versioned.write_bytes(target.read_bytes())

for path in live.glob('vmlinuz-*'):
    version = path.name.removeprefix('vmlinuz-')
    if version not in valid:
        path.unlink()
        (live / ('initrd.img-' + version)).unlink(missing_ok=True)

grub = binary / 'boot/grub/grub.cfg'
text = grub.read_text()
def keep_entry(match):
    versions = re.findall(r'/live/vmlinuz-([^\s]+)', match[0])
    return match[0] if all(version in valid for version in versions) else ''
text = re.sub(r'^menuentry[^\n]*\{\n.*?^\}\n', keep_entry, text, flags=re.M | re.S)
text = text.replace('Live system (amd64)', 'Blue — programação (amd64)')
text = re.sub(r'boot=live components(?: persistence persistence-label=blue-data)?',
              'boot=live components persistence persistence-label=blue-data', text)
grub.write_text(text, encoding='utf-8')
syslinux = binary / 'isolinux/live.cfg'
text = syslinux.read_text().replace('Live system (amd64)', 'Blue - programacao (amd64)')
text = re.sub(r'boot=live components(?: persistence persistence-label=blue-data)?',
              'boot=live components persistence persistence-label=blue-data', text)
syslinux.write_text(text, encoding='utf-8')
boot_art = Path(__file__).resolve().parent / 'assets/blue-boot.png'
if boot_art.exists():
    shutil.copyfile(boot_art, binary / 'isolinux/splash.png')
    shutil.copyfile(boot_art, binary / 'boot/grub/splash.png')

status = subprocess.check_output(['unsquashfs', '-cat', str(image), 'var/lib/dpkg/status']).decode()
packages = []
for stanza in status.split('\n\n'):
    values = dict(re.findall(r'^(Package|Version|Status): (.+)$', stanza, re.M))
    if values.get('Status') == 'install ok installed':
        packages.append(values['Package'] + ' ' + values['Version'])
manifest = '\n'.join(sorted(packages)) + '\n'
(live / 'filesystem.packages').write_text(manifest)
(work / 'Blue-0.3-amd64.packages').write_text(manifest)

lines = []
for path in sorted(binary.rglob('*')):
    if path.is_file() and path.name not in ('md5sum.txt', 'sha256sum.txt'):
        digest = hashlib.md5()
        with path.open('rb') as stream:
            while chunk := stream.read(1024 * 1024):
                digest.update(chunk)
        lines.append(digest.hexdigest() + '  ./' + path.relative_to(binary).as_posix())
(binary / 'md5sum.txt').write_text('\n'.join(lines) + '\n')

recipe = shlex.split((binary / '.disk/mkisofs').read_text())
if recipe[:3] != ['xorriso', '-as', 'mkisofs'] or recipe[-1] != 'binary':
    raise RuntimeError('Receita de criação de ISO não reconhecida.')
fd, path = tempfile.mkstemp(prefix='blue-finalized-', suffix='.iso', dir=work)
os.close(fd)
fixed = Path(path)
recipe[recipe.index('-o') + 1] = str(fixed)
recipe[-1] = str(binary)
subprocess.run(recipe, cwd=work, check=True)
fixed.replace(iso)
print('ISO finalizada com kernel consistente e manifest de pacotes do snapshot.', flush=True)
