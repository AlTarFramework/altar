# -*- Makefile -*-
#
# michael a.g. aïvázis
# parasim
# (c) 1998-2018 all rights reserved
#

tidy:
	find . -name \*~ -delete

clean: tidy
	$(rm.force-recurse) $(prefix)

# end of file
