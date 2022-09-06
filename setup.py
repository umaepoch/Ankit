# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in ankit/__init__.py
from ankit import __version__ as version

setup(
	name='ankit',
	version=version,
	description='For profit and loss report',
	author='jyoti',
	author_email='jyoti@meritsystems.com',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
