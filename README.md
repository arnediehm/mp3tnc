# mp3tnc

MP3 ID3 tag and filename cleaner

### Minimal Usage Example (reduced to a few files for ease of understanding)
```java
root directory: '/home/Documents/Music/Test'
```

*mp3tnc scans recursively and also processes all files in sub-folders!*

Three MP3 files with the following file names and ID3 tags are to be changed.

```java
    filename:       'my_music_test1.mp3'            ->    'my_music_1.mp3'
    id3Tag.title:   'my music test 1'               ->    'music test 1'
    
    filename:       'my_music_test2.mp3'            ->    'my_music_2.mp3'
    id3Tag.title:   'my music test 2'               ->    'music test 2'
    
    filename:       'my_music_test3.mp3'            ->    'my_music_3.mp3'
    id3Tag.title:   'my music test 3'               ->    'music test 3'
```

The following settings are applied in mp3tnc.py:

```java
filenameStr = 'test'
id3Str      = 'my'
```

Then either copy the python file to the root folder (to be scanned) or pass the root path as commandline argument.

```java
python mp3tnc.py '/home/Documents/Music/Test'
```

mp3tnc will ask if you want to run a dry run.

First run a dry run and verify that the proposed changes are valid by entering **n**.

Then run again and enter **y** to apply the changes to the Files.


Filenames before running mp3tnc             |  Title tags before running mp3tnc
:-------------------------:|:-------------------------:
![drawing](https://arnediehm.de/s/JezxjLq2f3Yoxyr/preview)  |  ![drawing](https://arnediehm.de/s/DzrnpeioHWcZn3w/preview)

Filenames after running mp3tnc             |  Title tags after running mp3tnc
:-------------------------:|:-------------------------:
![drawing](https://arnediehm.de/s/dpAEnHCJCDDzfyA/preview)  |  ![drawing](https://arnediehm.de/s/S3WPp6ZXt8dcxXy/preview)


