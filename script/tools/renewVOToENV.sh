#!/usr/bin/env sh
# To use VO in submitted job, you need to use this script and load enviorment like
# ( condor job ) in sub file : '''use_x509userproxy = true'''

#voms-proxy-init -voms cms -rfc -out ${HOME}/.x509up_${UID} -valid 192:00 && export X509_USER_PROXY=${HOME}/.x509up_${UID}  && cp ${HOME}/.x509up_${UID}  /tmp/x509up_u${UID}
grid-proxy-init -debug -verify -valid 192:00 -out ${HOME}/.x509up_u${UID}
voms-proxy-init -voms cms -rfc -out ${HOME}/.x509up_u${UID} -valid 192:00
export X509_USER_PROXY=${HOME}/.x509up_u${UID}
