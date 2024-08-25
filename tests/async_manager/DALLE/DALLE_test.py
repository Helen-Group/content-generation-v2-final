from src.async_manager.DALLE.DALLE import DALLE
from src.utils.ConfigLoader import ConfigLoader
from openai import AsyncOpenAI, OpenAI
import pytest
import os
import glob

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv()) # read local .env file

PATH = os.path.dirname(os.path.realpath(__file__))

@pytest.mark.asyncio
async def test_DALLE_generation():
    client = OpenAI()
    async_client = AsyncOpenAI()
    cl = ConfigLoader()

    filename = "sample_config.yaml"
    filepath = os.path.join(PATH, filename)
    config = cl.read(filepath)
    dalle = DALLE(client, async_client)

    url = await dalle.generate(config, "A Cat")
    assert "http" in url

def test_DALLE_regeneration():
    client = OpenAI()
    async_client = AsyncOpenAI()
    cl = ConfigLoader()

    filename = "sample_config.yaml"
    filepath = os.path.join(PATH, filename)
    config = cl.read(filepath)
    dalle = DALLE(client, async_client)

    url = dalle.regenerate(config, "A Cat")
    assert "http" in url

def test_DALLE_download():
    try:
        os.remove(os.path.join(PATH, "frame-1.png"))
    except:
        pass

    client = OpenAI()
    async_client = AsyncOpenAI()
    cl = ConfigLoader()

    filename = "sample_config.yaml"
    filepath = os.path.join(PATH, filename)
    config = cl.read(filepath)
    dalle = DALLE(client, async_client)

    url = "https://i.pinimg.com/originals/13/9f/92/139f92b6fd342540aa946a33012aaab5.png"

    filepath = dalle.download(config, url, 1)

    check = glob.glob(filepath)
    assert len(check) == 1


