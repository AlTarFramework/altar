# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
#
# (c) 2013-2018 parasim inc
# (c) 2010-2018 california institute of technology
# all rights reserved
#

ext.obj := .o
ext.lib := .a
ext.dll := .so


# there are three potential libraries to build:
# the base library, a library with the cuda code, and a library with mpi code

library.init = \
  ${eval $(1).name := $(1)} \
  ${eval $(1).src := $(src.lib)/$($(1).name)} \
  ${eval $(1).lib := $(dest.lib)} \
  ${eval $(1).inc := $(dest.inc)} \
  ${eval $(1).staging := $(dest.staging)/$($(1).name)}

# discover the library assets
library.assets = \
 \
  ${eval $(1).sources ?= ${shell find $($(1).src) -name \*.cc}} \
  ${eval $(1).headers ?= ${shell find $($(1).src) -name \*.h -or -name \*.icc}} \
  ${eval $(1).archive ?= $($(1).lib)/$($(1).name)$(ext.lib)}

# publish the library public headers
library.api = \
 \
  ${eval $(1).api := \
    ${addprefix \
      $($(1).inc)/$(project), \
      ${subst $($(1).src),,$($(1).headers)} \
    } \
  } \
 \
  ${eval $(1).api.dirs := \
    ${addprefix \
      $($(1).inc)/$(project), \
      ${subst $($(1).src),,${sort ${dir $($(1).headers)}}} \
    } \
  } \
 \
  ${eval $(1): $(1).api $(1).archive} \
 \
  ${eval $(1).api: $($(1).inc) $($(1).api.dirs) $($(1).api)} \
 \
  ${eval \
    $($(1).api) : $($(1).inc)/$(project)/% : $($(1).src)/% \
    ; \
      ${call log.action,publish,$$<} ; \
      $(cp) $$< $$@ \
  }

# build the project archive
library.archive = \
 \
  ${eval $(1).objs := \
    ${addprefix \
      $($(1).staging)/, \
      ${subst /,~,$($(1).sources:$($(1).src)/%.cc=%$(ext.obj))} \
    } \
  } \
 \
  ${eval $(1).archive: $($(1).lib) $($(1).staging) $($(1).archive)} \
 \
  ${eval $($(1).archive): $($(1).objs) ; \
    ${call log.action,ar,$$@} ; \
    $(ar.update) $$@ $$^ ; \
  } \
 \
  ${eval ${foreach source,$($(1).sources),\
      ${eval \
        $($(1).staging)/${subst /,~,$(source:$($(1).src)/%.cc=%$(ext.obj))} \
        : \
          $(source) \
        ; set -e; \
          ${call log.action,$(c++),$$<}; \
          ${call c++.compile,$(1),$$@,$$<}; \
          $(cp) $$(@:$(ext.obj)=.d) $$@.$$$$ ; \
          $(sed) \
              -e 's/\#.*//' \
              -e 's/^[^:]*: *//' \
              -e 's/ *\\$$$$//' \
              -e '/^$$$$/d' \
              -e 's/$$$$/ :/' \
              $$(@:$(ext.obj)=.d) < $$(@:$(ext.obj)=.d) >> $$@.$$$$ ; \
          $(mv) $$@.$$$$ $$(@:$(ext.obj)=.d) \
      } \
    } \
  }

# build all relevant directories
library.dirs = \
 \
  ${eval \
    $($(1).api.dirs) $($(1).staging) : \
    ; \
      ${call log.action,mkdir,$$@} ; \
      $(mkdirp) $$@ \
  }

# instantiate all the project libraries
${foreach \
    library,\
    $($(project).libraries), \
    ${call library.init,$(library)} \
    ${call library.assets,$(library)} \
    ${call library.api,$(library)} \
    ${call library.archive,$(library)} \
    ${call library.dirs,$(library)} \
}

# make a target that bulds them all
project.libraries: $($(project).libraries)

# end of file
