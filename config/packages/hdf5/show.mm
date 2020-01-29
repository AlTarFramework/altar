# -*- Makefile -*-
#
# michael a.g. aïvázis
# parasim
# (c) 1998-2020 all rights reserved
#

# display the hdf5 configuration
hdf5.show:
	${call show.sec,"hdf5",}
	${call show.var,"version",$(hdf5.version)}
	${call show.var,"configuration file",$(hdf5.config)}
	${call show.var,"home",$(hdf5.dir)}
	${call show.var,"compiler flags",$(hdf5.flags)}
	${call show.var,"defines",$(hdf5.defines)}
	${call show.var,"incpath",$(hdf5.incpath)}
	${call show.var,"linker flags",$(hdf5.ldflags)}
	${call show.var,"libpath",$(hdf5.libpath)}
	${call show.var,"libraries",$(hdf5.libraries)}
	${call show.var,"dependencies",$(hdf5.dependencies)}
	${call show.var,"c++ compile line",${call package.compile.options,c++,hdf5}}
	${call show.var,"c++ link line",${call package.link.options,c++,hdf5}}

# end of file
