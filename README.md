# DABS - Dorstijn Automated Building System
DABS is an automated building system for C/C++ projects.
It uses [ninja](https://ninja-build.org/) as a back-end to actually
do the building of the files, while providing a cli interface
for the generating of the file.

## Usage
Some options and and parts in the configuration file overlap,
where ever this is the case the arguments provided to the program
will override the settings in the configuration file.

## Setting configure.yaml
As mentioned before  are
manditory lists in `configure.yaml`. Optional added values are:
`includes, search_directories, libraries`

| includes              | List of folders to include                    |
| search\_directories   | List of folders where libraries are located   |
| libraries             | List of libraries to add                      |
| cc                    | The cc compiler to be used, default: gcc      |
| cxx                   | The cxx compiler to be used, default: g++     |
| source                | Source folder, overridden by -s               |
| build\_file           | File that will be build by the program        |

## History
When creating [DES](http://github.com/Drvanon/DES), we found
`make` to be archaic in it's use. After some research we decided
on using `ninja` as our building system of choice. Ninja suggests
creating an automated building system for generating it's build
files.

We found [this gist](https://gist.github.com/orlp/95f2b788bf02b7041cf7)
best suited our needs, so we used it as a template to create our
own automated building system. You are now looking at the result.
