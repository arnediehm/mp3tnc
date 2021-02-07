#!/usr/bin/python
from datetime import datetime
import eyed3
import os
import sys

# Settings
filenameStr = ''  # string to remove from Filename
id3Str = ''  # String to remove from ID3 Tags


def log(str, newline=False):

    logdatetime = datetime.now().strftime("%Y-%m-%d %H.%M.%S")

    f = open("mp3tnc.log", "a")
    if newline:
        f.write("\n")

    f.write(logdatetime + " " + str + "\n")
    f.close()


def scanID3(filepath, dryrun = True):
    # print("debug: " + filepath)

    # Version 1, 1.0 or 1.1
    ID3_V1 = (1, None, None)
    ID3_V2 = (2, None, None)
    ID3_ANY_VERSION = (ID3_V1[0] | ID3_V2[0], None, None)

    audiofile = eyed3.load(filepath, ID3_V2)

    title = audiofile.tag.title

    changeCounter = 0

    if id3Str in title:
        newTitle = title.replace(id3Str, '')

        print("ACTION (change id3Tag): \"" + audiofile.tag.title + "\" -> \"" + newTitle + "\"")

        if not dryrun:
            log("(changed id3Tag): \"" + audiofile.tag.title + "\" -> \"" + newTitle + "\"")

            audiofile.tag.title = newTitle
            audiofile.tag.save()
            changeCounter += 1

    #for frame in tag.frames:
    #    print(frame)

    return changeCounter

def main():

    # Ask for Dry run
    yes = {'yes', 'y', 'Yes', 'Y', 'YES'}

    print("\nDry run by default. Changes will only be shown in the terminal and not be saved to the files !\n")
    res = input("\nDisable dry run and actually change the mp3 files? (y/n): ")
    print("-------------------\n")

    # Enter without input keeps dry run enabled
    if res in yes:
        dryRun = False
    else:
        dryRun = True

    if len(sys.argv) == 2:
        rootDir = sys.argv[1]
        print("root path provided as commandline argument: ")
        print(rootDir)
    else:
        rootDir = os.path.dirname(os.path.realpath(__file__))

    # Change Filenames
    action = False # Variable stores if a change was made to a file in a subfolder
    globalAction = False # variable stores if any potential changes were found at all
    fileCounter = 0
    renameCounter = 0
    id3Counter = 0

    for subdir, dirs, files in os.walk(rootDir):
        for file in files:
            fileCounter += 1

            # print os.path.join(subdir, file)
            filepath = subdir + os.sep + file

            mp3 = {'mp3', 'MP3'}

            if os.path.splitext(filepath)[1][1:] in mp3:

                # Search- and change ID3 Tags
                id3Counter += scanID3(filepath, dryRun)

                # Search- and change File name
                if filenameStr in filepath:
                    newFilename = file.replace(filenameStr, '')

                    print("ACTION (change filename): \"" + file + "\" -> \"" + newFilename + "\"")

                    if not dryRun:
                        os.rename(filepath, subdir + os.sep + newFilename)
                        renameCounter += 1

                        if not action:
                            log("Folder: \"" + subdir + "\"", not action)

                        log("(changed filename): \"" + filepath + "\" -> \"" + subdir + os.sep + newFilename + "\"")

                    action = True
                    globalAction = True

        # Print new lines after action for every new sub folder
        if action:
            print()
            action = False

    print()
    if not globalAction:
        print(str(fileCounter) + " files scanned. No potential changes found.\n")
    else:
        print(str(fileCounter) + " files scanned.\n")
        print(str(renameCounter) + " files renamed")
        print(str(id3Counter) + " id3 Tags changed")

    if dryRun:
        print("Dry run. No changes were made to any files !\n")


if __name__ == "__main__":
    main()
