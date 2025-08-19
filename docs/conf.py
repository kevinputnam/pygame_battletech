import sys
from pathlib import Path

# add parent directory to path
sys.path.insert(0, str(Path('..').resolve()))

# import modules for use with autodoc
import world

project = 'Python Battletech'
copyright = '2025, Kevin Putnam'
author = 'Kevin Putnam'

extensions = ['sphinx_design','myst_parser','sphinx.ext.autodoc']

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_theme = 'pydata_sphinx_theme'

