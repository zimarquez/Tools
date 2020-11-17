import os
from pathlib import Path
from datetime import datetime

print("Py Start")

pwd = os.path.dirname(os.path.realpath(__file__))
currentYear = datetime.now().year
months = ["January","February","March","April",
          "May","June","July","August",
          "September","October","November","December"]

print("Checking year directories")
for year in range (2000, 2002): # replace the second year with 'currentYear'
  if os.path.isdir(str(year)):
    print("Directory " + str(year) + " already exists")
  else:
    print("Creating directory " + str(year))
    os.makedirs(str(year))
    num = 1
    for month in months:
      os.makedirs(str(year) + "/" + str(num) + "-" + month)
      num += 1
    # This line should work, but it doesn't.....
    #os.chmod(str(pwd) + "/" + str(year), 0o666)

  
print(pwd)
print(currentYear)
