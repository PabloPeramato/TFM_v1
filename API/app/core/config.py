import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")


class Settings:
    USERNAME_SWAGGER = os.getenv("USERNAME_SWAGGER")
    PASSWORD_SWAGGER = os.getenv("PASSWORD_SWAGGER")

    REMOTE_HOST_PXE = os.getenv("REMOTE_HOST_PXE")
    USERNAME_PXE = os.getenv("USERNAME_PXE")
    PASSWORD_PXE = os.getenv("PASSWORD_PXE")

    REMOTE_HOST_RPI3_85D9 = os.getenv("REMOTE_HOST_RPI3_85D9")
    REMOTE_HOST_RPI3_81B7 = os.getenv("REMOTE_HOST_RPI3_81B7")
    REMOTE_HOST_RPI3_8BA1 = os.getenv("REMOTE_HOST_RPI3_8BA1")

    REMOTE_HOST_RPI4_1718 = os.getenv("REMOTE_HOST_RPI4_1718")

    SERIAL_NUMBERS_3B = os.getenv("SERIAL_NUMBERS_3B").split(',')
    SERIAL_NUMBERS_4B = os.getenv("SERIAL_NUMBERS_4B").split(',')
    OPERATING_SYSTEMS = os.getenv("OPERATING_SYSTEMS").split(',')

    MQTT_BROKER = os.getenv("MQTT_BROKER")
    MQTT_PORT = os.getenv("MQTT_PORT")
    MQTT_TOPIC_RPI3_85D9 = os.getenv("MQTT_TOPIC_RPI3_85D9")
    MQTT_TOPIC_RPI3_81B7 = os.getenv("MQTT_TOPIC_RPI3_81B7")
    MQTT_TOPIC_RPI3_8BA1 = os.getenv("MQTT_TOPIC_RPI3_8BA1")
    MQTT_TOPIC_RPI4_1718 = os.getenv("MQTT_TOPIC_RPI4_1718")

    ORIGINS = os.getenv("ORIGINS").split(',')
    FAKE_USERS_DB = os.getenv("FAKE_USERS_DB").split(',')
    ALGORITHM = os.getenv("ALGORITHM")
    DATABASE_URL = os.getenv("DATABASE_URL")
    TABLE_NAME = os.getenv("TABLE_NAME")


settings = Settings()
