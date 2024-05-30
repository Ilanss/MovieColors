# MovieColors
This project take a video files and generate an image with the average colors of each frame of the video. It can process multiple video in batches and generate the output format you want.

![alt text](https://github.com/Ilanss/MovieColors/blob/main/results/sample.png?raw=true)

## Features

- Process single video file or by batch by giving it a folder (there's a recursive option)
- Any video format should work, the following are accepted by default, other will need to be added manually in the code: mp4, avi, mov, mkv, flv, wmv
- Select multiple output format, you can even add any amount of custom format

## Usage
### Prerequisites
- FFmpeg
- Python 3.10 or higher

### Installation
Use the requirements.txt to install libraries. It is recommended to use Python venv or something similar to get a controled environnement.

Run MovieColors.py and follow the instructions.
The resulting images will be stored in the "results" directory

**Warning:** Processing whole movies in full quality will take some minutes to be processed. Be aware before batching whole folder (especially recusively). However it will generate all format asked at soon as it has proceed a movie so you are not losing the work if you stop it.