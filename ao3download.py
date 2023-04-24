import AO3
import os.path
import argparse
import re
parser = argparse.ArgumentParser()
parser = argparse.ArgumentParser(description="Accepts an Archive of Our Own link, or a .txt file containing Ao3 links, and downloads the work or series as a requested file type. \n By default, works will download in the same location as this file. \n Series will download in a separate folder. \nAs series and works can share the same ID, this only supports links. \nPLease note that attempts to download large quantities of fanworks may result in being rate-limited by Ao3.")


#### Questions if it's a work or series.
group = parser.add_mutually_exclusive_group()
group.add_argument('--work', action='store_true',  help="Specify to download a singular work or series.")
group.add_argument('--file', action='store_true', help="Specify to download from a text file in the same location as this file.")

#### File type and location. Not optional.
parser.add_argument('path', type=str, help="If downloading a work or series, enter its Ao3 URL. \nIf downloading from a text file, enter the name of the text file (e.g fics.txt)")
parser.add_argument('filetype', type=str, const="PDF", help="Enter a file type out of one of the following: \nAZW3, EPUB, MOBI, PDF, HTML.")

args = parser.parse_args()
path = args.path
filetype = str(args.filetype)

def idSearch(link):
    id = re.findall(r'[A-Za-z]+/[0-9]+', link)
    id = ' '.join(id).replace("/", " " ).split()
    return id

#### WORK DOWNLOAD CODE ####
def workDownload(workLink):
    workLink = AO3.Work(workLink)
    filepath = rf'Archive of Our Own\Works'
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    with open(os.path.join(filepath, (str(workLink.title) + '.' + filetype)), "wb") as file:
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
    filepath = rf'Archive of Our Own\{seriesLink.name}' 
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    print(f"// Commencing the download of {seriesLink.name}.")
    for work in seriesworks:
        with open((os.path.join(filepath, work.title + '.'+ filetype)), "wb") as file:
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
    ficfile = open(str(args.path), 'r')
    lines = ficfile.readlines()
    threads = []
    works = []
    for i in lines:
        workDescriptor = idSearch(i)[0]
        workID = idSearch(i)[1]
        if workDescriptor == "works":
            workDownload(workID)
        elif workDescriptor == "series":
            seriesDownload(workID)
        else:
            print("Something went wrong. \nPlease make sure your links are in the right format, e.g https://archiveofourown.org/<works or series>/<id> ")
         