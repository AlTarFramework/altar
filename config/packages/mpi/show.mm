# -*- Makefile -*-
#
# michael a.g. aïvázis
# parasim
# (c) 1998-2019 all rights reserved
#

# display the mpi configuration
mpi.show:
	${call show.sec,"mpi",}
	${call show.var,"version",$(mpi.version)}
	${call show.var,"configuration file",$(mpi.config)}
	${call show.var,"home",$(mpi.dir)}
	${call show.var,"compiler flags",$(mpi.flags)}
	${call show.var,"defines",$(mpi.defines)}
	${call show.var,"incpath",$(mpi.incpath)}
	${call show.var,"linker flags",$(mpi.ldflags)}
	${call show.var,"libpath",$(mpi.libpath)}
	${call show.var,"libraries",$(mpi.libraries)}
	${call show.var,"c++ compile line",${call package.compile.options,c++,mpi}}
	${call show.var,"c++ link line",${call package.link.options,c++,mpi}}

# end of file
