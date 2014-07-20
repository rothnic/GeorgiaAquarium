# Currently unused, was going to process notebooks, but found and modified
# /ext/sphinx_notebook/notebook_sphinxext.py

__author__ = 'Nick'

import os
import json
from IPython.nbconvert import RSTExporter

# Python list of files in notebooks directory
files = os.listdir('./notebooks')

# Load JSON config file for notebooks
with open('./notebooks/notebooks.conf', 'r') as titlesfile:
    notebooks = json.load(titlesfile)


rst_export = RSTExporter()

for notebook in notebooks:
    filename = notebook['name'].encode('utf-8')
    newfile = rst_export.from_filename('./notebooks/' + filename)
    #nbconvert.writers.FilesWriter(newfile)