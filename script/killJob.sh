#!/usr/bin/env sh
cmd=$1
for a in `ps -U ltsai | grep "$cmd" | tr -s " " | cut -d" " -f2`; do kill $a; done
