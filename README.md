# DABS - Dorstijn Automated Building System
DABS is an automated building system for C/C++ projects.
(Currently the cpp part is still uder construction.) It
uses [ninja](https://ninja-build.org/) as a back-end to actually
do the building of the files, while providing a cli interface
for the generating of the file.

## Usage
1. Create a 'configure.yaml' in your projects directory.
2. Make sure that at least the following mappings:
    * `inlcudes`
    * `search_directories`
    * `libraries`
3. `$ dabs.py`
4. `$ ninja`

## History
When creating [DES](http://github.com/Drvanon/DES), we found
`make` to be archaic in it's use. After some research we decided
on using `ninja` as our building system of choice. Ninja suggests
creating an automated building system for generating it's build
files.

We found [this gist](https://gist.github.com/orlp/95f2b788bf02b7041cf7)
best suited our needs, so we used it as a template to create our
own automated building system. You are now looking at the result.
