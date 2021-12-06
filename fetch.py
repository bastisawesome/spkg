'''
TODO: Clean up this code!
TODO: Make the linter shut up, please!
TODO: Fix the output to be more accurate, currently missing spacing between elements.
'''
from __future__ import annotations
from argparse import Namespace
from typing import Any
import pathlib
import json
import time
from math import ceil
from appdirs import AppDirs
import requests
from util import Config, read_package_data, size_fmt, proceed_menu


def run(args: Namespace, config: Config, appdirs: AppDirs):
    if len(args.pkg_name) == 0 and not args.all:
        raise Exception("Must include at least 1 package to fetch.")

    if args.all:
        if not proceed_menu('Fetching all packages is heavily discouraged,\
 continue?'):
            return

    if not args.destdir:
        print('No output directory chosen, files will be downloaded to\n\t',
              f'{appdirs.user_cache_dir}')

    pkg_list, full_size = process_package_list(args, appdirs, config)

    if pre_download(pkg_list, full_size):
        try:
            download_packages(pkg_list, args, config, appdirs)
        except requests.HTTPError:
            print('Unable to read package, try updating your package database.')


def process_package_list(args: Namespace, appdirs: AppDirs,
                         config: Config) -> tuple[list[dict[str, Any]], int]:
    if args.all:
        return get_all_packages(appdirs)

    pkg_list: list[dict[str, Any]] = []
    full_size: int = 0
    for pkg_name in args.pkg_name:
        pkg_full = read_package_data(pkg_name, config, appdirs)
        pkg_list.append({
            'name': pkg_full['name'],
            'version': pkg_full['version'],
            'pkgsize': pkg_full['pkgsize']
        })

        full_size += pkg_full['pkgsize']

        if args.dependencies:
            for dep_name in pkg_full['deps']:
                dep_full = read_package_data(dep_name, config, appdirs)
                pkg_list.append({
                    'name': dep_full['name'],
                    'version': dep_full['version'],
                    'pkgsize': dep_full['pkgsize']
                })

                full_size += dep_full['pkgsize']

    pkg_list = sorted(pkg_list, key=lambda data: data['name'])

    return pkg_list, full_size


def get_all_packages(appdirs: AppDirs) -> tuple[list[dict[str, Any]], int]:
    pkg_list: list[dict[str, Any]] = []
    full_size: int = 0

    with open(pathlib.Path(appdirs.user_cache_dir, 'pkgdb.yaml'), 'r') as f:
        for line in f.readlines():
            pkg_data = json.loads(line)
            pkg_list.append({
                'name': pkg_data['name'],
                'version': pkg_data['version'],
                'pkgsize': pkg_data['pkgsize']
            })

            full_size += pkg_data['pkgsize']

    return pkg_list, full_size


def download_packages(pkg_list: list[dict[str, Any]], args: Namespace,
                      config: Config, appdirs: AppDirs):
    # First find the download location.
    out_path: pathlib.Path = pathlib.Path(appdirs.user_cache_dir)

    if args.destdir:
        out_path = pathlib.Path(args.destdir)

        # Ensure this path exists
        if not out_path.exists():
            out_path.mkdir()

    # Prepare the URL for downloading.
    fmt_repo_url = config.get_full_url()

    for pkg in pkg_list:
        # Prepare the package's location to be passed to the URL.
        pkg_name_version = f'{pkg["name"]}-{pkg["version"]}'
        pkg_location: str = f'{pkg_name_version}.pkg'
        repo_url = fmt_repo_url.format(pkg_location)

        # Prepare download stats
        download_size = 0
        total_size = pkg['pkgsize']
        start_time = time.perf_counter()
        fmt_str = 'Fetching ' + pkg_name_version+': {}%  {} {} {}'
        print(fmt_str.format(0, size_fmt(0), '0B/s', '00:00'), end='\r')

        # Actually download the thing.
        with requests.get(repo_url) as r:
            r.raise_for_status()

            with open(pathlib.Path(out_path, pkg['name']+'.pkg'), 'wb') as f:
                for chunk in r.iter_content():
                    dl = len(chunk)
                    if chunk:
                        f.write(chunk)
                        download_size += dl
                    elapsed = round(time.perf_counter() - start_time)
                    elapsed_min, elapsed_sec = divmod(elapsed, 60)
                    percent_downloaded = ceil(download_size / total_size * 100)
                    time_out = f'{elapsed_min:02d}:{elapsed_sec:02d}'
                    speed = download_size / elapsed_sec if elapsed_sec else 0
                    print(fmt_str.format(percent_downloaded, size_fmt(download_size, do_round=True), f'{size_fmt(speed)}B/s', time_out), end='\r')
                print()  # Newline to prevent overwriting the previous output.


def pre_download(pkg_list: list[dict[str, Any]], total_size: int) -> bool:
    out = 'The following packages will be fetched:\n'
    for pkg in pkg_list:
        name: str = pkg['name']
        version: str = pkg['version']
        size: int = pkg['pkgsize']
        percent_total: float = (size / total_size) * 100
        out += f'\t{name}: {version} ({size_fmt(size, do_round=True)}:\
 {round(percent_total,2)}% of the {size_fmt(total_size, do_round=True)} to\
 download)\n'

    print(out)

    print(f'Number of packages to be fetched: {len(pkg_list)}\n')

    print(f'{size_fmt(total_size, do_round=True)} to be downloaded.\n')

    if not proceed_menu('Proceed with fetching packages?'):
        return False

    return True
