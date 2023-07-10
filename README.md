# ao3downloader
Extremely basic CLI for downloading fanworks from archiveofourown.org in a variety of supported formats. This is largely for my own use, but figured I'd put it up anyways.

## Prerequisites
- [Python 3 or higher](https://www.python.org/downloads/)


- [ArmindoFlores' ao3_api](https://github.com/ArmindoFlores/ao3_api) (`pip install ao3_api`)


## Instructions for Use
- Clone the repository. 

`git clone https://github.com/phthallo/ao3downloader/`

- Run `cmd` in the location of the downloaded file.

```
usage: Ao3 Downloader [-h] [-save [SAVE]] [-format [{azw3,epub,mobi,pdf,html}]] [-login [LOGIN]]
                      [-source [{url,file,bookmarks}]]
                      path

Accepts an Archive of Our Own link, or a .txt file containing Ao3 links, and downloads the work or series as a     
requested file type in a specified location. Default settings can be viewed in settings.json. Source code and      
example usage can be found here: https://github.com/phthallo/ao3downloader

positional arguments:
  path                  If downloading a work or series, enter its Ao3 URL. If downloading from a text file,       
                        enter the location of the text file. If downloading from bookmarks, enter '+'

options:
  -h, --help            show this help message and exit
  -save [SAVE]          Specify a folder to save files in. This will be remembered.
  -format [{azw3,epub,mobi,pdf,html}]
                        Specify a file type out of one of the following: azw3, epub, mobi, pdf, html. This will    
                        be remembered.
  -login [LOGIN]        Specify your Ao3 login to download fanworks from your bookmarks or from restricted works,  
                        in the following format: username:password. This will be remembered.
  -source [{url,file,bookmarks}]
                        Specify to download from an AO3 work/series URL, from a file, or from your bookmarks. 
 ```
  
## Example usage
### Downloading a singular fanwork
Downloading works and series can both be done with this command. 

`python ao3download.py -source url https://archiveofourown.org/works/17400464`

This will save the fanfiction as `Stag Beetles and Broken Legs.pdf` at the following path: `C:/Users/USERNAME/Documents/Archive of Our Own/Works`. Individual fanfics will always be saved under a 'Works' folder within whatever save location you set.

`python ao3download.py -source url https://archiveofourown.org/series/1264421`

This will save the series as separate .pdf files for each work at the following path: `C:/Users/USERNAME/Documents/Archive of Our Own/entomology`. Series will always be saved under a folder of the series' name within whatever save location you set.  

### Downloading from a text file
#### textfile.txt
```
https://archiveofourown.org/works/17616617
https://archiveofourown.org/works/17616821
https://archiveofourown.org/works/17616881
https://archiveofourown.org/works/17623268
```
where all works are separated by newlines.

`python ao3download.py -source file C:\Users\USERNAME\foo\bar\textfile.txt`


## Changing default settings
You can update the default settings for save location and filetype by using the following commands in conjunction with standard usage. This information will be stored in the settings.json file. **Your login is stored in plaintext since it's run on your device, so do not share your `settings.json` file with anyone.**

`-save [SAVE]` [default is C:/Users/USERNAME/Documents/Archive of Our Own]

`-format [{azw3,epub,mobi,pdf,html}]` [default is PDF]

`-login [LOGIN]` [default needs to be changed to access authorised works or bookmarks. Entered in the format username:password]

## Saving from your bookmarks
In order to save from your bookmarks, you must have set your login using the `-login username:password` command. Even if you don't intend on saving from bookmarks, it's highly recommended that you do so in order to access works that may be restricted to logged-in users only. 

`python ao3download.py -login username:password -source bookmarks +` 

If setting your login for the first time or updating it, the login argument is compulsory for the download to work. Otherwise, it can be excluded.
- Please note that large bookmark quantities as well as works that are exceptionally long will of course take a long time to download or result in ratelimits. I've only tried downloading my ~190 bookmarks in the background, which was successful.
- Also note that the downloader doesn't seem to pull series from bookmarks, which seems to be an issue with the API used used. Downloading series using the `-work` command still works.  

## To-Do List
- [x] Allow user to customise locations of saved files.

- [x] Allow user to enter own path for text file. 

- [ ] Add author names to be added to file names.

- [ ] Allow user to search the archive and download from there. 

- [x] Merge separated --file/--work arguments.

- [ ] ...refactoring everything 

- [ ] Add appropriate error messsages.

