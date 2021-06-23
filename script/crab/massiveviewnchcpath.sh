tmppath=$1

for nchcpath in `cat $tmppath`;
do
    /home/ltsai/script/crab/viewNCHC.py -i $nchcpath <<EOF
1
1
1
EOF
outputname=`echo $nchcpath | rev | cut -d'/' -f1 | rev`
mv path.txt  ${outputname}.txt
done
