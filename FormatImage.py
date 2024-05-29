from PIL import Image
import numpy as np

def generateFromFormat(colors, width, height, image_name):
    num_frames = len(colors)

    if isinstance(width, str):
        width = num_frames
        
    print("Bringing to target image format...")

    if num_frames < width:
        # Calculate how many times each frame needs to be repeated
        repeats = width // num_frames
        remainder = width % num_frames
        repeated_colors = []

        for i in range(num_frames):
            # Convert color array to tuple
            color = tuple(colors[i].tolist())
            repeated_colors.extend([color] * repeats)
            if i < remainder:
                repeated_colors.append(color)

    else:
        # Average multiple frames to fit into width
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

    #line_pixels = [tuple(pixel) for pixel in colors]

    # Define the width and height of the image
    #width = len(line_pixels)

    # Create a new image with the given width and height
    image = Image.new('RGB', (width, height))

    # Generate pixel data for the entire image by repeating the line
    pixels = repeated_colors * height

    image.putdata(pixels)
    image.save("results/" + image_name + "-" + str(width) + "x" + str(height) + ".png")

    print("Image with average frame colors saved as '" + image_name + ".png'")
