import FormatImage
import AppFunctions

def main():
    mode = AppFunctions.processMode()

    match mode:
        case '1':
            files = [AppFunctions.fileSettings()]

        case _:
            files = AppFunctions.folderSetting()
            
    #file = AppFunctions.fileSettings()
    image_format = AppFunctions.imageFormat()

    frames_colors = {}

    for file in files:
        frame_colors = AppFunctions.readVideoFF(file)
        frames_colors[file] = frame_colors
        createImage(frame_colors, image_format, file)

    return frames_colors
    #return frames_colors, files

def handleFile():
    file = AppFunctions.fileSettings()
    frame_colors = AppFunctions.readVideoFF(file)
    #average_colors = AppFunctions.average_color(frame_colors)

    return frame_colors
    
def createImage(average_colors, image_format, file):
    import os

    # Split the file name and extension
    file_name, file_extension = os.path.splitext(os.path.basename(file))
    FormatImage.generateFromFormat(average_colors, image_format["target_width"], image_format["height"], file_name)

    return True

if __name__ == "__main__":
    frames_colors = main()
    while True:
        nextStep = AppFunctions.userContinue()
        match nextStep:
            case 1:
                image_format = AppFunctions.imageFormat()
                for file, average_colors in frames_colors.items():
                    createImage(average_colors, image_format, file)

            case 2:
                frames_colors = main()

            case 3:
                print("Goodbye!")
                break
