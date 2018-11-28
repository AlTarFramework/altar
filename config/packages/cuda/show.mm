# -*- Makefile -*-
#
# Lijun Zhu
# Caltech
# (c) 1998-2018 all rights reserved
#

# display the cuda configuration
mpi.show:
	${call show.sec,"cuda",}
	${call show.var,"version",$(cuda.version)}
	${call show.var,"configuration file",$(cuda.config)}
	${call show.var,"home",$(cuda.dir)}
	${call show.var,"compiler flags",$(cuda.flags)}
	${call show.var,"defines",$(cuda.defines)}
	${call show.var,"incpath",$(cuda.incpath)}
	${call show.var,"linker flags",$(cuda.ldflags)}
	${call show.var,"libpath",$(cuda.libpath)}
	${call show.var,"libraries",$(cuda.libraries)}
	${call show.var,"c++ compile line",${call package.compile.options,c++,cuda}}
	${call show.var,"c++ link line",${call package.link.options,c++,cuda}}

# end of file
