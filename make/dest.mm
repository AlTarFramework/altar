# -*- Makefile -*-
#
# michael a.g. aïvázis
# parasim
# (c) 1998-2018 all rights reserved
#

$(prefix):
	${call log.action,mkdir,$(prefix)}
	$(mkdirp) $(prefix)


# end of file
