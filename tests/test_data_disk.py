import importlib.util
from pathlib import Path
import tempfile
import unittest

script = Path(__file__).parents[1] / 'scripts/prepare-data-disk.py'
spec = importlib.util.spec_from_file_location('data_disk', script)
disk_setup = importlib.util.module_from_spec(spec)
spec.loader.exec_module(disk_setup)


class DiskPreparationTests(unittest.TestCase):
    def setUp(self):
        self.disk = {'serial': 'VB-new-disk', 'model': 'VBOX HARDDISK',
                     'type': 'disk', 'size': 32 * 1024**3,
                     'mountpoints': [None], 'fstype': None}

    def test_wrong_disk_is_rejected(self):
        with self.assertRaises(ValueError):
            disk_setup.check_disk(self.disk, 'VB-another-disk')

    def test_disk_with_partitions_is_rejected(self):
        self.disk['children'] = [{'path': '/dev/sdb1'}]
        with self.assertRaises(ValueError):
            disk_setup.check_disk(self.disk, 'VB-new-disk')

    def test_mounted_disk_is_rejected(self):
        self.disk['mountpoints'] = ['/']
        with self.assertRaises(ValueError):
            disk_setup.check_disk(self.disk, 'VB-new-disk')

    def test_existing_filesystem_is_rejected(self):
        self.disk['fstype'] = 'ext4'
        with self.assertRaises(ValueError):
            disk_setup.check_disk(self.disk, 'VB-new-disk')

    def test_old_partition_signature_is_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            image = Path(folder, 'disk.img')
            with image.open('wb') as target:
                target.truncate(4 * 1024**2)
                target.write(b'EFI PART')
            with self.assertRaises(ValueError):
                disk_setup.check_empty_sectors(image, image.stat().st_size)


if __name__ == '__main__':
    unittest.main()
