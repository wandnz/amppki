# This file is part of amppki.
#
# Copyright (C) 2015-2019 The University of Waikato, Hamilton, New Zealand.
#
# Authors: Brendon Jones
#
# All rights reserved.
#
# This code has been developed by the WAND Network Research Group at the
# University of Waikato. For further information please see
# http://www.wand.net.nz/
#
# amppki is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.
#
# amppki is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with amppki; if not, write to the Free Software Foundation, Inc.
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
# Please report any bugs, questions or comments to contact@wand.net.nz
#

import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
#README = open(os.path.join(here, 'README.txt')).read()
#CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'pyOpenSSL>=0.13',
    'pyasn1>=0.1.7',
    'pyasn1_modules>=0.0.3',
    'pycryptodomex>=3.4.7',
    'pyramid>=1.5.1',
    'waitress>=0.8.9',
    'zope.interface>=4.1.1',
    ]

setup(name='amppki',
      version='0.11',
      description='amp-pki',
      #long_description=README + '\n\n' +  CHANGES,
      long_description="AMP PKI web interface",
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='Brendon Jones',
      author_email='brendonj@waikato.ac.nz',
      url='http://amp.wand.net.nz',
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      #test_suite='amppki',
      install_requires=requires,
      scripts=["amppki/scripts/ampca"],
      entry_points="""\
      [paste.app_factory]
      main = amppki:main
      """,
      )
