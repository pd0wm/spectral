try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'High-performance spectrum sensing library',
    'author': 'Wessel Bruinsma, Kees Kroep, Robin Hes, Tom aan de Wiel, Willem Melching, Dorus Leliveld',
    'url': '',
    'download_url': '',
    'author_email': 'My email.',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['spectral'],
    'scripts': [],
    'name': 'spectral'
}

setup(**config)
