#!/bin/bash

python3 script_for_eawag01_04_for_testing.py

for i in $( ls -d */); do
ONE=`echo $i | cut -d'/' -f1`
echo $ONE;
MYDIR=$i;#$ONE + "/";
echo $MYDIR

#done
cp FetchSEEDSrxnsEAWAG2EdgesListV2.pl $MYDIR;
cp doTheMapping2SMILESandKEGGcmpIDs.pl $MYDIR;
cp addInfoSimcompWithHeader_v2.py $MYDIR;

#echo $MYDIR/EAWAGrxns.txt;done

cd $MYDIR;
cat EAWAGrxns.txt | while read line || [[ -n $line ]];do perl FetchSEEDSrxnsEAWAG2EdgesListV2.pl $line;done
cat *_cmpds.txt > myEdgeList.csv;
cat *_enzyme.txt > myEnzymeInfo.csv ;
cat *AND*.txt > _bothInfo.csv;

FILEbothInfo="_bothInfo.csv";PREFIX=$ONE;mv $FILEbothInfo $PREFIX;

FILE="myEdgeList.csv";
cut -d " " -f 1 $FILE > c1;
cut -d " " -f 2 $FILE > c2;
cat c* | sort | uniq | while read line || [[ -n $line ]];do perl doTheMapping2SMILESandKEGGcmpIDs.pl $line;done

cd "../";done
