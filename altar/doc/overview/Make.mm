# -*- Makefile -*-
#
# michael a.g. aïvázis
# parasim
# (c) 1998-2020 all rights reserved
#

PROJECT = isce
PACKAGE = doc/pyre

# the default document to build; override from the environment
DOCUMENT = overview

# the configuration dependencies
CONFIG = \
    $(wildcard $(addprefix config/, *.sty *.tex)) \

# section bodies
SECTIONS = \
    $(wildcard $(addprefix sections/, *.tex *.bib)) \

# source code listings
LISTINGS = \
    $(wildcard $(addprefix listings/, *.py *.pfg *.cfg *.pml))

# figures
FIGURES = \
    figures/*.pdf \

# make everything
all: $(DOCUMENT)

# the documents
overview: overview.pdf

# explcit targets
overview.pdf: overview.tex $(CONFIG) $(SECTIONS) $(LISTINGS) $(FIGURES)

# preview types
osx: $(DOCUMENT).pdf
	open $(DOCUMENT).pdf

xpdf: $(DOCUMENT).pdf
	xpdf -remote $(DOCUMENT) $(DOCUMENT).pdf

# housekeeping
PROJ_CLEAN += $(CLEAN_LATEX) *.snm *.nav *.vrb *.lbf
PROJ_DISTCLEAN = *.ps *.pdf $(PROJ_CLEAN)

# end of file
