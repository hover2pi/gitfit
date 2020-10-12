# gitfit
[![Build Status](https://travis-ci.org/hover2pi/gitfit.svg?branch=master)](https://travis-ci.org/hover2pi/gitfit)
[![Coverage Status](https://coveralls.io/repos/github/hover2pi/gitfit/badge.svg?branch=master)](https://coveralls.io/github/hover2pi/gitfit?branch=master)

`gitfit` is a simple Python 3.6+ tool to split and concatenate large FITS files so they don't exceed Github limit of 100MB.

## Installation
To install, you can clone this repo and install manually with
```
git clone https://github.com/hover2pi/gitfit.git
python setup.py gitfit/install
```

or install via `pip` with

```
pip install gitfit
```

## Usage
`gitfit` pulls the data out of large FITS file extensions and saves them in small chunked `.npy` files in a `_data` directory.

To accomplish this, call the `disassemble` function like so:

```
from gitfit import gitfit
file_list = gitfit.disassemble('/path/to/large_fits_file.fits')
```

This will return a list of the files that were created. Then you will be able to commit and push to your Github repo.

To read or reassemble the original file, call the `reassemble` function like so:

```
hdu_list = gitfit.reassemble('/path/to/large_fits_file.fits', save=False)
```

This reads the reassembled FITS file `HDUList` into memory but does not save it to disk so that it can continue to be pushed to Github in the smaller format. If `save` is set to `True`, the original large FITS file will be restored and the `_data` directory will be deleted.
