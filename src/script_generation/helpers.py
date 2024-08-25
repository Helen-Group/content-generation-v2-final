import random

def generate_transformation() -> str:
    TRANSFORMATIONS = [
        "pan_left_to_right",
        "pan_right_to_left", 
        "zoom_in", 
        "zoom_out"
    ]

    return TRANSFORMATIONS[random.randint(0, len(TRANSFORMATIONS) - 1)]

def add_transformations(config: any) -> any:
    for frame in config["scenes"]:
        frame["transformation_type"] = generate_transformation()