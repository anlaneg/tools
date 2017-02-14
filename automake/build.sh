#! /bin/bash
if [ ! -e configure.ac ];
then
    autoscan
    mv configure.scan configure.ac ;
    patch -p0 < configure.ac.diff
fi;
touch NEWS README ChangeLog AUTHORS 
aclocal
autoconf
autoheader
#automake -a
automake --add-missing
