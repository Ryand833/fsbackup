#/usr/bin/env python

from distutils.core import setup

setup(name='fsbackup',
	version='0.2.2',
	py_modules=['fsutils'],
	scripts=['scripts/fsbackup', 'scripts/fsrestore'],
	author='Ryan Dorn',
	author_email='ryan.dorn@gmail.com',
	url='http://www.rdorn.us',
	)

