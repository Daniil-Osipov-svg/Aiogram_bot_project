from environs import Env
from dataclasses import dataclass

# Датабаза
@dataclass
class DatabaseConfig:
    db_name: str
    db_host: str
    db_user: str
    db_password: str

# Бот
@dataclass
class BotConfig:
    token: str
    admins: list[int]

@dataclass
class Config:
    database: DatabaseConfig
    bot: BotConfig

env: Env = Env()
env.read_env()

def load_config(path: str | None = None) -> Config:
    env: Env = Env()
    env.read_env(path)

    return Config(
        database=DatabaseConfig(
            db_name=env('DB_NAME'),
            db_host=env('DB_HOST'),
            db_user=env('DB_USER'),
            db_password=env('DB_PASSWORD')
        ),
        bot=BotConfig(
            token=env('BOT_TOKEN'),
            admins=list(map(int, env.list('ADMIN_IDS')))
        )
    )