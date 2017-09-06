from setuptools import setup, find_packages

from sleety import __version__

requires = [
    'future==0.16.0',
    'lxml==3.8.0',
    'requests==2.18.4',
    'xmlschema==0.9.11',
    ]

setup(name='sleety',
      version=__version__,
      description='SDK for NiftyCloud',
      author='heriet',
      author_email='heriet@heriet.info',
      url='https://github.com/heriet/sleety',
      packages=find_packages(exclude=["example"]),
      package_date={
          '': [
              '*/schema/*.xsd'
          ]
      },
      install_requires=requires,
      license='MIT',
     )
