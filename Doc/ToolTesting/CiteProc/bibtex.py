#!/usr/bin/env python
# Is derived work from citeproc-py's bibtex.py example
#   https://github.com/citeproc-py/citeproc-py/blob/master/examples/bibtex.py

# The references are parsed from a BibTeX database, so we import the
# corresponding parser.
from citeproc.source.bibtex import BibTeX

# Import the citeproc-py classes we'll use below.
from citeproc import CitationStylesStyle, CitationStylesBibliography
from citeproc import formatter
from citeproc import Citation, CitationItem


# Parse the BibTeX database.

bib_source = BibTeX('library.bib')


# load a CSL style (from the current directory)

bib_style = CitationStylesStyle('chicago-author-date-fr', validate=False)


# Create the citeproc-py bibliography, passing it the:
# * CitationStylesStyle,
# * BibliographySource (BibTeX in this case), and
# * a formatter (plain, html, or you can write a custom formatter)

bibliography = CitationStylesBibliography(bib_style, bib_source,
                                          formatter.plain)


# Processing citations in a document needs to be done in two passes as for some
# CSL styles, a citation can depend on the order of citations in the
# bibliography and thus on citations following the current one.
# For this reason, we first need to register all citations with the
# CitationStylesBibliography.

citation1 = Citation([CitationItem('inbook-collecting-gold-dust:2019')])

bibliography.register(citation1)


# In the second pass, CitationStylesBibliography can generate citations.
# CitationStylesBibliography.cite() requires a callback function to be passed
# along to be called in case a CitationItem's key is not present in the
# bibliography.

def warn(citation_item):
    print("WARNING: Reference with key '{}' not found in the bibliography."
          .format(citation_item.key))


print('Citations')
print('---------')

print(bibliography.cite(citation1, warn))


# And finally, the bibliography can be rendered.

print('')
print('Bibliography')
print('------------')

for item in bibliography.bibliography():
    print(str(item))
