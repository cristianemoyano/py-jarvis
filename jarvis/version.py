import codecs
import os


__all__ = ['__version__', '__version_info__']

_version_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'version.txt')
with codecs.open(_version_file_path, mode='rb', encoding='utf8') as _version_file:
    __version__ = _version_file.read().strip()
__version_info__ = tuple(map(int, __version__.split('-', 1)[0].split('.', 2))) + tuple(__version__.split('-', 1)[1:])