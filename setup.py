import sys
from setuptools import setup

py_version = sys.version_info


setup(
    name='CGlue',
    version='0.2.0',
    packages=['cglue', 'cglue/plugins', 'cglue/utils'],
    package_dir={'cglue': 'cglue'},
    url='https://github.com/RevolutionRobotics/CGlue',
    license='MIT',
    author='Dániel Buga',
    author_email='daniel@revoltuionrobotics.org',
    description='Framework for C software',
    entry_points={
        "console_scripts": [
            "cglue = cglue.cli:cli",
            f"cglue-{py_version.major}.{py_version.minor} = cglue.cli:cli",
        ]
    },
    test_suite='nose2.collector.collector'
)
