from datetime import date
import os
import shutil

import toml

import audeer


config = toml.load(audeer.path("..", "pyproject.toml"))


# Project -----------------------------------------------------------------

project = config["project"]["name"]
author = ", ".join(author["name"] for author in config["project"]["authors"])
copyright = f"2020-{date.today().year} audEERING GmbH"
version = audeer.git_repo_version()
title = "Documentation"


# General -----------------------------------------------------------------

master_doc = "index"
source_suffix = ".rst"
exclude_patterns = [
    "api-src",
    "build",
    "tests",
    "Thumbs.db",
    ".DS_Store",
]
templates_path = ["_templates"]
pygments_style = None
extensions = [
    "jupyter_sphinx",  # executing code blocks
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",  # support for Google-style docstrings
    "sphinx.ext.autosummary",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx.ext.autosectionlabel",
    "sphinx_autodoc_typehints",
    "sphinx_copybutton",  # for "copy to clipboard" buttons
]

napoleon_use_ivar = True  # List of class attributes
autodoc_inherit_docstrings = False  # disable docstring inheritance

intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "numpy": ("https://docs.scipy.org/doc/numpy/", None),
    "pandas": ("https://pandas.pydata.org/pandas-docs/stable/", None),
}

# Do not copy prompot output
copybutton_prompt_text = r">>> |\.\.\. |\$ "
copybutton_prompt_is_regexp = True

# Disable auto-generation of TOC entries in the API
# https://github.com/sphinx-doc/sphinx/issues/6316
toc_object_entries = False


# HTML --------------------------------------------------------------------

html_theme = "sphinx_audeering_theme"
html_theme_options = {
    "display_version": True,
    "footer_links": False,
    "logo_only": False,
    "wide_pages": ["usage"],
}
html_context = {
    "display_github": True,
}
html_title = title


# Linkcheck ---------------------------------------------------------------

linkcheck_ignore = [
    "https://sail.usc.edu/",
    "http://sphinx-doc.org/",
]


# Copy API (sub-)module RST files to docs/api/ folder ---------------------

audeer.rmdir("api")
audeer.mkdir("api")
api_src_files = audeer.list_file_names("api-src")
api_dst_files = [
    audeer.path("api", os.path.basename(src_file)) for src_file in api_src_files
]
for src_file, dst_file in zip(api_src_files, api_dst_files):
    shutil.copyfile(src_file, dst_file)
