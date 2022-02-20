# Ultimate Library

Ultimate Library is a collection of libraries and programs useful for parsing and collecting statistics on message pools in BSL (Biblioteca Statale Loenense) format. The main program allows you to collect useful statistics via a command line interface. The commands to know are:
The program is organized into screens (it. schermata) that collect a number of related commands (e.g., screen for authors, screen for countries, screen for dates). The first screen you encounter is the general screen.
```
q: quit
b: go back to the general screen
h: display help about this screen
```

# Install (Linux)

To install the program download this repository from github and configure the dependecie by simply write into the terminal (in a folder of you choise):
```bash
$ git clone https://github.com/LoZack19/ultimate_library
$ cd ultimate_library
$ ./configure.sh
```

This script installs all the dependencies your program will need to run. Dependencies are listed in `dependencies.txt` in the `data/` folder

To run the program simply type:
```
$ python main.py
```
