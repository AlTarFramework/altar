# -*- Makefile -*-
#
# michael a.g. aïvázis
# parasim
# (c) 1998-2019 all rights reserved
#

# the list of external dependencies of the project
packages ?=

# load the package configuration file
include $(mm.home)/config.mm

# a pattern for loading package configuration files
%.config : config/packages/%/config.mm
	${call show.action,include,$^}
	${eval include $^}

# locate the configuration file of a package
#   usage: package.config {packages}
package.config = \
    ${foreach \
        pkg, \
        $(1), \
        ${and \
            ${strip $(pkg)}, \
            ${value $(pkg).dir}, \
            ${realpath $($(pkg).dir)}, \
            ${realpath config/packages/$(pkg)/config.mm} \
        } \
    }

# existence test
#   usage: package.exists {package}
package.exists = \
    ${and \
        ${call package.config,$(1)}, \
        $(1) \
    }

# construct the contribution of a package to the compile line
#  usage: package.compile.options {package}
package.compile.options = \
    ${foreach \
        category, \
        $(c++.compile.categories),\
        ${addprefix $($(c++).prefix.$(category)),$($(1).$(category))} \
    }

# construct the contribution of a package to the link line
#  usage: package.link.options {package}
package.link.options = \
    ${foreach \
        category, \
        $(c++.link.categories),\
        ${addprefix $($(c++).prefix.$(category)),$($(1).$(category))} \
    }

# given a set of {packages}, build the contribution to the compile line for a given {language}
#  usage: packages.compile.options {packages}
packages.compile.options = \
    ${foreach \
        package, \
        $(1), \
        ${call package.compile.options,$(package)} \
    }

# given a set of {packages}, build the contribution to the link line for a given {language}
#  usage: packages.link.options {packages}
packages.link.options = \
    ${foreach \
        package, \
        $(1), \
        ${call package.link.options,$(package)} \
    }


# end of file
