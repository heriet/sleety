from setuptools import find_packages, setup

from sleety import __version__

requires = [
    'future',
    'lxml',
    'requests',
    'xmlschema',
    ]

setup(
    name='sleety',
    version=__version__,
    description='SDK for NiftyCloud',
    author='heriet',
    author_email='heriet@heriet.info',
    url='https://github.com/heriet/sleety',
    packages=find_packages(exclude=["example", "test"]),
    include_package_data=True,
    package_date={
        '': [
            'sleety/computing/schema/*.xsd'
        ]
    },
    install_requires=requires,
    license='MIT',
    )
