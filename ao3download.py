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
                                 description="Accepts an Archive of Our Own link, a .txt file containing Ao3 links or login credentials to access user bookmarks, and downloads the works/series. Default settings can be viewed in settings.json. Source code and example usage can be found here: https://github.com/phthallo/ao3downloader")
# save file location and file type
parser.add_argument('-save', nargs = "?", help="Specify a folder to save files in. This will be remembered.", default=save)
parser.add_argument('-format', nargs = "?", choices = [
    "azw3", 
    "epub", 
    "mobi", 
    "pdf", 
    "html"], help="Specify a file type out of one of the following: \nazw3, epub, mobi, pdf, html. This will be remembered.", default=format)
parser.add_argument('-login', nargs="?", help="Specify your Ao3 login to download fanworks from your bookmarks or from restricted works, in the following format: username:password. This will be remembered.", default=login)
#### Questions if it's to be downloaded from a url, file or from bookmarks.
parser.add_argument('-source', nargs = "?", choices = [
    "url",
    "file",
    "bookmarks"], help="Specify to download from an Ao3 work/series URL, from a file, or from your bookmarks. ")

#### Location of fics to be downloaded.
parser.add_argument('path', type=str, help="If downloading a work or series, enter its Ao3 URL. If downloading from a text file, enter the location of the text file. If downloading from bookmarks, enter '+'")

#### Argument parsing
args = parser.parse_args()
source = args.source 
format = args.format
if args.login == ["DEFAULT", "DEFAULT"]: #if the person hasn't set a username and password.
    print("Please set your login using `-login yourusername:yourpassword` as one of your arguments.")
else: # if user has already set their login
    login = (re.sub(":", " ", args.login, 1)).split() #splits input into username and password based on the location of the first semicolon. ao3 can't have semicolons in the username, so this should work.
    sess = AO3.Session(login[0], login[1]) # load session: needed for restricted works and for bookmarked works
    print("Login credentials have been updated.")

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
    try:
        workLink = AO3.Work(workLink, session=sess)
    except:
        workLink.set_session(sess)
    filesave = f'{save}/Works'
    workTitle = stripPunctuation(workLink.title)
    createFolder(filesave)
    with open(os.path.join(filesave, workTitle + '.' + format), "wb") as file:
        file.write(workLink.download(format))
    print(f"'{workLink.title}' was downloaded.")

#### SERIES DOWNLOAD CODE ####
def seriesDownload(seriesLink):
    try:
        seriesLink = AO3.Series(seriesLink, session=sess)
    except:
        seriesLink.set_session(sess)
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

def overallDownload(Link):
    workDescriptor = idSearch(Link)[0]
    workID = idSearch(Link)[1]
    if workDescriptor == "works":
        workDownload(workID)
    elif workDescriptor == "series":
        seriesDownload(workID)

if source == "url":
    try:
        overallDownload(path)
    except:
        print("Something went wrong.")
        
elif source == "file":
    with open(path, 'r') as ficfile:
        lines = ficfile.readlines()
    for i in lines:
        try:
            overallDownload(i)
        except:
            print("Something went wrong. \nPlease make sure your links are in the right format, e.g https://archiveofourown.org/<works or series>/<id>.")

if source == "bookmarks" and path == "+":
    bookmarks = sess.get_bookmarks(use_threading=True)
    print(f"Loading {sess.bookmarks} bookmarks...")
    for i in bookmarks:
        i.set_session(sess)
        i.reload()
        try:
            workDownload(i)
        except:
            seriesDownload(i)
    print(f"{sess.bookmarks} bookmarks were downloaded.")