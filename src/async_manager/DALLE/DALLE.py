import requests
import shutil
import os
import time
from src.utils.Prototype import Prototype

class DALLE(Prototype):
    """
        Handles generating, regenerating DALLE images
        Generating is async, so it uses AsyncOpenAI as self.client
        Regenerating is sync, so it uses OpenAI as self.client
        Handles downloading images from URL
    """
    def __init__(self, client, async_client) -> None:
        super().__init__()
        self.client = client
        self.async_client = async_client

    def download(self, config: any, url: str, frame_num: int) -> str:
        """Downloads and names the image based on which frame number it is

        Args:
            config (any): Python object holding configuration settings
            url (str): URL to image
            frame_num (int): Frame number

        Returns:
            filepath (str): Output filepath of saved image

        Raises:
            e: If setting cannot be found
        """
        try:
            dalle_config = config["DALLE"]
            global_config = config["global_settings"]
            video_directory = global_config["output_path"]
        except KeyError as e:
            self.logger.error("Config file is missing settings for DALLE")
            raise e

        response = requests.get(url, stream=True)
        save_path = os.path.join(video_directory, f"{dalle_config['output_prefix']}-{str(frame_num)}.png")
        with open(save_path, 'wb+') as out_file:
            shutil.copyfileobj(response.raw, out_file)
            self.logger.info("Saving image: " + save_path)

        del response
        return save_path
        
        
    async def generate(self, config: any, prompt: str, size: str=None) -> str:
        """Generates a URL linking to a DALLE image from a text prompt
        Async function that speeds up image generation

        Args:
            config (any): Python object containing configuration
            prompt (str): Text DALLE prompt
            size (str, optional): Dimensions of the generated image. Defaults to None.

        Raises:
            e: Settings are missing

        Returns:
            str: URL to image
        """
        prev = time.time()

        try:
            dalle_config = config["DALLE"]
        except KeyError as e:
            self.logger.error("DALLE configuration missing")
            raise e
        
        # Default size
        if size == None:
            size = "1024x1024"

        # The 2 models take in different parameters
        match dalle_config["dalle_model"]:
            case "dall-e-3":
                response = await self.async_client.images.generate(
                    model="dall-e-3",
                    prompt=prompt,
                    size=size,
                    quality=dalle_config["quality"],
                    n=1,
                )
            case _:
                self.logger.error("This DALLE model is not supported!")

        self.logger.info(f"DALLE generation complete: Prompt={prompt}. Time taken={time.time() - prev}.")

        return response.data[0].url
    
    def regenerate(self, config: any, prompt: str, size: str=None) -> str:
        """Generates a frame using a prompt and size

        Args:
            config (any): Python object containing settings
            prompt (str): Text prompt
            size (str, optional): Dimensions of image. Defaults to None.

        Raises:
            e: If settings are missing from config

        Returns:
            str: URL to image
        """
        prev = time.time()

        try:
            dalle_config = config["DALLE"]
        except Exception as e:
            raise e
        
        if size == None:
            size = "1024x1024"

        # The 2 models take in different parameters
        match dalle_config["dalle_model"]:
            case "dall-e-3":
                response = self.client.images.generate(
                    model=dalle_config["dalle_model"],
                    prompt=prompt,
                    size=size,
                    quality=dalle_config["quality"],
                    n=1,
                )
            case _:
                self.logger.error("This DALLE model is not supported!")

        self.logger.info(f"DALLE generation complete: Prompt={prompt}. Time taken={time.time() - prev}.")

        return response.data[0].url