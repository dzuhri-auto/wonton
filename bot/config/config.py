import json
import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    LICENSE_KEY = os.getenv("LICENSE_KEY")

    API_ID = os.getenv("API_ID")
    API_HASH = os.getenv("API_HASH")

    AUTO_CLAIM_BADGE = os.getenv("AUTO_CLAIM_BADGE", "True")

    USE_RANDOM_DELAY_IN_RUN = os.getenv("AUTO_UPGRADE", "True")
    RANDOM_DELAY_IN_RUN = json.loads(os.getenv("RANDOM_DELAY_IN_RUN", "[5, 15]"))
    USE_PROXY_FROM_FILE = os.getenv("USE_PROXY_FROM_FILE", "False")


settings = Settings()
