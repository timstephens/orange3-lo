#!/usr/bin/env python3

from os import path, walk

from setuptools import setup, find_packages

#with io.open('README.pypi', 'r', encoding='utf-8') as f:
#    ABOUT = f.read()

NAME = 'Orange3-LivingOptics'

MAJOR = 0
MINOR = 0
MICRO = 1
VERSION = '%d.%d.%d' % (MAJOR, MINOR, MICRO)

AUTHOR = 'Tim Stephens'
AUTHOR_EMAIL = 'tim@livingoptics.com'

URL = 'https://github.com/livingoptics'
DESCRIPTION = 'Orange3 add-on for accessing Living Optics hyperspectral data.'
#LONG_DESCRIPTION = ABOUT
LONG_DESCRIPTION = DESCRIPTION
LICENSE = 'MIT'

CLASSIFIERS = [
    'Example :: Invalid',
]

KEYWORDS = [
    'orange3 add-on',
    'orange3-lo'
]

PACKAGES = ["orangecontrib"] # find_packages()

PACKAGE_DATA = {

}

ENTRY_POINTS = {
    'orange3.addon':
        ('Orange3-LivingOptics = orangecontrib.lo',),
    'orange.widgets':
        ('LivingOptics = orangecontrib.lo.widgets',),
#     # Register widget help
#     "orange.canvas.help": (
#         'html-index = orangecontrib.wfdb.widgets:WIDGET_HELP_PATH',)
}

DATA_FILES = [
    # Data files that will be installed outside site-packages folder
]


def include_documentation(local_dir, install_dir):
    global DATA_FILES
    # if 'bdist_wheel' in sys.argv and not path.exists(local_dir):
    #     print("Directory '{}' does not exist. "
    #           "Please build documentation before running bdist_wheel."
    #           .format(path.abspath(local_dir)))
    #     sys.exit(0)
    doc_files = []
    for dirpath, dirs, files in walk(local_dir):
        doc_files.append((dirpath.replace(local_dir, install_dir),
                          [path.join(dirpath, f) for f in files]))
    DATA_FILES.extend(doc_files)


if __name__ == '__main__':
#     include_documentation('doc/_build/html', 'help/orange3-lo')
#     include_documentation('doc/_build/html')
    setup(
        name=NAME,
        version=VERSION,
        author=AUTHOR,
        author_email=AUTHOR_EMAIL,
        url=URL,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        long_description_content_type='text/markdown',
        license=LICENSE,
        packages=PACKAGES,
        data_files=DATA_FILES,
        package_data=PACKAGE_DATA,
        keywords=KEYWORDS,
        classifiers=CLASSIFIERS,
        install_requires=[
            "AnyQt",
            "ndf >=0.1.4",
            "numpy >=1.16",
            "Orange3 >=3.35.0",
            "orange-canvas-core >=0.1.28",
            "orange-widget-base >=4.20.0",
            # Orange3 <3.35 does not work with Pandas 2.1, remove this
            # constraint when requiring Orange> 3.35
            "requests",
            "requests_cache",
            "scipy",
            "lo-sdk > 1.4.4"
            # Will also require LO SDK to be installed, in the same venv or globally on your computer.
        ],
        extras_require={
            'test': ['coverage', ],
            'doc': ['sphinx', 'recommonmark', 'sphinx_rtd_theme', ],
        },
        namespace_packages=['orangecontrib'],
        entry_points=ENTRY_POINTS,
    )