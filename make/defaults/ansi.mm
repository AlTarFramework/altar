# -*- Makefile -*-
#
# michael a.g. aïvázis
# parasim
# (c) 1998-2018 all rights reserved
#

# colors
csi = "[$(1)m"
palette.normal := ${call csi,0}
palette.black := ${call csi,0;30}
palette.red := ${call csi,0;31}
palette.green := ${call csi,0;32}
palette.brown := ${call csi,0;33}
palette.blue := ${call csi,0;34}
palette.purple := ${call csi,0;35}
palette.cyan := ${call csi,0;36}
palette.light-gray := ${call csi,0;37}

# bright-colors
palette.dark-gray := ${call csi,1;30}
palette.light-red := ${call csi,1;31}
palette.light-green := ${call csi,1;32}
palette.yellow := ${call csi,1;33}
palette.light-blue := ${call csi,1;34}
palette.light-purple := ${call csi,1;35}
palette.light-cyan := ${call csi,1;36}
palette.white := ${call csi,1;37}

# end of file
