# ao3downloader
Extremely basic CLI for downloading fanworks from archiveofourown.org in a variety of supported formats. This is largely for my own use, but figured I'd put it up anyways.

## Prerequisites
- [Python 3 or higher](https://www.python.org/downloads/)


- [ArmindoFlores' ao3_api](https://github.com/ArmindoFlores/ao3_api) (`pip install ao3_api`)


## Instructions for Use
- Clone the repository. 
- 
`git clone https://github.com/phthallo/ao3downloader/`

- Run `cmd` in the location of the downloaded file.

```
usage: Ao3 Downloader [-h] [-save [SAVE]] [-filetype [{azw3,epub,mobi,pdf,html}]] [--work | --file] path

Accepts an Archive of Our Own link, or a .txt file containing Ao3 links, and downloads the work or series as  
a requested file type in a specified location. Default settings can be viewed in settings.json. Source code   
can be found here: https://github.com/phthallo/ao3downloader

positional arguments:
  path                  If downloading a work or series, enter its Ao3 URL. If downloading from a text file,  
                        enter the location of the text file

options:
  -h, --help            show this help message and exit
  -save [SAVE]          Specify a folder to save files in. This will be remembered.
  -filetype [{azw3,epub,mobi,pdf,html}]
                        Specify a file type out of one of the following: azw3, epub, mobi, pdf, html. This    
                        will be remembered.
  --work                Specify to download a singular work or series.
  --file                Specify to download from a text file.
 ```
  
## Example usage
### Downloading a singular fanwork
`python ao3download.py -filetype pdf --work https://archiveofourown.org/works/17400464`

This will save the fanfiction as `Stag Beetles and Broken Legs.pdf` at the following path: `C:/Users/USERNAME/Documents/Archive of Our Own/Works`. 

### Downlading a series
`python ao3download.py -filetype pdf --work https://archiveofourown.org/series/1264421`

This will save the series as separate `.pdf` files for each work at the following path: `C:/Users/%username%/Documents/Archive of Our Own/Stag Beetles and Broken Legs`. 

### Downloading from a text file
#### textfile.txt
```
https://archiveofourown.org/works/17616617
https://archiveofourown.org/works/17616821
https://archiveofourown.org/works/17616881
https://archiveofourown.org/works/17623268
```
where all works are separated by newlines.

`python ao3download.py --file C:/Users/USERNAME/foo/bar/path/textfile.txt`

This will open the specified text file and save all files as `.pdf` files in the `/Works` folder. 
If there are series located in this text file as well, they will be saved at `Archive of Our Own\<series name>\` instead.

## Changing default settings
You can update the default settings for save location and filetype by using the following commands in conjunction with standard usage. This information will be stored in the settings.json file.

`-save [SAVE]` [default is C:/Users/USERNAME/Documents/Archive of Our Own]
`-filetype [{azw3,epub,mobi,pdf,html}]` [default is PDF]

## To-Do List
- [x] Allow user to customise locations of saved files.

- [x] Allow user to enter own path for text file. 

- [ ] Add author names to be added to file names.

- [ ] Allow user to search the archive and download from there.

- [ ] Merge separated --file/--work arguments.

- [ ] ...make the entire thing neater

