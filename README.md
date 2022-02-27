# Ultimate Library

Ultimate Library is a collection of libraries and programs useful for parsing and collecting statistics on message pools in BSL (Biblioteca Statale Loenense) format. The main program allows you to collect useful statistics via a command line interface. The commands to know are:
```
q: quit
b: go back to the general screen
h: display help about this screen
```

The program is organized into screens (it. schermata) that collect a number of related commands (e.g., screen for authors, screen for countries, screen for dates). The first screen you encounter is the general screen.

# Install

## Windows

On Windows you can install [python 3](https://www.microsoft.com/en-us/p/python-39/9p7qfqmjrfp7) from the Microsoft Store. For the best experience I also recommend installing [Windows Terminal](https://www.microsoft.com/en-us/p/windows-terminal/9n0dx20hk701?rtc=1&activetab=pivot:overviewtab).

Then download the [zip file](https://github.com/LoZack19/ultimate_library/archive/refs/heads/master.zip) for this project and unzip wherever you want. Then enter the folder within the terminal, preferably using PowerShell (either by navidating with the `dir` and `cd` command or by navigating with the windows `explorer.exe` file manager and right-clicking `open in Windows Terminal` when inside the project folder) and run:

```PowerShell
> pip install -r "requirements.txt"     # to install dependencies
                                        # only run before running the program for the firs time
> python main.py                        # to run the program
```

_**Note**: The text following the `#` (including the symbol) is a comment and should not be reported in the terminal.
Only commands should be reported in the terminal._

## Linux

In order to be able to run the program you will need python 3 installed on your machine. Follow online the instructions to download python 3 on your Linux distribution.

To install the program download this repository from github and configure the dependecie by simply write into the terminal (in a folder of you choise):
```bash
$ git clone https://github.com/LoZack19/ultimate_library
$ cd ultimate_library
$ pip install -r "date/requirements.txt"
```

This script installs all the dependencies your program will need to run. Dependencies are listed in `requirements.txt` in the `data/` folder

To run the program simply type:
```
$ python main.py
```

# Usage

## The config file

The `config.yaml` file contains important information that the program needs to run properly. You can have fun experimenting with the options, but only a few are the ones you need to know to use the program correctly.

### pool

The `pool` option points to the backup file of the library where the messages to be parsed are contained. If those messages are a direct telegram bacup, the `raw` option should be `True`. If the messages are in a format which is already parsed, for example the output of a `save works` command in the main program, then the `raw` option should be `False`. In most cases, you'll use just plain Telegram backups in json, so `raw` should be `True` in most cases.

### channel

This is the channel where the bot will post the works in bsl format when the command `!` is sent. If no token was set, or if the bot associated with that toke was not inside the chhannel where the messages were supposed to be sent, the operation will fail.

### token

Token poins to the file containing the token of the bot. The token of the bot is a is a unique code associated with each bot that allows you to command it through the telegram bot api. Never share the token if you don't want others to be able to control the bot however they want.

This is why the token information for my bot was not published on this repo and I could not directly put the token inside the config file, but I had to put it inside I file I had to keep private on my computer.

### other

Do not touch the other options if you don't know what you're doing.

## General screen

The program is organized in screens. Three options are valid in all screens:
```
b: go back to the general screen
h: get help about the screen
q: quit the program
```

The help screen should be enough to guide you through the program functionalities. If you don't find it clear enough report it as explained later in this text.

# Bug report

If you:

- find a bug
- manage to crash the application
- want a new feature
- find something not too clear

Send any report to @LoZack19 in the issues of github, or contact me on telegram - if you don't know how to contact me on telegram, this means you shouldn't ❤️.
