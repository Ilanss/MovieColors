def fileSettings():
    import tkinter as tk
    from tkinter import filedialog
    import questionary
    import os

    root = tk.Tk()
    root.withdraw() 
    
    video_path = filedialog.askopenfilename(
        title="Select a Video File",
        filetypes=[("Video Files", "*.mp4 *.avi *.mov *.mkv"), ("All Files", "*.*")]
    )

    file_stats = os.stat(video_path)

    while file_stats.st_size > 1000000:
        if questionary.confirm("Your file is bigger than 10mb, it may take a long time to process. Are you sure?").ask():
            break

        else:
            video_path = filedialog.askopenfilename(
                title="Select a Video File",
                filetypes=[("Video Files", "*.mp4 *.avi *.mov"), ("All Files", "*.*")]
            )

            file_stats = os.stat(video_path)


    #video_name = questionary.text("Enter file name: ").ask()
    image_name = questionary.text("Enter image name: ").ask()
    #video_path = "movies/" + video_name + ".mp4"

    #return {"video_name": video_name, "image_name": image_name, "video_path": video_path}
    return {"image_name": image_name, "video_path": video_path}

def userContinue():
    import questionary
    nextStep = questionary.select(
        "What do you want to do now?",
        choices=[
            questionary.Choice('Generate another format', value=1),
            questionary.Choice('Choose another video', value=2),
            questionary.Choice('Exit', value=3)
        ]
    ).ask()

    return nextStep

def imageFormat():
    import questionary

    image_format = questionary.select(
    "What image format do you want to generate?",
    choices=[
        'SD',
        'HD',
        '4K',
        'Custom'
    ]).ask()

    match image_format:
        case "SD":
            image_format_size = {"target_width": 960, "height": 720}

        case "HD":
            image_format_size = {"target_width": 1920, "height": 1080}

        case "4K":
            image_format_size = {"target_width": 3840, "height": 2160}

        case _:
            width = int(questionary.text("Enter width: ").ask())
            height = int(questionary.text("Enter height: ").ask())
            image_format_size = {"target_width": width, "height": height}

    return image_format_size

def readVideo(video_path):
    import cv2
    import multiprocessing as mp
    from tqdm import tqdm

    cap = cv2.VideoCapture(video_path)
    frame_colors = []

    print("")
    print("Reading video...")

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    pbar = tqdm(total=total_frames, desc="Reading frames")
    frame_skip=10
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if frame_count % frame_skip == 0:
            frame = cv2.resize(frame, (960, 540))
            frame_colors.append(frame)
            pass
        pbar.update(1)
        frame_count += 1

    pbar.close()
    cap.release()

    return frame_colors

# def average_color(frame_colors):
#     import numpy as np
#     from tqdm import tqdm

#     average_colors = [tuple(np.mean(frame, axis=(0, 1)).astype(int)) for frame in tqdm(frame_colors, desc="Processing frames")]

#     # average_colors = [tuple(np.mean(frame, axis=(0, 1)).astype(int)) for frame in frame_colors]

#     return average_colors

def average_color(frame_colors):
    from tqdm import tqdm
    import multiprocessing as mp

    with mp.Pool(mp.cpu_count()) as pool:
        average_colors = list(tqdm(pool.imap(compute_average_color, frame_colors), total=len(frame_colors), desc="Processing frames"))
    return average_colors

def compute_average_color(frame):
    import numpy as np

    return tuple(np.mean(frame, axis=(0, 1)).astype(int))
