from glob import glob
import os
from pkg_resources import resource_filename
import shutil
import sys
import unittest

from astropy.io import fits
import numpy as np

from gitfit import gitfit


class TestGitfit(unittest.TestCase):
    """Tests for gitfit.py"""
    def setUp(self):

        # Set minimum file size in MB
        self.MB_limit = 80

        # Make dummy large FITS file (960MB)
        self.file = resource_filename('gitfit', 'temp/big_fits_file.fits')
        gitfit.make_dummy_file(self.file)

        # Make small file
        self.smallfile = resource_filename('gitfit', 'temp/small_fits_file.fits')
        gitfit.make_dummy_file(self.smallfile, shape=(1, 10, 10))

    def test_disassemble(self):
        """Test that a large FITS file can be disassembled"""
        # Disassemble FITS file
        file_list = gitfit.disassemble(self.file, MB_limit=self.MB_limit)
        data_dir = os.path.basename(self.file).replace('.fits', '_data')
        temp_files = glob(resource_filename('gitfit', 'temp/{}/*'.format(data_dir)))

        # Test files were created
        for file in file_list:
            self.assertTrue(file in temp_files)

        # Test files are all below 80MB
        for file in temp_files:
            file_MB = os.path.getsize(file)/1000000
            self.assertTrue(file_MB < self.MB_limit)

    def test_disassemble_small(self):
        """Test that a small FITS file is not disassembled"""
        # Disassemble FITS file
        file_list = gitfit.disassemble(self.smallfile, MB_limit=self.MB_limit)
        data_dir = os.path.basename(self.smallfile).replace('.fits', '_data')

        # Make sure no dir was created
        no_data = resource_filename('gitfit', 'temp/{}'.format(data_dir))
        self.assertFalse(os.path.exists(no_data))

        # Check list of files is empty
        self.assertIsNone(file_list)

    def test_reassemble(self):
        """Test that a large FITS file can be reassembled"""
        # Reassemble HDUList
        hdulist = gitfit.reassemble(self.file)

        # Check number of extensions
        self.assertEqual(len(hdulist), 3)

        # Check data shapes
        self.assertEqual(hdulist[0].data.shape, self.data_shape)
        self.assertEqual(hdulist[1].data.shape, self.data_shape)

        # Reassemble HDUList and delete data
        hdulist = gitfit.reassemble(self.file, save=True)

        # Check number of extensions
        self.assertEqual(len(hdulist), 3)

        # Check data was removed
        self.assertFalse(os.path.exists(self.file.replace('.fits', '_data')))

    def test_reassemble_small(self):
        """Test that a small FITS file is not reassembled"""
        # Reassemble HDUList
        hdulist = gitfit.reassemble(self.smallfile)

        # Check number of extensions
        self.assertEqual(len(hdulist), 3)

        # Check data shapes
        self.assertEqual(hdulist[0].data.shape, self.data_shape)
        self.assertEqual(hdulist[1].data.shape, self.data_shape)

    def test_make_dummy_file(self):
        """Test the make_dummy_file function"""
        # Dummy file path
        path = resource_filename('gitfit', 'temp/dummy_file.fits')

        # Make the dummy file
        gitfit.make_dummy_file(path)

        # Check file was created
        os.path.isfile(path)

    def tearDown(self):
        """Remove test files"""
        # Temp dir
        temp = resource_filename('gitfit', 'temp')
        shutil.rmtree(temp)
        os.mkdir(temp)