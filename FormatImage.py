from PIL import Image
import numpy as np

def generateFromFormat(colors, width, height, image_name):
    num_frames = len(colors)

    print("Bringing to target image format...")

    if num_frames < width:
        # Calculate how many times each frame needs to be repeated
        repeats = width // num_frames
        remainder = width % num_frames
        repeated_colors = []
        for i in range(num_frames):
            repeated_colors.extend([colors[i]] * repeats)
            if i < remainder:
                repeated_colors.append(colors[i])
    else:
        # Average multiple frames to fit into 1920 width
        scale_factor = num_frames / width
        averaged_colors = []
        for i in range(width):
            start_idx = int(i * scale_factor)
            end_idx = int((i + 1) * scale_factor)
            if end_idx > num_frames:
                end_idx = num_frames
            segment = colors[start_idx:end_idx]
            averaged_color = tuple(np.mean(segment, axis=0).astype(int))
            averaged_colors.append(averaged_color)
        repeated_colors = averaged_colors

    # Step 4: Create the Image with Vertical Lines

    image = Image.new("RGB", (width, height))
    pixels = []

    print("Generating lines...")

    for _ in range(height):
        for color in repeated_colors:
            pixels.extend([color])

    print("Saving image...")

    image.putdata(pixels)
    image.save("results/" + image_name + "-" + str(width) + "x" + str(height) + ".png")

    print("Image with average frame colors saved as '" + image_name + ".png'")
