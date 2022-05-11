import logging


def setup_logger(logger):
    logging.basicConfig(level=logging.INFO)

    # Create handlers
    c_handler = logging.StreamHandler()
    c_handler.setLevel(logging.INFO)

    # Create formatters and add it to handlers
    c_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    c_handler.setFormatter(c_format)

    # Add handlers to the logger
    logger.addHandler(c_handler)
