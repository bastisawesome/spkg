# spkg
Simple PacKaGe downloader for FreeBSD.

SPKG is a package downloader inspired by PKG. It contains a subset of the
features found in PKG, including fetching packages, searching for packages in
the repo, and querying information about existing packages. Currently it only
supports the quarterly branch of the FreeBSD repos, though it may be updated
to support other branches.

SPKG works with the following releases of FreeBSD:
- FreeBSD 13
- FreeBSD 12
- FreeBSD 11
- FreeBSD 14

SPKG has only been tested on FreeBSD 13 using the AMD64, quarterly branch. It
may work with other branches, however, there is currently no method of tracking
multiple branches at once.

# Requirements
- Python 3.8+
- Requests
- Appdirs

# Running
SPKG can be run either from source or as a compiled application.

For compilation instructions see [#Building](#Building).

SPKG is a command line application mimicking PKG's interface. It supports a
small subset of PKG's commands and options. It is recommended to run:

`spkg --help`

to learn how to use it. All subcommands and options are documented in the help
command.

## Getting started
The first think you will want to do is run an update to download the current
package database. SPKG will not work without a package database, and if one is
not found, you will be asked to run an update automatically. If you decline, it
will not work.

To manually update the package database, all you have to do is run:

`spkg update`

and it will download the latest package database.

**NOTE**: The update command currently has an unused option to select a branch,
it will not do anything at this moment.

## Usage
SPKG is primarily used to download packages from the FreeBSD repos, however, it
can be used to search and query package information from the database. The
following commands have many options to help you find what you're looking for:

`spkg info [package-name(s)]`

`spkg search [pattern(s)]`

Info will display various stats about the package(s) specified, including
current version, package size, and more.

Search will list, with optional information, all packages matching the
pattern(s) specified, with an option to limit the search to an exact match. It
does not support regular expressions.

Finally, you can download packages directly from the FreeBSD repos. If you're
unsure if a package exists, you can use the search command. SPKG also contains
an option to download all packages, though you will be warned against it as the
total size, as of writing the program, of the repos is approximately 94GB.

# Building
Requirements:
- Pyinstaller

## *NIX
Requirements:
- GNU Make

It is recommended to use a virtual environment when building any Python
applications. Any of the following would work:
- Pipenv
- Venv
- Virtualenv

### Building
1) Start by creating a virtual environment using any of the above tools.
2) Activate the virtual environment and use Pip to install any of the
requirements.
3) Run `make` `make spkg` or `make all`.

By default, SPKG builds in-source, the build files are stored in `./build/` and
the executable is stored in `./dist/`. You can either copy the executable file
to a location on the path, or modify the makefile to change the installation
directory to your preferred location.

### Installing
SPKG's makefile does contain an install target which, by default, points to
`/local/bin` in the user's home directory. You can modify the path to fit any
location that is in your `$PATH`, but may require elevated permissions if using
a root location.

To install, simply run: `make install`.

### Uninstalling
There is a target for uninstalling which simply removes the files from the
output directory, editable in the makefile.

To uninstall, simply run: `make uninstall`.

### Cleaning
Like with installing and uninstalling, there is a clean target. It removes all
files generated from the build and the `__pycache__/` directory.

To clean, simply run: `make clean`.

## Windows
If using WSL, you can follow the above instructions.

### Building
It is recommended to use a virtual environment when building any Python
applications. Any of the following would work:
- Pipenv
- Venv
- Virtualenv

### Building
1) Start by creating a virtual environment using any of the above tools.
2) Activate the virtual environment and use Pip to install any of the
requirements.
3) Run the following command:
- `pyinstaller -F -y --specpath build/ -n spkg`

The final executable will be stored in `./dist/` and can be run either in 
Powershell (recommended) or CMD. Note that some features may not work properly
in CMD.

Changelog:
Version 0.0.2 (bugfix):
- Fixes bug with `fetch` when packages don't contain dependencies

Version 0.0.1:
- Initial release

# TODO:
SPKG is still a work-in-progress and as such many features are missing. This
list is by no means exhaustive, and some features not documented here are in the
source code at the top of some files.

- Multiple repo branch support
- Configuration support
    - Default repositories
    - Update configuration if the user asks to use a repo for the first time
    - Support for mirrors
- OpenBSD and NetBSD support
- Regular Expressions
- Skip downloading packages that are already downloaded
    - Applies to specifying a download location or cached downloads
- Use a proper package database
