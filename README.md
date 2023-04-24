# ao3downloader
Extremely basic CLI for downloading fanworks from archiveofourown.org in a variety of supported formats.

## Prerequisites
[Python 3 or higher](https://www.python.org/downloads/)


[ArmindoFlores' ao3_api](https://github.com/ArmindoFlores/ao3_api) (`pip install ao3_api`)


## Instructions for Use
Download [ao3download.py](https://github.com/phthallo/ao3downloader/blob/main/ao3download.py).

Run `cmd` in the location of the downloaded file.

```
usage: ao3download.py [-h] [--work | --file] path filetype

Accepts an Archive of Our Own link, or a .txt file containing Ao3 links, and downloads the work or series as a
requested file type. By default, works will download in the same location as this file. Series will download in a        
separate folder. As series and works can share the same ID, this only supports links. Please note that attempts to       
download large quantities of fanworks may result in being rate-limited by Ao3.

positional arguments:
  path        If downloading a work or series, enter its Ao3 URL. If downloading from a text file, enter the name of     
              the text file (e.g fics.txt)
  filetype    Enter a file type out of one of the following: AZW3, EPUB, MOBI, PDF, HTML.

options:
  -h, --help  show this help message and exit
  --work      Specify to download a singular work or series.
  --file      Specify to download from a text file in the same location as this file.
 ```
  
## Examples
### Downloading a singular fanwork
`python ao3download.py --work https://archiveofourown.org/works/17400464 pdf`

This will save the fanfiction as `Stag Beetles and Broken Legs.pdf` at the following path: `Archive of Our Own\Works\` relative to the location of the `ao3download.py` file. 

### Downlading a series
`python ao3download.py series https://archiveofourown.org/series/1264421 pdf`

This will save the series as separate `.pdf` files for each work at the following path: `Archive of Our Own\entomology\` relative to the location of the `ao3download.py` file.

### Downloading from a text file
#### textfile.txt
```
https://archiveofourown.org/works/17616617
https://archiveofourown.org/works/17616821
https://archiveofourown.org/works/17616881
https://archiveofourown.org/works/17623268
```
where the text file is located in the same folder as the `ao3download.py` file, and all works are separated by newlines.

`python ao3download.py series textfile.txt pdf`

This will save all works in the text file as `.pdf` files at the following path: `Archive of Our Own\Works\` relative to the location of the `ao3download.py` file.
If there are series located in this text file as well, they will be saved at `Archive of Our Own\<series name>\` instead.

## To-Do List
[ ] Allow user to customise locations of saved files.

[ ] Allow user to enter own path for text file. 

[ ] Add author names to be added to file names.

[ ] Allow user to search the archive and download from there.

