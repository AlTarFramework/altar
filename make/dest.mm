# -*- Makefile -*-
#
# michael a.g. aïvázis
# parasim
# (c) 1998-2018 all rights reserved
#

$(dest):
	${call log.action,mkdir,$(dest)}
	$(mkdirp) $(dest)


# end of file
