import os
import csv
import datetime
import subprocess
from math import ceil

base_input_folder = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
print(base_input_folder)


input_csv = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'input.csv'))
if not os.path.exists(input_csv):
    raise SystemExit('Input file not provided: ' + input_csv)

resolution_map = {
    '2720x1530': '2704x1520',
}
allowed_resolutions = [
    '3840x2160',
    '1920x1080',
] + list(resolution_map.values())

with open(input_csv, 'r') as file:
    lines = list(csv.reader(file))
header, *lines = lines
counter = 0
total = len(lines)
for line in lines:
    counter += 1
    input_dir, input_file_name, start, end = map(str.strip, line)

    input_full_path = os.path.join(base_input_folder, input_dir, input_file_name)
    if not os.path.exists(input_full_path):
        print(f'Error: file does not exist: {input_full_path}')
        continue

    if start:
        time_start = datetime.datetime.utcfromtimestamp(int(start)).strftime('%H:%M:%S')
    else:
        time_start = '00:00:00'

    # Use duration instead of end if end is not provided
    if end:
        time_end = datetime.datetime.utcfromtimestamp(int(end)).strftime('%H:%M:%S')
    else:
        # Calculate duration from the file
        duration_command = f"ffprobe -v error -show_entries format=duration -of csv=p=0 '{input_full_path}'"
        duration = subprocess.getoutput(duration_command).strip()
        time_end = datetime.datetime.utcfromtimestamp(ceil(float(duration))).strftime('%H:%M:%S')

    output_dir = os.path.realpath(os.path.join(os.path.dirname(__file__), '..' ,'output', input_dir))
    os.makedirs(output_dir, exist_ok=True)

    output_file_name = input_file_name.replace('.', f' - {time_start} - {time_end}.').replace(':', '-')
    output_path = os.path.join(output_dir, output_file_name)

    if os.path.exists(output_path):
        print(f'Warning: file already exists, skip: {output_path}')
        continue

    input_resolution = subprocess.getoutput(
        f"ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=s=x:p=0 '{input_full_path}'"
    ).strip()

    output_resolution = resolution_map.get(input_resolution, input_resolution)

    if output_resolution not in allowed_resolutions:
        print(f'Error: resolution not allowed: {output_resolution} - {input_full_path}')
        continue

    if input_resolution in resolution_map:
        command = (
            f"ffmpeg -i '{input_full_path}' -ss {time_start} -to {time_end} -c h264 -vf scale={output_resolution} "
            f"-loglevel warning -crf 18 -c:a copy '{output_path}'"
        )
    else:
        command = (
            f"ffmpeg -i '{input_full_path}' -ss {time_start} -to {time_end} -c copy -loglevel warning '{output_path}'"
        )

    print(f'{counter}/{total}: {input_resolution} -> {output_resolution} - {input_full_path}')
    print(command)
    # subprocess.run(command, shell=True)