#!/usr/bin/env sh

inputrootfile=$1
mkdir -p allhists
root -q -b '~/script/tools/DrawAllHists.C("'$1'")'
