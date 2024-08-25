import os
import json
import time
from src.utils.Prototype import Prototype
from src.utils.ConfigLoader import ConfigLoader
from src.script_generation.helpers import add_transformations

class GPT(Prototype):
    """
        Handles GPT prompt generation 
        Takes in parameters from config yaml format.
    """
    def __init__(self, client) -> None:
        super().__init__()
        self.client = client

    # Pre-generated prompt for testing and saving money
    def dummy_generate(self, *args) -> any:
        text = "{\"title\": \"Noah's Ark\", \"scenes\": [{\"sentence\": \"In a world drowned in sin, a divine voice echoed.\", \"prompt\": \"3d dramatic fantasy of a divine voice echoing in a sinful world\"}, {\"sentence\": \"Noah, a righteous man, was chosen for a divine mission.\", \"prompt\": \"Renaissance art of Noah receiving a divine mission\"}, {\"sentence\": \"Noah, a righteous man, was chosen for a divine mission.\", \"prompt\": \"Renaissance art of Noah receiving a divine mission\"}, {\"sentence\": \"Noah, a righteous man, was chosen for a divine mission.\", \"prompt\": \"Renaissance art of Noah receiving a divine mission\"}]}"
        return json.loads(text)
    
    def get_templates(self) -> tuple[str, str]:
        user = "Generate <story here> in 15 sentences of text. Sentences should be 10 words on average, aimed at Tiktok viewers with low attention spans that need every sentence to be stimulating. The first sentence, in particular, should be a general question embedded with mystery about the story. Make it super captivating, and include language that is dramatic, and digestible to the average teenager. Always speak from the third person, and do not use any dialogue between characters. Instead, say <person> says to <person2> <dialogue>. Then, for each sentence, generate a lively, super colorful Dall-E prompt in one of four styles (3d dramatic fantasy, rennaissance art, hyper-realistic, oil painting) that we can use as descriptive imagery. This should be really entertaining to an audience and use very bright colors. Imagery should, seem religious and spiritual. The Dall-E prompt should be detailed and at least 20 words. Do not repeat the same image prompts. The output type is json in this format: {\"title\": <title>, \"scenes\": [{\"sentence\": <sentence>, \"prompt\": <prompt>}, {\"sentence\": <sentence>, \"prompt\": <prompt>}, etc.]}. The response should be in a single line. Do not use any escape characters."
        system = "You are an epic fantasy story writer and content creator optimized to create engaging short-form videos for social media platforms like Tiktok and Instagram Reels. Your writing is creative and descriptive"
        return user, system

    def save_yaml(self, filename: str, config: any, content: any) -> any:
        """Saves JSON or python object as YAML into the filepath specified in config

        Args:
            filename (str): Filename
            config (any): Initial config file, where a file path must be defined under global_settings
            content (any): JSON or python object
        
        Returns:
            content (any): Python object representation of the saved config

        Raises:
            e: This value is missing from configuration
        """
        try:
            global_config = config["global_settings"]
            script_directory = global_config["output_path"]
        except KeyError as e:
            self.logger.error("Config file is missing settings for GPT")
            raise e
        
        # Add augmentations to script
        add_transformations(content)
        
        save_path = os.path.join(script_directory, f"{filename}")

        cl = ConfigLoader()
        cl.write(save_path, content)
        
        self.logger.info("Saving GPT Output: " + save_path)
        return content

    # Validates config and performs request and validates request
    def generate(self, config: any) -> str:
        """Generates a GPT response via OpenAI API

        Args:
            config (any): What the ConfigLoader reads

        Raises:
            e: If the required configuration cannot be found

        Returns:
            str: _description_
        """
        self.logger.info("GPT generating...")
        prev = time.time()

        try:
            gpt_config = config["GPT"]
        except KeyError as e:
            self.logger.error("Config file does not contain key script_generation")
            raise e
        
        try:
            messages = [{"role": "system", "content": gpt_config["system"]},
                    {"role": "user", "content": gpt_config["user"]},
                    ]
            
            response = self.client.chat.completions.create(
                model=gpt_config["gpt_model"],
                messages=messages,
                temperature=gpt_config["temperature"]
            )
        except KeyError as e:
            self.logger.error("Config settings not found for script_generation")
            raise e
        
        self.logger.info(f"GPT generation complete: Time taken={time.time() - prev}. ID={response.id}. Model={response.model}.")
        # Ignore exception in case GPT generates the format wrong
        try:
            JSON_result = json.loads(response.choices[0].message.content)
            return JSON_result
        except Exception as e:
            self.logger.error("GPT script JSON format is invalid")
        
        return {}
        