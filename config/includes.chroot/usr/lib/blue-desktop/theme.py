#!/usr/bin/env python3
"""Aplica o acabamento Blue preservando atalhos do gerenciador de janelas."""
from pathlib import Path
import subprocess
import xml.etree.ElementTree as ET

folder = Path.home() / '.config/openbox'
target = folder / 'rc.xml'
marker = Path.home() / '.config/blue-theme-initialized'
if not marker.exists():
    source = target if target.exists() else Path('/etc/xdg/openbox/rc.xml')
    tree = ET.parse(source)
    namespace = 'http://openbox.org/3.4/rc'
    ET.register_namespace('', namespace)
    name = tree.find(f'{{{namespace}}}theme/{{{namespace}}}name')
    if name is not None:
        name.text = 'Blue'
        folder.mkdir(parents=True, exist_ok=True)
        tree.write(target, encoding='utf-8', xml_declaration=True)
        marker.touch()
        subprocess.run(['openbox', '--reconfigure'], check=False)
