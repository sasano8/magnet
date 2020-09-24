from pydantic import BaseSettings, BaseModel, SecretStr, Field
from typing import List, Dict, Optional, Literal, Final
from libs.decorators import Instantiate
from rabbitmq import RabbitApp
import os

# TODO: pydanticのSchemaドキュメントにconstやsecureなど説明が記載されてないのがあるのでpull requestしたい
# TODO: 環境変数を読み込むのにクラスベースだけでなく、関数も使いたい @deco(env_file=".env")def load みたいな
# TODO: 環境変数版のopenapiのようなものはないか

env_path = os.path.join(os.path.dirname(__file__), "..", ".env")

class EnvBase(BaseSettings):
    class Config:
        env_file = str(env_path)


class Logging(EnvBase):
    class Config:
        env_prefix = "LOG_"

    level: Literal["CRITICAL", "FATAL", "ERROR", "WARN", "WARNING", "INFO", "DEBUG", "NOTSET"] = "INFO"
    format_date: str = "%Y-%m-%d %H:%M:%S"
    format_msg: str = "%(levelname)s: %(asctime)s %(module)s %(funcName)s %(lineno)d: %(message)s"


class APICredential(BaseSettings):
    api_key: SecretStr = ""
    api_secret: SecretStr = ""


class APICredentialZaif(EnvBase, APICredential):
    class Config:
        env_prefix = "API_ZAIF_"


class APICredentialBitflyer(EnvBase, APICredential):
    class Config:
        env_prefix = "API_BITFLYER_"


class Rabbitmq(EnvBase, BaseSettings):
    class Config:
        env_prefix = "RABBITMQ_"

    url: str = ""


# class MessageQueue(BaseSettings):
#     broker_url: str = "rabbitmq"
#     queue_name: str = "default"
#     auto_ack: bool = False
#     durable: bool = True
#     queue_delete: bool = True


class DatabaseCredential(BaseSettings):
    def get_connection_string(self):
        raise NotImplementedError()


class DatabaseSQLiteCredential(EnvBase, DatabaseCredential):
    class Config:
        env_prefix = "DB_SQLITE_"

    filepath: Optional[str] = "./sql_app.db"

    def get_connection_string(self):
        return "sqlite:///{}".format(
            user=self.filepath,
        )


class DatabasePostgresCredential(EnvBase, DatabaseCredential):
    class Config:
        env_prefix = "DB_POSTGRES_"

    user: str
    password: SecretStr
    host: str
    database: str

    def get_connection_string(self):
        return "postgresql://{user}:{password}@{host}/{database}".format(
            user=self.user,
            password=self.password.get_secret_value(),
            host=self.host,
            database=self.database
        )


class UserAccessToken(EnvBase):
    class Config:
        env_prefix = "ACCESSTOKEN_"

    url: str = Field("/users/token", const=True)
    secret_key: SecretStr
    algorithm: str = "HS256"
    expire_minutes: int = 30


@Instantiate
class Env(BaseSettings):
    access_token: UserAccessToken = UserAccessToken()
    logging: Dict[str, Logging] = {
        "default": Logging()
    }
    databases: Dict[str, DatabaseCredential] = {
        "default": DatabasePostgresCredential()
    }
    queues: Dict[str, RabbitApp] = {
        # "default": MessageQueue(
        #     broker_url=Rabbitmq().url,
        #     queue_name="default",
        #     auto_ack=False,
        #     durable=True,
        #     queue_delete=True,
        # )
        "default": RabbitApp(
            broker_url=Rabbitmq().url,
            queue_name="default",
            auto_ack=False,
            durable=True,
            queue_delete=True,
        )
    }
    api_credentials: Dict[str, APICredential] = {
        "zaif": APICredentialZaif(),
        "bitflyer": APICredentialBitflyer()
    }
