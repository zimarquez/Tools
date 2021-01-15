PicStorage

Goal:
The purpose of this script is to take a collection of files - primarily images - and organize them into month and year directories. This is most useful in organizing images taken over a long time period (images stored on the phone).

Supported file types:
- jpg/JPG `
- jpeg `
- png `
- mp4 `
- mp3 `
- mpg `
- mov `
- mkv `
- 3gp `
- avi
- wmv

Known Name Date Formats:
yyy-mm-dd
yyymmdd


Current Features:
- Create year and month directories from year 2000 to current year
- Create directory for storing copies of exisiting files
- Create directory for storing files with unsupported name format

Planned Features:
- Read image exif data for those without date in file names (partially done. currently only works for jpg files. will expand to support other files if possible. Also need to add a check for files with no exif data)
- Implement exif data extraction with exiftool

Current Issues (or annoying little things that need to be fixed):
- some file names may have the date in a different order (mmddyyyy VS ddmmyyyy). Need to figure out how to handle this (will likely need to be done through user input of date format).

Notes:
- The script prioritizes storage based on dates in filename rather than file metadata. The argument for this is that the dates in filenames are likely more accurate. If the file is a screenshot of an older image, the metadata will have origin date as the screenshot date and not the original image's date. Additionally, if a file has a date in the name it is likely accurate because who would deliberately assign an incorrect date in a file's name? I mean what kind of person does that? So with that in mind, dates in filenames are prioritized given the assumption that the file naming/dating was done reasonably.