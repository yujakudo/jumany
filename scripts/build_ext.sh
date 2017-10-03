#!/bin/sh
set -e

if [ "$1" = "build" ]; then
	tar xf archives/juman-7.01_subset.tar.gz
	cd juman-7.01_subset
	patch -p1 < ../archives/ext_juman-7.01_03.patch
	./configure --prefix=/var/tmp CFLAGS="-O3 -march=native" LDFLAGS="-Wl,-lc"
	cd lib
	make
	cd ../..
	mkdir -p build/lib/jumany
	cp juman-7.01_subset/lib/.libs/libjuman.so build/lib/jumany

elif [ "$1" = "clean" ]; then
	rm -rf juman-7.01_subset
	rm -f build/lib/jumany/libjuman.so

else
	echo "Unknown command $1"
fi
