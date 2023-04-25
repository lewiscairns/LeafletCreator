from distutils.core import setup
from setuptools import find_packages
import os

# Optional project description in README.md:
current_directory = os.path.dirname(os.path.abspath(__file__))

try:
    with open(os.path.join(current_directory, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()
except Exception:
    long_description = ''

setup(

    # Project name:
    name='Leaflet Creator',

    # Packages to include in the distribution:
    packages=find_packages(),

    # Project version number:
    version='1.0',

    # List a license for the project, eg. MIT License
    license='',

    # Short description of your library:
    description='Install dependencies for Leaflet Creator',

    # Long description of your library:
    long_description=long_description,
    long_description_content_type='text/markdown',

    # Your name:
    author='Lewis Cairns',

    # Your email address:
    author_email='lwcairns@dundee.ac.uk',

    # Link to your github repository or website:
    url='https://github.com/lewiscairns/LeafletCreator/tree/main',

    # Download Link from where the project can be downloaded from:
    download_url='https://github.com/lewiscairns/LeafletCreator/tree/main',

    # List of keywords:
    keywords=[],

    # List project dependencies:
    install_requires=['numpy', 'regex', 'pillow', 'textstat', 'python-docx', 'textblob', 'nltk', 'customtkinter'],

    # https://pypi.org/classifiers/
    classifiers=[]
)
