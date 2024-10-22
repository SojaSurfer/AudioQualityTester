from pathlib import Path
import time

import pygame
import pygame.mixer as mixer

from .logger import modelLogger



class AudioPlayer():
    """The class is used to play MP3 & wave audio files using pygame."""

    def __init__(self):

        mixer.init()
        pygame.init()

        self.isPlaying = False
        self.startTime = 0
        self.key = None
        self._playType = None

        modelLogger.debug(f'{self.__class__.__qualname__} initialized')
        return None
    

    def playFile(self, file:str, startTime:int = 0) -> None:
        """The method plays a mp3  or wav file at a specified start time. 
        If a file is already playing it is stopped before starting the new one.
        """

        self.stopFile()
        
        mixer.music.load(file)
        mixer.music.play(start=startTime)
        return None


    def stopFile(self) -> None:
        """The method stops the playin of an audio file."""

        if mixer.music.get_busy():
            mixer.music.stop()              
        return None


    def managePlaying(self, key:str) -> None:
        """The method actives the metrics about the play time."""

        self.isPlaying = True
        self.startTime = time.time()
        self.key = key
        return None
    

    def manageStopping(self) -> tuple[str, int]:
        """The method returns the id and the play duration of the audio file and resets those values."""

        key = self.key
        duration = 0

        if self.isPlaying:
            duration = int(round(time.time() - self.startTime))

        self.manageRest()
        return key, duration


    def manageRest(self) -> None:
        """The method resets the metrics about the play time"""
        self.key = None
        self.startTime = 0
        self.isPlaying = False
        return None



