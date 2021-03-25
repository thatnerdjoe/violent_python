# Import Python libraries
import os                   # For file operations
import random               # For pseudo-random numbers
import math

# Import 3rd-party Python libraries
from PIL import Image       # Python Image Lib. for processing images

# Script header

SCRIPT_AUTHOR = 'Joseph Miller'
SCRIPT_NAME = 'Assignment 14 - Covert Communications'
SCRIPT_DATE = '2021-03-28'

"""
*******************************************************************************
PROMPT:
    After participating in this weeks live webinar.  Employ the concepts
    provided to create simple covert communication capability within the true
    color image provided.  You will be using the Python Image Library (PIL),
    the true color bmp file provided and the simple code book provided here.

        Submit:
            1) Your Python Script
            2) Your image embedded with the hidden content.

    (NOTE: your submitted image must be the same type/size as original image)
*******************************************************************************
"""


###
# FUNCTIONS
###
def line_break(l):
    """
    Line break made from '=' characters
    """
    print('='*l)


def quit_script(img):
    """
    Save image and tidy up before terminating.
    """
    try:
        img.codebook.close()
        img.image.close()
        print('\nDone!')
        exit(0)
    except Exception as e:
        print(e)
        exit(1)

###
# CLASSES
###


class Const():
    """
    This class enforces constant values by creating @classmethods
    which return a single value.
    """
    # Value of source image for data hiding
    @staticmethod
    def ORIG_IMG():
        return 'monalisa.bmp'
    """
    PIL returns RGB values of a pixel as a tuple, each value is a macro
    for it's respective index within the tuple.
    """
    @staticmethod
    def RED():
        return 0

    @staticmethod
    def GRN():
        return 1

    @staticmethod
    def BLU():
        return 2


class ImageTransform():
    """
    This class alters an image modifying the LSB of a pixel's
    RBG values to embed a code into the image. Each code is a three
    digit binary value which can be translated with a code book.
    """

    def __init__(self):
        self.image = None
        self.img_width = None
        self.img_height = None
        self.pixel_count = 0
        self.codebook = None
        self.pix_picker = None
        self.message = []

    def embed_msg(self):
        """
        Embed the selected image with the message
        """
        # Set the message to be embedded in the image
        self._select_message()
        line_break(promptLen)
        print('Embedding message into image...')

        # Randomly select a pixel to embed info within
        col = random.choice(range(self.img_width // 2))
        row = random.choice(range(self.img_height // 2))

        count = 0
        while count < len(self.message):
            try:
                msg = self.message[count]
                # Increment pixel location
                col += 1
                row += 1

                # Parse out each byte from the RGB tuple
                pixel = self.pix_picker[col, row]
                pix_red = int(pixel[Const.RED()])
                pix_grn = int(pixel[Const.GRN()])
                pix_blu = int(pixel[Const.BLU()])

                # Find new pixel if LSBs match the message code
                check = str(pix_red & 0x1)+str(pix_grn & 0x1) + \
                    str(pix_blu & 0x1)
                if check == self.message[count]:
                    continue

                # Set the LSB of each color value of the pixel and update the pixel
                pix_red = (int(pix_red) & 0xFE) | (int(msg[Const.RED()]) & 0x1)
                pix_grn = (int(pix_grn) & 0xFE) | (int(msg[Const.GRN()]) & 0x1)
                pix_blu = (int(pix_blu) & 0xFE) | (int(msg[Const.BLU()]) & 0x1)

                # Update image pixel
                pixel = (pix_red, pix_grn, pix_blu)
                self.pix_picker[col, row] = pixel
                count += 1
            # Find new pixel if OOB error
            except IndexError:
                col = random.choice(range(self.img_width // 2))
                row = random.choice(range(self.img_height // 2))
                continue
        # Save the transformed image
        try:
            self.image.save('steg-out.bmp')
            line_break(promptLen)
        except Exception as e:
            print(e)

    def extract_msg(self, steg_img):
        """
        Extract the message from selected image
        """
        print('Extracting message from image...')
        line_break(promptLen)
        print()

        codes = []
        idx = 0

        try:
            steg = Image.open(steg_img)
            pix_steg = steg.load()

            if steg.size != self.image.size:
                print('ERROR: Files likely not matching.\n Quitting...')
                exit(1)

            for col in range(self.img_width):
                for row in range(self.img_height):

                    # Add embedded code to list for decoding
                    if self.pix_picker[col, row] != pix_steg[col, row]:
                        pixel = pix_steg[col, row]
                        pix_red = int(pixel[Const.RED()] & 0x1)
                        pix_grn = int(pixel[Const.GRN()] & 0x1)
                        pix_blu = int(pixel[Const.BLU()] & 0x1)
                        codes.append(str(pix_red) +
                                     str(pix_grn) + str(pix_blu))

            # Print respective lines of text from codebook for found codes
            for each_code in self.codebook:
                if(each_code.startswith(codes[idx])):
                    idx += 1
                    print(each_code, end='')
            print()
            line_break(promptLen)

        except Exception as e:
            print(e)

    def _select_message(self):
        """
        Select message to embed within an image.
        """

        # Populate a list with the lines from the codebook
        codes = {}
        for idx, line in enumerate(self.codebook):
            codes.update({
                idx: line
            })

        # Prompt user for messages to embed
        while(1):
            line_break(promptLen)
            print("Select the codes to embed: \n")

            # Print options for user selection
            for key, value in codes.items():
                print(f'\t[{key}] - {value[4:]}', end='')

            print('\n\t[55] - Save message to image and quit')
            print('\t[99] - Quit without saving')

            selection = int(input('\nSelection: '))

            # Remove selection from options and add it to the embed list
            if selection in codes.keys():
                temp = codes[selection][:3]
                self.message.append(temp)
                codes.pop(selection)
            # Continue with embed operation
            elif selection == 55:
                return
            # Quit without saving
            elif selection == 99:
                print("Quiting...")
                exit(1)
            # Prompt user of invalid selection
            else:
                print("ERROR: Invalid entry.")

    def setup(self, img_path, codebook_path):
        """
        Setup the object by creating file descriptors to image and codebook
        """
        print('Opening image: "' + img_path + '"')
        try:
            self.image = Image.open(img_path, "r")
            self.pix_picker = self.image.load()
            self.img_width = self.image.width
            self.img_height = self.image.height
        except Exception as e:
            print(e)

        print('Opening codebook: "' + codebook_path + '"')
        try:
            self.codebook = open(codebook_path, "r")
        except Exception as e:
            print(e)


###
# SCRIPT ENTRY POINT
###
if __name__ == '__main__':

    # Set up input prompt
    prompt = 'Enter the image path:'
    promptLen = len(prompt)

    # Print program header
    line_break(promptLen)
    print('\n' + SCRIPT_AUTHOR + '\n' + SCRIPT_NAME +
          '\n' + SCRIPT_DATE, end='\n\n')

    # Commented out for testing
    # separator(promptLen)
    # image_path = input(prompt + ' ')
    image_path = Const.ORIG_IMG()
    codebook_path = '../CodeBook.txt'
    line_break(promptLen)

    # Create image decoder/encoder object
    IMG = ImageTransform()
    IMG.setup(image_path, codebook_path)

    # Selection for embedding or extracting message from an image
    if 0:
        IMG.embed_msg()
    else:
        IMG.extract_msg('steg-out.bmp')

    quit_script(IMG)
