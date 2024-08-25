import typing
from src.utils.helpers import merge_defaults
from src.movie_production.scene import Scene
from moviepy.editor import (
    concatenate_videoclips,
    AudioFileClip,
    CompositeAudioClip
)
import json
import os

class MovieRequiresOneSceneError(Exception):
    pass

class Movie:
    """
    A Movie object, in its simplest form, is a succession
    of Scene objects put together with (optionally)
    audio and/or other decorations on top.
    """
    default_options: dict[str, typing.Any] = {
        "background_audio_file": None, # represents audio that will play during whole of movie
        "scenes": [], # Look at Scene.default_options for how to populate
    }

    def __init__(self, options):
        self.options = merge_defaults(options, self.default_options)

        # Ensure at least one scene
        if len(self.options["scenes"]) == 0:
            raise MovieRequiresOneSceneError
        
        # Combine all the scenes present
        video = self.combine_scenes()
        
        # Add background audio if present
        background_audio_file = self.options["background_audio_file"]
        if background_audio_file:
            video = self.apply_background_audio(video)
        
        self.video = video

    def combine_scenes(self):
        scenes = self.options["scenes"]
        
        # Construct list of videos from every scene
        scene_videos = []
        for scene_options in scenes:
            scene_object = Scene(scene_options)
            scene_video = scene_object.get_video()
            scene_videos.append(scene_video)
        
        if len(scene_videos) == 1:
            # Case when there is only one scene in this movie
            return scene_videos[0]
        
        # Case when there are multiple scenes in this movie
        return concatenate_videoclips(scene_videos, method="compose")
    
    def apply_background_audio(self, video):
        audio_file = self.options["background_audio_file"]
        music_clip = (
            AudioFileClip(audio_file)
            .subclip(0, video.duration)
            .volumex(0.28)
        )

        # Need to combine existing audio of video clip with background audio
        composite_audio = CompositeAudioClip([video.audio, music_clip])

        return video.set_audio(composite_audio)
    
    def log_options(self):
        """
        For logging what the input options to this class actually are
        """
        print(json.dumps(self.options, indent=4))

    def get_video(self):
        """
        Returns VideoClip containing this scene
        """
        return self.video
    
    def save_to_file(self, file_path):
        """
        Populates specified file the video representing this scene (i.e. self.video)
        """
        if os.path.isfile(file_path):
            raise FileExistsError
        
        # We can only use base filenames (without a '/')
        # with Movie.py
        current_working_directory = os.getcwd()
        file_directory = os.path.dirname(file_path)
        file_base_name = os.path.basename(file_path)
        
        os.chdir(file_directory)
        video = self.get_video()
        video.write_videofile(
            file_base_name,
            codec="libx264",
            audio_codec="aac",
            audio_bitrate="3000k",  # Tiktok recommends 1000
            threads=16,  # Set this to be 1 at first, then experiment with higher numbers
        )

        os.chdir(current_working_directory)

        return file_path
