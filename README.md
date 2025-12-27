# Ace Combat 6: Fires of Liberation - FHM tools

## About

Ace Combat 6's assets inside the ISO image are stored in PAC files that are compressed and encrypted. I have no knowledge of compression/encryption algorithms, much less how to implement them, so the only way I could get access to the unmodified assets was to poke into Xenia's memory while it was emulating the game. Creating a memory dump of the emulator will also keep all the game assets that were loaded in the emulated X360 memory at that moment, so I created these scripts to extract them.

Most decompressed/decrypted assets (such as 3D models, textures, etc.) seem to be stored in generic file containers whose header contains the "FHM" magic word. The game seems to have been developed using Namco's in-house tools ("NU Library"?) because some file formats used here can also be found in other games Namco-developed games (such as Tekken 6, Tekken Tag Tournament 2).

The "fhm_scanner" script will look for these FHM containers in a DMP (memory dump) file. The "fhm_unpacker" script will extract the contents from any FHM container that was dumped using the "fhm_scanner" script.

## Required tools and files

- Python 3.12.8 (or latest) for Windows installed in your computer.

- Xenia emulator and ISO file of Ace Combat 6: Fires of Liberation. The version/region of Ace Combat 6 should not matter as long Xenia can emulate it.

- Any tool capable of dumping a process's RAM to a file. Windows' own Task Manager should be enough.

## Usage

Start Xenia with Ace Combat 6 and select a mission and an aircraft. Once in the mission, pause the game then run Task Manager and create a dump file.

Depending on the processing power of your computer, it could take some time for the dump file to be created. Once the dumping process is complete, you will find the file in the following path:

>C:\Users\<YourUsername>\AppData\Local\Temp

#### Extracting FHM files

Place the DMP file and Python scripts in the same directory. Run the "fhm_scanner.py" (or "fhm_scanner_alt.py", see **NOTES** section) script and wait while it scans the file. It will create a folder using the name of the DMP file and dump any FHM file found there. 
Once the process is complete the script will create a log text detailing the position of the files detected within the DMP file.

#### Extracting the contents from FHM files

Place the "fhm_unpacker.py" script in the same location as the FHM files and run it. The script will create a folder using the name of the FHM file being processed and dump its contents there. It will also create a log file detailing which files were processed successfully and which encountered errors.

## Notes

- Some FHM containers may contain smaller FHM containers within them. To preserve the "file integrity" of the larger FHM containers, I wrote two scripts:

	- The "fhm_scanner" script will attempt to dump the larger FHM files and skip the ones nested within them. You can later use the unpacker script to process these nested containers.

	- The "fhm_scanner_alt" script will instead dump any FHM file it detects whether it's a standalone file or part of a larger FHM container.

- The scripts can batch process multiple DMP/FHM files.

- If you have used a different tool to get memory dumps make sure you change their extension to "DMP". The scanning scripts will only read files with that extension.

- 3D models seems to be stored as NDX files while textures are stored with the NTX extension.

- The unpacker script will attempt to give an extension to a file during extraction. If the script is unable to assign an extension the file will be extracted as an UNK file (**unk**-nown).

- If you see a FHM container inside a non-DMP/non-FHM file, change that file's extension to DMP and run the scanner script on it.

## Issues

- File detection is nowhere perfect so don't expect a full and/or correct extraction.

- Extracted files will be named in numerical order.

- Some FHM files will not work with the unpacker script.

- DMP files will contain multiple duplicate FHM files. Since the scanner scripts cannot distinguish between duplicate archives during the dumping process you will need to manually delete them after completion. If you are looking for a freeware application that detects and removes duplicate files I recommend [Anti-Twin](https://antitwin.org/en/).

- Process can take a while, especially if the DMP file is larger size or there are too many FHM files to be processed.

- Expect some system "freezes" while the scripts are running.

---
## FHM format specs
[Available here](https://github.com/deaththed0g/AC6-FHM-utilities/wiki/FHM-file-format-specs)
