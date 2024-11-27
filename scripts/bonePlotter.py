import matplotlib.pyplot as plt
import numpy as np
import mplcursors

class BonePlotter:
    def __init__(self, file_name, scene):
        self.file_name = file_name
        self.scene = scene

    def plot_orientation(self, time_stamps, orientations : np.array, orientation_labels, bone_name, file_name, fbx_player=None):
        """Plots the 3D orientation of a bone over time with interactivity for orientation labels."""
    
        # Convert time_stamps to a NumPy array if it's a list
        time_stamps = np.array(time_stamps)

        plt.figure(figsize=(10, 6))
        x_line, = plt.plot(time_stamps, orientations[:, 0], label='Rotation X (degrees)')
        y_line, = plt.plot(time_stamps, orientations[:, 1], label='Rotation Y (degrees)')
        z_line, = plt.plot(time_stamps, orientations[:, 2], label='Rotation Z (degrees)')

        # Dynamic axis limits based on data range
        time_range = (time_stamps.min(), time_stamps.max())
        rotation_range = (orientations.min(), orientations.max())
        plt.xlim(time_range)  # Set x-axis limit based on timestamps
        plt.ylim(rotation_range)  # Set y-axis limit based on orientation values

        plt.gcf().canvas.manager.set_window_title(f"Orientation of {bone_name} - {file_name}")
        plt.title(f"3D Orientation of Bone: {bone_name} (File: {file_name})")
        plt.xlabel("Time (frames)")
        plt.ylabel("Rotation (degrees)")
        plt.legend()
        plt.grid()

        # Add cursor for interactivity
        cursor = mplcursors.cursor([x_line, y_line, z_line], hover=True)

        @cursor.connect("add")
        def on_add(sel):
            # Determine the index of the hovered point
            index = np.argmin(np.abs(time_stamps - sel.target[0]))
            line_label = sel.artist.get_label()  # Get the line label (X, Y, Z)

            # Determine which line (X, Y, or Z) is hovered
            if sel.artist == x_line:
                rotation_value = orientations[index, 0]  # X rotation
            elif sel.artist == y_line:
                rotation_value = orientations[index, 1]  # Y rotation
            elif sel.artist == z_line:
                rotation_value = orientations[index, 2]  # Z rotation
            else:
                rotation_value = None  # Shouldn't happen in this setup

            # Get the corresponding palm orientation label
            palm_orientation = orientation_labels[index]

            # Display orientation details in the hover annotation
            sel.annotation.set_text(
                f"{line_label}\nTime: {time_stamps[index]:.2f}s\n"
                f"Value: {rotation_value:.2f}°\n"
                f"Palm Orientation: {palm_orientation if palm_orientation else 'Unknown'}"
            )
            sel.annotation.get_bbox_patch().set(fc="white", alpha=0.8)

            if fbx_player:
                # Sync animation with the selected time
                self.sync_animation_with_graph(time_stamps[index], fbx_player)

        plt.show()

    def sync_animation_with_graph(self, timestamp, fbx_player):
        """Update the animation to the specified frame."""
        print(f"Setting animation to frame {timestamp}")

