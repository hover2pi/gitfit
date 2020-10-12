#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', ]

setup(
    author="Joe Filippazzo",
    author_email='jfilippazzo@stsci.edu',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6'
    ],
    description="Make large FITS files fit on Github",
    install_requires=['numpy', 'astropy'],
    license="MIT license",
    # long_description=readme + '\n\n' + history,
    long_description="Make large FITS files fit on Github",
    include_package_data=True,
    keywords='gitfit',
    name='gitfit',
    packages=find_packages(include=['gitfit']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/hover2pi/gitfit',
    version='0.1.1',
    zip_safe=False,
)
