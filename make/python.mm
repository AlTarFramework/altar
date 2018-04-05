# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
#
# (c) 2010-2018 california institute of technology
# (c) 2013-2018 parasim inc
# all rights reserved
#

# compiler
python ?= python3

# default values for user choices
# source layout
src.py ?= $(project)
src.lib ?= lib
src.ext ?= ext
src.bin ?= bin
# destination layout
dest ?= $(prefix)
dest.py ?= $(dest)/packages
dest.lib ?= $(dest)/lib
dest.ext ?= $(dest.py)/$(project)/ext
dest.bin ?= $(dest)/bin

# the layout of the source directory
python.src.py := $(src.py)
python.src.lib := $(src.lib)
python.src.ext := $(src.ext)
python.src.bin := $(src.bin)

# the layout of the destination directory
python.dest.py := $(dest.py)
python.dest.lib := $(dest.lib)
python.dest.ext := $(dest.py)/$(project)/ext
python.dest.bin := $(dest.bin)

# sources
# compute the full list of python sources
python.sources := ${shell find $(python.src.py) -name \*.py}
# the full list of python drivers
python.drivers := ${subst bin/,,${wildcard $(python.src.bin)/*}}
# products
# the stems of the python sources; used to build the target {.pyc} filenames
python.prod.stems := ${basename $(python.sources)}
# the target {.pyc}
python.prod.pyc := $(python.prod.stems:%=$(python.dest.py)/%.pyc)
# the directory layout in the destination
python.prod.dirs := ${sort ${dir $(python.prod.pyc)}}
# the list of drivers
python.prod.drivers := $(python.drivers:%=$(python.dest.bin)/%)

# the package meta-data
python.src.meta.raw := ${wildcard $(python.src.py)/meta}
python.src.meta = ${if $(python.src.meta.raw),$(python.src.meta.raw).py,}
python.prod.meta = ${if $(python.src.meta.raw),$(python.dest.py)/$(python.src.meta.raw).pyc,}


# the main recipe
python.pkg: $(python.prod.pyc) $(python.prod.meta) $(python.prod.drivers)


# the directories
$(python.prod.dirs) $(python.dest.bin): | $(dest)
	${foreach dir,$(@),${call log.action,mkdir,$(dir)};}
	$(mkdirp) $(@)


# the drivers
$(python.prod.drivers): $(python.dest.bin)/% : $(python.src.bin)/% | $(python.dest.bin)
	${call log.action,cp,$<}
	$(cp) $< $(python.dest.bin)


# pyc files
$(python.prod.pyc): $(python.dest.py)/%.pyc: %.py | $(python.prod.dirs)
	${call log.action,python,$<}
	$(python) -m compileall -b -q ${abspath $<}
	$(mv) $(<:.py=.pyc) $@

# package meta-data
$(python.prod.meta): $(python.src.meta) | ${dir $(python.prod.meta)}
	${call log.action,python,$<}
	$(python) -m compileall -b -q ${abspath $<}
	$(mv) $(<:.py=.pyc) $@
	$(rm) $<

$(python.src.meta): ${wildcard $(python.src.py)/meta}
	${call log.action,sed,$<}
	$(sed) \
          -e "s:PROJECT:$(project):g" \
          -e "s:MAJOR:$($(project).major):g" \
          -e "s:MINOR:$($(project).minor):g" \
          -e "s:REVISION:$($(project).revision):g" \
          -e "s|YEAR|$(now.year)|g" \
          -e "s|TODAY|$(now.date)|g" \
          $< > $<.py

# debug targets
python.src:
	${call log.sec,"python source layout",}
	${call log.var,"sources",$(python.src.py)}
	${call log.var,"lib",$(python.src.lib)}
	${call log.var,"extension",$(python.src.ext)}
	${call log.var,"bin",$(python.src.bin)}


python.dest:
	${call log.sec,"python destination layout",}
	${call log.var,"packages",$(python.dest.py)}
	${call log.var,"lib",$(python.dest.lib)}
	${call log.var,"extension",$(python.dest.ext)}
	${call log.var,"bin",$(python.dest.bin)}


python.sources:
	${call log.sec,"python sources","in 'packages'"}
	${foreach src,${sort $(python.sources)},${call log.info,$(log.indent)$(src)};}


python.directories:
	${call log.sec,"python product directories","in '$(python.dest.py)'"}
	${foreach dir,${sort $(python.prod.dirs)},${call log.info,$(log.indent)$(dir)};}

python.pyc:
	${call log.sec,"python byte compiled files","in '$(python.pkg.root)'"}
	${foreach pyc,\
            ${sort $(python.pkg.pyc) $(python.pkg.altar.meta)}, \
            ${call log.info,$(log.indent)$(pyc)};}

log.python.sources:
	echo $(python.sources)

log.python.pyc:
	echo $(python.prod.pyc)

log.python.drivers:
	echo $(python.drivers)
	echo $(python.prod.drivers)


# end of file
