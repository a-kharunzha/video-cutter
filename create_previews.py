import os
import subprocess
from concurrent.futures import ThreadPoolExecutor

base_input_folder = os.path.realpath('/media/rolland/other/Dronie/2023-11-26 Cascais')

# Create the preview folder if it doesn't exist
preview_folder = os.path.join(base_input_folder, 'preview')
if not os.path.exists(preview_folder):
    os.makedirs(preview_folder)

# Get a list of all video files in the base folder
video_files = [f for f in os.listdir(base_input_folder) if f.lower().endswith(('.mp4', '.avi', '.mkv', '.mov'))]

def process_video(video_file):
    video_path = os.path.join(base_input_folder, video_file)
    preview_path = os.path.join(preview_folder, video_file)

    # Check if preview video already exists
    if os.path.exists(preview_path):
        print(f"Preview for {video_file} already exists. Skipping.")
        return

    # Create ffmpeg command to resize the video
    ffmpeg_command = (
        f"ffmpeg -hide_banner -loglevel panic -i '{video_path}' -vf scale=640:-1 -c:a copy '{preview_path}'"
    )

    # Print the command and execute it
    print(f"Creating preview for {video_file}:")
    print(ffmpeg_command)
    subprocess.run(ffmpeg_command, shell=True)

# Set the maximum number of threads based on your system capabilities
max_threads = 4  # Adjust as needed

with ThreadPoolExecutor(max_threads) as executor:
    executor.map(process_video, video_files)

print("Processing complete.")