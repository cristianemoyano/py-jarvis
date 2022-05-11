import logging


def setup_logger(logger):
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - L#%(lineno)s - %(name)s - %(levelname)s - %(message)s",
    )
