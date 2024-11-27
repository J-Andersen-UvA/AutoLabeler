import fbx
from fbx import FbxManager, FbxImporter

class FBXReader:
    def __init__(self):
        pass

    def load_fbx_animation(self, file_path):
        """Loads the FBX file and returns the scene object."""
        manager = FbxManager.Create()
        importer = FbxImporter.Create(manager, "")

        if not importer.Initialize(file_path, -1):
            raise RuntimeError(f"Error initializing importer: {importer.GetStatus().GetErrorString()}")

        scene = fbx.FbxScene.Create(manager, "scene")
        importer.Import(scene)
        importer.Destroy()

        return manager, scene

    def find_bone_by_name(self, node, bone_name):
        """Recursively searches for a bone by name in the FBX node hierarchy."""
        if bone_name in node.GetName():  # Using the 'in' operator to check for substring
            return node

        for i in range(node.GetChildCount()):
            result = self.find_bone_by_name(node.GetChild(i), bone_name)
            if result:
                return result

        return None

    def print_all_bone_names(self, node):
        """Recursively prints all bone names in the FBX node hierarchy."""
        if node.GetSkeleton():
            print(node.GetName())

        for i in range(node.GetChildCount()):
            self.print_all_bone_names(node.GetChild(i))

    def get_frame_rate(self, scene):
        timeModes = {
            fbx.FbxTime.EMode.eDefaultMode: 1,
            fbx.FbxTime.EMode.eFrames120: 120,
            fbx.FbxTime.EMode.eFrames100: 100,
            fbx.FbxTime.EMode.eFrames60: 60,
            fbx.FbxTime.EMode.eFrames50: 50,
            fbx.FbxTime.EMode.eFrames48: 48,
            fbx.FbxTime.EMode.eFrames30: 30,
            fbx.FbxTime.EMode.eFrames30Drop: 30,
            fbx.FbxTime.EMode.eNTSCDropFrame: 30,
            fbx.FbxTime.EMode.eNTSCFullFrame: 30,
            fbx.FbxTime.EMode.ePAL: 25,
            fbx.FbxTime.EMode.eFrames24: 24,
            fbx.FbxTime.EMode.eFrames1000: 1000,
            fbx.FbxTime.EMode.eFilmFullFrame: 24,
            fbx.FbxTime.EMode.eCustom: 1
        }

        # get some global settings
        global_settings = scene.GetGlobalSettings()
        fileTimeMode = global_settings.GetTimeMode()
        return timeModes[fileTimeMode]

class FBXPlayer:
    def __init__(self):
        self.frame_rate = None
        pass

    def seek_to_frame(self, scene, frame_number):
        """Seek the animation to the specified frame."""
        print("Seeking to frame:", frame_number)
        anim_stack = scene.GetSrcObject(fbx.FbxCriteria.ObjectType(fbx.FbxAnimStack))
        if anim_stack:
            scene.SetCurrentAnimationStack(anim_stack)
            time = fbx.FbxTime()
            time.Set(frame_number)
            scene.GetRootNode().SetCurrentTime(time)
