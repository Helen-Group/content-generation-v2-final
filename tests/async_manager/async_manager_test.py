from src.async_manager.async_manager import AsyncClient
from src.utils.ConfigLoader import ConfigLoader
from src.async_manager.DALLE.DALLE import DALLE
from src.async_manager.TTS.TTS import TTS
from openai import OpenAI, AsyncOpenAI
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv()) # read local .env file
import os
import glob

PATH = os.path.dirname(os.path.realpath(__file__))

def setup() -> AsyncClient:
    cl = ConfigLoader()
    base_config_path = os.path.join(PATH, "base_config.yaml")
    base_config = cl.read(base_config_path)

    sample_output_path = os.path.join(PATH, "sample_output.yaml")
    sample_output_config = cl.read(sample_output_path)


    client = OpenAI()
    async_client = AsyncOpenAI()
    dalle = DALLE(client, async_client)

    tts = TTS()

    my_client = AsyncClient(base_config, sample_output_config, DALLE=dalle, TTS=tts)
    return my_client

def test_AsyncClient_run_DALLE():
    try:
        os.remove(os.path.join(PATH, "*.png"))
    except:
        pass
    return_obj = {}
    client = setup()
    client._run_DALLE(return_obj)
    assert "return" in return_obj
    assert len(return_obj["return"]) == 2
    assert ".png" in return_obj["return"][0]
    filepath = return_obj["return"][0]

    # Validate returned filepath
    check = glob.glob(filepath)
    assert len(check) == 1

def test_AsyncClient_run_TTS():
    try:
        os.remove(os.path.join(PATH, "*.mp3"))
    except:
        pass
    return_obj = {}
    client = setup()
    client._run_TTS(return_obj)

    # Check return values are correct
    assert "return" in return_obj
    assert len(return_obj["return"]) == 2
    assert ".mp3" in return_obj["return"][0]
    filepath = return_obj["return"][0]

    # Validate returned filepath
    check = glob.glob(filepath)
    assert len(check) == 1


def test_AsyncClient_run():
    try:
        os.remove(os.path.join(PATH, "*.png"))
    except:
        pass

    try:
        os.remove(os.path.join(PATH, "*.mp3"))
    except:
        pass

    client = setup()
    output = client.run()

    assert len(output) == 2

    filepath = output[0]["image_file"]
    check = glob.glob(filepath)
    assert len(check) == 1

    filepath = output[1]["audio_file"]
    check = glob.glob(filepath)
    assert len(check) == 1


