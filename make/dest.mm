# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
#
# (c) 2013-2018 parasim inc
# (c) 2010-2018 california institute of technology
# all rights reserved
#

$(dest) $(dest.py) $(dest.lib) $(dest.bin) $(dest.staging) :
	${call log.action,mkdir,$@}
	$(mkdirp) $@

# end of file
