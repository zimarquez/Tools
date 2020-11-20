import os
import re
from pathlib import Path
from datetime import datetime

pwd = os.path.dirname(os.path.realpath(__file__))
currentYear = datetime.now().year
months = ["01-January","02-February","03-March","04-April",
          "05-May","06-June","07-July","08-August",
          "09-September","10-October","11-November","12-December"]
fileTypes = (".jpg",".jpeg",".png",".mp4")

def CreateDirectories():
  print("~~Checking year directories~~")

  for year in range (2000, currentYear+1):
    if os.path.isdir(str(year)):
      print("Directory " + str(year) + " already exists")
    else:
      print("Creating directory " + str(year))
      os.makedirs(str(year))
      for month in months:
        os.makedirs(str(year) + "/" + month)

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
  else:
    print("ERROR: No valid date found")

  
def MoveImages(listOfImages):
  print("~~Moving images~~")
  
  for image in listOfImages:
    sourcePath = pwd + "/" + image
    destinationPath = pwd + GetDateDirectory(image) + "/" + image;
    #print("Old: ", sourcePath)
    #print("New: ", destinationPath)
    if os.path.exists(destinationPath):
      print("WARNING: " + image + " already exists. Skipping.")
    else:
      os.rename(sourcePath, destinationPath)

def main():
  CreateDirectories()
  MoveImages(GetNewImages())

if __name__ == "__main__":
  main()

