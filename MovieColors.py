import FormatImage
import AppFunctions

def main():
    mode, cmdMode = AppFunctions.processMode()

    match mode:
        case '1':
            files = [AppFunctions.fileSettings(cmdMode)]
            
            while AppFunctions.otherFiles():
                files.append(AppFunctions.fileSettings(cmdMode))

        case _:
            files = AppFunctions.folderSetting(cmdMode)
            
    #file = AppFunctions.fileSettings()
    image_formats = AppFunctions.imageFormat()

    frames_colors = {}

    for file in files:
        frame_colors = AppFunctions.readVideoFF(file)
        frames_colors[file] = frame_colors

        for image_format in image_formats:
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
                image_formats = AppFunctions.imageFormat()
                for file, frame_colors in frames_colors.items():
                    for image_format in image_formats:
                        createImage(frame_colors, image_format, file)

            case 2:
                frames_colors = main()

            case 3:
                print("Goodbye!")
                break
