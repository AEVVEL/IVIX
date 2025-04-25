import os

from dotenv import load_dotenv

load_dotenv()


INITIAL_BACKOFF = int(os.getenv("INITIAL_BACKOFF")) if os.getenv("INITIAL_BACKOFF") else 1