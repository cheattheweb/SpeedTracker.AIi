import subprocess

def calculate_frame_time(video_path):
    # Run ffprobe to get the frames per second (FPS)
    ffprobe_cmd = [
        'ffprobe',
        '-v', 'error',
        '-select_streams', 'v:0',
        '-show_entries', 'stream=avg_frame_rate',
        '-of', 'default=noprint_wrappers=1:nokey=1',
        video_path
    ]

    fps_str = subprocess.check_output(ffprobe_cmd, universal_newlines=True).strip()
    numerator, denominator = map(int, fps_str.split('/'))
    fps = numerator / denominator

    # Calculate time per frame
    time_per_frame = 1 / fps

    return time_per_frame


