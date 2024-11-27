from enum import Enum

class PalmOrientation(Enum):
    PALM_FORWARD = "Palm Forward: The palm faces directly away from the body, forward along the +Z axis."
    PALM_BACKWARD = "Palm Backward: The palm faces directly toward the body, backward along the -Z axis."
    PALM_UP = "Palm Up: The palm faces upward along the +Y axis (like holding a tray)."
    PALM_DOWN = "Palm Down: The palm faces downward along the -Y axis (like pushing down on a surface)."
    PALM_LEFT = "Palm Left: The palm faces to the left along the -X axis (relative to the body or viewer)."
    PALM_RIGHT = "Palm Right: The palm faces to the right along the +X axis (relative to the body or viewer)."


class BoneInfoExtractor:
    def __init__(self):
        pass

    def extract_bone_orientation(self, node, scene, frame_rate=1):
        """Extracts the 3D orientation (rotation) of a bone over time."""
        # Get the animation stack
        anim_stack = scene.GetCurrentAnimationStack()
        anim_layer = anim_stack.GetMember(0)

        # Get the curve nodes for rotation channels
        rotation_curves = {
            'X': node.LclRotation.GetCurve(anim_layer, 'X'),
            'Y': node.LclRotation.GetCurve(anim_layer, 'Y'),
            'Z': node.LclRotation.GetCurve(anim_layer, 'Z')
        }

        # Extract keyframe data
        orientations = []
        time_stamps = []
        for key_index in range(rotation_curves['X'].KeyGetCount()):
            time = rotation_curves['X'].KeyGetTime(key_index)
            # Use supplied frame rate to convert time to frames, default to 1 frame per second
            time_stamps.append(time.GetSecondDouble() * frame_rate)

            rotation = (
                rotation_curves['X'].KeyGetValue(key_index),
                rotation_curves['Y'].KeyGetValue(key_index),
                rotation_curves['Z'].KeyGetValue(key_index)
            )
            orientations.append(rotation)

        return time_stamps, orientations

    def calculate_palm_orientation(self, orientations):
        """Calculates the orientation of the palm based on the bone orientations."""
        # Extract the last orientation (assuming the last keyframe)
        last_orientation = orientations[-1]

        # Extract the individual rotation values
        rotation_x, rotation_y, rotation_z = last_orientation

        print(rotation_x, rotation_y, rotation_z)

        # Adjust thresholds to match observed data range
        if rotation_x > 5:
            return PalmOrientation.PALM_LEFT
        elif rotation_x < -5:
            return PalmOrientation.PALM_RIGHT
        elif rotation_y > 5:
            return PalmOrientation.PALM_UP
        elif rotation_y < -5:
            return PalmOrientation.PALM_DOWN
        elif rotation_z > 5:
            return PalmOrientation.PALM_BACKWARD
        elif rotation_z < -5:
            return PalmOrientation.PALM_FORWARD
        else:
            # Values are close to neutral, orientation is unclear
            return None
