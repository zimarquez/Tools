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
fileTypes = (".jpg",".jpeg",".png",".mp4",".JPG",".MOV",".MPG")
existingFileDirectory = "Copies"
unknownDateDirectory = "Unknown Date"

def CreateDirectories():
  print("~~Checking year directories~~")

  # Create year directories
  for year in range (2000, currentYear+1):
    if not os.path.isdir(str(year)):
      print("Creating directory " + str(year))
      os.makedirs(str(year))
      for month in months:
        os.makedirs(str(year) + "/" + month)

  # Create directory for exisiting images
  if not os.path.isdir(existingFileDirectory):
    print("Creating directory " + existingFileDirectory)
    os.makedirs(existingFileDirectory)

  # Create directory for files needing manual organization
  if not os.path.isdir(unknownDateDirectory):
    print("Creating directory " + unknownDateDirectory)
    os.makedirs(unknownDateDirectory)

def GetNewFiles():
  print("~~Making file list~~")
  listOfAllFiles = os.listdir(pwd)
  listOfFiles = []
  for f in listOfAllFiles:
    if f.endswith(fileTypes):
      listOfFiles.append(f)
    
  return listOfFiles

def IncrementFileName(fileName, number):
  newFileName = ""
  for character in fileName:
    if character == '.':
      newFileName = newFileName + "_COPY_(" + str(number) + ")"
    newFileName = newFileName + character
  
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

def GetDateFromFileData(currentFile):
  print("Checking file data for date...")
  sourcePath = pwd + "/" + currentFile
  destinationPath = -1
  createDateTag = "CreateDate"
  fileModifyDateTag = "FileModifyDate"

  with exiftool.ExifTool() as et:
    createDate = et.get_tag(createDateTag, sourcePath)
    fileModifyDate = et.get_tag(fileModifyDateTag, sourcePath)
    oldestDate = GetOldestDate(createDate, fileModifyDate)

    year = oldestDate[0:4]
    month = oldestDate[5:7]
    day = oldestDate[8:10]
    print("Year: " + year)
    print("Month: " + month)
    print("Day: " + day)
    destinationPath = (str(year) + "/" + months[int(month)-1])

  return destinationPath

def GetDateFromFileName(fileName):
  print("Checking file name for date...")
  # yyyymmdd
  date = re.search("\d\d\d\d\d\d\d\d", fileName)
  if date:
    date = date.group()
    year = date[0:4]
    month = date[4:6]
    day = date[6:8]
    print(int(month))
    destination = (str(year) + "/" + months[int(month)-1])
    return destination

  # yyyy-mm-dd
  date = re.search("\d\d\d\d-\d\d-\d\d", fileName)
  if date:
    date = date.group()
    year = date[0:4]
    month = date[5:7]
    day = date[8:10]
    destination = (str(year) + "/" + months[int(month)-1])
    return destination

  # Move files with unsupported format to separate directory
  print("No date found in file name")
  return -1
  
def MoveFiles(listOfFiles):
  print("~~Moving images~~")
  
  for fileName in listOfFiles:
    print("Using image: " + fileName)
    # Extract date from file name
    dateDirectory = GetDateFromFileName(fileName)
    # Extract date from file data
    if dateDirectory == -1:
      dateDirectory = GetDateFromFileData(fileName)
      if dateDirectory == -1:
        print("WARNING: no date found for '" + fileName + "' Moving to '" + unknownDateDirectory + "' directory")
        dateDirectory = unknownDateDirectory
    
    destinationPath = pwd + "/" + dateDirectory + "/" + fileName
    existingFilePath = pwd + "/" + existingFileDirectory + "/" + fileName

    if os.path.exists(destinationPath):
      print("WARNING: the file '" + fileName + "' already exists in " + str(destinationPath) + ". Moving to Copies directory.")
      i = 1
      while os.path.exists(existingFilePath):
        newFileName = IncrementFileName(fileName, i)
        existingFilePath = pwd + "/" + existingFileDirectory + "/" + newFileName
        i += 1
      #os.rename(sourcePath, existingFilePath)
    else:
      print("Moving file: '" + fileName + "' to '" + dateDirectory)
      #os.rename(sourcePath, destinationPath)

def main():
  CreateDirectories()
  MoveFiles(GetNewFiles())

if __name__ == "__main__":
  main()

