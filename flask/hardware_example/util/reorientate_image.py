from PIL import Image
from PIL import ExifTags
import os, sys

"""
Used to reorientate images taken on an iPhone, which when imported into PAIV are not loaded in correctly.
"""

""" Constants """
PATH_TO_INPUT_DIR = '/Users/thomas.farrandibm.com/Desktop/spanner_photos'
PATH_TO_OUTPUT_DIR = '/Users/thomas.farrandibm.com/Desktop/spanner_photos' + '_output'

""" Functions """
def reorientateImage(infile, output_dir):
     outfile = os.path.splitext(infile)[0] + "_reorientated"
     extension = os.path.splitext(infile)[1]

     if (extension == ".jpg") or (extension == ".JPG") or (extension == ".jpeg") or (extension == ".JPEG"):

        if infile != outfile:

            # try :
            im = Image.open(infile)
            exif = im._getexif()
            exif = dict(exif.items())
            
            if 271 in exif:
                if exif[271] == 'Apple':
                    if exif[274] == 3:
                        im=im.rotate(180, expand=True)
                    elif exif[274] == 8:
                        im = im.rotate(90, expand=True)
                    elif exif[274] == 6:
                        im = im.rotate(270, expand=True)
                    else:
                        pass;

            absolute_name_with_path = PATH_TO_OUTPUT_DIR + "/" + outfile + ".JPEG"
            im.save(absolute_name_with_path,"JPEG")
            # except IOError:
            #     print ("cannot reduce image for ", infile)

def create_output_folder():
    if not os.path.exists(PATH_TO_OUTPUT_DIR):
        os.mkdir(PATH_TO_OUTPUT_DIR)


os.chdir(PATH_TO_INPUT_DIR)
dir = os.getcwd() 

create_output_folder()

for file in os.listdir(PATH_TO_INPUT_DIR):
    reorientateImage(file, PATH_TO_OUTPUT_DIR)