from setuptools import find_packages, setup

# not possible due to importing not installed modules
# from source.audioQualityTester import __version__ as version


with open('Readme.md', 'r') as f:
    long_description = f.read()


setup(
    name="audioQualityTester",
    version='0.2',
    description="A standalone application for testing the differences of MP3 formats.",
    packages=find_packages(),
    package_data= {'audioQualityTester': ['resources/*',
                                        'view/Generated/*',
                                        'view/Project/*',
                                        'view/Project/desinger/*',
                                        'view/ProjectContent/*',
                                        'view/ProjectContent/fonts/*',
                                        'view/Python/*',
                                        'view/Python/autogen/*'
                                        ]},
    include_package_data=True,
    # package_dir={'': 'audioQualityTester'},
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Julian Wagner',
    author_email='julian.s.wagner@t-online.de',
    url='https://github.com/SojaSurfer/AudioQualityTester.git',
    license='GNU General Public License v3 (GPLv3)',
    install_requires=['bson >= 0.5.10',
                      'PySide6>=6.0,<=7.0',
                      'PySide6_Addons>=6.0,<=7.0',
                      'PySide6_Essentials>=6.0,<=7.0',
                      'pygame>=2.0,<=3.0',
                      'pydub>=0.20,<=1.0',
                      'librosa>=0.10,<=1.0',
                      'mutagen>=1.0,<=2.0',
                      'numpy>=1.0,<=2.0',
                      'scipy>=1.0,<=2.0',
                      'matplotlib>=3.0,<=4.0',
                      'tqdm>=4.0,<=5.0',
                      ],
    extras_require={'dev': ['rich<=13.0,<=14.0']},
    python_requires='>=3.10',
    classifiers=['Programming Language :: Python :: 3',
                 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
                 'Operating System :: OS Independent',
                ],
)