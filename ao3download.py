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
filetype = settings["file_type"]

parser = argparse.ArgumentParser()
parser = argparse.ArgumentParser(prog="Ao3 Downloader", 
                                 description="Accepts an Archive of Our Own link, or a .txt file containing Ao3 links, and downloads the work or series as a requested file type in a specified location. Default settings can be viewed in settings.json. Source code can be found here: https://github.com/phthallo/ao3downloader")
# save file location and file type
parser.add_argument('-save', nargs = "?", help="Specify a folder to save files in. This will be remembered.", default=save)
parser.add_argument('-filetype', nargs = "?", choices = [
    "azw3", 
    "epub", 
    "mobi", 
    "pdf", 
    "html"], help="Specify a file type out of one of the following: \nazw3, epub, mobi, pdf, html. This will be remembered.", default=filetype)

#### Questions if it's a work or series.
group = parser.add_mutually_exclusive_group()
group.add_argument('--work', action='store_true',  help="Specify to download a singular work or series.")
group.add_argument('--file', action='store_true', help="Specify to download from a text file.")

#### Location of fics to be downloaded. Not optional.
parser.add_argument('path', type=str, help="If downloading a work or series, enter its Ao3 URL. \nIf downloading from a text file, enter the location of the text file")
args = parser.parse_args()
path = args.path
if save == "C:/Users/USERNAME/Documents/Archive of Our Own": #if the save location is the default
    save = f"C:/Users/{os.getlogin()}/Documents/Archive of Our Own" #replace it with the actual username.
else:
     save = args.save
filetype = (args.filetype).lower()

# dump settings.
with open('settings.json', "w") as json_file:
    settings = {"save_location": save,
                "file_type": filetype}
    json.dump(settings, json_file)
    json_file.close()

#retrieve two things: work/series status and id of the given link.
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
    with open(os.path.join(filesave, workTitle + '.' + filetype), "wb") as file:
        file.write(workLink.download(filetype))
    print(f"{workLink.title} was downloaded.")

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
        with open(str(os.path.join(filesave, workTitle + '.'+ filetype)), "wb") as file:
            file.write(work.download(filetype))
            print(f"{work.title} was downloaded. {seriesworks.index(work)+1} out of {len(seriesworks)} series downloads complete.")
    print(f"// The series '{seriesLink.name}' was downloaded.")

if args.work:
    workDescriptor = idSearch(path)[0]
    workID = idSearch(path)[1]
    if workDescriptor == "works":
        workDownload(workID)
    elif workDescriptor == "series":
        seriesDownload(workID)
    else:
        print("Something went wrong. Did you mean to enter in --file instead?")

if args.file:
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
            print("Something went wrong. \nPlease make sure your links are in the right format, e.g https://archiveofourown.org/<works or series>/<id> ")
         
