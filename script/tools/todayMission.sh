#!/usr/bin/env sh

#cowsay to notify today's mission

inputFile=$1

(echo -e "today's mission:\n"; echo -e `cat -n $inputFile`) | cowsay -W80 -e 'oo'

