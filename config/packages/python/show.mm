# -*- Makefile -*-
#
# michael a.g. aïvázis
# parasim
# (c) 1998-2019 all rights reserved
#

# display the python configuration
python.show:
	${call show.sec,"python",}
	${call show.var,"version",$(python.version)}
	${call show.var,"configuration file",$(python.config)}
	${call show.var,"home",$(python.dir)}
	${call show.var,"compiler flags",$(python.flags)}
	${call show.var,"defines",$(python.defines)}
	${call show.var,"incpath",$(python.incpath)}
	${call show.var,"linker flags",$(python.ldflags)}
	${call show.var,"libpath",$(python.libpath)}
	${call show.var,"libraries",$(python.libraries)}
	${call show.var,"dependencies",$(python.dependencies)}
	${call show.var,"c++ compile line",${call package.compile.options,c++,python}}
	${call show.var,"c++ link line",${call package.link.options,c++,python}}

# end of file
