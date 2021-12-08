from typing import Any
import json
import pathlib
from appdirs import AppDirs


def size_fmt(num: float, do_round: bool = False) -> str:
    for unit in ['B', 'KiB', 'MiB', 'GiB']:
        if abs(num) < 1024.0:
            if not do_round:
                return f'{num:3.2f}{unit}'
            return f'{round(num)}{unit}'
        num /= 1024.0
    if not do_round:
        return f'{num:.2f}GiB'
    return f'{round(num)}GiB'


class Config():
    AUTHOR = 'BastIsAwesome'
    APP_NAME = 'spkg'
    VERSION = '0.0.2'
    REPO_URL = 'http://pkg.freebsd.org/{ABI}/{RELEASE_TYPE}/All/'

    # Supported FreeBSD variables
    FREEBSD_VERSIONS = [11, 12, 13, 14]
    FREEBSD_ARCHITECTURES = ['i386', 'amd64', 'powerpc', 'powerpc64',
                             'powerpc64le', 'powerpcspe', 'armv6', 'armv7',
                             'aarch64', 'riscv64']
    FREEBSD_RELEASE_TYPES = ['latest', 'quarterly', 'release_0', 'release_1',
                             'release_2', 'release_3', 'release_4']
    CHUNK_SIZE = 512  # Used by Requests iter_lines function as the default size

    def __init__(self):
        self._freebsd_version = 13
        self._architecture = 'amd64'
        self._release_type = 'quarterly'

    def get_full_url(self):
        '''Return the full URL to the repo.

        Return the full URL to the repo.
        This function also adds an extra formatter to the end as a utility,
        as the full URL to the repo isn't useful on its own, this allows callers
        to format the end with the specific package they are looking for.
        '''
        return self.REPO_URL.format(ABI=self.abi,
                                    RELEASE_TYPE=self._release_type) + '{}'

    @property
    def freebsd_version(self):
        return self._freebsd_version

    @freebsd_version.setter
    def freebsd_version(self, ver: int):
        if ver in Config.FREEBSD_VERSIONS:
            self._freebsd_version = ver
        else:
            raise Exception("Unsupported FreeBSD version: {}".format(ver))

    @property
    def architecture(self):
        return self._architecture

    @architecture.setter
    def architecture(self, arch: str):
        if arch in Config.FREEBSD_ARCHITECTURES:
            self._architecture = arch
        else:
            raise Exception("Unsupported platform architecture: {}".
                            format(arch))

    @property
    def release_type(self):
        return self._release_type

    @release_type.setter
    def release_type(self, rtype: str):
        if rtype in Config.FREEBSD_RELEASE_TYPES:
            self._release_type = rtype
        else:
            raise Exception("Unsupported release type: {}".format(rtype))

    @property
    def abi(self):
        return f'FreeBSD:{self.freebsd_version}:{self.architecture}'


_PKG_CACHE: dict[str, dict[str, Any]] = {}
_pkg_cache_pos: int = 0


def read_package_data(pkg_name: str, _config: Config,
                      appdirs: AppDirs) -> dict[str, Any]:
    if pkg_name in _PKG_CACHE:
        return _PKG_CACHE[pkg_name]

    global _pkg_cache_pos  # pylint: disable=global-statement

    data: dict[str, Any] = {}
    with open(pathlib.Path(appdirs.user_cache_dir, 'pkgdb.yaml'), 'r') as f:
        f.seek(_pkg_cache_pos)
        line = f.readline()

        while line:
            data = json.loads(line)
            _PKG_CACHE[data['name']] = data

            if data['name'] == pkg_name:
                _pkg_cache_pos = f.tell()
                break

            line = f.readline()

    return data


def proceed_menu(prompt: str) -> bool:
    choice: str = ''

    while choice.lower() != 'y' and choice.lower() != 'yes':
        choice = input(prompt + ' [y/N] ')

        if choice.lower() == 'n' and choice.lower() != 'no':
            return False
        if choice.lower() != 'y' and choice.lower() != 'yes':
            print('Please type Y[es] or N[o] to make a selection')

    return True
