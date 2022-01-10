"""Docs Module."""
# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------
# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#

import os
import sys
from datetime import datetime
from pathlib import Path

from pybtex.plugin import register_plugin
from pybtex.style.formatting.unsrt import Style as UnsrtStyle
from pybtex.style.labels import BaseLabelStyle
from sphinx_gallery.sorting import ExplicitOrder, FileNameSortKey

import scphylo as scp

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent))
sys.path.insert(0, os.path.abspath("_ext"))

# -- Project information -----------------------------------------------------
nitpicky = True  # Warn about broken links. This is here for a reason: Do not change.
needs_sphinx = "3.4"  # Nicer param docs
release = "master"
version = f"master ({scp.__version__})"

language = None

# -- General configuration ---------------------------------------------------
# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named "sphinx.ext.*") or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
    "nbsphinx",
    "sphinx.ext.mathjax",
    "sphinx.ext.napoleon",
    "sphinx_autodoc_typehints",  # needs to be after napoleon
    "sphinx.ext.autosummary",
    "sphinx_paramlinks",
    "sphinx_copybutton",
    "sphinx_click.ext",
    "sphinxcontrib.bibtex",
    "sphinx_gallery.gen_gallery",
]

# bibliography
bibtex_bibfiles = ["references.bib"]
bibtex_default_style = "mystyle"

# nbsphinx specific settings
exclude_patterns = ["build", "**.ipynb_checkpoints"]
nbsphinx_execute = "never"

templates_path = ["_templates"]
source_suffix = ".rst"

# Generate the API documentation when building
autosummary_generate = True
autodoc_member_order = "bysource"
napoleon_google_docstring = True  # for pytorch lightning
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_use_rtype = True  # having a separate entry generally helps readability
napoleon_use_param = True
napoleon_custom_sections = [("Params", "Parameters")]
todo_include_todos = False
numpydoc_show_class_members = False
annotate_defaults = True  # scanpydoc option, look into why we need this

# The master toctree document.
master_doc = "index"

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "numpy": ("https://docs.scipy.org/doc/numpy/", None),
    "scipy": ("https://docs.scipy.org/doc/scipy/reference/", None),
    "networkx": ("https://networkx.github.io/documentation/stable/", None),
    "pandas": ("https://pandas.pydata.org/pandas-docs/stable/", None),
    "matplotlib": ("https://matplotlib.org/", None),
    "sklearn": ("https://scikit-learn.org/stable/", None),
    "seaborn": ("https://seaborn.pydata.org/", None),
    "anndata": ("https://anndata.readthedocs.io/en/latest/", None),
}


# General information about the project.
project = "scphylo"
author = "Farid Rashidi"
copyright = f"{datetime.now():%Y}, {author}, NCI"
title = "a python toolkit for single-cell tumor phylogenetic analysis"


# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.


# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "default"
pygments_dark_style = "default"

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = False


# -- Options for HTML output -------------------------------------------
html_show_sourcelink = True
html_theme = "pydata_sphinx_theme"

html_context = {
    # "display_github": True,  # Integrate GitHub
    "github_user": "Farid Rashidi",  # Username
    "github_repo": "scphylo",  # Repo name
    "github_version": "master",  # Version
    "doc_path": "docs/",  # Path in the checkout to the docs root
}
# Set link name generated in the top bar.
html_title = "scphylo"
html_logo = "_static/images/logo.svg"

html_theme_options = {
    "github_url": "https://github.com/faridrashidi/scphylo-tools",
    "twitter_url": "https://twitter.com/farid_rashidi",
}
# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]
html_css_files = ["css/override.css", "css/sphinx_gallery.css"]
html_show_sphinx = False


# a simple label style which uses the bibtex keys for labels
class MyLabelStyle(BaseLabelStyle):
    def format_labels(self, sorted_entries):
        for entry in sorted_entries:
            yield entry.key


class MyStyle(UnsrtStyle):

    default_label_style = MyLabelStyle


register_plugin("pybtex.style.formatting", "mystyle", MyStyle)


def setup(app):
    """[summary].

    Parameters
    ----------
    app : [type]
        [description]
    """
    app.config.pygments_dark_style = "default"


# -- sphinx gallery ------------------------------------------
def reset_matplotlib(gallery_conf, fname):
    import matplotlib as mpl

    mpl.use("agg")

    import matplotlib.pyplot as plt

    plt.rcdefaults()
    mpl.rcParams["savefig.bbox"] = "tight"
    mpl.rcParams["savefig.transparent"] = True


example_dir = HERE.parent.parent / "examples"
rel_example_dir = Path("..") / ".." / "examples"


sphinx_gallery_conf = {
    "image_scrapers": "matplotlib",
    "reset_modules": (
        "seaborn",
        reset_matplotlib,
    ),
    "filename_pattern": f"{os.path.sep}(plot_|compute_)",
    "examples_dirs": example_dir,
    "gallery_dirs": "auto_examples",  # path to where to save gallery generated output
    "abort_on_example_error": True,
    "show_memory": True,
    "within_subsection_order": FileNameSortKey,
    "subsection_order": ExplicitOrder(
        [
            rel_example_dir / "reconstruction",  # really must be relative
            rel_example_dir / "comparison",
        ]
    ),
    "reference_url": {
        "sphinx_gallery": None,
    },
    "line_numbers": False,
    "compress_images": ("images", "thumbnails"),
    "inspect_global_variables": False,
    "backreferences_dir": "gen_modules/backreferences",
    "doc_module": "scphylo",
    "download_all_examples": False,
    "pypandoc": True,  # convert rST to md when downloading notebooks
}
