import os
import tarfile
import zipfile
import gzip
import subprocess
from lutris.util.log import logger


def extract_archive(path, to_directory='.'):
    path = os.path.abspath(path)
    logger.debug("Extracting %s to %s", path, to_directory)
    if path.endswith('.zip'):
        opener, mode = zipfile.ZipFile, 'r'
    elif path.endswith('.tar.gz') or path.endswith('.tgz'):
        opener, mode = tarfile.open, 'r:gz'
    elif path.endswith('.tar.bz2') or path.endswith('.tbz'):
        opener, mode = tarfile.open, 'r:bz2'
    else:
        raise ValueError(
            "Could not extract `%s` as no appropriate extractor is found"
            % path)
    cwd = os.getcwd()
    os.chdir(to_directory)
    handler = opener(path, mode)
    handler.extractall()
    handler.close()
    os.chdir(cwd)


def decompress_gz(file_path):
    """Decompress a gzip file"""
    if file_path.endswith('.gz'):
        dest_path = file_path[:-3]
    else:
        raise ValueError("unsupported file type")

    f = gzip.open(file_path, 'rb')
    file_content = f.read()
    f.close()

    dest_file = open(dest_path, 'wb')
    dest_file.write(file_content)
    dest_file.close()

    return dest_path


def unzip(filename, dest=None):
    """Unzips a file"""
    command = ["unzip", '-o', filename]
    if dest:
        command = command + ['-d', dest]
    subprocess.call(command)


def unrar(filename):
    """Unrar a file"""

    subprocess.call(["unrar", "x", filename])


def untar(filename, dest=None, method='gzip'):
    """Untar a file"""
    cwd = os.getcwd()
    if dest is None or not os.path.exists(dest):
        dest = cwd
    logger.debug("Will extract to %s" % dest)
    os.chdir(dest)
    if method == 'gzip':
        compression_flag = 'z'
    elif method == 'bzip2':
        compression_flag = 'j'
    else:
        compression_flag = ''
    cmd = "tar x%sf %s" % (compression_flag, filename)
    logger.debug(cmd)
    subprocess.Popen(cmd, shell=True)
    os.chdir(cwd)