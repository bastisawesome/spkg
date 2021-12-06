from __future__ import annotations
from typing import Any
import json
import pathlib
from argparse import Namespace
from appdirs import AppDirs
from util import size_fmt, Config


def run(args: Namespace, _config: Config, appdirs: AppDirs):
    patterns: list[str] = args.pkg_name

    hits: list[dict[str, Any]] = begin_search(patterns, args.comment,
                                              args.description,
                                              args.exact, appdirs)
    hits = sorted(hits, key=lambda data: data['name'])

    display_results(hits, args.depends_on, args.origins, args.prefix, args.size)


def begin_search(patterns: list[str], search_comments: bool,
                 search_descriptions: bool,
                 exact: bool, appdirs: AppDirs) -> list[dict[str, Any]]:
    hits: list[dict[str, Any]] = []
    with open(pathlib.Path(appdirs.user_cache_dir, 'pkgdb.yaml'), 'r') as f:
        for line in f.readlines():
            data: dict[str, Any] = json.loads(line)
            for pattern in patterns:
                if not exact:
                    if pattern in data['name']:
                        hits.append(data)
                        break
                    if search_comments and pattern in data['comment']:
                        hits.append(data)
                        break
                    if search_descriptions and pattern in data['description']:
                        hits.append(data)
                        break
                else:
                    if pattern == data['name']:
                        hits.append(data)
                        break
                    if search_comments and pattern == data['comment']:
                        hits.append(data)
                        break
                    if search_descriptions and pattern == data['description']:
                        hits.append(data)
                        break

    return hits


def display_results(results: list[Any], display_dependents: bool,
                    display_origins: bool, display_prefix: bool,
                    display_size: bool):
    out = ""
    fmt_str = '{:16} : {}\n'
    for result in results:
        # Displaying is done in a very specific order:
        # First we always display the package name, however, the output is
        # based on whether or not certain arguments are passed.
        if (not display_dependents and not display_prefix and not display_size):
            # Origin and normal display always show package name/origin and
            # the package comment.
            if display_origins:
                out += f"{result['origin']:<26} {result['comment']}\n"
            else:
                out += f"{result['name']+'-'+result['version']:<30}\
 {result['comment']}\n"

            continue

        # Specific formatting here:
        # First, we have the name or the origin
        # Next line we have the prefix
        # Comment
        # Size
        # And finally, the complex part, the dependencies
        # Also, comment is always displayed, but it's displayed in a particular
        # position (as seen above).

        # Start with the name
        out += result['origin'] if display_origins else \
            result['name']+'-'+result['version']
        out += '\n'

        # Prefix?
        if display_prefix:
            out += fmt_str.format('Prefix', result['prefix'])

        # Comment
        out += fmt_str.format('Comment', result['comment'])

        # Size?
        if display_size:
            out += fmt_str.format('Flat size', size_fmt(result['flatsize']))

        # Dependents?
        if display_dependents:
            # This is the most complex, logically.
            # We need to find all packages that have this package as a
            # dependent, so we need to go back through the package database and
            # search through everything.
            deps: dict[str, Any] = result.get('deps', {})
            if deps:
                out += fmt_str.format('Depends on', '')

                for name, dep in deps.items():
                    out += f"\t{name}-{dep['version']}\n"

    print(out.strip())
