from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

VERSION_STR = '0.1'

setup(
    name             = 'date_translator',
    version          = VERSION_STR,
    author           = '''Sandesh P V''',
    author_email     = 'sandesh2k18@gmail.com',
    description      = '''Document translator''',
    long_description = long_description,
    license          = 'Free',
    zip_safe         = False,

    setup_requires = ['setuptools'],

    include_package_data = True,

    install_requires = [
        "flask",
        "pytest",
    ],

    packages    = find_packages('src'),
    package_dir = { '' : 'src' },

    # make sure we never accidently upload to PyPI
    classifiers = [
        'Private :: Do Not Upload'
    ]
)
