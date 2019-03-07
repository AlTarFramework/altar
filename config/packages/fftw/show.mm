# -*- Makefile -*-
#
# michael a.g. aïvázis
# parasim
# (c) 1998-2019 all rights reserved
#

# display the fftw configuration
fftw.show:
	${call show.sec,"fftw",}
	${call show.var,"version",$(fftw.version)}
	${call show.var,"configuration file",$(fftw.config)}
	${call show.var,"home",$(fftw.dir)}
	${call show.var,"compiler flags",$(fftw.flags)}
	${call show.var,"defines",$(fftw.defines)}
	${call show.var,"incpath",$(fftw.incpath)}
	${call show.var,"linker flags",$(fftw.ldflags)}
	${call show.var,"libpath",$(fftw.libpath)}
	${call show.var,"libraries",$(fftw.libraries)}
	${call show.var,"dependencies",$(fftw.dependencies)}
	${call show.var,"c++ compile line",${call package.compile.options,c++,fftw}}
	${call show.var,"c++ link line",${call package.link.options,c++,fftw}}

# end of file
