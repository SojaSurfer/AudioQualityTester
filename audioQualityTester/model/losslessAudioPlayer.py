import time
import threading

from pydub import AudioSegment
import simpleaudio as sa

from .logger import modelLogger



""" Not Used """
class LosslessAudioPlayer:
    """The class is a test for playing lossless audio formats like WAV, FLAC, OGG with pydub in a thread.
    It is currently unused because of threading issues in combination with PySide6.
    """

    def __init__(self):
        self._stopEvent = threading.Event()
        self._playThread = None
        self._isPlayingLossless = False
        self._lock = threading.Lock()
        self.playObj = None

        return None


    def playFileLossless(self, filepath: str, startTime: int = 0) -> None:
        """The method plays an audio from a specific start point."""

        with self._lock:
            if self._isPlayingLossless:
                print("Audio is already playing.")
                return

            self._stopEvent.clear()

        # Load the audio file
        self.audio = AudioSegment.from_file(filepath)

        # Start the playback thread
        self._playThread = threading.Thread(target=self._playAudioLossless, args=(startTime * 1_000,))
        self._playThread.start()
        return None
    

    def _playAudioLossless(self, startTime_ms: int) -> None:
        """Internal method to handle the actual playback in a separate thread."""

        print('playFile lossless method')

        # Slice the audio from the specific start time
        playSegment = self.audio[startTime_ms:]
        playback_data = playSegment.raw_data

        # Play the audio asynchronously
        self.playObj = sa.play_buffer(playback_data,
                                      num_channels=self.audio.channels,
                                      bytes_per_sample=self.audio.sample_width,
                                      sample_rate=self.audio.frame_rate)

        with self._lock:
            self._isPlayingLossless = True

        # Keep the thread alive until the audio finishes or is stopped
        while not self._stopEvent.is_set() and self.playObj.is_playing():
            time.sleep(0.1)

        # If stop was called, stop the audio
        if self.playObj is not None and self.playObj.is_playing():
            print('Stopping audio playback')
            self.playObj.stop()

        with self._lock:
            self._isPlayingLossless = False
        print("Playback stopped.")
        return None
    

    def stopFileLossless(self) -> None:
        """The method stops the audio playback."""
        if self._playThread and self._isPlayingLossless:
            self._stopEvent.set()

            if self._playThread.is_alive():
                self._playThread.join()  # Wait for the thread to finish

            sa.stop_all()  # Safely stop all audio playback
            print('Stopped lossless audio')
        else:
            print("Audio is not playing.")
        return None


