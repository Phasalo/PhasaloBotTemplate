from dishka import Provider, Scope, make_container, provide

from config.settings import Config
from db.repositories.queries import QueriesRepository
from db.repositories.users import UsersRepository


class AppProvider(Provider):
    scope = Scope.APP

    def __init__(self, config: Config):
        super().__init__()
        self._config = config

    @provide
    def get_config(self) -> Config:
        return self._config

    @provide
    def users_repo(self, config: Config) -> UsersRepository:
        return UsersRepository(config.db_path)

    @provide
    def queries_repo(self, config: Config) -> QueriesRepository:
        return QueriesRepository(config.db_path)


def build_container(config: Config):
    return make_container(AppProvider(config))
