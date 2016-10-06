import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
#README = open(os.path.join(here, 'README.txt')).read()
#CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'argparse>=1.2.1',
    'pyOpenSSL>=0.13',
    'pyasn1>=0.1.7',
    'pyasn1_modules>=0.0.3',
    'pycrypto>=2.6.1',
    'pyramid_chameleon>=0.3',
    'pyramid>=1.5.1',
    'pyramid_assetviews>=1.0a3',
    'waitress>=0.8.9',
    'zope.interface>=4.1.3',
    ]

setup(name='amppki',
      version='0.4',
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
