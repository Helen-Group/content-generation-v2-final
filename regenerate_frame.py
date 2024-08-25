from src.async_manager.DALLE.DALLE import DALLE
from src.utils.ConfigLoader import ConfigLoader
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv()) # read local .env file
from openai import OpenAI, AsyncOpenAI
import os

# Small manual tool to regenerate a frame. Use in case of a frame failing to generate

FRAMES = [11]
FOLDER_NAME = "TheEpicTaleofCainandAbel"

# --- Do not touch ---
FULL_PATH = os.path.join("movie_workspace", FOLDER_NAME)
CONFIG_PATH = os.path.join(FULL_PATH, "config.yaml")

config = {
    "DALLE" : {
        "dalle_model" : "dall-e-3",
        "quality" : "standard",
        "output_prefix" : "i"
    },
    "TTS" : {
        "voice" : "oH7WLysPgrahlQ0DFWUT",
        "output_prefix" : "a"
    },
    "global_settings" : {
        "output_path": f"{FULL_PATH}"
    }
}

cl = ConfigLoader()
output_config = cl.read(CONFIG_PATH)
scenes = output_config["scenes"]
client = OpenAI()
async_client = AsyncOpenAI()
interface = DALLE(client, async_client)

for frame in FRAMES:
    url = interface.regenerate(config, scenes[frame-1]["prompt"])
    interface.download(config, url, frame)