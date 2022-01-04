#!/usr/bin/env sh
# if your VOMS is out of date
# use this to certificate

#temp="/tmp/x509up_u91519"
#mypath="/afs/cern.ch/user/l/ltsai/private/"

# test your grid certificate
grid-proxy-init -debug -verify -valid 192:00 -out ${HOME}/.x509up_u${UID}
export X509_USER_PROXY=${HOME}/.x509up_u${UID}
# Choose time range you want to run jobs or CRAB
#voms-proxy-init -voms cms --valid 192:00

#cp ${temp
