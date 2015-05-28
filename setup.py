#!/usr/bin/env python
#from distribute_setup import use_setuptools
#use_setuptools()
from setuptools import setup

import re
import platform
import os
import sys


if 'test' in sys.argv:
    # Setup test unloads modules after the tests have completed. This causes an
    # error in atexit's exit calls because the registered modules no longer
    # exist.  This hack resolves this issue by disabling the register func
    import atexit
    atexit.register = lambda be_gone_nasty_traceback: True


def load_version(filename='fuzzyhashlib/version.py'):
    """Parse a __version__ number from a source file"""
    with open(filename) as source:
        text = source.read()
        match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", text)
        if not match:
            msg = "Unable to find version number in {}".format(filename)
            raise RuntimeError(msg)
        version = match.group(1)
        return version


#see if we have a pre-built libfuzzyhashlib for this platform
arch, exetype = platform.architecture()
system = platform.system().lower()
machine = platform.machine().lower()

if machine in ['i686', 'x86']:
    machine = 'x86_32'

if machine in ['amd64']:
    machine = 'x86_64'

if system == 'windows':
    ext = '.dll'
else:
    ext = '.so'

data_files = []
for l in ["libssdeep"]:
    fuzzyhashlib_path = os.path.join('.', 'libs', system, machine, l + ext)

    if os.path.exists(fuzzyhashlib_path):
        if system == 'windows':
            install_libdir = os.path.join(sys.prefix, 'DLLs')
        else:
            install_libdir = os.path.join(sys.prefix, 'lib')
        data_files.append((install_libdir, [fuzzyhashlib_path]))

setup(
    name="fuzzyhashlib",
    version=load_version(),
    packages=['fuzzyhashlib'],
    data_files=data_files,
    zip_safe=False,
    author="Stephen Tonkin",
    author_email="sptonkin@outlook.com",
    #TODO - get a URI for this project.
    url="TODO - URI to project page.",
    description="One-stop, ctypes-based library for all your fuzzy hash needs",
    long_description=open('README.rst').read(),
    license="Apache Software Licence",
    install_requires = [],
    #TODO - does this need a CLI?
    #entry_points={
    #    'console_scripts': [
    #        'fuzzyhashlib-ctypes = fuzzyhashlib.cli:entry'
    #        ]
    #},
    #TODO - initial version will only support linux. others aspirational?
    platforms=['linux'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: Apache Software License',
        #'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Security',
        'Topic :: System :: Monitoring'
    ],
    test_suite="tests"
)

if not data_files:
    print("\nWARNING: Could not find %s" % libfuzzyhashlib_path)
    print("fuzzyhashlib may be unsupported on your system.")
    print("See http://pythonhosted.org/fuzzyhashlib/ for help")