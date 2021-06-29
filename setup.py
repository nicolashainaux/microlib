# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from microlib import __version__, read_text

readme = read_text('README')

setup(
    long_description=readme,
    name='microlib',
    version=__version__,
    python_requires='==3.*,>=3.6.0',
    author='Nicolas Hainaux',
    author_email='nh.techn@gmail.com',
    packages=['microlib'],
    package_dir={"": "."},
    package_data={"microlib": ["data/*.json", "data/*.toml", "meta/*.toml"]},
    install_requires=[
        'blessed==1.*,>=1.18.1', 'click==8.*,>=8.0.1',
        'importlib-metadata==3.*,>=3.1.0; '
        'python_version == "3.6.*" or python_version == "3.7.*"',
        'toml==0.*,>=0.10.2'
    ],
    extras_require={
        "dev": [
            "coverage==5.*,>=5.3.0", "coveralls==2.*,>=2.2.0",
            "flake8==3.*,>=3.8.4", "pyfakefs==4.*,>=4.5.0",
            "pytest==5.*,>=5.2.0", "pytest-mock==3.*,>=3.3.1"
        ]
    },
)
