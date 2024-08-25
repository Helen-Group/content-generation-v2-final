from src.utils.ConfigLoader import ConfigLoader
import os

PATH = os.path.dirname(os.path.realpath(__file__))

def test_read():
    filepath = os.path.join(PATH, "testread.yaml")
    conf_loader = ConfigLoader()
    obj = conf_loader.read(filepath)
    assert obj["title"] == "TITLE"

def test_write():
    filepath = os.path.join(PATH, "testwrite.yaml")
    data = {"data": "Hello!"}
    conf_loader = ConfigLoader()
    conf_loader.write(filepath, data)
    obj = conf_loader.read(filepath)
    assert obj["data"] == "Hello!"
