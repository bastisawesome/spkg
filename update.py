'''
TODO: Check signature of package database.
TODO: Implement -r arg
'''

from __future__ import annotations
import tarfile
import pathlib
import tempfile
import shutil
from argparse import Namespace
import requests
from appdirs import AppDirs
from util import Config


def run(_args: Namespace, config: Config, appdirs: AppDirs):
    cache_dir = pathlib.Path(appdirs.user_cache_dir)
    if not cache_dir.exists():
        cache_dir.mkdir()
    tmpdir = pathlib.Path(tempfile.gettempdir(), 'spkg')
    tmpdir.mkdir(parents=True, exist_ok=True)

    tar_path = pathlib.Path(tmpdir, 'packagesite.txz')

    # Ensure there is a packagesite.yaml for this ABI
    url = config.get_full_url()
    print('Downloading packagesite.txz...')
    with requests.get(url.format('packagesite.txz')) as r:
        r.raise_for_status()
        with open(pathlib.Path(tar_path), 'wb') as f:
            for chunk in r.iter_content():
                if chunk:
                    f.write(chunk)
                    # f.flush()
                    # os.fsync(f.fileno())
    print('packagesite.txz downloaded.')
    print('Extracting...')
    with tarfile.open(tar_path, 'r:xz') as f:
        
        import os
        
        def is_within_directory(directory, target):
            
            abs_directory = os.path.abspath(directory)
            abs_target = os.path.abspath(target)
        
            prefix = os.path.commonprefix([abs_directory, abs_target])
            
            return prefix == abs_directory
        
        def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
        
            for member in tar.getmembers():
                member_path = os.path.join(path, member.name)
                if not is_within_directory(path, member_path):
                    raise Exception("Attempted Path Traversal in Tar File")
        
            tar.extractall(path, members, numeric_owner=numeric_owner) 
            
        
        safe_extract(f, tmpdir)

    print('packagesite.txz extracted.')

    # Verification would be done here
    # print('Verifying packagesite.yaml')

    print('Generating package database...')
    shutil.copy(pathlib.Path(tmpdir, 'packagesite.yaml'),
                pathlib.Path(cache_dir, 'pkgdb.yaml'))
    print('Package database generated.')
    print('Cleaning up...')
    shutil.rmtree(tmpdir)
    print('Update complete!')
