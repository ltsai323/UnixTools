#!/usr/bin/env bash
#sed -e'17aptCut="lbtkPt>20.&&lbtkPt<30."' -e'17aptRange="ptRange20.30"'  template_sysErr_LbTk_noKine.py> tmp.py; time python tmp.py
#sed -e'17aptCut="lbtkPt>30.&&lbtkPt<33."' -e'17aptRange="ptRange30.33"'  template_sysErr_LbTk_noKine.py> tmp.py; time python tmp.py > /dev/null 2>&1
#sed -e'17aptCut="lbtkPt>33.&&lbtkPt<38."' -e'17aptRange="ptRange33.38"'  template_sysErr_LbTk_noKine.py> tmp.py; time python tmp.py > /dev/null 2>&1
#sed -e'17aptCut="lbtkPt>38.&&lbtkPt<45."' -e'17aptRange="ptRange38.45"'  template_sysErr_LbTk_noKine.py> tmp.py; time python tmp.py > /dev/null 2>&1
#sed -e'17aptCut="lbtkPt>45."            ' -e'17aptRange="ptRange45"   '  template_sysErr_LbTk_noKine.py> tmp.py; time python tmp.py > /dev/null 2>&1
sed -e'17aptCut="lbtkPt>20.&&lbtkPt<30."' -e'17aptRange="ptRange20.30"'  template_sysErr_LbTk_noKine_keepMC.py> tmp.py; time python tmp.py
sed -e'17aptCut="lbtkPt>30.&&lbtkPt<33."' -e'17aptRange="ptRange30.33"'  template_sysErr_LbTk_noKine_keepMC.py> tmp.py; time python tmp.py > /dev/null 2>&1
sed -e'17aptCut="lbtkPt>33.&&lbtkPt<38."' -e'17aptRange="ptRange33.38"'  template_sysErr_LbTk_noKine_keepMC.py> tmp.py; time python tmp.py > /dev/null 2>&1
sed -e'17aptCut="lbtkPt>38.&&lbtkPt<45."' -e'17aptRange="ptRange38.45"'  template_sysErr_LbTk_noKine_keepMC.py> tmp.py; time python tmp.py > /dev/null 2>&1
sed -e'17aptCut="lbtkPt>45."            ' -e'17aptRange="ptRange45"   '  template_sysErr_LbTk_noKine_keepMC.py> tmp.py; time python tmp.py > /dev/null 2>&1
rm tmp.py
