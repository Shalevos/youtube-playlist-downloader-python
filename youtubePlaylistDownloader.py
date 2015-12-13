"""
The following code will download a youtube playlist to a desired directory on your computer.
Notes: selenium and firefox must be installed
"""
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.webdriver import FirefoxProfile
import magic
import time
import re

"""
This function checks for any ongoing downloads in the download directory.
"""
def isDownloadDone():
    #Goes through all files in downloadDir
    print("Hi")
    for path,subdirs,files in os.walk(downloadDir):
        print("This")
        for filename in files:
            print("is")
            # Checks if there a file with .part extension
            #if(filename.endswith(".part")):
            print(magic.from_file(downloadDir + filename, mime = True))
            if(magic.from_file(downloadDir + filename, mime = True) != "audio/mpeg"):
                return False
    return True


"""
This function beautifies a file name.
Feel free to change this to a format you like.
"""
def formatName(filename):
    newName = re.sub("[\(\[].*?[\)\]]", "", filename) # removes anything enclosed in () or []
    newName = re.sub("lyrics","",newName)
    newName = re.sub("Lyrics","",newName)
    newName = re.sub("LYRICS","",newName)
    newName = re.sub("HD","",newName)
    newName = re.sub("HQ","",newName)
    newName = re.sub("  "," ",newName)# gets rid of any double spaces formed
    newName = newName.strip()
    if newName[-1] == '.' or newName[-1] == '_':
        newName = newName[:-1]
    newName = newName + ".mp3"
    return newName

# We will be timing the process
t0 = time.time()

# Change this to the folder path you would like it to download to.
downloadDir = "~/Music/Rock/"
# Change this to the playlist URL
playlistURL = "https://www.youtube.com/playlist?list=PLEv648BeDhnIfnmKNM9yQ-9rbwBaEwktu"
fp = webdriver.FirefoxProfile()

# Some profile settings.
fp.set_preference("browser.download.folderList",2)
fp.set_preference("browser.download.manager.showWhenStarting",False)
fp.set_preference("browser.download.dir", downloadDir)
fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "audio/mpeg")

driver = webdriver.Firefox(firefox_profile=fp)
# First we will go to the playlist URL
driver.get(playlistURL)

# This will expand the list to show all the songs
moreThan100 = True
while (moreThan100):
    try:
        loadMore = driver.find_element_by_class_name("load-more-text")
        loadMore.click()
        time.sleep(2)
    except:
        moreThan100 = False

# We now create a list with all the videos' URLs
videoList = []
ytDomain = "https://www.youtube.com/watch?v="
linkElements = driver.find_elements_by_class_name("pl-video-title-link")
for link in linkElements:
    videoList.append(link.get_attribute("href")[32:43])
print (videoList)
print (len(videoList))

# Now for the download section:
i = 1
driver.get("http://www.youtube-mp3.org/")
for video in videoList:
    textField = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID ,"youtube-url")))
    print (ytDomain+video)
    textField.clear()
    textField.send_keys(ytDomain+video)
    textField.send_keys(Keys.RETURN)
    try:
        downloadLink= WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Download"))
        )
        downloadLink.click()
        print (str(i) + " of " + str(len(videoList)))
    except:
        print ("Not all files have been dowloaded")
    i=i+1

#-----------Renaming Files-----------------

#while(isDownloadDone() == False):
 #   time.sleep(0.5)
print(isDownloadDone())

for path, subdirs, files in os.walk(downloadDir):
   for filename in files:
       print(filename)
       nName = formatName(filename[:-4])
       print (nName)
       os.rename(downloadDir + filename,downloadDir + nName)
    
print (time.time() - t0)
