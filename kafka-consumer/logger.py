import logging
import os


def setup_logger():
    # Get the name of the current directory (project folder name)
    folder_name = os.path.basename(os.getcwd())

    # Create a logger
    logger = logging.getLogger(__name__)

    # Configure logging
    logging.basicConfig(
        filename=f"{folder_name}.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    return logger


# Call the setup_logger function to get the configured logger
logger = setup_logger()
