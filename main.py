'''
TODO: Implement repository support.
TODO: Implement RegEx support for necessary commands.
TODO: Implement checks against invalid package names.
TODO: Maybe potentially bring back raw printing of package info?
'''

import argparse
import pathlib
from typing import Sequence, Union, Any
from appdirs import AppDirs
from util import Config

# Command imports
import fetch
import info
import search
import update


config = Config()

# Not including version information here as I don't feel the need to isolate
# version-specific files.
dirs = AppDirs(Config.APP_NAME, Config.AUTHOR)
coms = {
    'update': update.run,
    'fetch': fetch.run,
    'info': info.run,
    'search': search.run
}


# pylint: disable=protected-access
class InfoAction(argparse._StoreTrueAction):  # type: ignore
    def __call__(self, parser: argparse.ArgumentParser,
                 namespace: argparse.Namespace,
                 values: Union[str, Sequence[Any], None],
                 option_string: Union[str, None] = ...) -> None:
        # print(f'{namespace}, {values}, {option_string}')
        if option_string and (option_string.lower() == '-f' or
                              option_string.lower() == '--full'):
            setattr(namespace, '_force_full', True)
            setattr(namespace, self.dest, True)
            return
        if not getattr(namespace, '_force_full', False):
            setattr(namespace, self.dest, True)
            setattr(namespace, 'full', False)


def main(args: argparse.Namespace):
    # Update configuration
    if args.freebsd_version:
        config.freebsd_version = args.freebsd_version
    if args.arch:
        config.architecture = args.arch
    if args.release_type:
        config.release_type = args.release_type

    if not check_pkgdb() and not args.command == 'update':
        resp = input("No package database downloaded. Would you like to run \
update first? [y/n]> ")
        if resp[0] == 'y':
            coms['update'](argparse.Namespace(), config, dirs)

    # Execute the command we need to be running
    coms[args.command](args, config, dirs)


def check_pkgdb():
    fpath = pathlib.Path(dirs.user_cache_dir, 'pkgdb.yaml')
    return fpath.exists()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(Config.APP_NAME,
                                     description='manipulate packages',
                                     allow_abbrev=False)
    parser.add_argument('-v', '--version', action='version',
                        version=f'{Config.APP_NAME} v{Config.VERSION} by \
                            {Config.AUTHOR}')
    parser.add_argument('--freebsd-version', action='store', type=int,
                        help="Version of FreeBSD to download packages for.")
    parser.add_argument('--arch', '--architecture', action='store', type=str,
                        help="Architecture to download packages for.")
    parser.add_argument('--release-type', action='store', type=str,
                        help="Which release type to download packages from.\
                            (do not mix release types, if you chose LATEST\
                                before, choose latest again if using the same\
                                    version of BSD).")

    commands = parser.add_subparsers(title='commands', required=True,
                                     dest='command')

    update_p = commands.add_parser('update',
                                   help="Download the latest packagesite.yaml.",
                                   description="Update the local catalogues of the\
                                     enabled package repositories")
    update_p.add_argument('-r', '--repository', action="store", type=str,
                          help="Download the catalogue for the named repository\
                            only.")

    fetch_p = commands.add_parser('fetch',
                                  help="Fetch packages from remote repository.",
                                  description="Fetch remote packages.")
    fetch_p.add_argument('-a', '--all', action='store_true',
                         help="Fetch all packages.")
    fetch_p.add_argument('-o', '--output', action="store", type=str,
                         dest='destdir',
                         help="Place files in the sub-directory specified.")
    fetch_p.add_argument('-d', '--dependencies', action='store_true',
                         help="Fetch the package and its dependencies.")
    fetch_p.add_argument('pkg_name', action='store', nargs='*',
                         help="Package(s) to fetch.")

    info_p = commands.add_parser('info',
                                 help="Display information about package files.\
                                     ",
                                 description="Display information for packages")

    info_p.add_argument('-A', '--annotations', action=InfoAction,
                        help="Display any annotations added to the package.")
    info_p.add_argument('-f', '--full', action=InfoAction, default=True,
                        help="Display the full information about the packages\
                            matching pkg_name.")
    info_p.add_argument('-D', '--pkg-message', action=InfoAction,
                        help="Show the pkg-message for matching packages.")
    info_p.add_argument('-I', '--comment', action=InfoAction,
                        help="Display the specified packages and their\
                               comments.")
    info_p.add_argument('-d', '--dependencies', action=InfoAction,
                        help="Display the list of packages on which pkg_name\
                               depends.")
    info_p.add_argument('-r', '--required-by', action=InfoAction,
                        help="Display the list of packages on which pkg_name\
                            depends.")
    info_p.add_argument('-b', '--provided-shlibs', action=InfoAction,
                        help="Display all shared libraries provided by\
                            pkg_name")
    info_p.add_argument('-B', '--required-shlibs', action=InfoAction,
                        help="Display all shared libraries used by pkg_name.")
    info_p.add_argument('-s', '--size', action=InfoAction,
                        help="Display the total size of files installed by\
                            pkg_name.")
    info_p.add_argument('-o', '--origin', action=InfoAction,
                        help="Display pkg_name origin.")
    info_p.add_argument('-p', '--prefix', action=InfoAction,
                        help="Display the installation prefix for each package\
                            matching pkg_name.")
    info_p.add_argument('pkg_name', action='store', nargs='+',
                        help="Package(s) to display information for.")

    search_p = commands.add_parser('search',
                                   help="Search for package in remote\
                                     repositories.",
                                   description="Search package repository\
                                       catalogues.")
    search_p.add_argument('-c', '--comment', action='store_true',
                          help="Search for packages with comment text matching\
                             pkg_name.")
    search_p.add_argument('-D', '--description', action='store_true',
                          help="Search for packages with description text\
                              matching pkg_name.")
    search_p.add_argument('-d', '--depends-on', action='store_true',
                          help="Display the list of packages depended on by each\
                          matched package.")
    search_p.add_argument('-e', '--exact', action='store_true',
                          help="pkg_name should be an exact match against the\
                              search field.")
    search_p.add_argument('-o', '--origins', action='store_true',
                          help="List packages by origin for each package\
                              matching pkg_name.")
    search_p.add_argument('-p', '--prefix', action='store_true',
                          help="Display the package installation prefix for each\
                              matched package.")
    search_p.add_argument('-s', '--size', action='store_true',
                          help="Display the installed size of matched packages.\
                              ")
    search_p.add_argument('pkg_name', action='store', nargs='+',
                          help="Package name or pattern to search for. RegEx not\
                              supported.")

    main(parser.parse_args())
