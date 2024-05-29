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

    for file in files:
        frame_colors = AppFunctions.readVideoFF(file)
        createImage(frame_colors, image_format, file)

    return frame_colors, file

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
    average_colors, file = main()
    while True:
        nextStep = AppFunctions.userContinue()
        match nextStep:
            case 1:
                image_format = AppFunctions.imageFormat()
                createImage(average_colors, image_format, file)

            case 2:
                average_colors, file = main()

            case 3:
                print("Goodbye!")
                break
