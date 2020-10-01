"""
Module to split up and reassemble large files so they can be
committed to Github repositories
"""
from glob import glob
import os
import sys

from astropy.io import fits
import numpy as np


def disassemble(file, MB_limit=80, destination=None):
    """
    Disassemble a FITS file into smaller chunks

    Parameters
    ----------
    file: str
        The path to the large file
    MB_limit: float, int
        The maximum file size affter disassembly
    destination: str (optional)
        The destination for the disassembled files

    Returns
    -------
    list
        The list of file paths
    """
    # Determine the file extension
    ext = file.split('.')[-1].lower()

    # List of files to return
    filelist = []

    # Check file size in MB
    filesize = os.stat(file).st_size/1000000

    # Get destination
    if destination is None:
        destination = os.path.dirname(file)

    # If already small enough, do nothing
    if filesize <= MB_limit:
        filelist.append(file)

    else:

        # Open the FITS file
        hdulist = fits.open(file, mode='update')

        # Strip file of data
        extensions = {}
        for hdu in hdulist:

            # Save the real data
            extensions[hdu.name] = hdu.data

            # Replace with tiny dummy array
            hdulist[hdu.name].data = None

        # Write to the file
        hdulist.flush()

        # Write the data to .npz files
        for ext, data in extensions.items():

            # Some are None
            if data is not None:

                # Check data size in MB
                datasize = sys.getsizeof(data)/1000000

                # Get number of chunks
                nchunks = np.ceil(datasize/MB_limit).astype(int)

                # Break up into chunks
                chunks = np.split(data, nchunks)

                # Save as .npz files
                for n, chunk in enumerate(chunks):

                    # Determine filename
                    filename = os.path.basename(file).replace('.fits', '.{}.{}.npy'.format(ext, n))

                    # Save the chunk to file
                    filepath = os.path.join(destination, filename)
                    np.save(filepath, chunk)

                    # Add to list of filenames
                    filelist.append(filepath)

        # Close the file
        hdulist.close()

        return filelist


def reassemble(file, save=False):
    """
    Reassemble a FITS file from its components

    Parameters
    ----------
    file: str
        The path to the FITS file
    save: bool
        Save the data to the file again

    Returns
    -------
    astropy.io.fits.HDUList
        The HDU list
    """
    # Open the FITS file
    hdulist = fits.open(file, mode='update')
    filename = os.path.basename(file)
    directory = os.path.dirname(file)

    # Populate file with data
    for hdu in hdulist:

        # Get the real data files
        filestr = filename.replace('.fits', '.{}.*'.format(hdu.name))
        files = glob(os.path.join(directory, filestr))

        # Load and recombine the data
        if len(files) > 0:
            data = np.concatenate([np.load(f) for f in files])
        else:
            data = None

        # Replace with real data
        hdulist[hdu.name].data = data

    # Write the file changes
    if save:
        hdulist.flush()

    # Close the file
    hdulist.close()

    return hdulist