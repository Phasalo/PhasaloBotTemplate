import logging
import logging.handlers
import os
import sys
from dataclasses import dataclass
from pathlib import Path

import colorlog
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from dotenv import find_dotenv, load_dotenv

from config.const import BASE_DIR

load_dotenv(find_dotenv())

Path(BASE_DIR / 'logs').mkdir(exist_ok=True)


@dataclass
class LogConfig:
    level: str = 'DEBUG'  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    format: str = '%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    file_format: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    file_path: str = 'logs/bot.log'
    max_size: int = 10  # MB
    backup_count: int = 3


@dataclass
class TgBot:
    token: str
    password: str
    message_max_symbols: int = 400


@dataclass
class Config:
    tg_bot: TgBot
    log: LogConfig


def __load_config() -> Config:
    return Config(
        tg_bot=TgBot(token=os.getenv('BOT_TOKEN'), password=os.getenv('PASSWORD')),
        log=LogConfig(
            level=os.getenv('LOG_LEVEL', 'INFO'),
            file_path=os.getenv('LOG_FILE', 'logs/bot.log'),
            max_size=int(os.getenv('LOG_MAX_SIZE', 10)),
            backup_count=int(os.getenv('LOG_BACKUP_COUNT', 3)),
        ),
    )


def setup_logging(cfg: LogConfig):
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


config: Config = __load_config()
bot = Bot(token=config.tg_bot.token, default=DefaultBotProperties(parse_mode='HTML'))

setup_logging(config.log)
