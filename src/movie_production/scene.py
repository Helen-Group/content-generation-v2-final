from src.utils.helpers import merge_defaults
import textwrap
import json
from moviepy.editor import (
    AudioFileClip,
    TextClip,
    CompositeVideoClip,
    ImageClip,
)
import os

class RequiredFieldError(Exception):
    pass

class Scene:
    """
    A Scene represents one frame/slide of a video;
    it always has a visual (image file) associated
    with it that may also have animations, audio,
    and overlayed text
    """
    default_options = {
        "image_file" : None, # required
        "audio_file" : None, # recommended
        "text" : None, # recommended
        "animation_type" : "no_transform", # recommended
        "video_width":1024,
        "video_height":1792,
        "audio_padding" : 0.15,
        "text_options" : {
            "font": "Tahoma-Bold",
            "font_size": 60,
            "text_box_width": 23,
            "stroke_width": 3,
            "color" : "white",
        }
    }

    class Animation:
        # Animation_types
        ZOOM_IN = "zoom_in"
        ZOOM_OUT = "zoom_out"
        PAN_LEFT_TO_RIGHT = "pan_left_to_right"
        PAN_RIGHT_TO_LEFT = "pan_right_to_left"
        NO_TRANSFORM = "no_transform"

    def __init__(self, options):
        # Use all the specified fields provided in the constructor,
        # then populate rest of the fields with fields from the
        # default options paramater
        self.options = merge_defaults(options, self.default_options)
        image_file = options["image_file"]

        if not image_file:
            raise RequiredFieldError("Need to include image_file argument")
        
        # Load raw video/image
        video = self.load_image_clip()

        # Add audio if specified
        audio_file = options["audio_file"]
        if audio_file:
            video = self.apply_audio(video)

        # Add animations and resizing relevant
        # to this video
        # This should be done before text is added
        video = self.apply_transformation(video)
        
        # Add text overlay
        text = self.options["text"]
        if text:
            video = self.apply_text_overlay(video)

        # Final video
        self.video = video
        

    def load_image_clip(self):
        file_path = self.options["image_file"]
        image_clip = ImageClip(file_path).set_duration(1).set_fps(30)
        return image_clip
    
    def apply_audio(self, base_video):
        file_path = self.options["audio_file"]
        audio_padding = self.options["audio_padding"]

        audio_clip = AudioFileClip(file_path)

        # Duration of this final video is whatever is:
        # max(duration of audio with padding, duration of base_video)
        clip_duration = max(audio_clip.duration + 2 * audio_padding, base_video.duration)
        video_clip = base_video.set_duration(clip_duration).set_fps(30)

        # Ensure audio clip starts 'padding' seconds in
        audio_clip = audio_clip.set_start(audio_padding)


        # NOTE: NEED TO ADD CompositeVideoClip if we are acommodating
        # video files on top of image files!
        return CompositeVideoClip([video_clip]).set_audio(audio_clip)

    def apply_text_overlay(self, base_video):
        text = self.options["text"]
        text_options = self.options["text_options"]
        wrapped_text = (
            " " + " \n ".join(textwrap.wrap(text=text, width=text_options["text_box_width"])) + " "
        )
        text_clip = TextClip(
            wrapped_text,
            fontsize=text_options["font_size"],
            color=text_options["color"],
            method="label",
            font=text_options["font"],
            stroke_color="black",
            stroke_width=text_options["stroke_width"],
        ).set_duration(base_video.duration)

         # Dynamically determine the position of this clip relative to its containing clip
        base_clip_height = self.options["video_height"]
        text_overlay_clip = text_clip.set_position(
            ("center", base_clip_height * 0.6),
        )

        combined_video_with_text = CompositeVideoClip([base_video, text_overlay_clip]).set_audio(base_video.audio)

        return combined_video_with_text
    
    def apply_transformation(self, input_video):
        """
        Manages animations ALONG WITH resizing to fit the current dimensions
        """
        video_height = self.options["video_height"]
        video_width = self.options["video_width"]
        animation_type = self.options["animation_type"]

        resized_video = input_video.resize(height=video_height)

        if animation_type in [Scene.Animation.PAN_LEFT_TO_RIGHT, Scene.Animation.PAN_RIGHT_TO_LEFT]:
            # Calculate how fast our video's cross-section has to move along the video
            resized_image_width = resized_video.size[0]
            
            # For moving from left to right
            starting_position = 0
            ending_position = -(resized_image_width - video_width)

            # Reverse positions if moving from right to left
            if (animation_type == Scene.Animation.PAN_RIGHT_TO_LEFT):
                ending_position = 0
                starting_position = -(resized_image_width - video_width)                

            pixels_per_second = (
                ending_position - starting_position  # 0 is the start
            ) / resized_video.duration

            resized_video = resized_video.set_position(
                lambda t: (starting_position + t * pixels_per_second, "center")
            )
            resized_video.fps = 30
            transformed_clip = CompositeVideoClip(
                [resized_video], size=(video_width, video_height)
            )
        elif animation_type in [Scene.Animation.ZOOM_IN, Scene.Animation.ZOOM_OUT]:
            # For ZOOMING IN
            starting_magnification_factor = 1.0
            terminal_magnification_factor = 1.5

            if (animation_type == Scene.Animation.ZOOM_OUT):
                # Reverse terminal and starting magnification factors for
                # ZOOMING OUT
                starting_magnification_factor = 1.5
                terminal_magnification_factor = 1.0

            # How fast image zooms in
            magnifying_rate = (
                terminal_magnification_factor - starting_magnification_factor
            ) / resized_video.duration

            def magnification_factor_by_time(t):
                return t * magnifying_rate + starting_magnification_factor

            resized_video = resized_video.resize(
                magnification_factor_by_time
            ).set_position("center", "center")
            resized_video.fps = 30
            transformed_clip = CompositeVideoClip(
                [resized_video], size=(video_width, video_height)
            )
        else:
            resized_video = resized_video.set_position(("center", "center"))
            transformed_clip =  CompositeVideoClip(
                    [resized_video], size=(video_width, video_height)
                )
        
        return transformed_clip
    
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
    
    def save_to_file(self, filename):
        """
        Populates specified file the video representing this scene (i.e. self.video)
        """
        if os.path.isfile(filename):
            raise FileExistsError

        video = self.get_video()
        video.write_videofile(
            filename,
            codec="libx264",
            audio_codec="aac",
            audio_bitrate="3000k",  # Tiktok recommends 1000
            threads=16,  # Set this to be 1 at first, then experiment with higher numbers
        )


