#! /usr/bin/perl

# This script takes rxn id from eawag database, 
# use rxnID as argument to fetch the associate web page 
# go through all the lines grabbing duplet or triplets of kind 
# c1_c2 or c1 enzyme c2
# this script will be embedded inside Rscript running igraph
# it is meant to generate edge list for igraph function
#
# usage example  cat EAWAGrxns.txt | while read line || [[ -n $line ]]; 
#do ./FetchSEEDSrxnsEAWAG2EdgesList.pl $line; 
#cat *cmpds.txt > myEdgeList.csv; cat *enzyme.txt > myEnzymeInfo.csv ;cat *AND*.txt > both;
# done
# inside EAWAGrxns.txt
# you will have something like
#r1205
#r1206
#r1210
#
# added a check to see if a reac id in eawag can have more than one pair of compounds 
# associated with the same reac id
# 19-10-20
# Author: Maria Persico
# 
# This software is distributed under open-source license
# with no liability accepted for any loss or damage arising from the use of the script.
# The code can be re-destributed and altered
# with the acknowledgement of the original source.

use strict;

use POSIX qw(strftime);

my $date = strftime "%m_%d_%Y_%T", localtime;
print "$date\n";
# define two hashes to collect relevant info
my %reacID_c1_c2;
my %reacID_enzymeID; 

my $value;
if (defined $ARGV[0]) {
    $value = $ARGV[0];
}
else {
    $value = <STDIN>;
}

print "$value\n";
chomp $value;

my $rxnID = $value; #example "r0074";

our $output_file2=$date . "_" . $rxnID . "_cmpds.txt";
print  "$output_file2\n";

our $output_file3=$date . "_" . $rxnID . "_enzyme.txt";
print  "$output_file3\n";

our $output_file4=$date . "_" . $rxnID . "_enzymeANDcmpds.txt";
print  "$output_file4\n";

our $expasyInfo;

my $content=$value . '.html';

print "$content\n";

#chomp $ARGV[0];

system("wget -O- \"http://eawag-bbd.ethz.ch/servlets/pageservlet?ptype=r&reacID=$value\" > $content");

open(FILECONTENT, "<$content") || die "non posso aprire $content\n";
my $flag = 1; # check if there is more than one pair of cmpds

while (!eof(FILECONTENT))
{

###

my  $line=<FILECONTENT>;

chomp $line;

if ($line =~ /href/ && $line =~ /compID=c[0-9]{4}/) {
print "found match with cmpID  \n";
my @datacompID = split '=', $&;
print $datacompID[1],"\n";

# now put the info inside hash for pairs of cmpds

    if (!exists $reacID_c1_c2{$rxnID}){ # $data2[1] is c1 or first occurrence compID=c[0-9]{4}
    print "initialize dictio\n";
    $reacID_c1_c2{$rxnID} = $datacompID[1];

    print "key is rxnID, value is cmpID first element of the duplet: $reacID_c1_c2{$rxnID}\n";

    }elsif(exists $reacID_c1_c2{$rxnID}){ 
    # now I have to update the hash with second element of the duplet made by the two cmpds
    $reacID_c1_c2{$rxnID} = $reacID_c1_c2{$rxnID} . ' ' . $datacompID[1];

    print "key is rxnID value is cmpID second element of the duplet: $reacID_c1_c2{$rxnID}\n";

    open(F_OUT2, ">>$output_file2") || die "non posso aprire $output_file2\n";
    print F_OUT2 "$reacID_c1_c2{$rxnID}\n";
    close F_OUT2;
    }

}
                 
if ($line =~ /href/ && $line =~ /enzymeID=e[0-9]{4}/) {
print "getting enzyme id  \n";
my @data1 = split '=', $&;
print $data1[1],"\n";

# put inside hash rxn enzymeID

    if (!exists $reacID_enzymeID{$rxnID}){ # 
    print "hello enzyme\n";
                
    $reacID_enzymeID{$rxnID} = $data1[1];
    open(F_OUT3, ">>$output_file3") || die "non posso aprire $output_file3\n";
    print F_OUT3 "$rxnID $reacID_enzymeID{$rxnID}\n";
    close F_OUT3;
    }elsif(exists $reacID_enzymeID{$rxnID} && $flag == 1){ 
    print "attention required, it is strange to have more than one enzyme for a specific reaction\n";
    exit;
    }
} # end of fetching eawag enzyme ID 
if ($line =~ /href/ && $line =~ /http\:\/\/enzyme\.expasy\.org\/EC\//) {

#now I have to update the hash with enzyme info
      my $expasyInfoDirty =$';

      print "here expasy info:$expasyInfo\n";
my @dataexpasyInfoDirty = split '\"\>ExPASy', $';
print $dataexpasyInfoDirty[0],"\n";
my $expasyInfo=$dataexpasyInfoDirty[0];
      $reacID_enzymeID{$rxnID} = $reacID_enzymeID{$rxnID} . ' ' . $expasyInfo;
      open(F_OUT3, ">>$output_file3") || die "non posso aprire $output_file3\n";
      print F_OUT3 "$rxnID $reacID_enzymeID{$rxnID}\n";
      close F_OUT3;
}
                 
############## if there is another couple of cmpds / @enzyme??? partecipating in the same reaction
# one needs to grab the others cmpds id and update the hash
### update flag of one unit
if ($line =~ /href/ && $line =~ /Display/) {
open(F_OUT4, ">>$output_file4") || die "non posso aprire $output_file4\n";
      print F_OUT4 "$rxnID $reacID_c1_c2{$rxnID} $reacID_enzymeID{$rxnID}\n";
      close F_OUT4;


$flag++;
next;
}else{
next;
}

} # end of while

close FILECONTENT;

while ((my $k,my $v) = each %reacID_c1_c2) {
print "check hash content $k\t$v\n";
}

while ((my $k,my $v) = each %reacID_enzymeID) {
print "check hash with enzyme info $k\t$v\n";
}







