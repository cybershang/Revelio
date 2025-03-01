import json
from pathlib import Path
import requests


def download_data():
    pass


def build_gt():
    pass


def input_data(video_path) -> dict:
    """Send video to assessment API"""
    with open(video_path, "rb") as video:
        try:
            response = requests.post(
                "http://localhost:8000/api/assess",
                headers={"Content-Type": "multipart/form-data"},
                files={"file": video},
            )

            if response.status_code == 200:
                return response.json()
        except Exception as e:
            return e


def evaluating():
    with open("ground_truth.json", "r") as f:
        gt = json.load(f)

    dataset_dir = Path("./dataset")
    for video in dataset_dir.iterdir():
        result = input_data(video)
        # fn=0 means, video being checked
        gt[video.stem]["fn"] = 0

        if gt[video.stem] == result["is_violence"]:
            # tn=0 means non violence
            if not gt[video.stem]:
                gt[video.stem]["tn"] = 1
            else:
                gt[video.stem]["tp"] = 1
        else:
            gt[video.stem]["fp"] = 1


def main():
    download_data()
    build_gt()
    evaluating()


if __name__ == "__main__":
    main()
