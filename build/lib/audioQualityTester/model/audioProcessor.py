from pathlib import Path
import secrets

from pydub import AudioSegment
# from audiosegment import AudioSegment as AS
import librosa
import librosa.display

import numpy as np
from scipy.signal import spectrogram
import matplotlib.pyplot as plt
from tqdm import tqdm

from .logger import modelLogger
from .backend import BaseFactory, StartSettingInspector




class AudioProcessor(BaseFactory):
    """The class handles the processing of audio files like doing compressions and saving metadata."""

    def __init__(self, **kwargs):
        
        self.compressionDict = kwargs.get('compressionDict', {})
        self.statusDict = kwargs.get('statusDict', {})
        self.metadata = kwargs.get('metadata', {})
        self.audioFormat = kwargs.get('audioFormat', None)
        self.tempDir = self.getTempDir(**kwargs)
        self.filepath = Path(self.statusDict.get('fileLoad'), '')
        self.inputAudioFormat = kwargs.get('inputAudioFormat', '')
        self.randomAudioDict = kwargs.get('randomAudioDict', {})

        self.activeCompressions = {key:value for key, value in self.compressionDict.items() if value['selected']}
        self.bitratePathList: list[dict[str:Path]] = []

        modelLogger.debug(f'{self.__class__.__qualname__} initialized')

        return None


    def getTempDir(self, **kwargs) -> dict[str:Path]:
        """The method returns the temp dir used w.r.t. the debug settings."""

        if self.statusDict['debug']:
            tempDir = self.getTempDirDEBUG()
        else:
            tempDir = kwargs.get('tempDir', None)

        return tempDir


    def setup(self) -> None:
        """The method loads the audio file, exports it to the specified formats and creates a random assignment for the listening screen."""

        self.audio = AudioSegment.from_file(self.filepath)
        # self.audio2 = AS(self.audio, 'AS_name')

        self.exportSpecifiedBitrateCompression()

        self._getRandomizedAudioFiles()
        self._saveData()

        return None


    def exportSpecifiedBitrateCompression(self) -> None:
        """The method exports the audio file to different formats specified in activeCompressions.
        It will add the save path to the activeCompression dictionary.
        """
        
        def parseFormat(formatString:str) -> dict:
            formatDict = {}
            formatList = formatString.split('_')
            formatDict['format'] = formatList[0].strip().lower()

            if len(formatList) > 1:
                if formatList[1].startswith('cbr'):
                    formatDict['bitrate'] = f'{formatList[1][3:]}k'
                    formatDict['string'] = f"{formatDict['format']}_CBR{formatDict['bitrate']}"
                elif formatList[1].startswith('vbr'):
                    formatDict['parameters'] = ["-q:a", formatList[1][3:]]
                    formatDict['string'] = f"{formatDict['format']}_VBR{formatList[1][3:]}"
                else:
                    raise ValueError(f'Unknown format settings for {formatList}')
            
            return formatDict


        for key, rawFormat in tqdm(self.activeCompressions.items(), ncols=80, desc='Converting'):

            if rawFormat['id'] == self.inputAudioFormat:
                # use the provided file for the original audio file
                self.activeCompressions[key]['path'] = self.filepath
            
            else:
                formatDict = parseFormat(rawFormat['id'])

                path = self.tempDir['audio'] / f'{self.filepath.stem}_{formatDict.pop("string")}.mp3'

                if not path.exists():
                    # create the compressed audio file
                    self.audio.export(path, **formatDict)
                    modelLogger.info(f'Saved compressed file to {path} with settings {formatDict}')

                self.activeCompressions[key]['path'] = str(path)
        
        return None
    

    def exportConstantBitrateCompression(self) -> None:
        """The method will export the file to all available constant bitrate formats."""

        modelLogger.debug('Converting file to different compression levels')
        
        self.cbrList = list(range(96, self.metadata['bitrate']+32, 32))

        for bitrate in tqdm(self.cbrList[:-1], ncols=80, desc='Converting'):

            path = self.filepath.parent / f'{self.filepath.stem}_{bitrate}.mp3'
            
            if not path.is_file:
                self.audio.export(path, format='mp3', bitrate=f'{bitrate}k')

            self.bitratePathList[bitrate] = path

        self.bitratePathList[self.cbrList[-1]] = self.filepath  # add the initial audio file

        return None


    def exportVariableBitrateCompression(self) -> None:
        """The method will export the file to all available variable bitrate formats."""

        for vbr in tqdm(self.vbrList):
            path = self.filepath.parent / f'{self.filepath.stem}_vbr{vbr}.mp3'

            if not path.is_file:
                self.audio.export(path, format='mp3', parameters=["-q:a", str(vbr)])

            self.bitratePathList[f'vbr{vbr}'] = path
        
        return None


    def _getRandomizedAudioFiles(self) -> dict[int:dict]:
        """The method creates and returns a randomized dictionary with the specified audio files."""

        self.randomAudioDict.clear()
        activeCompressions = list(self.activeCompressions.values())
        inspector = StartSettingInspector(makeAssertion=False)

        for i in range(self.COMPRESSIONBOXES_CHECKED):
            selection = secrets.choice(activeCompressions)
            activeCompressions.remove(selection)

            inspector.loadMetadata(selection['path'])
            selection['fileMetadata'] = inspector.metadata
            selection['listeningDuration'] = 0

            self.randomAudioDict[i] = selection
        
        return self.randomAudioDict


    def _saveData(self) -> None:
        """The method saves all settings into a json file."""
        
        randomAudioDict = self.pathToString(self.randomAudioDict)
        filepath = self.tempDir['etc'] / 'randomizedAudioFiles.json'
        self.saveJson(filepath, randomAudioDict)

        filepath = self.tempDir['etc'] / 'settings.json'
        settingsJson = {'compressionDict': self.compressionDict,
                        'statusDict': self.statusDict,
                        'metadata': self.metadata}
        self.saveJson(filepath, settingsJson)

        modelLogger.info(f'{self.__class__.__qualname__} data saved')
        return None


    def pathToString(self, dictionary:dict) -> dict:
        """The method converts every Path type in a dictionary to string."""

        for key, value in dictionary.items():

            if isinstance(value, Path):
                dictionary[key] = str(value)
            elif isinstance(value, dict):
                self.pathToString(value)
        
        return dictionary


    def computeResult(self, comboBoxChoices:dict[str:str], duration:int) -> dict:
        """The method evaluates the user result by comparing it to the created randomAudioDict. 
        The results are saved as json and returned.
        """

        for key, randDict in self.randomAudioDict.items():
            correctFormat = randDict['name']

            if comboBoxChoices[str(key)] == correctFormat:
                randDict['correct'] = True
            else:
                randDict['correct'] = False
            
            randDict['choice'] = comboBoxChoices[str(key)]
        

        for key, value in self.randomAudioDict.items():
            value['fileMetadata'] = self.getFileInfoDict(value['fileMetadata'])
        
        filepath = self.tempDir['etc'] / 'result.json'
        self.saveJson(filepath, self.pathToString(self.randomAudioDict))

        modelLogger.info(f'Results: {self.randomAudioDict}')
        return self.randomAudioDict

    @staticmethod
    def getFileInfoDict(metadataDict:dict) -> dict:
        """The method extracts the metadata that are used in the result screen from the available metadata."""
        
        fileInfo = {}

        for key, value in metadataDict.items():
            match key:
                case 'bitrate':
                    fileInfo['Bitrate'] = f'{value} kbps'
                case 'bitrateMode':
                    fileInfo['Bitrate Mode'] = value
                case 'sample_rate':
                    fileInfo['Sample Rate'] = f'{(value/1_000):.1f} kHz'
                case 'filesize':
                    fileInfo['filesize'] = f'{value:.2f} MB'
                case _:
                    pass
        
        return fileInfo


    def formatResult(self, result:dict) -> list[dict[str, str|tuple]]:
        """The method formats the result consisting of a boolean, text info and two images to transfer it to the Qt view element."""

        formattedResultList = []

        for id, valueDict in result.items():
            formattedResult = {}
            formattedResult['resultText'] = self._formatResultText(id, valueDict)
            formattedResult['spectrogramSource'] = str(valueDict['path_Spectrogram'])
            formattedResult['melSource'] = str(valueDict['path_MEL'])
            formattedResult['correct'] = valueDict['correct']
            formattedResultList.append(formattedResult)
        
        return formattedResultList


    @staticmethod
    def _formatResultText(id:int, valueDict:dict) -> str:
        """The method formats the audio info/metadata text to be displayed on the Qt window."""

        resultString = f"Example 0{id+1}"
        meta = valueDict['fileMetadata']

        formatString = f"\n\nFormat: {valueDict['name']}\nChosen: {valueDict['choice']}"
        otherMetaInfo = f"\nListening Duration: {valueDict['listeningDuration']} sec\nBitrate: {meta['Bitrate']}\nSample rate: {meta['Sample Rate']}\nFile size: {meta['filesize']}"

        resultString += formatString + otherMetaInfo

        if 'Bitrate Mode' in meta.keys():
            info = f"\nBitrate Mode: {meta['Bitrate Mode']}"
            resultString += info
        
        return resultString



class AudioPlotter(BaseFactory):
    """The class creates graphics from audio files, like spectrograms and waveforms."""

    def __init__(self, plotPath:Path, debug:bool):
        self.plotPath = plotPath
        self.figsize = (12,8)
        self.debug = debug  # unused

        self.bitratePathList: dict[str:Path] = []
        self.randomAudioDict: dict[int:dict[str:Path]] = {}

        modelLogger.debug(f'{self.__class__.__qualname__} initialized')
        return None


    def plotAllResults(self, results:dict) -> None:
        """The method creates and saves the spectrogram plots for every audio file."""

        modelLogger.debug('Start plotting all results')
        
        for resultDict in tqdm(results.values(), ncols=80, desc='Plotting'):
            audio = AudioSegment.from_file(resultDict['path'])

            path = self.plotPath / f'MEL-spectrogram_{resultDict["id"]}.png'
            resultDict['path_MEL'] = path

            if not path.is_file():
                self._plotMelSpectrogram(audio)
                plt.savefig(path)

            path = self.plotPath / f'spectrogram_{resultDict["id"]}.png'
            resultDict['path_Spectrogram'] = path

            if not path.is_file():
                self._plotSpectrogram(audio)
                plt.savefig(path)
        
        return results


    def plotFrequencyDomain(self) -> None:
        """NOT USED: The method plots the frequency domains."""

        hist_bins, hist_vals = self.audio2.fft()
        hist_vals_real_normed = np.abs(hist_vals) / len(hist_vals)
        
        fig, ax = plt.subplots(figsize=self.figsize)
        ax.plot(hist_bins / 1000, hist_vals_real_normed)

        ax.set_xlabel("kHz")
        ax.set_ylabel("dB")
        ax.set_xlim([0.02,22.5])
        ax.set_ylim(bottom=0, top=150)

        plt.show()
        plt.close()
        return None


    def createWaveforms(self) -> None:
        """The method creates and saves the waveforms of all audio files."""

        for bitrate, path in tqdm(self.bitratePathList.items(), ncols=80, desc='creating waveforms'):
            audio = AudioSegment.from_mp3(path)

            self._plotWaveform(audio)
            plt.savefig(self.plotPath / f'waveform_{path.stem}.png')
        
        return None


    def _plotWaveform(self, audio:AudioSegment, show:bool=False) -> None:
        """The method plots the waveform of an audio file."""

        samples = np.array(audio.get_array_of_samples())

        # If stereo, take only one channel (optional)
        if audio.channels == 2:
            samples = samples[::2]

        # Create time axis
        time_axis = np.linspace(0, len(samples) / audio.frame_rate, num=len(samples))

        # Plot the waveform
        fig, ax = plt.subplots(figsize=self.figsize)
        plt.plot(time_axis, samples / np.iinfo(np.int16).max, linewidth=0.05)

        ax.set_title("Waveform")
        ax.set_xlabel("Time [s]")
        ax.set_ylabel("Amplitude")
        ax.set_xlim([0, int(self.metadata['length'])+1])  # all files should have the same length
        ax.set_ylim([-1, 1])  # min/max values of int16

        plt.tight_layout()
        if show:
            plt.show()
            plt.close()
        return None


    def createMelSpectrogram(self) -> None:
        """The method creates and saves the MEL spectrograms of all audio files."""

        for bitrate, path in tqdm(self.bitratePathList.items(), ncols=80, desc='creating mel-spectrograms'):
            audio = AudioSegment.from_mp3(path)

            self._plotMelSpectrogram(audio)
            plt.savefig(self.plotPath / f'mel-spectrogram_{path.stem}.png')
        
        return None


    def _plotMelSpectrogram(self, audio:AudioSegment, show:bool=False) -> None:
        """The method plots the MEL spectrogram of an audio file."""
        
        if audio is None: audio = self.audio
        # Convert AudioSegment to numpy array
        samples = np.array(audio.get_array_of_samples())

        # If stereo, take only one channel (optional)
        if audio.channels == 2:
            samples = samples[::2]

        # Get the sample rate
        sample_rate = audio.frame_rate

        # Normalize samples (if needed, librosa expects float32 type)
        samples = samples.astype(np.float32) / np.iinfo(np.int16).max

        # Compute the Mel-spectrogram using librosa
        S = librosa.feature.melspectrogram(y=samples, sr=sample_rate, n_mels=128)

        # Convert to log scale (dB)
        S_dB = librosa.power_to_db(S, ref=np.max)

        # Plot the Mel-spectrogram
        plt.figure(figsize=self.figsize)
        librosa.display.specshow(S_dB, sr=sample_rate, x_axis='time', y_axis='mel')
        plt.colorbar(format='%+2.0f dB')
        plt.title('Mel-Spectrogram')

        plt.tight_layout()
        if show:
            plt.show()
            plt.close()
        return None


    def createSpectrograms(self) -> None:
        """The method creates and saves the spectrograms of all audio files."""

        for bitrate, path in tqdm(self.bitratePathList.items(), ncols=80, desc='creating spectrograms'):
            audio = AudioSegment.from_mp3(path)

            self._plotSpectrogram(audio)
            plt.savefig(self.plotPath / f'spectrogram_{path.stem}.png')
        
        return None

    @staticmethod
    def _plotSpectrogram(audio:AudioSegment, show:bool=False, nperseg:int=1024, noverlap:int=512) -> None:
        """The method plots the spectrogram of an audio file."""

        samples = np.array(audio.get_array_of_samples())
        if audio.channels == 2:
            samples = samples[::2]
        
        freqs, times, Sxx = spectrogram(samples, fs=audio.frame_rate, nperseg=nperseg, noverlap=noverlap)
        # Convert power spectrogram (Sxx) to dB scale
        Sxx_dB = 10 * np.log10(Sxx + 1e-9)


        # Plot
        fig, ax = plt.subplots(figsize=(12,8))
        ax.pcolormesh(times, freqs, Sxx_dB, shading='auto')

        ax.set_title('Spectrogram')
        ax.set_xlabel("Time in Seconds")
        ax.set_ylabel("Frequency in Hz")

        
        plt.tight_layout()
        if show:
            plt.show()
            plt.close()

        return None


    def _plotChromagram(self, audio_path) -> None:
        """UNUSED: The method plots the chromagram of an audio file."""

        y, sr = librosa.load(audio_path, sr=None)

        # Compute the chromagram
        chroma = librosa.feature.chroma_stft(y=y, sr=sr)

        # Plot the chromagram
        plt.figure(figsize=self.figsize)
        librosa.display.specshow(chroma, x_axis='time', y_axis='chroma', cmap='coolwarm')
        plt.colorbar()
        plt.title('Chromagram')
        plt.show()
        plt.close()

        return None


    def _plotTonnetz(self, audio_path: str) -> None:
        """UNUSED: The method plots the tonal centroid features of an audio file."""

        y, sr = librosa.load(audio_path, sr=None)

        # Compute the tonnetz (tonal centroid features)
        tonnetz = librosa.feature.tonnetz(y=y, sr=sr)

        # Plot the tonnetz
        plt.figure(figsize=self.figsize)
        librosa.display.specshow(tonnetz, y_axis='tonnetz', x_axis='time')
        plt.colorbar()
        plt.title('Tonal Centroid Features (Tonnetz)')
        plt.show()
        plt.close()
        return None


