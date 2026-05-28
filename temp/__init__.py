import logging
from os import listdir, unlink
from os.path import abspath, dirname, isdir, isfile, islink, join

logger = logging.getLogger(__name__)


def clear(temp_dir: str | None = None) -> bool:
    if not temp_dir:
        temp_dir = dirname(__file__)

    try:
        for filename in listdir(temp_dir):
            file_path = join(temp_dir, filename)

            if abspath(file_path) == abspath(__file__):
                continue

            if isfile(file_path) or islink(file_path):
                unlink(file_path)
            elif isdir(file_path):
                clear(file_path)
        return True
    except Exception as e:
        logger.error(f'Failed to clear temporary directory: {type(e).__name__} (dir: {temp_dir})')
        return False
