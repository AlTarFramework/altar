# -*- Makefile -*-
#
# michael a.g. aïvázis
# parasim
# (c) 1998-2020 all rights reserved
#

# display the pyre configuration
pyre.show:
	${call show.sec,"pyre",}
	${call show.var,"version",$(pyre.version)}
	${call show.var,"configuration file",$(pyre.config)}
	${call show.var,"home",$(pyre.dir)}
	${call show.var,"compiler flags",$(pyre.flags)}
	${call show.var,"defines",$(pyre.defines)}
	${call show.var,"incpath",$(pyre.incpath)}
	${call show.var,"linker flags",$(pyre.ldflags)}
	${call show.var,"libpath",$(pyre.libpath)}
	${call show.var,"libraries",$(pyre.libraries)}
	${call show.var,"dependencies",$(pyre.dependencies)}
	${call show.var,"c++ compile line",${call package.compile.options,c++,pyre}}
	${call show.var,"c++ link line",${call package.link.options,c++,pyre}}

# end of file
