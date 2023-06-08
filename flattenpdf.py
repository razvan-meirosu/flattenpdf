# -----------------------------------------------------------------
# Flatten PDF Script
#
# Description: Flatten all pdf files from the "input" folder and 
# saves them to the "output" folder. This script convert all PDF 
# files into scanned PDF's, making your PDF's look like scanned.
#
# Author: Razvan Meirosu / https://github.com/razvan-meirosu
# License: GNU GPL V3 
# -----------------------------------------------------------------

import os, glob, fitz
from PIL import Image

os.chdir("input") # Folder that contains original pdf files
for original_pdf_file in glob.glob("*.pdf"):
    print("Flattening file: " + original_pdf_file)

# Step 1: Converting each pdf file to multipage tif

multipage_tif = "output.tif" # Output tif file name
compression = 'zip'

zoom = 2 # Used to increase the resolution of tif file
mat = fitz.Matrix(zoom, zoom)

pdf_file = fitz.open(original_pdf_file)
image_list = []
for page in pdf_file:
    pixmap = page.get_pixmap(matrix = mat)
    img = Image.frombytes("RGB", [pixmap.width, pixmap.height], pixmap.samples)
    image_list.append(img)
        
if image_list:
    image_list[0].save(
        multipage_tif,
        save_all=True,
        append_images=image_list[1:],
        compression=compression,
        dpi=(300, 300),
    )

# Step 2: Converting multipage tif back to pdf

img = Image.open(multipage_tif)
img.save('../output/' + original_pdf_file, save_all=True) # Folder where flattened pdf's are saved
img.close()
os.remove("output.tif") # Removing the tif image

print("Done")