from filetype import guess as __guess_mime
from os.path import join as __path_join
from os.path import split as __path_split
from os import makedirs as __path_mkdirs

guess_mime = lambda file_path:__guess_mime(file_path).mime

def read_bytes(file_path):
    with open(file_path,'rb') as fp:
        return fp.read()

def link_path(*paths):
    return __path_join('',*paths)

def mkdirs(path):
    __path_mkdirs(__path_split(path)[0],exist_ok=True)