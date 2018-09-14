#!/usr/bin/env sh
# if your VOMS is out of date
# use this to certificate

#temp="/tmp/x509up_u91519"
#mypath="/afs/cern.ch/user/l/ltsai/private/"

# test your grid certificate
grid-proxy-init -debug -verify
# Choose time range you want to run jobs or CRAB
voms-proxy-init -voms cms --valid 168:00

#cp ${temp
