# -*- Makefile -*-
#
# michael a.g. aïvázis
# parasim
# (c) 1998-2019 all rights reserved
#

# display the gsl configuration
gsl.show:
	${call show.sec,"gsl",}
	${call show.var,"version",$(gsl.version)}
	${call show.var,"blas",$(gsl.blas)}
	${call show.var,"configuration file",$(gsl.config)}
	${call show.var,"home",$(gsl.dir)}
	${call show.var,"compiler flags",$(gsl.flags)}
	${call show.var,"defines",$(gsl.defines)}
	${call show.var,"incpath",$(gsl.incpath)}
	${call show.var,"linker flags",$(gsl.ldflags)}
	${call show.var,"libpath",$(gsl.libpath)}
	${call show.var,"libraries",$(gsl.libraries)}
	${call show.var,"dependencies",$(gsl.dependencies)}
	${call show.var,"c++ compile line",${call package.compile.options,c++,gsl}}
	${call show.var,"c++ link line",${call package.link.options,c++,gsl}}

# end of file
