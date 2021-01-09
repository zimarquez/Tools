import os
import re
import exiftool
from PIL import Image
from PIL.ExifTags import TAGS
from pathlib import Path
from datetime import datetime

pwd = os.path.dirname(os.path.realpath(__file__))
currentYear = datetime.now().year
months = ["01-January","02-February","03-March","04-April",
          "05-May","06-June","07-July","08-August",
          "09-September","10-October","11-November","12-December"]
fileTypes = (".jpg",".jpeg",".png",".mp4",".JPG",".MOV")
badFormatDirectory = "Unsupported Format"
existingImageDirectory = "Copies"
unknownDateDirectory = "Unknown Date"
dateTimeOriginalID = 36867

def CreateDirectories():
  print("~~Checking year directories~~")

  # Create year directories
  for year in range (2000, currentYear+1):
    if os.path.isdir(str(year)):
      i = 0
      #print("Directory " + str(year) + " already exists")
    else:
      print("Creating directory " + str(year))
      os.makedirs(str(year))
      for month in months:
        os.makedirs(str(year) + "/" + month)

  # Create directory for unsupported file formats
  if os.path.isdir(badFormatDirectory):
    print("Directory " + badFormatDirectory + " already exists")
  else:
    print("Creating directory " + badFormatDirectory)
    os.makedirs(badFormatDirectory)

  # Create directory for exisiting images
  if os.path.isdir(existingImageDirectory):
    print("Directory " + existingImageDirectory + " already exists")
  else:
    print("Creating directory " + existingImageDirectory)
    os.makedirs(existingImageDirectory)

  # Create directory for files needing manual organization
  if os.path.isdir(unknownDateDirectory):
    print("Directory " + unknownDateDirectory + " already exists")
  else:
    print("Creating directory " + unknownDateDirectory)
    os.makedirs(unknownDateDirectory)

  # This line should work, but it doesn't.....
  #os.chmod(str(pwd) + "/" + str(year), 0o666)

def GetNewImages():
  print("~~Making image list~~")

  listOfFiles = os.listdir(pwd)
  listOfImages = []
  for f in listOfFiles:
    if f.endswith(fileTypes):
      listOfImages.append(f)
    
  return listOfImages

def IncrementImageName(image, number):
  newImageName = ""
  for x in image:
    if x == '.':
      newImageName = newImageName + "(" + str(number) + ")"
    newImageName = newImageName + x
  
  return newImageName

# extracts file origin date from exif data
def GetJPGDate(imageName):
  imagePath = pwd + "/" + imageName
  image = Image.open(imagePath)
  if image._getexif() != None:
    for dataID, dataValue in image._getexif().items():
      #print(TAGS[dataValue])
      if dataID == dateTimeOriginalID:
        print(dataValue)
        year = dataValue[0:4]
        month = dataValue[5:7]
        day = dataValue[8:10]
        destination = ("/" + str(year) + "/" + months[int(month)-1])
        return destination
  else:
    print("The file: " + imagePath + " does not contain exif data")
    return -1

def GetMP4Date(fileName):
  print("Foo")
  
# FileModifyDate
# CreateDate
def GetExifData(fileName):
  sourcePath = pwd + "/" + fileName
  tag = "CreateDate"
  with exiftool.ExifTool() as et:
    #metadata = et.execute("-time:all " + str(sourcePath))
    metadata = et.get_metadata(sourcePath)
    specificTag = et.get_tag(tag, sourcePath)
  print(tag + ": " + specificTag)

def GetDateFromFileData(currentFile):
  filePath = pwd + "/" + currentFile
  if filePath.endswith((".jpg",".JPG",".jpeg")):
    print("Valid jpg file")
    destinationPath = GetJPGDate(currentFile)
  elif filePath.endswith((".mp4", ".MOV")):
    print("Valid mp4 file")
    #destinationPath = GetExifData(currentFile)
    return -1
  #elif filePath.endswith((".jpg",".JPG",".jpeg")):
  #elif filePath.endswith((".jpg",".JPG",".jpeg")):
  else:
    print("Invalid image type")
    return -1
  
  return destinationPath

def GetDateFromFileName(imageName):
  print("~~Getting destination directory~~")

  print("Using image: " + imageName) 
  date = re.search("\d\d\d\d\d\d\d\d", imageName)
  if date:
    date = date.group()
    year = date[0:4]
    month = date[4:6]
    day = date[6:8]
    print(int(month))
    destination = ("/" + str(year) + "/" + months[int(month)-1])
    return destination

  date = re.search("\d\d\d\d-\d\d-\d\d", imageName)
  if date:
    date = date.group()
    year = date[0:4]
    month = date[5:7]
    day = date[8:10]
    destination = ("/" + str(year) + "/" + months[int(month)-1])
    return destination

  # Move files with unsupported format to separate directory
  else:
    #GetDateFromExif(imageName)
    destination = ("/" + badFormatDirectory)
    print("WARNING: No valid date found")
    return -1

  return destination

  
def MoveImages(listOfImages):
  print("~~Moving images~~")
  
  for image in listOfImages:
    sourcePath = pwd + "/" + image

    # Extract date from file name
    dateDirectory = GetDateFromFileName(image)
    if dateDirectory != -1:
      destinationPath = pwd + dateDirectory + "/" + image
    # Extract date from file data
    else:
      print("It's sorta working :D")
      dateDirectory = GetDateFromFileData(image)
      if dateDirectory == -1:
        print("The file '" + image + "' could not be organized. Moving to '" + unknownDateDirectory + "' directory")
        dateDirectory = "/" + unknownDateDirectory
      destinationPath = pwd + dateDirectory + "/" + image
    
    badFormatPath = pwd + "/" + badFormatDirectory + "/" + image
    existingImagePath = pwd + "/" + existingImageDirectory + "/" + image
    
    #print("Old: ", sourcePath)
    #print("New: ", destinationPath)

    if destinationPath == badFormatPath:
      print("WARNING: the file '" + image + "' is not in a valid name format. Moving to 'Unsupported' directory")
      #os.rename(sourcePath, badFormatPath)
    elif os.path.exists(destinationPath):
      print("WARNING: the file '" + image + "' already exists in " + str(destinationPath) + ". Moving to Copies directory.")
      i = 1
      while os.path.exists(existingImagePath):
        newImageName = IncrementImageName(image, i)
        existingImagePath = pwd + "/" + existingImageDirectory + "/" + newImageName
        i += 1
      #os.rename(sourcePath, existingImagePath)
    else:
      print("bruh")
      #os.rename(sourcePath, destinationPath)

def main():
  CreateDirectories()
  MoveImages(GetNewImages())

if __name__ == "__main__":
  main()

