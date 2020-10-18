## GUI image Sorter:
This script primarily uses the tkinter library to give the user the ability to look through a directory, and sort images in that directory, moving them into subfolders.

### Motivation in making this script:
A lot of my spare time went into sorting images on my phone, so friends that would relate more or less to types of images I had on my phone (ranging from recipes to images that just looked interesting). However, the efficiency of moving them inside of my phone was very limited, so I tried to make a script that could function as a program and help me efficiently move images from some primary folder to subfolders quickly and efficiently.

This program was also the second case of me working with the TKinter library, but the first time I had really looked into its capabilities, most especially creating a UI that was flexible- meaning that there was no preset amount of buttons or options, and doing so helped me greatly familiarize myself with the library.

### Installation Instructions:
#### Libraries imported:
pillow (Used to help display images with tkinter library)

After installing above libraries, the code is ready to run!


### How to use:
Select a directory for the script to use (Default is current working directory)
[Image of directory chooser here]

Press Begin When ready, images will show up centered in the window
[Image of what window looks like in progress]

Click on the button with the folder with the name you would like to send the file, or choose from one of the options.
[Image of example sidebar]
###### Be careful- deleting an image is not reversible.

Once all the images inside of a directory have been sorted, the script will stop looking through the current directory. You're free to input another directory or continue on, images sorted.
