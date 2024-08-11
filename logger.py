import logging
import os


def setup_logger(log_file="mcinstaller.log"):
    logger = logging.getLogger("mcinstaller")
    logger.setLevel(logging.DEBUG)

    # Create file handler
    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.DEBUG)

    # Create console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    # Create formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # Add handlers to logger
    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger


logger = setup_logger()
