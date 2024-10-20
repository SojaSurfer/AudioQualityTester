from setuptools import find_packages, setup

from source.audioQualityTester import __version__ as version


with open('Readme.md', 'r') as f:
    long_description = f.read()


setup(
    name="audioQualityTester",
    version=version,
    description="A standalone application for testing the differences of MP3 formats.",
    packages=find_packages(where="source"),
    package_dir={'': 'source'},
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Julian Wagner',
    author_email='julian.s.wagner@t-online.de',
    url='',
    license='GNU General Public License v3 (GPLv3)',
    install_requires=['bson >= 0.5.10',
                      'PySide6>=6.0,<=7.0',
                      'PySide6_Addons>=6.0,<=7.0',
                      'PySide6_Essentials>=6.0,<=7.0',
                      'pygame>=2.0,<=3.0',
                      'pydub>=0.20,<=1.0',
                      'librosa>=0.10,<=1.0',
                      'numpy>=1.0,<=2.0',
                      'scipy>=1.0,<=2.0',
                      'matplotlib>=3.0,<=4.0',
                      'tqdm>=4.0,<=5.0',
                      'matplotlib>=0.20,<=1.0',
                      ],
    extras_require={'dev': ['rich<=13.0,<=14.0']},
    python_requires='>=3.10',
    classifiers=['Programming Language :: Python :: 3',
                 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
                 'Operating System :: OS Independent',
                ],
)