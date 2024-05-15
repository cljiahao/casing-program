import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)


class Settings:
    PMSS_API_URL: str = os.getenv("PMSS_API_URL")
    CM_API_URL: str = os.getenv("CM_API_URL")
    USER: str = os.getenv("USER")
    PWD: str = os.getenv("PWD")
    ROB_API_KEY: str = os.getenv("ROB_API_KEY")
    GLS_API_KEY: str = os.getenv("GLS_API_KEY")


settings = Settings()
