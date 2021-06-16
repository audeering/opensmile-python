import configparser
from datetime import date
import os
from subprocess import check_output


config = configparser.ConfigParser()
config.read(os.path.join('..', 'setup.cfg'))

# Project -----------------------------------------------------------------

author = config['metadata']['author']
copyright = f'2020-{date.today().year} audEERING GmbH'
project = config['metadata']['name']
# The x.y.z version read from tags
try:
    version = check_output(['git', 'describe', '--tags', '--always'])
    version = version.decode().strip()
except Exception:
    version = '<unknown>'
title = '{} Documentation'.format(project)


# General -----------------------------------------------------------------

master_doc = 'index'
extensions = []
source_suffix = '.rst'
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', '**.ipynb_checkpoints']
pygments_style = None
extensions = [
    'jupyter_sphinx',  # executing code blocks
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',  # support for Google-style docstrings
    'sphinx.ext.viewcode',
    'sphinx.ext.intersphinx',
    'sphinx.ext.autosectionlabel',
    'sphinx_autodoc_typehints',
    'sphinx_copybutton',  # for "copy to clipboard" buttons
]

napoleon_use_ivar = True  # List of class attributes
autodoc_inherit_docstrings = False  # disable docstring inheritance

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'numpy': ('https://docs.scipy.org/doc/numpy/', None),
    'pandas': ('https://pandas-docs.github.io/pandas-docs-travis/', None),
}

# Do not copy prompot output
copybutton_prompt_text = r'>>> |\.\.\. |\$ '
copybutton_prompt_is_regexp = True

# HTML --------------------------------------------------------------------

html_theme = 'sphinx_audeering_theme'
html_theme_options = {
    'display_version': True,
    'footer_links': False,
    'logo_only': False,
    'wide_pages': ['usage'],
}
html_context = {
    'display_github': True,
}
html_title = title

# Linkcheck ---------------------------------------------------------------

linkcheck_ignore = [
    'https://sail.usc.edu/',
    'http://sphinx-doc.org/',
]
