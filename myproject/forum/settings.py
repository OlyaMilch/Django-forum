import os
from pathlib import Path


'''
Needed for working with files, such as avatars.

__file__ - variable containing the path to the current file(setting.py)
.resolve() - converts this path into an absolute path, i.e. full - like C:/Users/
.parent.parent - the folder where manage.py is located is the root of the project
'''

BASE_DIR = Path(__file__).resolve().parent.parent

MEDIA_URL = '/media/'  #  URL where the files will be available
MEDIA_ROOT = BASE_DIR / 'media'  # The path on the disk where the files are saved (real folder on disk)


INSTALLED_APPS = [
    'forum'
]
