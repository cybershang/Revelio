import subprocess
from pathlib import Path

# ffmpeg -i input_video.mp4 -vf "fps=1" image_%d.png


def framming(fps: int, in_path: Path, output_pattern: Path) -> list:
    # multi thread/process
    command = [
        'ffmpeg', '-i', in_path, '-vf', f'fps={fps}', output_pattern
    ]
    subprocess.run(command)

    file_name_list = sorted(
        [f.name for f in output_pattern.parent.iterdir() if f.is_file()])
    file_list = [output_pattern.parent / Path(name) for name in file_name_list]
    return file_list
