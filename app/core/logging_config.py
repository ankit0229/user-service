import logging

LOG_FORMAT = "%(levelname)s: %(asctime)s - %(message)s"


def setup_logging():
    logging.basicConfig(level=logging.INFO,
                        format=LOG_FORMAT,
                        handlers=[
                            logging.FileHandler("app.log"),
                            logging.StreamHandler()
                        ])
