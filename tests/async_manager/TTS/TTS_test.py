import os
import glob
from src.async_manager.TTS.TTS import TTS 
from src.utils.ConfigLoader import ConfigLoader

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv()) # read local .env file

PATH = os.path.dirname(os.path.realpath(__file__))

def test_TTS():
    try:
        os.remove(os.path.join(PATH, "audio__test.mp3"))
    except:
        pass

    cl = ConfigLoader()
    filepath = os.path.join(PATH, "sample_config.yaml")
    config = cl.read(filepath)

    text = "Hello!"
    tts = TTS()
    filepath = tts.generate_audio(config, text, "test")

    check = glob.glob(filepath)
    assert len(check) == 1

    
