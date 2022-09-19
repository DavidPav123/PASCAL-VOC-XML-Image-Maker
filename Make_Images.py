from os import listdir
from random import randint
from PIL import Image
from xml.dom.minidom import Document

if __name__ == "__main__":
    # Variable to control how many times each image must be used
    PICTURE_USAGE: int = 1
    # Width and height of background images
    IMAGE_WIDTH: int = 1024
    IMAGE_HEIGHT: int = 1024

    # Get a list of images to paste onto backgrounds
    unitPngs: list[str] = listdir("cut_images/")

    # Create dictionary to keep track of number of times pngs were used
    png_dictionary: dict = {}
    for pictures in unitPngs:
        png_dictionary[pictures] = 0

    # Variable to keep track of the number of images created
    loop: int = 0

    loop_tracker:bool = True
    while loop_tracker:
        # Loop for the number of backgrounds in the background folder to ensure even usage of backgrounds
        for i in listdir("backgrounds/"):

            # Open background image
            im = Image.open(f"backgrounds/{i}")

            # Create XML document
            root = Document()

            xml = root.createElement("annotation")
            root.appendChild(xml)

            # folder
            folder = root.createElement("folder")
            xml.appendChild(folder)
            folderText = root.createTextNode("images")
            folder.appendChild(folderText)

            # filename
            fileName = root.createElement("filename")
            xml.appendChild(fileName)
            fileNameText = root.createTextNode(f"Image{loop}.jpg")
            fileName.appendChild(fileNameText)

            # path
            path = root.createElement("path")
            xml.appendChild(path)
            pathText = root.createTextNode(f"images/Image{loop}.xml")
            path.appendChild(pathText)

            # source
            source = root.createElement("source")
            xml.appendChild(source)
            database = root.createElement("database")
            source.appendChild(database)
            databaseText = root.createTextNode("Unknown")
            database.appendChild(databaseText)

            # size
            size = root.createElement("size")
            xml.appendChild(size)
            width = root.createElement("width")
            size.appendChild(width)
            widthText = root.createTextNode(str(IMAGE_WIDTH))
            width.appendChild(widthText)
            height = root.createElement("height")
            size.appendChild(height)
            heightText = root.createTextNode(str(IMAGE_HEIGHT))
            height.appendChild(heightText)
            depth = root.createElement("depth")
            size.appendChild(depth)
            depthText = root.createTextNode("3")
            depth.appendChild(depthText)

            # segmented
            segmented = root.createElement("segmented")
            xml.appendChild(segmented)
            segmentedText = root.createTextNode("0")
            segmented.appendChild(segmentedText)

            for b in range(4):
                chosenUnit: int = randint(0, len(unitPngs) - 1)
                pngImg = Image.open(f"cut_images/{unitPngs[chosenUnit]}")
                png_dictionary[unitPngs[chosenUnit]] += 1

                if b == 0:
                    xCord = 0
                    yCord = 0
                elif b == 1:
                    xCord = IMAGE_WIDTH - pngImg.getbbox()[2]
                    yCord = 0
                elif b == 2:
                    xCord = 0
                    yCord = IMAGE_HEIGHT - pngImg.getbbox()[3]
                elif b == 3:
                    xCord = IMAGE_WIDTH - pngImg.getbbox()[2]
                    yCord = IMAGE_HEIGHT - pngImg.getbbox()[3]

                # Paste selected image onto background
                im.paste(pngImg, (xCord, yCord), pngImg)

                # add object to xml file
                object = root.createElement("object")
                xml.appendChild(object)

                # add name
                name = root.createElement("name")
                object.appendChild(name)
                unitName = unitPngs[chosenUnit]
                size = len(unitName)
                unitName = unitName[: size - 6]
                nameText = root.createTextNode(f"{unitName}")
                name.appendChild(nameText)

                # add pose
                pose = root.createElement("pose")
                object.appendChild(pose)
                poseText = root.createTextNode("Unspecified")
                pose.appendChild(poseText)

                # add truncated
                truncated = root.createElement("truncated")
                object.appendChild(truncated)
                truncatedText = root.createTextNode("0")
                truncated.appendChild(truncatedText)

                # add difficult
                difficult = root.createElement("difficult")
                object.appendChild(difficult)
                difficultText = root.createTextNode("0")
                difficult.appendChild(difficultText)

                # add bndbox around pasted image
                bndbox = root.createElement("bndbox")
                object.appendChild(bndbox)
                xmin = root.createElement("xmin")
                bndbox.appendChild(xmin)
                xminText = root.createTextNode(str(xCord))
                xmin.appendChild(xminText)
                ymin = root.createElement("ymin")
                bndbox.appendChild(ymin)
                yminText = root.createTextNode(str(yCord))
                ymin.appendChild(yminText)
                xmax = root.createElement("xmax")
                bndbox.appendChild(xmax)
                xmaxText = root.createTextNode(str(xCord + pngImg.getbbox()[2]))
                xmax.appendChild(xmaxText)
                ymax = root.createElement("ymax")
                bndbox.appendChild(ymax)
                ymaxText = root.createTextNode(str(yCord + pngImg.getbbox()[3]))
                ymax.appendChild(ymaxText)

            # Save completed image to image folder
            im.save(f"images/Image{loop}.jpg")

            # Fix formatting in XML file
            xml_str = root.toprettyxml(indent="\t")
            save_path_file = (
                f"images/Image{loop}.xml"  # Path where completed XML files are saved
            )
            # Save XML file with desegnated path
            with open(save_path_file, "w+") as f:
                f.write(xml_str)

            break_or_dont: bool = False
            # Check if each image has bene used the desired amount of times
            for ele in png_dictionary:
                if png_dictionary[ele] < PICTURE_USAGE:
                    print(ele, png_dictionary[ele])
                    break_or_dont = True
                    break

            # If each image has not been used the desired amount of times then continue on to the next loop
            if break_or_dont:
                loop += 1
                continue

            # Break out of the loop if all pictures have been used declared amount of times
            print("Done")
            loop_tracker = False
            
        
