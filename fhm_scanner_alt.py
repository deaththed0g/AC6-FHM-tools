###################################################
# Ace Combat 6: Fires of Liberation - FHM sniffer #
# deaththed0g @ Github, death_the_d0g @ Xitter    #
# v200125                                         #
###################################################

import os
import glob
import re
import io
import shutil
import sys
import msvcrt

# Wait for user input to exit the program.

def pressKeyExit():
    
    print("<<< No DMP files were detected. Press any key to exit... >>")
    msvcrt.getch()  # Waits for a single character input
    sys.exit(1)  # Exits the program with error

# Set current directory as the working one.

basedir = os.getcwd()

# Get any DMP file present in the working directory.
# Store filename to use them as the name of the folder where any content inside FHM files will be dumped to.

file_list = []
file_name = []

for f in os.listdir(basedir):

        path = os.path.join(basedir, f)

        if f.endswith(".dmp") or f.endswith(".DMP"):

                file_list.append(path)

                file_name.append(os.path.splitext(f)[0])


# If DMP files were detected then proceed with the next block.

if len(file_list) != 0:

    # FHM format byte signature.

    fhm_signature = re.compile(b"\x46\x48\x4D\x20\x01\x01\x00\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")

    """
    # Chunk size
    
    Dump files can be very large in size and reading them in their entirety can severely impact performance.

    By default this script will read the current DMP file in chunks of 1 GB each one but the chunk size
    can be adjusted by editing the "1024" value.
    
    Please use values of power of two (512, 1024, 2048, 4096, etc.) when adjusting the chunk reading size.
    """
    
    chunk_size = 1024 * (1048576)
    
    # Open LOG file.
    
    output_log = open(basedir + "//fhm_sniffer_log_alt.txt", "w")

    # Process DMP files.
    
    for i in range(len(file_list)):
    
            chunk_total_read = 0 # Keep track of how many data has been read.
    
            fhm_found_count = 0 # Keep track of how many FHM files were found in the current DMP file. For logging purposes only.
    
            print(">> Reading [" + file_name[i] + ".dmp], please wait...")
            
            output_log.write(">> Reading [" + str(file_name[i]) + ".dmp], please wait...\n")
    
            dmp_file = open(file_list[i], "rb") # Open and read file.
    
            dmp_file_size = dmp_file.seek(0, os.SEEK_END) # Get current DMP file's size.
    
            dmp_file.seek(0, 0)
    
            chunk = io.BytesIO(dmp_file.read(chunk_size)) # Read current chunk to be scanned.
            
            file_numbering = 0 # Used for naming FHM files.
            
            # Create output folder for the current DMP file.
            # If the folder exists delete it and create it again.
            
            ouput_directory = basedir + "\\" + file_name[i] + "_alt"
    
            if os.path.isdir(ouput_directory):
    
                    shutil.rmtree(ouput_directory)
    
            os.mkdir(ouput_directory)
            
            # Repeat code block as long the amount of data read does not exceed the current file size.
            
            while not (chunk_total_read > dmp_file_size):
                    
                    # Scan for FHM files.
                    
                    for match_obj in re.finditer(fhm_signature, chunk.read()):
    
                            chunk.seek(match_obj.start(0) + 16, 0) # Jump to where the FHM file's data index is located.
    
                            nof = int.from_bytes(chunk.read(4), "big") # Number of entries in FHM file's data index.
    
                            if not nof == 0:
                                    
                                    """
                                    # Check if the current FHM file can be processed.
                    
                                    This check consists of reading the current FHM file's data index and get the offset and size of the last file in this index.
                                    Adding both values should give the FHM file's "true" size.
                    
                                    If the current file's size is greater than the "true" size then it's a file that can't be processed.
                                    Skip it and continue with the next one.
                                    """
        
                                    chunk.seek(match_obj.start(0) + 20 + (nof * 4) - 4, 0)
        
                                    last_file_offset = int.from_bytes(chunk.read(4), "big")
        
                                    chunk.seek(match_obj.start(0) + 20 + (nof * 8) - 4, 0)
        
                                    last_file_size = int.from_bytes(chunk.read(4), "big")
        
                                    chunk.seek(match_obj.start(0), 0)
        
                                    fhm_filesize = last_file_offset + last_file_size
        
                                    if not (fhm_filesize >= 268435456 or fhm_filesize <= 0): # If the FHM file's size is equal or smaller than zero or bigger than 256 mb then skip it.
                                            
                                            output_log.write("  >> FHM file found at position " + str(match_obj.start(0) + chunk_total_read) + " (" + str(file_numbering).zfill(4) + ".fhm)\n")
        
                                            output_file = open(ouput_directory + "\\" + str(file_numbering).zfill(4) + ".fhm", "wb")
        
                                            ouput_file_data = chunk.read(last_file_offset + last_file_size)
                            
                                            output_file.write(ouput_file_data)
                            
                                            output_file.close()
                            
                                            file_numbering += 1
        
                                            fhm_found_count += 1
                                    
                                    else:
                                        
                                        output_log.write("  >> [ERROR]: unable to process FHM file found at position " + str(match_obj.start(0)) + " (file size error)\n")

                            else:
                                
                                output_log.write("  >> [ERROR]: unable to process FHM file found at position " + str(match_obj.start(0)) + " (file index error)\n")
                            
                    # Keep adding adding chunk size as soon they are done being scanned.
                    # keep repeating the process as long the "total_chunk_read" doesn't exceed the DMP file's size.
                    
                    chunk_total_read += chunk_size 
                    
                    print("  >> Total MBs read so far: " + str(chunk_total_read // 1048576))
                
                    if not chunk_total_read > dmp_file_size:
    
                            dmp_file.seek(chunk_total_read, 0)
    
                            chunk = io.BytesIO(dmp_file.read(chunk_size))
                            
            print()
            output_log.write(">> Total amount of FHM containers found and dumped to [\\" + ouput_directory + "]: " + str(fhm_found_count) + "\n\n")
            
            dmp_file.close()
            
    output_log.close()
    
else:
    
    pressKeyExit()

exit()
