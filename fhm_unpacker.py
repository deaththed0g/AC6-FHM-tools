#####################################################################
# Ace Combat 6: Fires of Liberation - FHM unpacker by death_the_d0g #
# deaththed0g @ Github, death_the_d0g @ Xitter                      #
# v200125                                                           #
#####################################################################

import os
import glob
import re
import shutil
import sys
import msvcrt

# Wait for user input to exit the program.

def pressKeyExit():
    
    print(">> No FHM files were detected. Press any key to exit...")
    msvcrt.getch()  # Waits for a single character input
    sys.exit(1)  # Exits the program with error

# Set current directory as the working one.

basedir = os.getcwd()
base_path = ""

# Get any FHM file present in the working directory.
# Store filename to use them as the name of the folder where any content inside FHM files will be dumped to.

file_list = []
file_name = []

for f in os.listdir(basedir):
    
    path = os.path.join(basedir, f)
    
    if f.endswith(".fhm"):
        
        file_list.append(path)
        
        file_name.append(os.path.splitext(f)[0])

# If FHM files were detected then proceed with the next block.

if len(file_list) != 0:

    # Iterate 'file_name' list and check if any folder present in the working directory uses the same file name found inside said list.
    # If true, delete that folder.
    
    for i in range(len(file_name)):
        
        dir_list = glob.iglob(os.path.join(base_path, str(file_name[i])))
        
        for path in dir_list:
            
            if os.path.isdir(path):
                
                shutil.rmtree(path)
    
    # Open LOG file.
    
    output_log = open(basedir + "//fhm_unpacker.txt", "w")
    
    
    # Process files.
    
    for i in range(len(file_list)):
        
        # Open and read file.
        # Retrieve current file's name.
    
        input_file = open(file_list[i], "rb")
    
        filename = str(file_name[i])
        
        """
        # Check if the current FHM file can be processed.
        
        This check consists of reading the current FHM file's ToC and get the offset and size of the last file in this index.
        Adding both values should give the FHM file's "true" size.
        
        Then compare this "true" size with the size that was obtained by using 'os.SEEK_END' on the current
        FHM file being read.
        
        If the current file's size is greater than the "true" size then it's a file that can't be processed.
        Skip it and continue with the next one.
        """
        
        input_file.seek(16, 0)
    
        nof = int.from_bytes(input_file.read(4), "big") # Number of entries in FHM file's ToC.
    
        input_file.seek(20 + (nof * 4) - 4, 0)
    
        last_file_offset = int.from_bytes(input_file.read(4), "big")
    
        input_file.seek(20 + (nof * 8) - 4, 0)
    
        last_file_size = int.from_bytes(input_file.read(4), "big")
    
        fhm_filesize = last_file_offset + last_file_size
    
        input_file.seek(0, 0)
        
        input_file_size = input_file.seek(0, os.SEEK_END)
    
        if not input_file_size > fhm_filesize: # Check if the file can be processed.
            
            # Read ToC and store offsets and sizes.
            
            offset_list = []
            
            file_size_list  = []
    
            input_file.seek(20, 0)
    
            for i in range(nof):
    
                offset_list.append(int.from_bytes(input_file.read(4), "big"))
    
            for i in range(nof):
    
                file_size_list.append(int.from_bytes(input_file.read(4), "big"))
    
            os.mkdir(filename) # Create a folder using the file's name. This where the contents of the FHM will be dumped to.
    
            for i in range(nof):
    
                input_file.seek(offset_list[i], 0)
                
                """
                # Get file extension.
                
                The script will try to get an extension to attach it to the file being extracted from a FHM container.
                
                It will read an amount of bytes then convert it to a string. If the string has valid/printable characters
                then it will become the file's extension otherwise the extension will be "unk" (unknown).
                """
    
                file_extension_check = input_file.read(16) # Special check to extract XML files.
    
                file_extension = file_extension_check.decode('UTF-8', errors = 'ignore')
    
                if file_extension_check == b"\xEF\xBB\xBF\x3C\x3F\x78\x6D\x6C\x20\x76\x65\x72\x73\x69\x6F\x6E":
    
                    file_extension = "xml"
    
                else:
    
                    if file_extension[:3].isalnum():
    
                        file_extension = file_extension[:3]
    
                    else:
    
                        file_extension = "unk"
                
                # Write and dump data.
                
                input_file.seek(offset_list[i], 0)
    
                file_output = open(filename + "//" + str(i).zfill(4) + "." + file_extension.lower(), "wb")
    
                file_output.write(input_file.read(file_size_list[i]))
    
                file_output.close()
            
            output_log.write(">> Processing " + filename + ".fhm: OK!\n")
        
        else:
            
            output_log.write(">> processing " + filename + ".fhm: ERROR!\n")
    
        input_file.close()

else:
    
    pressKeyExit()

output_log.close()

exit()
