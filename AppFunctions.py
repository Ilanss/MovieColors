def fileSettings():
    import tkinter as tk
    from tkinter import filedialog
    # import questionary
    # import os

    root = tk.Tk()
    root.withdraw() 
    
    video_path = filedialog.askopenfilename(
        title="Select a Video File",
        filetypes=[("Video Files", "*.mp4 *.avi *.mov *.mkv"), ("All Files", "*.*")]
    )

    # if video_path == '':
    #     video_path = 'movies/your_videov.mp4'
    # file_stats = os.stat(video_path)

    # while file_stats.st_size > 1000000:
    #     if questionary.confirm("Your file is bigger than 10mb, it may take a long time to process. Are you sure?").ask():
    #         break

    #     else:
    #         video_path = filedialog.askopenfilename(
    #             title="Select a Video File",
    #             filetypes=[("Video Files", "*.mp4 *.avi *.mov"), ("All Files", "*.*")]
    #         )

    #         file_stats = os.stat(video_path)

    # image_name = questionary.text("Enter image name: ").ask()

    #return {"video_name": video_name, "image_name": image_name, "video_path": video_path}
    return video_path

def otherFiles():
    import questionary

    otherFiles = questionary.confirm("Do you want to add another file?").ask()

    return otherFiles

def folderSetting():
    import tkinter as tk
    from tkinter import filedialog
    import glob
    import questionary
    import os

    root = tk.Tk()
    root.withdraw() 
    
    directory_path = filedialog.askdirectory(
        title="Select a video directory"
    )

    video_paths = []
    
    if questionary.confirm("Do you want to search the folder recursively?").ask():
        video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv']
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                # Check if the file has a video extension
                if any(file.endswith(ext) for ext in video_extensions):
                    video_paths.append(os.path.join(root, file))

    else:
        video_extensions = ('*.mp4', '*.avi', '*.mov', '*.mkv', '*.flv', '*.wmv')    
        for ext in video_extensions:
            video_paths.extend(glob.glob(os.path.join(directory_path, ext)))

       
    return video_paths

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

def processMode():
    import questionary
    from questionary.prompts.common import Choice

    mode = questionary.select(
        "In which mode do you want to run?",
        choices=[
            Choice(title="single file", value="1"),
            Choice(title="batch", value="2"),
        ]
    ).ask()

    return mode

def engineChoice():
    import questionary
    from questionary.prompts.common import Choice

    choice = questionary.select(
        "What engine do you wish to run?",
        choices=[
            Choice(title="ffmpeg", value="1"),
            Choice(title="OpenCV", value="2"),
            Choice(title="merge", value="3"),
        ]
    )

    return choice

def imageFormat():
    import questionary
    from questionary.prompts.common import Choice
    
    image_formats = questionary.checkbox(
    "What image format do you want to generate?",
    choices=[
        Choice(title="SD", value="1"),
        Choice(title="HD", value="2"),
        Choice(title="4K", value="3"),
        Choice(title="Full", value="4"),
        Choice(title="Custom", value="5"),
    ]).ask()

    image_format_size = []

    for image_format in image_formats:
        match image_format:
            case '1':
                image_format_size.append({"target_width": 960, "height": 720})

            case '2':
                image_format_size.append({"target_width": 1920, "height": 1080})

            case '3':
                image_format_size.append({"target_width": 3840, "height": 2160})

            case '4':
                image_format_size.append({"target_width": 'full', "height": 720})

            case _:
                width = int(questionary.text("Enter width: ").ask())
                height = int(questionary.text("Enter height: ").ask())
                image_format_size.append({"target_width": width, "height": height})

                while questionary.confirm("Do you want to create another custom format?").ask():
                    width = int(questionary.text("Enter width: ").ask())
                    height = int(questionary.text("Enter height: ").ask())
                    image_format_size.append({"target_width": width, "height": height})


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
            frame = cv2.resize(frame, (1,1))
            frame_colors.append(frame)
            pass
        pbar.update(1)
        frame_count += 1

    pbar.close()
    cap.release()

    return frame_colors

def readVideoFF(video_path):
    import ffmpeg
    import numpy as np

    frame_colors = []

    print("")
    print("Reading video...")

    frame_skip=10

    process = (
        ffmpeg
        .input(video_path)
        #.filter('select', f'not(mod(n\,{frame_skip}))')
        .output('pipe:', format='rawvideo', pix_fmt='rgb24', s='1x1')
        .run_async(pipe_stdout=True)
    )

    while True:
        in_bytes = process.stdout.read(3)  # Read 3 bytes (1x1 RGB frame)
        if not in_bytes:
            break
        color = np.frombuffer(in_bytes, np.uint8)
        frame_colors.append(color.tolist())

    process.wait()

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
