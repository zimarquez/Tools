import os
import re
from PIL import Image
from PIL.ExifTags import TAGS
from pathlib import Path
from datetime import datetime

pwd = os.path.dirname(os.path.realpath(__file__))
currentYear = datetime.now().year
months = ["01-January","02-February","03-March","04-April",
          "05-May","06-June","07-July","08-August",
          "09-September","10-October","11-November","12-December"]
fileTypes = (".jpg",".jpeg",".png",".mp4", ".JPG")
badFormatDirectory = "Unsupported Format"
existingImageDirectory = "Copies"
dateTimeOriginalID = 36867

def CreateDirectories():
  print("~~Checking year directories~~")

  # Create year directories
  for year in range (2000, currentYear+1):
    if os.path.isdir(str(year)):
      print("Directory " + str(year) + " already exists")
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

def GetDateFromExif(imagePath):
  if imagePath.endswith((".jpg",".JPG", ".jpeg")):
    print("Valid jpg image")
    image = Image.open(imagePath)
    for dataID, dataValue in image._getexif().items():
      #print(TAGS[dataValue])
      if dataID == dateTimeOriginalID:
        print(dataValue)
        year = dataValue[0:4]
        month = dataValue[5:7]
        day = dataValue[8:10]
        print(year)
        print(month)
        print(day)
        destination = ("/" + str(year) + "/" + months[int(month)-1])
        return destination
  else:
    print("Invalid image type")
    return ("/testing")

def GetDateDirectory(image):
  print("~~Getting destination directory~~")

  print("Using image: " + image) 
  date = re.search("\d\d\d\d\d\d\d\d", image)
  if date:
    date = date.group()
    year = date[0:4]
    month = date[4:6]
    day = date[6:8]
    print(int(month))
    destination = ("/" + str(year) + "/" + months[int(month)-1])
    return destination

  date = re.search("\d\d\d\d-\d\d-\d\d", image)
  if date:
    date = date.group()
    year = date[0:4]
    month = date[5:7]
    day = date[8:10]
    destination = ("/" + str(year) + "/" + months[int(month)-1])
    return destination

  # Move files with unsupported format to separate directory
  else:
    GetDateFromExif(image)
    destination = ("/" + badFormatDirectory)
    print("WARNING: No valid date found")
    return 0

  return destination

  
def MoveImages(listOfImages):
  print("~~Moving images~~")
  
  for image in listOfImages:
    sourcePath = pwd + "/" + image
    dateDirectory = GetDateDirectory(image)
    if dateDirectory:
      destinationPath = pwd + dateDirectory + "/" + image
    else:
      print("It's sorta working :D")
      dateDirectory = GetDateFromExif(sourcePath)
      destinationPath = pwd + dateDirectory + "/" + image
    
    badFormatPath = pwd + "/" + badFormatDirectory + "/" + image
    existingImagePath = pwd + "/" + existingImageDirectory + "/" + image
    
    #print("Old: ", sourcePath)
    #print("New: ", destinationPath)

    if destinationPath == badFormatPath:
      print("WARNING: the file '" + image + "' is not in a valid name format. Moving to 'Unsupported' directory")
      #os.rename(sourcePath, badFormatPath)
    elif os.path.exists(destinationPath):
      print("WARNING: the file '" + image + "' already exists. Moving to Copies directory.")
      #os.rename(sourcePath, existingImagePath)
    else:
      print("bruh")
      os.rename(sourcePath, destinationPath)

def main():
  CreateDirectories()
  MoveImages(GetNewImages())

if __name__ == "__main__":
  main()

