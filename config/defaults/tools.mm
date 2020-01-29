# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
#
# (c) 2013-2020 parasim inc
# (c) 2010-2020 california institute of technology
# all rights reserved
#

# librarian
ar = ar
ar.create = $(ar) $(ar.flags.create)
ar.extract = $(ar) $(ar.flags.extract)
ar.remove = $(ar) $(ar.flags.remove)
ar.update = $(ar) $(ar.flags.update)
ar.flags.create = rc
ar.flags.extract = x
ar.flags.remove = d
ar.flags.update = cru

# bzr
bzr = bzr
bzr.revno = $(bzr) revno

# cwd
cd = cd

# file attributes
chgrp = chgrp
chgrp.recurse = $(chgrp) $(chgrp.flags.recurse)
chgrp.flags.recurse = -R

chmod = chmod
chmod.recurse = $(chmod) $(chmod.flags.recurse)
chmod.write = $(chmod) $(chmod.flags.write)
chmod.write-recurse = $(chmod.recurse) $(chmod.flags.write)
chmod.flags.recurse = -R
chmod.flags.write = +w

chown = chown
chown.recurse = $(chown) $(chown.flags.recurse)
chown.flags.recurse = -R

# copy
cp = cp
cp.force = $(cp) $(cp.flags.force)
cp.recurse = $(cp) $(cp.flags.recurse)
cp.force-recurse = $(cp) $(cp.flags.force-recurse)
cp.flags.force = -f
cp.flags.recurse = -r
cp.flags.force-recurse = -fr

# data
date = date
date.year = $(date) '+%Y'
date.stamp = $(date) -u

# git
git = git
git.hash = $(git) log --format=format:"%h" -n 1

# loader
ld = ld
ld.out = $(ld) $(ld.flags.out)
ld.shared = $(ld) $(ld.flags.shared)
ld.flags.out =  -o
ld.flags.shared =  -shared

# directories
mkdir = mkdir
mkdirp = $(mkdir) $(mkdir.flags.make-parents)
mkdir.flags.make-parents = -p

# move
mv = mv
mv.f = $(mv) $(mv.flags.force)
mv.flags.force = -f

# ranlib
ranlib = ranlib
ranlib.flags =

# remove
rm = rm
rm.force = $(rm) $(rm.flags.force)
rm.recurse = $(rm) $(rm.flags.recurse)
rm.force-recurse = $(rm) $(rm.flags.force-recurse)
rm.flags.force = -f
rm.flags.recurse = -r
rm.flags.force-recurse = -rf

rmdir = rmdir

# rsync
rsync = rsync
rsync.recurse = $(rsync) $(rsync.flags.recurse)
rsync.flags.recurse = -ruavz --progress --stats

# ssh
ssh = ssh
scp = scp
scp.recurse = $(scp) $(scp.flags.recurse)
scp.flags.recurse = -r

# sed
sed = sed

# tags
tags = true
tags.flags =
tags.home =
tags.file = $(tags.home)/TAGS

# tar
tar = tar
tar.flags.create = -cvj -f

# TeX and associated tools
tex.tex = tex
tex.latex = latex
tex.pdflatex = pdflatex
tex.bibtex = bibtex
tex.dvips = dvips
tex.dvipdf = dvipdf

# yacc
yacc = yacc
yacc.c = y.tab.c
yacc.h = y.tab.h

# end of file
