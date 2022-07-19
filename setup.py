# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
from pathlib import Path
from shutil import copyfile

import toml

pp_path = Path(__file__).parent / 'pyproject.toml'
meta_path = Path(__file__).parent / 'microlib/meta'
copyfile(pp_path, meta_path / 'pyproject.toml')
print('[setup.py] Copied pyproject.toml to microlib/meta/')
with open(pp_path, 'r') as f:
    pp = toml.load(f)

metadata = pp['tool']['poetry']
dep = metadata['dev-dependencies']
excluded = ['*tests', '*.pytest_cache', '*.venv', '*.vscode',
            '*microlib.build', '*microlib.egg-info', '*dist']

setup(
    long_description=Path('README.rst').read_text(),
    name='microlib',
    version=metadata['version'],
    python_requires='==3.*,>=3.7.0',
    author='Nicolas Hainaux',
    author_email='nh.techn@posteo.net',
    packages=['microlib'],
    package_dir={"": "."},
    package_data={"microlib": ["data/*.json", "data/*.toml", "meta/*.toml"]},
    classifiers=metadata['classifiers'],
    install_requires=[
        'blessed==1.*,>=1.18.1', 'click==8.*,>=8.0.1',
        'importlib-metadata==3.*,>=3.1.0; '
        'python_version == "3.7.*" or python_version == "3.8.*"'
        ' or python_version == "3.9.*" or python_version == "3.10.*"',
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
