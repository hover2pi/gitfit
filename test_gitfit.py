from glob import glob
import os
from pkg_resources import resource_filename
import sys
import unittest

from astropy.io import fits
import numpy as np

import gitfit


class TestGitfit(unittest.TestCase):
    """Tests for gitfit.py"""
    def setUp(self):

        # Set minimum file size in MB
        self.MB_limit = 80

        # Make dummy large FITS file (960MB)
        self.file = resource_filename('gitfit', 'temp/big_fits_file.fits')
        gitfit.make_dummy_file(self.file)

    def test_disassemble(self):
        """Test that a large FITS file can be disassembled"""
        # Disassemble FITS file
        file_list = gitfit.disassemble(self.file, MB_limit=self.MB_limit)
        temp_files = glob(resource_filename('gitfit', 'temp/*'))

        # Test files were created
        for file in file_list:
            self.assertTrue(file in temp_files)

        # Test files are all below 80MB
        for file in temp_files:
            file_MB = os.path.getsize(file)/1000000
            self.assertTrue(file_MB < self.MB_limit)

    def test_reassemble(self):
        """Test that a large FITS file can be reassembled"""
        # Reassemble HDUList
        hdulist = gitfit.reassemble(self.file)

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
        os.path.exists(path)

    def tearDown(self):
        """Remove test files"""
        for file in glob(resource_filename('gitfit', 'temp/*')):
            os.remove(file)