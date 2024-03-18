import os
import logging

def setup_logger(file_name, log_level=logging.INFO):
    # Create a folder named "log" if it doesn't exist

    log_folder = os.path.join("workspace", "logs")
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

    # Set up logging
    log_file_path = os.path.join(log_folder, file_name)
    logging.basicConfig(filename=log_file_path, level=log_level,
                        format='%(asctime)s - %(levelname)s - %(message)s')

    logger = logging.getLogger()
    return logger