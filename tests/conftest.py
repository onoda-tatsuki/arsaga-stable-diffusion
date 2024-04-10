import pytest
from dotenv import load_dotenv
import os


@pytest.fixture(autouse=True)
def init_env() -> None:
    load_dotenv('.env.test', verbose=True)