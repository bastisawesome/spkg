from __future__ import annotations
from typing import Any, Union
from argparse import Namespace
from appdirs import AppDirs
from util import Config, read_package_data, size_fmt


def run(args: Namespace, config: Config, appdirs: AppDirs):
    packages = args.pkg_name
    if args.full:
        for package in packages:
            data = read_package_data(package, config, appdirs)
            print_full(data)
        return

    for package in packages:
        pkg_data = read_package_data(package, config, appdirs)
        print_data(pkg_data, args)


# pylint: disable=too-many-branches
def print_data(pkg_data: dict[str, Any], args: Namespace):
    out = ''
    FMT_STR = '{:15}: {}\n'
    SUB_FMT_STR = '\t{}\n'

    out += f'{pkg_data["name"]}-{pkg_data["version"]}\n'

    if args.origin:
        out += FMT_STR.format('Origin', pkg_data['origin'])

    if args.prefix:
        out += FMT_STR.format('Prefix', pkg_data['prefix'])

    if args.comment:
        out += FMT_STR.format('Comment', pkg_data['comment'])

    if args.required_shlibs:
        if pkg_data.get('shlibs_required', None):
            out += 'Shared Libs required:\n'
            for lib in pkg_data['shlibs_required']:
                out += SUB_FMT_STR.format(lib)

    if args.provided_shlibs:
        if pkg_data.get('shlibs_provided', None):
            out += 'Shared Libs provided:\n'
            for lib in pkg_data['shlibs_provided']:
                out += SUB_FMT_STR.format(lib)

    if args.annotations:
        if pkg_data.get('annotations', None):
            out += FMT_STR.format('Annotations', '')
            for key, value in pkg_data['annotations'].items():
                out += f'\t{key:15}: {value}\n'

    if args.size:
        out += FMT_STR.format('Flat size', size_fmt(pkg_data['flatsize']))

    if args.pkg_message:
        out += FMT_STR.format('Message', '')
        if pkg_data.get('messages', None):
            out += parse_messages(pkg_data['messages'])

    if args.dependencies:
        if pkg_data.get('deps', None):
            out += FMT_STR.format('Depends on', '')
            for pkg_name, sub_data in pkg_data['deps'].items():
                out += f'\t{pkg_name}-{sub_data["version"]}\n'

    if args.required_by:
        raise NotImplementedError(
            'Unable to pull packages requiring this package.')

    print(out.strip())


def parse_messages(messages: Union[list[dict[str, Any]], str]) -> str:
    out = ''
    if isinstance(messages, list):
        for message in messages:
            if not message['type']:
                out += 'Always:\n'
                out += message['message']
                continue

            if message['type'] == 'install':
                out += 'On install:\n'
                out += message['message']
                continue

            if message['type'] == 'upgrade':
                out += 'On upgrade:\n'
                out += message['message']
                continue

            if message['type'] == 'remove':
                out += 'On remove:\n'
                out += message['message']
                continue
    else:
        # Raw message type.
        out += 'On install:\n'
        out += messages

    out += '\n\n'

    return out


def print_full(pkg_data: dict[str, Any]):
    # Order of output:
    # Package name+version (name-version)
    # Name:
    # Version:
    # Origin:
    # Architecture: {abi, not arch}
    # Prefix:
    # Categories:
    # Licenses:
    # Maintainer:
    # WWW:
    # Comment:
    # Options:
    # Shared Libs Required:
    #  {No separation between label and `:`}
    #  {Newline with list}
    # Shared Libs Provided:
    #  {see above}
    # Annotations:
    # Flat size:
    # Description:
    # 16 chars between label and `:`
    # Options cut if no data is found.

    # Begine parsing through package data.
    out = ''
    FMT_STR = '{:15}: {}\n'
    # Yeah, I have no idea what BSD actually refers to this as.
    fully_qualified_name: str = f'{pkg_data["name"]}-{pkg_data["version"]}'

    out += fully_qualified_name + '\n'
    out += FMT_STR.format('Name', pkg_data['name'])
    out += FMT_STR.format('Version', pkg_data['version'])
    out += FMT_STR.format('Origin', pkg_data['origin'])
    out += FMT_STR.format('Architecture', pkg_data['abi'])
    out += FMT_STR.format('Prefix', pkg_data['prefix'])
    out += FMT_STR.format('Categories',
                          ', '.join([str(c) for c in pkg_data['categories']]))

    # Special license logic. A package can be single or multi licensed,
    # so to avoid an unnecessary loop we first check the license type.
    if pkg_data['licenselogic'] == 'single':
        out += FMT_STR.format('Licenses', pkg_data['licenses'][0])
    else:
        out += FMT_STR.format('Licenses',
                              ', '.join(str(c) for c in pkg_data['licenses']))

    out += FMT_STR.format('Maintainer', pkg_data['maintainer'])
    out += FMT_STR.format('WWW', pkg_data['www'])
    out += FMT_STR.format('Comment', pkg_data['comment'])

    # Options is special, it's optional and displays in a slightly different
    # format, similar to shared libraries required/provided
    if pkg_data.get('options', None):
        out += FMT_STR.format('Options', '')
        for opt, status in pkg_data['options'].items():
            out += f'\t{opt:16} : {status}\n'

    # Share libraries required/provided may not be defined, so those also
    # require custom logic
    if pkg_data.get('shlibs_required', None):
        # Special formatting required for this as well
        out += 'Shared Libs required:\n'
        for lib in pkg_data['shlibs_required']:
            out += f'\t{lib}\n'
    if pkg_data.get('shlibs_provided', None):
        out += 'Shared Libs provided:'
        for lib in pkg_data['shlibs_provided']:
            out += f'\t{lib}\n'

    # Annotations is weird, as unlike the above two formats,
    # annotations does use a 16-character alignment, but also outputs
    # each annotation on a new line.
    if pkg_data.get('annotations', None):
        # Blank string as the second argument because it's not actually filled
        # in.
        out += FMT_STR.format('Annotations', '')
        for key, val in pkg_data['annotations'].items():
            # This is also a weird format!
            out += f'\t{key:15}: {val}\n'

    out += FMT_STR.format('Flat size', size_fmt(pkg_data['flatsize']))
    out += FMT_STR.format('Description', '')
    out += pkg_data['desc']

    print(out.strip())
