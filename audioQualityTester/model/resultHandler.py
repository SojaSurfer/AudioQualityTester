from pathlib import Path
import os
import zipfile

from .logger import modelLogger


class ResultHandler():
    """The class is the backend of the ResultScreen(-Controller)."""

    def __init__(self):
        return None
    
    @staticmethod
    def zipDirectory(directory:str, outputPath:str) -> None:
        """The method zips all files of a directory and saves it in outputPath."""

        if not os.path.isdir(outputPath):
            modelLogger.warning('Directory for zipped results does not exist')
            raise FileNotFoundError()
        
        zipPath = os.path.join(outputPath, 'AudioQualityTester.zip')

        with zipfile.ZipFile(zipPath, 'w', zipfile.ZIP_DEFLATED) as zipf:

            # Walk through the directory
            for foldername, subfolders, filenames in os.walk(directory):

                for filename in filenames:

                    # Create the full filepath
                    filepath = os.path.join(foldername, filename)

                    # Add file to zip, use arcname to avoid adding the full path
                    arcname = os.path.relpath(filepath, directory)
                    zipf.write(filepath, arcname)
        
        modelLogger.info(f'Zipped results to {outputPath}')

        return None


