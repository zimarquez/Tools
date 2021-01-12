import os
import re
import exiftool
from PIL import Image
from PIL.ExifTags import TAGS
from pathlib import Path
from datetime import datetime

pwd = os.path.dirname(os.path.realpath(__file__))
currentYear = datetime.now().year
months = ["01-January","02-February","03-March","04-April","05-May","06-June","07-July",
          "08-August", "09-September","10-October","11-November","12-December"]
fileTypes = (".jpg",".jpeg",".png",".mp4",".JPG",".MOV")
badFormatDirectory = "Unsupported Format"
existingFileDirectory = "Copies"
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
  if os.path.isdir(existingFileDirectory):
    print("Directory " + existingFileDirectory + " already exists")
  else:
    print("Creating directory " + existingFileDirectory)
    os.makedirs(existingFileDirectory)

  # Create directory for files needing manual organization
  if os.path.isdir(unknownDateDirectory):
    print("Directory " + unknownDateDirectory + " already exists")
  else:
    print("Creating directory " + unknownDateDirectory)
    os.makedirs(unknownDateDirectory)

  # This line should work, but it doesn't.....
  #os.chmod(str(pwd) + "/" + str(year), 0o666)

def GetNewFile():
  print("~~Making image list~~")

  listOfAllFiles = os.listdir(pwd)
  listOfFiles = []
  for f in listOfAllFiles:
    if f.endswith(fileTypes):
      listOfFiles.append(f)
    
  return listOfFiles

def IncrementFileName(fileName, number):
  newFileName = ""
  for x in fileName:
    if x == '.':
      newFileName = newFileName + "_COPY_(" + str(number) + ")"
    newFileName = newFileName + x
  
  return newFileName

def GetOldestDate(createDate, modifyDate): 
  if createDate == None:
    return modifyDate
  elif modifyDate == None:
    return -1
  elif createDate[0:4] == modifyDate[0:4]:
    if createDate[5:7] > modifyDate[5:7]:
      return modifyDate
    else:
      return createDate
  elif createDate[0:4] > modifyDate[0:4]:
    return modifyDate
  else:
    return createDate

# FileModifyDate
# CreateDate
def GetExifData(fileName):
  sourcePath = pwd + "/" + fileName
  createDateTag = "CreateDate"
  fileModifyDateTag = "FileModifyDate"

  with exiftool.ExifTool() as et:
    createDate = et.get_tag(createDateTag, sourcePath)
    fileModifyDate = et.get_tag(fileModifyDateTag, sourcePath)
    oldestDate = GetOldestDate(createDate, fileModifyDate)

    year = oldestDate[0:4]
    month = oldestDate[5:7]
    day = oldestDate[8:10]
    #print("Year: " + year)
    #print("Month: " + month)
    #print("Day: " + day)
    destination = ("/" + str(year) + "/" + months[int(month)-1])
  
  return destination

def GetDateFromFileData(currentFile):
  print("Getting path from exif")
  destinationPath = GetExifData(currentFile)
  return destinationPath

def GetDateFromFileName(imageName):
  print("~~Getting destination directory~~")

  print("Using image: " + imageName)
  # yyyymmdd
  date = re.search("\d\d\d\d\d\d\d\d", imageName)
  if date:
    date = date.group()
    year = date[0:4]
    month = date[4:6]
    day = date[6:8]
    print(int(month))
    destination = ("/" + str(year) + "/" + months[int(month)-1])
    return destination
  # yyyy-mm-dd
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

  
def MoveFiles(listOfFiles):
  print("~~Moving images~~")
  
  for fileName in listOfFiles:

    # Extract date from file name
    dateDirectory = GetDateFromFileName(fileName)
    if dateDirectory != -1:
      destinationPath = pwd + dateDirectory + "/" + fileName
    # Extract date from file data
    else:
      dateDirectory = GetDateFromFileData(fileName)
      if dateDirectory == -1:
        print("The file '" + fileName + "' could not be organized. Moving to '" + unknownDateDirectory + "' directory")
        dateDirectory = "/" + unknownDateDirectory
      destinationPath = pwd + dateDirectory + "/" + fileName
    
    badFormatPath = pwd + "/" + badFormatDirectory + "/" + fileName
    existingFilePath = pwd + "/" + existingFileDirectory + "/" + fileName

    if destinationPath == badFormatPath:
      print("WARNING: the file '" + fileName + "' is not in a valid name format. Moving to 'Unsupported' directory")
      #os.rename(sourcePath, badFormatPath)
    elif os.path.exists(destinationPath):
      print("WARNING: the file '" + fileName + "' already exists in " + str(destinationPath) + ". Moving to Copies directory.")
      i = 1
      while os.path.exists(existingFilePath):
        newFileName = IncrementFileName(fileName, i)
        existingFilePath = pwd + "/" + existingFileDirectory + "/" + newFileName
        i += 1
      #os.rename(sourcePath, existingFilePath)
    else:
      print("bruh")
      #os.rename(sourcePath, destinationPath)

def main():
  CreateDirectories()
  MoveFiles(GetNewImages())

if __name__ == "__main__":
  main()

