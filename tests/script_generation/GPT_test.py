from src.script_generation.GPT import GPT
from src.utils.ConfigLoader import ConfigLoader
from openai import OpenAI
import os
import json

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv()) # read local .env file

PATH = os.path.dirname(os.path.realpath(__file__))

def test_GPT_generation():
    cl = ConfigLoader()
    client = OpenAI()
    gpt = GPT(client)

    filepath = os.path.join(PATH, "sample_config.yaml")
    config = cl.read(filepath)
    res = gpt.generate(config)
    assert len(res) > 0

def test_GPT_save():
    try:
        os.remove(os.path.join(PATH, "sample_output.yaml"))
    except:
        pass

    cl = ConfigLoader()
    client = OpenAI()
    gpt = GPT(client)

    dummy_data = gpt.dummy_generate()
    filename = "sample_config.yaml"
    filepath = os.path.join(PATH, filename)
    config = cl.read(filepath)

    gpt.save_yaml("sample_output.yaml", config, dummy_data)

    res = cl.read(os.path.join(PATH, "sample_output.yaml"))
    assert len(res["scenes"]) > 0




