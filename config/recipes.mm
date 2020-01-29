# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
#
# (c) 2013-2020 parasim inc
# (c) 2010-2020 california institute of technology
# all rights reserved
#

# tidy up the source tree
tidy:
	${call log.action,tidy,${realpath .}}
	find . -name \*~ -delete

# clean the staging area
clean: tidy
	${call log.action,clean,${realpath $(prefix)}}
	$(rm.force-recurse) $(prefix)

# show me the default goal
default.info:
	${call log.var,defaultgoal,$(.DEFAULT_GOAL)}

# language settings
c++.info:
	${call log.sec,"c++", "command line"}
	${call log.var,"compiler",$(c++)}
	${call log.var,"external packages",$(packages)}
	${call log.var,"compile",${call c++.compile.options,$(packages)}}
	${call log.var,"link",${call c++.link.options,$(packages)}}

# end of file
