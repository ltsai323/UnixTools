#!/usr/bin/env bash
#sed -e'10aptCut="lbl0Pt>20.&&lbl0Pt<30."' -e'10aptRange="ptRange20.30"' template_0th_LbL0_noKine_TEST.py > tmp.py; time python tmp.py 
#sed -e'10aptCut="lbl0Pt>30.&&lbl0Pt<33."' -e'10aptRange="ptRange30.33"' template_0th_LbL0_noKine_TEST.py > tmp.py; time python tmp.py > /dev/null 2>&1
#sed -e'10aptCut="lbl0Pt>33.&&lbl0Pt<38."' -e'10aptRange="ptRange33.38"' template_0th_LbL0_noKine_TEST.py > tmp.py; time python tmp.py > /dev/null 2>&1
#sed -e'10aptCut="lbl0Pt>38.&&lbl0Pt<45."' -e'10aptRange="ptRange38.45"' template_0th_LbL0_noKine_TEST.py > tmp.py; time python tmp.py > /dev/null 2>&1
#sed -e'10aptCut="lbl0Pt>45."            ' -e'10aptRange="ptRange45"   ' template_0th_LbL0_noKine_TEST.py > tmp.py; time python tmp.py > /dev/null 2>&1
sed -e'10aptCut="lbl0Pt>20.&&lbl0Pt<30."' -e'10aptRange="ptRange20.30"' template_0th_LbL0_noKine_keepMC.py > tmp.py; time python tmp.py 
sed -e'10aptCut="lbl0Pt>30.&&lbl0Pt<33."' -e'10aptRange="ptRange30.33"' template_0th_LbL0_noKine_keepMC.py > tmp.py; time python tmp.py > /dev/null 2>&1
sed -e'10aptCut="lbl0Pt>33.&&lbl0Pt<38."' -e'10aptRange="ptRange33.38"' template_0th_LbL0_noKine_keepMC.py > tmp.py; time python tmp.py > /dev/null 2>&1
sed -e'10aptCut="lbl0Pt>38.&&lbl0Pt<45."' -e'10aptRange="ptRange38.45"' template_0th_LbL0_noKine_keepMC.py > tmp.py; time python tmp.py > /dev/null 2>&1
sed -e'10aptCut="lbl0Pt>45."            ' -e'10aptRange="ptRange45"   ' template_0th_LbL0_noKine_keepMC.py > tmp.py; time python tmp.py > /dev/null 2>&1
rm tmp.py
