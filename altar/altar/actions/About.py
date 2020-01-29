# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
#
# (c) 2013-2020 parasim inc
# (c) 2010-2020 california institute of technology
# all rights reserved
#


# get the package
import altar


# declaration
class About(altar.panel(), family='altar.actions.about'):
    """
    Display information about this application
    """


    # user configurable state
    root = altar.properties.str()
    root.tip = "specify the portion of the namespace to display"


    @altar.export(tip="the name of the app for configuration purposes")
    def name(self, plexus, **kwds):
        """
        Print the name of the app for configuration purposes
        """
        # show me
        plexus.info.log(f"{plexus.pyre_name}")
        # all done
        return


    @altar.export(tip="the application home directory")
    def home(self, plexus, **kwds):
        """
        Print the application home directory
        """
        # show me
        print(altar.home)
        # all done
        return


    @altar.export(tip="the application installation directory")
    def prefix(self, plexus, **kwds):
        """
        Print the application installation directory
        """
        # show me
        print(altar.prefix)
        # all done
        return


    @altar.export(tip="the directory with the altar models")
    def models(self, plexus, **kwds):
        """
        Print the altar model directory
        """
        # show me
        print(altar.modelPrefix)
        # all done
        return


    @altar.export(tip="print the build timestamp")
    def when(self, plexus, **kwds):
        """
        Print the build timestamp
        """
        # show me
        print(altar.meta.date)
        # all done
        return


    @altar.export(tip="the application configuration directory")
    def etc(self, plexus, **kwds):
        """
        Print the application configuration directory
        """
        # show me
        print(altar.etc)
        # all done
        return


    @altar.export(tip="print the version number")
    def version(self, plexus, **kwds):
        """
        Print the version of the altar package
        """
        # make some space
        plexus.info.log(altar.meta.header)
        # all done
        return


    @altar.export(tip="print the copyright note")
    def copyright(self, plexus, **kwds):
        """
        Print the copyright note of the altar package
        """
        # show the copyright note
        plexus.info.log(altar.meta.copyright)
        # all done
        return


    @altar.export(tip="print out the acknowledgments")
    def credits(self, plexus, **kwds):
        """
        Print out the license and terms of use of the altar package
        """
        # make some space
        plexus.info.log(altar.meta.acknowledgments)
        # all done
        return


    @altar.export(tip="print out the license and terms of use")
    def license(self, plexus, **kwds):
        """
        Print out the license and terms of use of the altar package
        """
        # make some space
        plexus.info.log(altar.meta.license)
        # all done
        return


    @altar.export(tip='dump the application configuration namespace')
    def nfs(self, plexus, **kwds):
        """
        Dump the application configuration namespace
        """
        # get the prefix
        prefix = self.root or "altar"
        # show me
        plexus.pyre_nameserver.dump(prefix)
        # all done
        return


    @altar.export(tip='dump the application private filesystem')
    def pfs(self, plexus, **kwds):
        """
        Dump the application private filesystem
        """
        # build the report
        report = "\n".join(plexus.pfs.dump())
        # sign in
        plexus.info.line("pfs:")
        # dump
        plexus.info.log(report)
        # all done
        return


    @altar.export(tip='dump the application virtual filesystem')
    def vfs(self, plexus, **kwds):
        """
        Dump the application virtual filesystem
        """
        # get the prefix
        prefix = self.root or "/altar"
        # build the report
        report = '\n'.join(plexus.vfs[prefix].dump())
        # sign in
        plexus.info.line(f"vfs: root={prefix}")
        # dump
        plexus.info.log(report)
        # all done
        return


# end of file
