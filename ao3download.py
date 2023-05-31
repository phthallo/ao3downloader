# TO DO 
# Merge -work/series and -file argument to instead be a parameter which accepts three arguments (url/file/bookmarks)
# [x] Argument merged, just need to fix up everything else.
# Add users login functionality to save works from bookmarks 
# [x] Allow user to enter login IT'S STORED IN PLAINTEXT DON'T SHARE YOUR FILES
# Update readme
# [X] Fixed inconsistency with apostrophes in series and work downloads

import AO3
import os.path
import argparse
import re
import json
# import default settings
with open('settings.json') as json_file:
    settings = json.load(json_file)
    json_file.close()
save = settings["save_location"]
format = settings["format"]
login = settings["login"]

parser = argparse.ArgumentParser()
parser = argparse.ArgumentParser(prog="Ao3 Downloader", 
                                 description="Accepts an Archive of Our Own link, or a .txt file containing Ao3 links, and downloads the work or series as a requested file type in a specified location. Default settings can be viewed in settings.json. Source code and example usage can be found here: https://github.com/phthallo/ao3downloader")
# save file location and file type
parser.add_argument('-save', nargs = "?", help="Specify a folder to save files in. This will be remembered.", default=save)
parser.add_argument('-format', nargs = "?", choices = [
    "azw3", 
    "epub", 
    "mobi", 
    "pdf", 
    "html"], help="Specify a file type out of one of the following: \nazw3, epub, mobi, pdf, html. This will be remembered.", default=format)
parser.add_argument('-login', nargs="?", help="Specify your Ao3 login to download fanworks from your bookmarks, in the following format: username:password. This will be remembered.", default=login)
#### Questions if it's a work or series.
parser.add_argument('-source', nargs = "?", choices = [
    "url",
    "file",
    "bookmarks"], help="Specify to download from an AO3 work/series URL, from a file, or from your bookmarks.")

#### Location of fics to be downloaded. Not optional.
parser.add_argument('path', type=str, help="If downloading a work or series, enter its Ao3 URL. If downloading from a text file, enter the location of the text file. If downloading from bookmarks, enter '+'")

#### Argument parsing
args = parser.parse_args()
source = args.source 
format = args.format
if args.login == ["DEFAULT", "DEFAULT"] and source == "bookmarks": #if the person is trying to access their bookmarks but they haven't set a username and password, prompt them to.
    print("Before using this command, set your login using `python ao3download.py -login yourusername:yourpassword`")
    quit()
elif args.login != ["DEFAULT", "DEFAULT"]: #if the person is just trying to set their login, regex the : out and makes it a list.
    login = (re.sub(":", " ", args.login, 1)).split() #splits input into username and password based on the location of the first semicolon. ao3 can't have semicolons in the username, so this should work.
    print("Login credentials recorded.")
path = args.path
if save == "C:/Users/DEFAULT/Documents/Archive of Our Own": #if the save location is the default
    save = f"C:/Users/{os.getlogin()}/Documents/Archive of Our Own" #replace it with the actual username of the profile. Originally set as %username%, but that was interpreted literally and started creating files in the Users folder.
else:
     save = args.save 

# dump settings.
with open('settings.json', "w") as json_file:
    settings = {"save_location": save,
                "format": format,
                "login": login}
    json.dump(settings, json_file)
    json_file.close()

#retrieve two things: work/series status and id of the given link and returns as list. 
def idSearch(link):
    id = re.findall(r'[A-Za-z]+/[0-9]+', link)
    id = ' '.join(id).replace("/", " " ).split()
    return id

#strip punctuation that cannot be in file names from the work's title.
def stripPunctuation(worktitle): 
    forbiddenPunc = '''\/:*?"<>|'''
    for character in worktitle:
        if character in forbiddenPunc:
            worktitle = worktitle.replace(character, "")
    return worktitle

#check if save folder exists
def createFolder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

#### WORK DOWNLOAD CODE ####
def workDownload(workLink):
    workLink = AO3.Work(workLink)
    filesave = f'{save}/Works'
    workTitle = stripPunctuation(workLink.title)
    createFolder(filesave)
    with open(os.path.join(filesave, workTitle + '.' + format), "wb") as file:
        file.write(workLink.download(format))
    print(f"'{workLink.title}' was downloaded.")

#### SERIES DOWNLOAD CODE ####
def seriesDownload(seriesLink):
    seriesLink = AO3.Series(seriesLink)
    seriesworks = []
    seriesthreads = []
    for work in seriesLink.work_list:
        seriesworks.append(work)
        seriesthreads.append(work.reload(threaded=True))
    for thread in seriesthreads:
        thread.join()
    filesave = rf'{save}/{seriesLink.name}' 
    createFolder(filesave)
    print(f"// Commencing the download of {seriesLink.name}.")
    for work in seriesworks:
        workTitle = stripPunctuation(work.title)
        with open(str(os.path.join(filesave, workTitle + '.'+ format)), "wb") as file:
            file.write(work.download(format))
            print(f"{work.title} was downloaded. {seriesworks.index(work)+1} out of {len(seriesworks)} series downloads complete.")
    print(f"// The series '{seriesLink.name}' was downloaded.")

if source == "url":
    workDescriptor = idSearch(path)[0]
    workID = idSearch(path)[1]
    if workDescriptor == "works":
        workDownload(workID)
    elif workDescriptor == "series":
        seriesDownload(workID)
    else:
        print("Something went wrong.")
        
elif source == "file":
    with open(path, 'r') as ficfile:
        lines = ficfile.readlines()
    for i in lines:
        workDescriptor = idSearch(i)[0]
        workID = idSearch(i)[1]
        if workDescriptor == "works":
            workDownload(workID)
        elif workDescriptor == "series":
            seriesDownload(workID)
        else:
            print("Something went wrong. \nPlease make sure your links are in the right format, e.g https://archiveofourown.org/<works or series>/<id>.")

if source == "bookmarks" and path == "+":
    print("Bookmarks downloads coming soon.")