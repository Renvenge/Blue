#!/usr/bin/env python3
"""Prepara um disco VirtualBox vazio, identificado pelo número de série."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import tempfile


def run(*command, **options):
    return subprocess.run(command, check=True, text=True, **options)


def check_disk(disk, serial):
    if disk.get('serial') != serial or not serial.startswith('VB'):
        raise ValueError('O número de série não corresponde ao disco criado para o Blue.')
    if disk.get('type') != 'disk' or disk.get('model', '').strip() != 'VBOX HARDDISK':
        raise ValueError('Este preparador aceita apenas discos virtuais do VirtualBox.')
    if disk.get('children') or disk.get('fstype') or any(disk.get('mountpoints') or []):
        raise ValueError('O disco contém partições, um sistema de arquivos ou está montado.')
    if int(disk['size']) < 4 * 1024**3:
        raise ValueError('O disco precisa ter pelo menos 4 GB.')


def check_empty_sectors(device, size):
    with device.open('rb', buffering=0) as source:
        beginning = source.read(1024 * 1024)
        source.seek(size - 1024 * 1024)
        ending = source.read(1024 * 1024)
    if any(beginning) or any(ending):
        raise ValueError('Há dados no disco. A preparação foi cancelada.')


def prepare(device, serial):
    device = device.resolve(strict=True)
    info = run('lsblk', '--json', '--bytes', '--output',
               'PATH,TYPE,SIZE,MODEL,SERIAL,FSTYPE,MOUNTPOINTS', str(device), capture_output=True)
    disk = json.loads(info.stdout)['blockdevices'][0]
    check_disk(disk, serial)
    check_empty_sectors(device, int(disk['size']))
    run('sfdisk', str(device), input='label: gpt\nstart=2048, type=linux\n')
    run('udevadm', 'settle')
    partition = Path(str(device) + '1')
    run('mkfs.ext4', '-m', '1', '-L', 'blue-data', str(partition))
    with tempfile.TemporaryDirectory(prefix='blue-data-') as folder:
        run('mount', str(partition), folder)
        try:
            Path(folder, 'persistence.conf').write_text('/ union\n')
        finally:
            run('umount', folder)
    print('Disco Blue pronto para preservar arquivos e programas.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('device', type=Path)
    parser.add_argument('--serial', required=True)
    args = parser.parse_args()
    if os.geteuid() != 0:
        parser.error('Execute este preparador como administrador no Linux.')
    try:
        prepare(args.device, args.serial)
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        parser.exit(1, f'Não foi possível preparar o disco: {error}\n')


if __name__ == '__main__':
    main()
