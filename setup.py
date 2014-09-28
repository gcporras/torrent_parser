#!/usr/bin/env python
# -*- coding: utf-8 -*-
import codecs
from setuptools.command.test import test as TestCommand
import sys


class Tox(TestCommand):

    user_options = [('tox-args=', 'a', "Arguments to pass to tox")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.tox_args = None

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import tox
        import shlex
        args_value = []
        if self.tox_args:
            args_value = shlex.split(self.tox_args)
        errno = tox.cmdline(args=args_value)
        sys.exit(errno)


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


readme = codecs.open('README.md').read()
history = codecs.open('HISTORY.md').read().replace('.. :changelog:', '')

requirements = [
]

test_requirements = [
    'tox==1.7.2'
]

setup(
    name='torrent_parser',
    version='0.1.0',
    description='A library to parse BitTorrent files.',
    long_description=readme + '\n\n' + history,
    author='Gerardo Cepeda Porras',
    author_email='gerardo.cepeda@gmail.com',
    url='https://github.com/gcporras/torrent_parser',
    packages=[
        'torrent_parser',
    ],
    package_dir={'torrent_parser':
                 'torrent_parser'},
    include_package_data=True,
    install_requires=requirements,
    license="MIT",
    zip_safe=False,
    keywords='torrent_parser',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Operating System :: OS Independent",
        'Programming Language :: Python :: 2.7',
    ],
    test_suite='torrent_parser.tests',
    tests_require=test_requirements,
    extras_require={
        'testing': test_requirements,
    },
    cmdclass={'test': Tox},
)
