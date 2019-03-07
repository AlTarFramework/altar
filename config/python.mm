# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
#
# (c) 2013-2019 parasim inc
# (c) 2010-2019 california institute of technology
# all rights reserved
#

# compiler
python ?= python3

# compute the module suffix
python.module-suffix := ${shell $(python)-config --extension-suffix}

# the layout of the source directory
python.src.py := $(src.py)
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
$(project).package: $(python.prod.pyc) $(python.prod.meta) $(python.prod.drivers)
	${call log.asset,$(project).package}


# the directories
$(python.prod.dirs) : | $(dest) $(python.dest.bin)
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
$(python.prod.meta): | ${dir $(python.prod.meta)}
	${call log.action,sed,$(python.src.meta.raw)}
	$(sed) \
          -e "s:PROJECT:$(project):g" \
          -e "s:MAJOR:$($(project).major):g" \
          -e "s:MINOR:$($(project).minor):g" \
          -e "s:REVISION:$($(project).revision):g" \
          -e "s|YEAR|$(now.year)|g" \
          -e "s|TODAY|$(now.date)|g" \
          $(python.src.meta.raw) > $(python.src.meta)
	${call log.action,python,$(python.src.meta)}
	$(python) -m compileall -b -q ${abspath $(python.src.meta)}
	$(mv) $(python.src.meta:.py=.pyc) $(python.prod.meta)
	$(rm) $(python.src.meta)

# always rebuild the meta file since it really depends on the git hash more than anything else
.PHONY: $(python.prod.meta)

# debug targets
python.src:
	${call log.sec,"python source layout",}
	${call log.var,"sources",$(python.src.py)}
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
