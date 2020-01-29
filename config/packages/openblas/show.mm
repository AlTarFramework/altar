# -*- Makefile -*-
#
# michael a.g. aïvázis
# parasim
# (c) 1998-2020 all rights reserved
#

# display the openblas configuration
openblas.show:
	${call show.sec,"openblas",}
	${call show.var,"version",$(openblas.version)}
	${call show.var,"blas",$(openblas.blas)}
	${call show.var,"configuration file",$(openblas.config)}
	${call show.var,"home",$(openblas.dir)}
	${call show.var,"compiler flags",$(openblas.flags)}
	${call show.var,"defines",$(openblas.defines)}
	${call show.var,"incpath",$(openblas.incpath)}
	${call show.var,"linker flags",$(openblas.ldflags)}
	${call show.var,"libpath",$(openblas.libpath)}
	${call show.var,"libraries",$(openblas.libraries)}
	${call show.var,"c++ compile line",${call package.compile.options,c++,openblas}}
	${call show.var,"c++ link line",${call package.link.options,c++,openblas}}

# end of file
