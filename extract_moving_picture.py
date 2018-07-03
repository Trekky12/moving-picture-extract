#!/usr/bin/env python3

import os
import sys, getopt

filename = "IMG_20180703_085041.jpg"


def extract(file, extractImage):
    with open(filename, "rb") as binary_file:
        name, ext = os.path.splitext(binary_file.name)

        binary_file.seek(0, 2)  # Seek the end
        num_bytes = binary_file.tell()  # Get the file size

        jpg_found = False
        for i in range(num_bytes):
            binary_file.seek(i)
            
            if extractImage and not jpg_found:
                jpg_end_bytes = binary_file.read(4)
                if jpg_end_bytes == b"\xFF\xD9\x00\x00":  # JPG end
                    # Go back to beginning of the file and extract the jpg
                    binary_file.seek(0)
                    jpg_data = binary_file.read(i + 4)
                    with open("%s_i.jpg" %(name), "wb") as outfile:
                        outfile.write(jpg_data)
                    jpg_found = True
            
            else:
                mp4_start_bytes = binary_file.read(16)
                if mp4_start_bytes == b"\x00\x00\x00\x18\x66\x74\x79\x70\x6D\x70\x34\x32\x00\x00\x00\x00":  # MP4 Start
                    # Go to to beginning of the mp4 file and extract
                    binary_file.seek(i)
                    mp4_data = binary_file.read(num_bytes - i)
                    with open("%s.mp4" %(name), "wb") as outfile:
                        outfile.write(mp4_data)

def usage():
    print('extract_moving_picture.py -i <file>')
    print('extract_moving_picture.py -f <folder>\n')
    print('extract_moving_picture.py -i <file> -e')
    print('extract_moving_picture.py -f <folder> -e\n')
    print('when you append -e the original image is also extracted')
                        
if __name__ == "__main__":
    print("Huawei Moving Picture / Momente Extractor\n")

    if sys.version_info[0] < 3:
        print("This script requires Python 3")
        sys.exit(-1)
    
    filename = None
    extractImage = False
    isFolder = False

    try:
        opts, args = getopt.getopt(sys.argv[1:],"hi:f:e",["ifile=, folder="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            usage()
            sys.exit()
        elif opt in ("-i", "--ifile"):
            filename = arg
        elif opt in ("-f", "--folder"):
            filename = arg
            isFolder = True
        elif opt == "-e":
            extractImage = True
    if filename is None:
        usage()
        sys.exit(2)
    
    if not isFolder:
        print('Extract MP4 from file "%s"' %(filename))
        extract(filename, extractImage)
    else:
        foldername = os.path.join(os.path.abspath("."), filename)
        print('Extract MP4 from folder "%s"' %(foldername))
        for root, dirs, files in os.walk(foldername):
            for file_ in files:
                filename = os.path.join(root, file_)
                print('Extract MP4 from file "%s"' %(filename))
                extract(filename, extractImage)
    