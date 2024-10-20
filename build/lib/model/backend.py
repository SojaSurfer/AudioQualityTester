from pathlib import Path
import tempfile
import os
import sys
import json
import functools
import logging

from .logger import modelLogger



def tempDirWrapper(func):
    """The wrapper creates a temporary directory which can be accessed as long as the wrapped
    function is running."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        with tempfile.TemporaryDirectory() as temporaryDir:
            tempDir = createTempDirectories(Path(temporaryDir))

            return func(*args, **kwargs, tempDir=tempDir)
    return wrapper


def createTempDirectories(temporaryDir:tempfile.TemporaryDirectory=None) -> dict[str, Path]:
    """The function creates a temporary directory and folders within it and returns it as a dictionary."""
    
    if temporaryDir is None: 
        temporaryDir = tempfile.TemporaryDirectory()
    else:
        root = Path(temporaryDir)

    tempDir = {'root': root,
               'images': root / 'images',
               'audio': root / 'audio',
               'etc': root / 'etc'
              }

    for path in tempDir.values():
        path.mkdir(exist_ok=True)

    modelLogger.debug(f'Created temporary directories in {tempDir["root"]}')
    return tempDir



class BaseFactory():
    """The factory class defines certain attributes and methods which are used in several model classes."""

    SUPPORTED_AUDIOFILES = ['MP3', 'MP4', 'WAV', 'FLAC', 'AIFF', 'OGG', 'AAC', 'AC3']
    COMPRESSIONBOXES_CHECKED = 5
    TEMPDIR_IN_USE = False

    def __init__(self):
        return None

    @staticmethod
    def loadJson(path:str|Path) -> dict:
        """The method loads a json file. If the path does not exists it defaults to the debug temp dir
        which is located in test/temp.
        """

        if not isinstance(path, Path):
            path = Path(path)

        if path.exists():
            with open(path, 'r') as file:
                data = json.load(file)

        else:
            # temporary directory was not created fall back to debug data in test directory
            print('temporary directory was not created fall back to debug data in test directory')
            tempDir = BaseFactory.getTempDirDEBUG()
            with open(tempDir / path.name, 'r') as file:
                data = json.load(file)
        
        return data


    def createTempDir(self) -> None:
        """The method creates a temporary directory for audio and image files."""
        
        self.temporaryDir = tempfile.TemporaryDirectory()
        root = Path(self.temporaryDir.name)

        self.tempDir = {'root': root,
                        'imgs': root / 'imgs',
                        'audio': root / 'audio'
                        }

        for path in self.tempDir.values():
            path.mkdir(exist_ok=True)

        return None


    @classmethod
    def getTempDirDEBUG(cls) -> dict[str, Path]:
        """The function returns a tempDir dictionary that points to the test directory for debug purposes."""

        root = Path(__file__).parent.parent.parent / 'test' / 'temp'
        tempDir = {'root': root,
                    'images': root / 'images',
                    'audio': root / 'audio',
                    'etc': root / 'etc'}
        
        if not cls.TEMPDIR_IN_USE:
            modelLogger.warning('Debug temp dir will be used')
            cls.TEMPDIR_IN_USE = True
        
        return tempDir

    @staticmethod
    def saveJson(filepath:Path|str, data:dict) -> None:
        """The method securly saves data to a json file."""

        tempfilepath = str(filepath) + '.temp'

        with open(tempfilepath, 'w') as file:
            json.dump(data, file)
        os.replace(tempfilepath, filepath)

        modelLogger.debug(f'Saved json to {filepath}')
        return None



class StartSettingInspector(BaseFactory):
    """The method validates the user input stemming from the start screen."""

    def __init__(self, makeAssertion:bool = True):

        self.defaultBitrateList = [96, 128, 160, 192, 224, 256, 288, 320]
        self.cbrList: list[int] = []
        self.vbrList: list[int] = [0,2,4,6,9]

        self.makeAssertion = makeAssertion
        self.metadata = {}

        self.errorMsg = ''

        modelLogger.debug(f'{self.__class__.__qualname__} initialized')
        return None


    def returnAudioFormat(self, format: int = 0) -> str|tuple[str,str]:
        """The method returns the format of the loaded audio file in a specified format.
        
        Arguments:
            format (int): 0 - string of format id, 1 - string of readable format, 2 - tuple of both formats.
        """
        
        lookup = {'None': 'cbr', 'constant': 'cbr', 'variable': 'vbr'}
        
        bitrateMode = lookup[self.metadata.get('bitrateMode', 'None')]

        format0 = f'{self.metadata["format"]}_{bitrateMode}{self.metadata["bitrate"]}'
        format1 = f'{self.metadata["format"]} [{self.metadata["bitrate"]} kbps]'

        if format == 0:
            return format0
        elif format == 1:
            return format1
        elif format == 2:
            return format0, format1
        else: 
            raise ValueError('Incorrect format argument')


    def loadMetadata(self, filepath:str=None) -> bool:
        """The method loads the metadata of an audio file using the mutagen module. It returns true if it was successful."""
        
        if filepath is not None:
            self.filepath = Path(filepath)

        fileExt = self.filepath.suffix.lower()

        match fileExt:
            case '.mp3':
                self.metadata = self.loadMetadataMP3()
            case '.mp4':
                self.metadata = self.loadMetadataMP4()
            case '.wav':
                self.metadata = self.loadMetadataWAV()
            case '.aif':
                self.metadata = self.loadMetadataAIFF()
            case '.aiff':
                self.metadata = self.loadMetadataAIFF()
            case '.ogg':
                self.metadata = self.loadMetadataOGG()
            case '.flac':
                self.metadata = self.loadMetadataFLAC()
            case '.aac':
                self.metadata = self.loadMetadataAAC()
            case '.ac3':
                self.metadata = self.loadMetadataAC3()
            case _:
                error = f"Error: Unknown file with extension '{fileExt}'. Only the following formats are supported: {', '.join(self.SUPPORTED_AUDIOFILES)}"
                self.errorMsg += '\n' + error
                return False
                raise NotImplementedError(f"Unknown file with extension {fileExt}. Only the following formats are supported: {self.SUPPORTED_AUDIOFILES}")
        
        self.metadata['filesize'] = os.path.getsize(self.filepath) / 1_000_000

        modelLogger.debug(f'Loaded metadata for {filepath}')
        return True
    

    def loadMetadataFLAC(self) -> dict:
        from mutagen.flac import FLAC

        audio = FLAC(self.filepath)

        metadata = {'format': 'FLAC',
                    'bitrate': int(audio.info.bitrate / 1_000),
                    'bitsPerSample': audio.info.bits_per_sample,
                    'channels': audio.info.channels,
                    'length': int(round(audio.info.length)),
                    'sample_rate': audio.info.sample_rate,
                    'total_samples': audio.info.total_samples,
        }

        return metadata
    
    
    def loadMetadataAC3(self) -> dict:
        from mutagen.ac3 import AC3
        
        audio = AC3(self.filepath)

        metadata = {'format': 'AC3',
                    'bitrate': int(audio.info.bitrate / 1_000),
                    'channels': audio.info.channels,
                    'codec': audio.info.codec,
                    'length': int(round(audio.info.length)),
                    'sample_rate': audio.info.sample_rate,
        }

        return metadata
    

    def loadMetadataMP4(self) -> dict:
        from mutagen.mp4 import MP4
        
        audio = MP4(self.filepath)

        metadata = {'format': 'MP4',
                    'bitrate': int(audio.info.bitrate / 1_000),
                    'bitsPerSample': audio.info.bits_per_sample,
                    'channels': audio.info.channels,
                    'codec': audio.info.codec,
                    'length': int(round(audio.info.length)),
                    'sample_rate': audio.info.sample_rate,
        }

        return metadata


    def loadMetadataAAC(self) -> dict:
        from mutagen.aac import AAC  # AAC.__name__ -> 'AAC'
        
        audio = AAC(self.filepath)

        metadata = {'format': 'AAC',
                    'bitrate': int(audio.info.bitrate / 1_000),
                    'channels': audio.info.channels,
                    'length': int(round(audio.info.length)),
                    'sample_rate': audio.info.sample_rate,
        }

        return metadata


    def loadMetadataOGG(self) -> dict:
        from mutagen.oggflac import OggFLAC, OggFLACHeaderError
        from mutagen.oggvorbis import OggVorbis

        try:
            audio = OggFLAC(self.filepath)
        except OggFLACHeaderError:
            audio = OggVorbis(self.filepath)
        

        metadata = {'format': 'OGG',
                    'bitrate': int(audio.info.bitrate / 1_000),
                    'channels': audio.info.channels,
                    'length': int(round(audio.info.length)),
                    'sample_rate': audio.info.sample_rate,
                    'serial': audio.info.serial
        }
        return metadata


    def loadMetadataAIFF(self) -> dict:
        from mutagen.aiff import AIFF

        audio = AIFF(self.filepath)

        metadata = {'format': 'AIFF',
                    'bitrate': int(audio.info.bitrate / 1_000),
                    'bitsPerSample': audio.info.bits_per_sample,
                    'channels': audio.info.channels,
                    'length': int(round(audio.info.length)),
                    'sample_rate': audio.info.sample_rate,
                    'sample_size': audio.info.sample_size
        }
        return metadata


    def loadMetadataWAV(self) -> dict:
        from mutagen.wave import WAVE

        audio = WAVE(self.filepath)

        metadata = {'format': 'WAV',
                    'bitrate': int(audio.info.bitrate / 1_000),
                    'bitsPerSample': audio.info.bits_per_sample,
                    'channels': audio.info.channels,
                    'length': int(round(audio.info.length)),
                    'sample_rate': audio.info.sample_rate,
        }

        return metadata


    def loadMetadataMP3(self) -> dict:
        from mutagen.mp3 import MP3

        audio = MP3(self.filepath)

        brMode = str(audio.info.bitrate_mode)
        if 'CBR' in brMode or 'UNKNOWN' in brMode:
            bitrateMode = 'constant'
        else:
            bitrateMode = 'variable'
            # raise NotImplementedError('Currently only mp3 with constant bitrate are supported')
        
        metadata = {'format': 'MP3',
                    'bitrate': int(audio.info.bitrate / 1_000),
                    'bitrateMode': bitrateMode,
                    'channels': audio.info.channels,
                    'length': int(round(audio.info.length)),
                    'sample_rate': audio.info.sample_rate,
                    'layer': audio.info.layer}

        if self.makeAssertion:
            assert metadata['bitrate'] in self.defaultBitrateList, f'found bitrate not covered in bitrateList: {metadata["bitrate"]}'

        return metadata


    def validateUserInput(self, **kwargs) -> bool:
        """The method validates the input of the start screen. It returns True if the settings are valid, False otherwise
        and it will populate the errorMsg variable with found errors.
        """

        self.errorMsg = ''
        self.statusDict = kwargs.get('statusDict', {})
        self.compressionDict = kwargs.get('compressionDict', {})
        self.filepath = Path(self.statusDict.get('fileLoad', ''))

        self.adjustLogLevel()
        
        userInputIsValid = self.isCorrectFile() and self.loadMetadata() and self.correctCheckboxes()

        if userInputIsValid:
            modelLogger.info('Start Screen User input is valid')
        else:
            modelLogger.warning(f'Start Screen User input is defective: {self.errorMsg.replace("\n", ", ")}')

        return userInputIsValid


    def adjustLogLevel(self) -> None:
        """The method sets the root logger level (std out) to INFO for debug mode and WARNING for non-debug."""
        
        if self.statusDict.get('debug', False):
            logging.getLogger().setLevel(logging.INFO)
        else:
            logging.getLogger().setLevel(logging.WARNING)
        return None


    def correctCheckboxes(self) -> bool:
        """The method checks if the correct amount of checkboxes were checked."""

        checkedCompressionBoxes = sum(checkbox['selected'] for checkbox in self.compressionDict.values())

        if checkedCompressionBoxes == self.COMPRESSIONBOXES_CHECKED:
            return True
        else:
            self.errorMsg += '\nError: Please select exactly 5 compression levels.'
            return False


    def isCorrectFile(self) -> bool:
        """The method checks if the audio filepath exists."""
        
        if self.filepath.is_file():
            return True
        
        elif not self.filepath or self.filepath == Path(''):
            self.errorMsg += '\nError: Provide a path to a audio file.'
        else:
            self.errorMsg += '\nError: Audio filepath is not correct.'
        
        return False






