#!/bin/bash

NKF=nkf
JUMAN=../dist/juman-7.01_ext_win32/juman.exe
# if MinGW
if [ "$COMSPEC" != "" ]; then
	NKF=/b/bin/nkf32.exe
fi

if [ "$1" != "" ]; then
	JUMAN=$1
fi

function test() {
	of=result_$1_to_$2.txt
	option="--if $1 --of $of --enc $3"
	echo "juman $option"
	$JUMAN $option
	if [ ! -s $of ]; then
		echo "NG :File not exists or zero."
		return -1
	fi
	if [ ! $($NKF -g $of | grep -e $2) ]; then
		echo "NG : Encoding is "
		$NKF -g $of
		return -1
	fi
	echo "OK"
	return 0
}

rm -f result_*.txt
echo Test $JUMAN

echo Test UTF-8 to UTF-8
test utf-8.txt UTF-8 utf-8

echo Test UTF-8 to Shift_JIS
test utf-8.txt Shift_JIS ",sjis"

echo Test Shift_JIS to UTF-8
test sjis.txt UTF-8 "sjis,"

echo Test Shift_JIS to Shift_JIS
test sjis.txt Shift_JIS "sjis"
