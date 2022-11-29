import datetime
from sphinx_rtd_theme import get_html_theme_path

# -- General configuration -----------------------------------------------------

general_theme = "sphinx_rtd_theme"

# Documentation theme.
theme_path = get_html_theme_path() + "/" + general_theme

# Minimal Sphinx version.
needs_sphinx = "5.1.0"

# Add any extenstions here. These could be both Sphinx or custom ones.
extensions = [
    "myst_parser",
    "sphinx.ext.todo",
    "sphinx.ext.ifconfig",
    "sphinx.ext.extlinks",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinxcontrib.mermaid",
    "numpydoc",
]

# If true, figures, tables and code-blocks are automatically numbered
# if they have a caption.
numfig = True

# The suffix of source filenames.
source_suffix = {
    ".md": "markdown",
    ".rst": "restructuredtext",
}

# The main toctree document.
master_doc = "index"

# General information about the project.
project = "Tetris documentation"
output_filename = "tetris-docs"
authors = "Wiktoria Kuna"
copyright = authors + ", {}".format(datetime.datetime.now().year)

# Specify time format. Used in 'Last Updated On:'.
today_fmt = "%H:%M %Y-%m-%d"

# The name of the Pygments (syntax highlighting) style to use.
# This affects the code blocks. More styles: https://pygments.org/styles/
pygments_style = "sphinx"

# -- HTML output ---------------------------------------------------------------

# The theme to be used for HTML documentation.
html_theme = general_theme

# The title to be shown at all html documents.
# Deafult is "<project> v<release> documentation".
html_title = project

# A shorter title to appear at the navigation bar. Default is html_title.
html_short_title = "Tetris"

# 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format. To disable set it to ''.
html_last_updated_fmt = today_fmt

# If True show "Created using Sphinx" in the HTML footer.
html_show_sphinx = False

# -- Options for LaTeX output --------------------------------------------------

# Grouping the document tree into LaTeX files.
latex_documents = [
    ("index", output_filename + ".tex", project, authors, "manual"),
]

man_pages = [("index", output_filename, project, [authors], 1)]

# Speficy LaTeX prolog.
rst_prolog = """
.. role:: raw-latex(raw)
   :format: latex

.. role:: raw-html(raw)
   :format: html
"""

# Specify LaTeX epilog.
rst_epilog = (
    """
.. |project| replace:: %s
"""
    % project
)


# -- Custom filters ------------------------------------------------------------

# Exclude some methods from the api documentation
def hide_non_private(app, what, name, obj, skip, options):
    if "elaborate" in name:
        # skip elaborates
        return True
    else:
        # otherwise generate an entry
        return None


def setup(app):
    app.connect("autodoc-skip-member", hide_non_private)


# If set to False it doesn't generate summary of class Methods if not
# explicitly desctibed in docsting. This prevents many mostly empty Method
# sections in most classes since 'elaborate' methods are not documented.
numpydoc_show_class_members = False
