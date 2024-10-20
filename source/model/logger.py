from pathlib import Path
import logging

from PySide6.QtCore import QtMsgType, qInstallMessageHandler



logFile = Path(__file__).parent.parent / 'resources' / 'application.log'  # need to change!


def setupRootLogger(level: int = logging.WARNING) -> logging.Logger:
    """The function sets the level and format of the root logger (std out)."""

    rootLogger = logging.getLogger()

    if rootLogger.hasHandlers():
        rootLogger.handlers.clear()

    # Create and configure the console handler
    consoleHandler = logging.StreamHandler()
    consoleHandler.setLevel(level)  # Console handler level controls console output
    consolerFormatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    consoleHandler.setFormatter(consolerFormatter)
    
    rootLogger.addHandler(consoleHandler)

    return rootLogger


def setupLogger(name:str, level: int = logging.DEBUG, logFile: str = logFile) -> logging.Logger:
    """The function creates a logger with a name. The logger will propagate to the root logger."""

    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Check if handlers already exist to avoid duplicate logs
    if not logger.handlers:
        # File handler
        fileHandler = logging.FileHandler(logFile)
        fileHandler.setLevel(level)
        fileFormatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fileHandler.setFormatter(fileFormatter)

        # Adding handlers
        logger.addHandler(fileHandler)
    
    logger.propagate = True  # only a file handler is added because the logger will propagate its msgs to the root logger

    return logger


def installCustomMessageHandlerQT() -> None:
    """The function installs a custom message handler for Qt to be able to have two separate logger 
    for console (std out) and log file.
    """

    qInstallMessageHandler(_messageHandlerQT)
    return None


def _messageHandlerQT(mode:QtMsgType, context, message:str) -> None:
    """The function is a lookup table for the Qt messages."""

    if mode == QtMsgType.QtDebugMsg:
        viewLogger.debug(message)
    elif mode == QtMsgType.QtInfoMsg:
        viewLogger.info(message)
    elif mode == QtMsgType.QtWarningMsg:
        viewLogger.warning(message)
    elif mode == QtMsgType.QtCriticalMsg:
        viewLogger.error(message)
    elif mode == QtMsgType.QtFatalMsg:
        viewLogger.critical(message)
    
    return None




rootLogger = setupRootLogger()
mainLogger = setupLogger('Main')
modelLogger = setupLogger('Model')
viewLogger = setupLogger('View')
controllerLogger = setupLogger('Controller')




