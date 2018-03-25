# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
#
# (c) 2010-2018 california institute of technology
# (c) 2013-2018 parasim inc
# all rights reserved
#

# compilers
python ?= python3

# python
python.bin.root := bin
python.src.root := packages

# sources
python.sources := ${shell find $(python.src.root) -name \*.py}
python.scripts := ${shell find $(python.bin.root) -type f}

# products
python.pkg.root := $(blddir)
python.pkg.bin := $(blddir)/bin
python.pkg.stems := ${basename $(python.sources)}
python.pkg.altar.meta := $(python.pkg.root)/packages/altar/meta.pyc
python.pkg.pyc := $(python.pkg.stems:%=$(python.pkg.root)/%.pyc)
python.pkg.dirs := ${sort ${dir $(python.pkg.pyc)}}
python.pkg.scripts := $(python.scripts:%=$(python.pkg.root)/%)

# the overall python recipe
python.pkg: $(python.pkg.pyc) $(python.pkg.altar.meta) $(python.pkg.scripts)

# the scripts
$(python.pkg.scripts): $(python.pkg.root)/% : % | $(python.pkg.bin)
	${call log.action,cp,$<}
	$(cp) $< $(python.pkg.bin)

# python
$(python.pkg.pyc): $(python.pkg.root)/%.pyc: %.py | $(python.pkg.dirs)
	${call log.action,python,$<}
	$(python) -m compileall -b -q ${abspath $<}
	$(mv) $(<:.py=.pyc) $@

$(python.pkg.altar.meta): $(python.src.root)/altar/meta.py
	${call log.action,python,$<}
	$(python) -m compileall -b -q ${abspath $<}
	$(mv) $(<:.py=.pyc) $@
	$(rm) $(python.src.root)/altar/meta.py

$(python.src.root)/altar/meta.py: $(python.src.root)/altar/meta
	${call log.action,sed,$<}
	$(sed) \
          -e "s:MAJOR:$(altar.major):g" \
          -e "s:MINOR:$(altar.minor):g" \
          -e "s:REVISION:$(altar.revision):g" \
          -e "s|YEAR|$(now.year)|g" \
          -e "s|TODAY|$(now.date)|g" \
          $< > $<.py

$(python.pkg.dirs) $(python.pkg.bin): | $(blddir)
	${foreach dir,$(@),${call log.action,mkdir,$(dir)};}
	$(mkdirp) $(@)

# debug target
python.sources:
	${call log.sec,"python sources","in 'packages'"}
	${foreach src,${sort $(python.sources)},${call log.info,$(log.indent)$(src)};}

python.directories:
	${call log.sec,"python product directories","in '$(python.pkg.root)'"}
	${foreach dir,${sort $(python.pkg.dirs)},${call log.info,$(log.indent)$(dir)};}

python.pyc:
	${call log.sec,"python byte compiled files","in '$(python.pkg.root)'"}
	${foreach pyc,\
            ${sort $(python.pkg.pyc) $(python.pkg.altar.meta)}, \
            ${call log.info,$(log.indent)$(pyc)};}

# end of file
