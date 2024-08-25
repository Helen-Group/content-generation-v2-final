from src.utils.Prototype import Prototype
import asyncio
from threading import Thread
import copy
import os 

class AsyncClient(Prototype):
    def __init__(self, base_config: any, output_config: any, **kwargs) -> None:
        """Initializes with all the relevant submodules

        Args:
            base_config (any): Original configuration file
            output_config (any): Output configuration file
        """
        super().__init__()

        self.RATE_LIMIT = 4
        self.BASE_CONFIG = base_config
        self.OUTPUT_CONFIG = output_config

        # Load supported modules
        self.dalle = None
        self.tts = None

        try:
            self.dalle = kwargs["DALLE"]
        except KeyError as e:
            self.logger.info("Async: DALLE module is missing, skipping module!")

        try:
            self.tts = kwargs["TTS"]
        except KeyError as e:
            self.logger.info("Async: TTS module is missing, skipping module!")


    def _run_DALLE(self, return_obj) -> bool:
        """Wrapper for thread which generates all DALLE images for a video

        Returns:
            bool: Success message
        """
        async def wrapper(dalle_prompt: str, frame_num: int) -> str:
            """Wrapper to asynchronously generate DALLE images

            Args:
                dalle_prompt (str): DALLE text prompt
                frame_num (int): Frame number in video

            Returns:
                str: Image URL
            """
            # Maximize parallelism for rate limit
            await asyncio.sleep(frame_num // self.RATE_LIMIT * 60)
            try:
                url = await self.dalle.generate(self.BASE_CONFIG, dalle_prompt, None)
                # Download image from URL
                saved_filepath = self.dalle.download(self.BASE_CONFIG, url, frame_num)
            except:
                # Default image if somehow generation fails
                saved_filepath = self.dalle.download(self.BASE_CONFIG, "https://www.freeiconspng.com/thumbs/x-png/x-png-15.png", frame_num)
            return saved_filepath

        if not self.dalle:
            return False
        
        # Funny trick because async works weirdly with threads
        # Basically the main loop only applies to the parent thread, so I need to
        # Create a new loop for this thread
        DALLE_task_pool = []
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        # Need to extract config, prompt, size to generate image
        # Need to extract config, url, frame_num to save image
        for frame_num, scene in enumerate(self.OUTPUT_CONFIG["scenes"]):
            dalle_prompt = scene["prompt"]
            task = loop.create_task(wrapper(dalle_prompt, frame_num+1))
            DALLE_task_pool.append(task)

        loop.run_until_complete(asyncio.wait(DALLE_task_pool))
        loop.close()

        # Collect results
        ret = [task.result() for task in DALLE_task_pool]
        return_obj["return"] = ret

        return True

    
    def _run_TTS(self, return_obj) -> bool:
        """Generates all the audio needed for a video

        Returns:
            bool: Success
        """
        filepaths = []
        if not self.tts:
            return False
        
        for i, scene in enumerate(self.OUTPUT_CONFIG["scenes"]):
            text_prompt = scene["sentence"]
            filename = f"{self.BASE_CONFIG['TTS']['output_prefix']}-{i+1}"
            saved_filepath = self.tts.generate_audio(self.BASE_CONFIG, text_prompt, filename)
            filepaths.append(saved_filepath)

        return_obj["return"] = filepaths
        return True


    def run(self) -> any:
        """A Simple thread Manager to run processes in parallel

        Returns:
            any: Python object containing results of submodules
        """
        dalle_result = {"return": None}
        tts_result = {"return": None}

        threads = []
        if self.dalle:
            threads.append(Thread(target=self._run_DALLE, args=[dalle_result]))
        if self.tts:
           threads.append(Thread(target=self._run_TTS, args=[tts_result]))

        # DO NOT TOUCH
        #---------------
        for t in threads:
            t.start()

        for t in threads:
            t.join()
        #---------------
        output = []
        for i, frame in enumerate(self.OUTPUT_CONFIG["scenes"]):
            new_frame = copy.deepcopy(frame)
            new_frame["image_file"] = dalle_result["return"][i]
            new_frame["audio_file"] = tts_result["return"][i]
            output.append(new_frame)

        return output
