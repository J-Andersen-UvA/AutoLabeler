import scripts.bonePlotter as bonePlotter
import scripts.fbxReader as fbxReader
import scripts.palmOrientationCalculator as palmOrientationCalculator
import numpy as np

def main(file_path, bone_name, file_name):
    fbxr = fbxReader.FBXReader()
    fbxp = fbxReader.FBXPlayer()
    orientationCalc = palmOrientationCalculator.BoneInfoExtractor()

    """Main function to load FBX, extract bone data, and plot orientation."""
    manager, scene = fbxr.load_fbx_animation(file_path)

    bp = bonePlotter.BonePlotter(file_name, scene)

    root_node = scene.GetRootNode()
    if not root_node:
        raise RuntimeError("The FBX file has no root node.")

    # print_all_bone_names(root_node)

    bone_node = fbxr.find_bone_by_name(root_node, bone_name)
    if not bone_node:
        raise ValueError(f"Bone '{bone_name}' not found in the FBX file.")

    frame_rate = fbxr.get_frame_rate(scene)
    fbxp.frame_rate = frame_rate
    time_stamps, orientations = orientationCalc.extract_bone_orientation(bone_node, scene, frame_rate)
    orientations = np.array(orientations)

    # Classify each orientation into an enum
    orientation_labels = [orientationCalc.calculate_palm_orientation([ori]) for ori in orientations]
    print(orientation_labels)

    bp.plot_orientation(time_stamps, orientations, orientation_labels, bone_name, file_name, fbxp)

    manager.Destroy()

if __name__ == "__main__":
    # Example usage
    file_path = "testAnims/IDEE.fbx"  # Replace with the path to your FBX file
    bone_name = "RightHand"  # Replace with the name of the bone you want to analyze
    # filename extract from filepath
    file_name = file_path.split('/')[-1].split('.')[0]
    main(file_path, bone_name, file_name)
