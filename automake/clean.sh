#! /bin/bash
if [ -e Makefile ];
then
    make distclean
fi;
rm -f AUTHORS  autoscan.log  ChangeLog  configure.in  COPYING  INSTALL  NEWS  README config.h.in~  \
        configure.ac.orig  configure.ac.rej stamp-h1 
rm -rf autom4te.cache
rm -f  configure config.h config.log aclocal.m4  compile  config.status  install-sh  Makefile.in  missing depcomp 
