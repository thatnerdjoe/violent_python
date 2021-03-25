'''
Image Embedding
Professor Hosmer
August 2020
'''

''' 3rd Party Library '''
from PIL import Image               # pip install pillow

# Pixel tuple index psuedo constants
RED   = 0
GREEN = 1
BLUE  = 2

''' Obtain the Basic image information '''

img       = Image.open('monalisa.bmp')      


'''
Image Orientation

         |
         |
y (rows) |
         |
         |     
         -----------------------------
                     x (columns)
'''
y  = img.height
x  = img.width

pix = img.load()  

cnt = 0
for row in range(0, y):
    
    for col in range(0, x):
        
        cnt += 1
        pixel = pix[col, row]   # Pixel values
        
        redPx = pixel[RED]      # Extract the RGB
        grnPx = pixel[GREEN]
        bluPx = pixel[BLUE]
        
        print("="*20)
        print("Row", row, "COL", col)
        print("RED: ", '{:08b}'.format(redPx))
        print("GRN: ", '{:08b}'.format(grnPx))
        print("BLU: ", '{:08b}'.format(bluPx))

    
print("Total Pixels: ", cnt)
    
