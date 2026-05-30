import logging
import logging.handlers
import sys

import colorlog

from config.const import BASE_DIR
from config.settings import LogConfig


def setup_logging(cfg: LogConfig) -> None:
    formatter = colorlog.ColoredFormatter(
        fmt=cfg.format,
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bold_red',
        },
    )

    stdout_handler = colorlog.StreamHandler(stream=sys.stdout)
    stdout_handler.setFormatter(formatter)

    logging.basicConfig(
        level=getattr(logging, cfg.level),
        format=cfg.file_format,
        handlers=[
            logging.handlers.RotatingFileHandler(
                filename=BASE_DIR / cfg.file_path,
                maxBytes=cfg.max_size * 1024 * 1024,
                backupCount=cfg.backup_count,
                encoding='utf-8',
            ),
            stdout_handler,
        ],
    )

    logging.getLogger('aiogram').setLevel(logging.WARNING)
    logging.getLogger('asyncio').setLevel(logging.INFO)
    logging.getLogger('aiogram_dialog').setLevel(logging.INFO)
