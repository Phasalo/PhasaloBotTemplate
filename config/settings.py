import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import find_dotenv, load_dotenv

from config.const import BASE_DIR


@dataclass
class TgBot:
    token: str
    admin_password: str
    proxy_url: str | None = None
    message_max_symbols: int = 400


@dataclass
class LogConfig:
    level: str = 'INFO'
    format: str = '%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    file_format: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    file_path: str = 'logs/bot.log'
    max_size: int = 10
    backup_count: int = 3


@dataclass
class Config:
    tg_bot: TgBot
    log: LogConfig
    db_path: Path


def load_config() -> Config:
    load_dotenv(find_dotenv())
    return Config(
        tg_bot=TgBot(
            token=os.getenv('BOT_TOKEN'),
            admin_password=os.getenv('PASSWORD'),
            proxy_url=os.getenv('PROXY_URL') or None,
        ),
        log=LogConfig(
            level=os.getenv('LOG_LEVEL', 'INFO'),
            file_path=os.getenv('LOG_FILE', 'logs/bot.log'),
            max_size=int(os.getenv('LOG_MAX_SIZE', 10)),
            backup_count=int(os.getenv('LOG_BACKUP_COUNT', 3)),
        ),
        db_path=BASE_DIR / 'db' / 'data.db',
    )
