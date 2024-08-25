from elevenlabs import generate, save
import os
from src.utils.Prototype import Prototype

class TTS(Prototype):
    def __init__(self) -> None:
        super().__init__()

    def generate_audio(self, config: any, text: str, filename: str) -> str:
        """Generates TTS audio for a frame of a video and saves it

        Args:
            config (any): Python object storing TTS configuration
            text (str): Text to be converted to audio
            image_filename (str): Image filename

        Returns:
            filepath (str): Filepath of the saved audio file

        Raises:
            e: If setting cannot be found
        """
        try:
            global_config = config["global_settings"]
            TTS_config = config["TTS"]
            voice = TTS_config["voice"]
        except KeyError as e:
            self.logger.error("Configuration values missing in TTS config")
            raise e

        audio = generate(text=text, voice=voice)

        output_path = os.path.join(global_config["output_path"], f"{filename}.mp3")
        save(audio, output_path)
        return output_path