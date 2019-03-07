# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
#
# (c) 2013-2019 parasim inc
# (c) 2010-2019 california institute of technology
# all rights reserved
#

# the name and layout of the extension
extension.layout = \
  ${eval $(1).name := $(1)} \
  ${eval $(1).src := $(src.ext)} \
  ${eval $(1).lib := $(dest.lib)} \
  ${eval $(1).ext := $(dest.ext)} \
  ${eval $(1).staging := $(dest.staging)/$($(1).name)} \

# the parts necessary to build the extension module
extension.products = \
  ${eval $(1).module := $(1:%module=%)} \
  ${eval $(1).module.entry := $($(1).module).cc} \
  ${eval $(1).module.src := $($(1).src)/$($(1).module.entry)} \
  ${eval $(1).module.so := $($(1).ext)/$($(1).module)$(python.module-suffix)} \

# make the module library
extension.lib = \
  ${eval $(1).library := lib$($(1).name)} \
  ${eval $($(1).library).src := $($(1).src)} \
  ${eval $($(1).library).staging := $($(1).staging)} \
 \
  ${eval $($(1).library).sources := \
      ${shell find $($(1).src) -name \*.cc -and -not -name $($(1).module.entry)}} \
  ${eval $($(1).library).headers :=} \
  ${eval $($(1).library).packages := $($(1).packages)} \
 \
  ${call library.init,$($(1).library)} \

# accommodate the external dependencies
extension.packages = \
  ${eval $(1).packages ?=} \
  ${eval include $($(1).packages:%=config/packages/%/config.mm)} \
  ${eval $(1).packages: $($(1).packages:%=%.config) }

extension.targets = \
  ${eval $(1).module.dep := \
    $($(1).module.src) \
    ${foreach lib,$($(project).libraries),$($(lib).archive)} \
    $($($(1).library).archive) } \
 \
  ${eval \
    $(1): $(1).archive $(1).extension \
    ; \
      ${call log.asset,$(1)} \
  } \
 \
  ${eval $(1).archive: $($(1).library).archive} \
 \
  ${eval $(1).extension : $(1).module} \
 \
  ${eval $(1).module : $($(1).module.so)} \
 \
  ${eval \
    $($(1).module.so) : $($(1).module.dep)\
    ; \
      ${call log.action,shared,$$@} ; \
      ${call c++.so,$$@,$$<,$($(1).packages)}; \
  } \

# debugging targets
extension.log = \
  ${eval \
    $(1).c++ : $(1).packages ; \
      ${call log.sec,$(1),compiling} ; \
      ${call log.var,compiler,$(c++)}; \
      ${call log.var,packages,$($(1).packages)}; \
      ${call log.var,compile,${call c++.compile.options,$($(1).packages)}}; \
      ${call log.var,link,${call c++.link.options,$($(1).packages)}}; \
  }

# the constructor
extension.init = \
  ${call extension.layout,$(1)} \
  ${call extension.products,$(1)} \
  ${call extension.lib,$(1)} \
  ${call extension.targets,$(1)} \
  ${call extension.log,$(1)} \

# instantiate the project extensions
${foreach \
  extension, \
  $($(project).extensions), \
  ${call extension.init,$(extension)} \
}

# make a target that builds them all
$(project).extensions: $(project).libraries $($(project).extensions)

# end of file
