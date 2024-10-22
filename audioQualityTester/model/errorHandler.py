from pydub.utils import which

from .logger import modelLogger



def verifyExternalDependencies() -> None:
    """The function checks if ffmpeg is installed and accesible."""

    if which("ffmpeg") is None:
        modelLogger.error("FFmpeg not found.")
        raise RuntimeError("FFmpeg must be installed to use this program. Please install it and ensure it's in your system's PATH.")
    
    modelLogger.info('Found ffmpeg backend installed.')
    return None


