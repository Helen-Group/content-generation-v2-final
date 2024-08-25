from movie import Movie
from scene import Scene

scene_options_a = {
    "image_file" : "image.png", # required
    "audio_file" : "audio.mp3", # recommended
    "text" : "No transformation at all, whatsoever, no KIZZY", # recommended
    "animation_type" : Scene.Animation.NO_TRANSFORM,
}

scene_options_b = {
    "image_file" : "image.png", # required
    "audio_file" : "audio.mp3", # recommended
    "text" : "Zoom In", # recommended
    "animation_type" : Scene.Animation.ZOOM_IN,
}

scene_options_c = {
    "image_file" : "image.png", # required
    "audio_file" : "audio.mp3", # recommended
    "text" : "Zoom Out", # recommended
    "animation_type" : Scene.Animation.ZOOM_OUT,
}

scene_options_d = {
    "image_file" : "image.png", # required
    "audio_file" : "audio.mp3", # recommended
    "text" : "Left to Right", # recommended
    "animation_type" : Scene.Animation.PAN_LEFT_TO_RIGHT,
}

scene_options_e = {
    "image_file" : "image.png", # required
    "audio_file" : "audio.mp3", # recommended
    "text" : "Right to Left", # recommended
    "animation_type" : Scene.Animation.PAN_RIGHT_TO_LEFT,
}

movie_options_a = {
    "background_audio_file" : None,
    "scenes":[
        scene_options_a,
        scene_options_b,
        scene_options_c,
        scene_options_d,
        scene_options_e
    ]
}

Scene(scene_options_a).save_to_file("scene_a.mp4")
Scene(scene_options_b).save_to_file("scene_b.mp4")
Scene(scene_options_c).save_to_file("scene_c.mp4")
Scene(scene_options_d).save_to_file("scene_d.mp4")
Scene(scene_options_e).save_to_file("scene_e.mp4")

Movie(movie_options_a).save_to_file("video_a.mp4")
