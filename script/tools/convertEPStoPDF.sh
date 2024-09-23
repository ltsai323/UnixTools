#!/usr/bin/env sh
inputEPSfile=$1
outputPDFfile=${inputEPSfile%.eps}.pdf

if [ ! -z "$CMSSW_BASE" ]; then
    echo -e "\n\n\n---> CMSSW environment detected. Please open a new section without CMSSW. Thanks"
    exit
fi

ps2pdf $inputEPSfile $outputPDFfile
echo "output file $outputPDFfile"
