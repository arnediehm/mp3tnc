#!/usr/bin/python
from datetime import datetime
import eyed3
import os
import sys

# Settings
filenameStr = ''  # string to remove from Filename
id3Str = ''  # String to remove from ID3 Tags


def log(str, newline=False):

    log_datetime = datetime.now().strftime("%Y-%m-%d %H.%M.%S")

    f = open("mp3tnc.log", "a")
    if newline:
        f.write("\n")

    f.write(log_datetime + " " + str + "\n")
    f.close()


def scan_id3(filepath, dry_run = True):
    # print("debug: " + filepath)

    # Version 1, 1.0 or 1.1
    id3_v1 = (1, None, None)
    id3_v2 = (2, None, None)
    id3_any_version = (id3_v1[0] | id3_v2[0], None, None)

    audio_file = eyed3.load(filepath, id3_v2)

    title = audio_file.tag.title                # Titel
    artist = audio_file.tag.artist              # Interpret
    album = audio_file.tag.album                # Album
    album_artist = audio_file.tag.album_artist  # Album Interpret
    composer = audio_file.tag.composer          # Komponist
    #  track_num = audio_file.tag.track_num     # Track Nummer

    change_counter = 0

    if id3Str in title:
        audio_file.tag.title = title.replace(id3Str, '')
        print("ACTION (id3.title): \"" + title + "\" -> \"" + audio_file.tag.title + "\"")
        change_counter += 1

    if id3Str in artist:
        audio_file.tag.artist = artist.replace(id3Str, '')
        print("ACTION (id3.artist): \"" + artist + "\" -> \"" + audio_file.tag.artist + "\"")
        change_counter += 1

    if id3Str in album:
        audio_file.tag.album = album.replace(id3Str, '')
        print("ACTION (id3.album): \"" + album + "\" -> \"" + audio_file.tag.album + "\"")
        change_counter += 1

    if id3Str in album_artist:
        audio_file.tag.album_artist = album_artist.replace(id3Str, '')
        print("ACTION (id3.album_artist): \"" + album_artist + "\" -> \"" + audio_file.tag.album_artist + "\"")
        change_counter += 1

    if id3Str in composer:
        audio_file.tag.composer = composer.replace(id3Str, '')
        print("ACTION (id3.composer): \"" + composer + "\" -> \"" + audio_file.tag.composer + "\"")
        change_counter += 1

    if dry_run:
        change_counter = 0
    else:
        audio_file.tag.save()

    return change_counter


def main():

    if not filenameStr or not id3Str:
        print("\nEmpty Settings. Running like this is not recommended !")

    # Ask for Dry run
    yes = {'yes', 'y', 'Yes', 'Y', 'YES'}

    print("\nDry run by default. Changes will only be shown in the terminal and not be saved to the files !\n")
    res = input("\nDisable dry run and actually change the mp3 files? (y/n): ")
    print("-------------------\n")

    # Enter without input keeps dry run enabled
    if res in yes:
        dry_run = False
    else:
        dry_run = True

    if len(sys.argv) == 2:
        root_dir = sys.argv[1]
        print("root path provided as commandline argument: ")
        print(root_dir)
    else:
        root_dir = os.path.dirname(os.path.realpath(__file__))

    # Change Filenames
    action = False # Variable stores if a change was made to a file in a sub folder
    global_action = False # variable stores if any potential changes were found at all
    file_counter = 0
    rename_counter = 0
    id3_counter = 0

    for subdir, dirs, files in os.walk(root_dir):
        for file in files:
            file_counter += 1

            # print os.path.join(subdir, file)
            filepath = subdir + os.sep + file

            mp3 = {'mp3', 'MP3'}

            if os.path.splitext(filepath)[1][1:] in mp3:

                # Search- and change File name
                if filenameStr in filepath:
                    new_filename = file.replace(filenameStr, '')

                    print("ACTION (filename): \"" + file + "\" -> \"" + new_filename + "\"")

                    if not dry_run:
                        os.rename(filepath, subdir + os.sep + new_filename)

                        rename_counter += 1

                        if not action:
                            log("Folder: \"" + subdir + "\"", not action)

                        log("(filename): \"" + filepath + "\" -> \"" + subdir + os.sep + new_filename + "\"")

                    action = True
                    global_action = True

                # Search- and change ID3 Tags
                if action:
                    filepath = subdir + os.sep + new_filename

                id3_counter += scan_id3(filepath, dry_run)

                if id3_counter:
                    global_action = True

        # Print new lines after action for every new sub folder
        if action:
            print()
            action = False

    print()
    print("-------------------")
    if not global_action and not dry_run:
        print(str(file_counter) + " files scanned. No potential changes found.\n")
    else:
        print(str(file_counter) + " files scanned.\n")
        print(str(rename_counter) + " files renamed")
        print(str(id3_counter) + " id3 Tags changed")

    if dry_run:
        print("Dry run. No changes were made to any files !\n")


if __name__ == "__main__":
    main()
