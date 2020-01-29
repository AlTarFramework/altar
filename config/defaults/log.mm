# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
#
# (c) 2013-2020 parasim inc
# (c) 2010-2020 california institute of technology
# all rights reserved
#

# rendering functions
log ?= echo
# indentation
log.halfdent = "  "
log.indent = "    "

# sections
log.sec = \
    $(log) \
    $(palette.cyan)$(1)$(palette.normal): $(2)

# variables
log.var = \
    $(log) \
    $(palette.blue)$(log.indent)$(1)$(palette.normal) \
    = \
    $(palette.normal)$(2)$(palette.normal)

# commands and targets
log.help = \
    $(log) \
    $(palette.blue)$(log.indent)$(1)$(palette.normal) \
    : \
    $(palette.normal)$(2)$(palette.normal)

# text
log.info = $(log) $(1)

# render a build action
log.action = \
    $(log) \
    $(palette.blue)"  [$(1)]"$(palette.normal) \
    $(2)

log.asset = \
    $(log) \
    $(palette.purple)"  [$(1)]"$(palette.normal) \
    $(2)

log.info = \
    $(log) \
    $(palette.cyan)"  [$(1)]"$(palette.normal) \
    $(2)

# terminals that support the ansi color commands
terminals.ansi = ansi vt100 vt102 xterm xterm-color xterm-256color

# colors
ifeq ($(TERM),${findstring $(TERM),$(terminals.ansi)})
include config/defaults/ansi.mm
else
include config/defaults/dumb.mm
endif

# end of file
