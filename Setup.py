from distutils.core import setup
from setuptools import find_packages
from setuptools.command.install import install as _install
import os

# Optional project description in README.md:
current_directory = os.path.dirname(os.path.abspath(__file__))

try:
    with open(os.path.join(current_directory, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()
except Exception:
    long_description = ''


class Install(_install):
    def run(self):
        _install.do_egg_install(self)
        import nltk
        nltk.download('wordnet')


setup(

    # Use custom install class
    cmdclass={'install': Install},

    name='Leaflet Creator',

    # Packages to include in the distribution:
    packages=find_packages(),

    version='1.0',

    description='Install dependencies for Leaflet Creator',

    author='Lewis Cairns',

    author_email='lwcairns@dundee.ac.uk',

    url='https://github.com/lewiscairns/LeafletCreator/tree/main',

    download_url='https://github.com/lewiscairns/LeafletCreator/tree/main',

    install_requires=['numpy', 'regex', 'pillow', 'textstat', 'python-docx', 'textblob', 'nltk'],
)
