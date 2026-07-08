import logging

from app.config import ensure_directories, get_project_paths

LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
LOG_FILE_NAME = "planneros.log"


def get_logger(name: str) -> logging.Logger:
    """Return a shared logger configured for console and file output.

    The logger writes INFO-and-above records to the console and appends
    them to logs/planneros.log. Handlers are only attached once per
    logger name to avoid duplicate log lines.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.propagate = False

    if not logger.handlers:
        formatter = logging.Formatter(LOG_FORMAT)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

        paths = get_project_paths()
        ensure_directories(paths)
        log_file = paths["logs"] / LOG_FILE_NAME

        file_handler = logging.FileHandler(log_file, mode="a")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger