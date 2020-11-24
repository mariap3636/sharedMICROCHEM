#! /usr/bin/perl



use strict;

use POSIX qw(strftime);

my $date = strftime "%m_%d_%Y_%T", localtime;
print "$date\n";
# define two hashes to collect relevant info

#my %reacID_c1_c2;
my %cmpID_SMILES_keggcmpID; 
#$reacID_enzymeID

my $value;
if (defined $ARGV[0]) {
    $value = $ARGV[0];
}
else {
    $value = <STDIN>;
}

print "$value\n";
chomp $value;

my $cmpPrefix;# = $value; #example "gly";


our $output_file=$date . "_" . $cmpPrefix . "_withMapping2SMILESandKEGG.txt";
print  "$output_file\n";


my $content=$value . '.html';

print "$content\n";

#chomp $ARGV[0];

system("wget -O- \"http://eawag-bbd.ethz.ch/servlets/pageservlet?ptype=c&compID=$value\" > $content");

open(FILECONTENT, "<$content") || die "non posso aprire $content\n";
my $flag = 1; # check if there is more than one pair of cmpds

while (!eof(FILECONTENT))
{

my  $line=<FILECONTENT>;

chomp $line;

if ($line =~ /SMILES String:/){
print "found match with smiles string  \n";
my $smilesInfoDirty =$';
print "here smiles info:$smilesInfoDirty\n";
my @datasmilesInfoDirty = split '<p>', $';
print $datasmilesInfoDirty[0],"\n";
my $smilesInfo=$datasmilesInfoDirty[0];
      $cmpID_SMILES_keggcmpID{$value} = $smilesInfo;#$cmpID_SMILES_keggcmpID{$value} . ' ' . $smilesInfo;
#} # && $line =~ /compID=c[0-9]{4}/) {

my $myKEGGcmpIDfile=$value . '_simcompOut.txt';

system("curl -F smiles=\'$smilesInfo\' -F cutoff=0.99 -F limit=10 http://rest.genome.jp/simcomp/ > $myKEGGcmpIDfile");

}else{
next;
}

} # end of while

close FILECONTENT;

while ((my $k,my $v) = each %cmpID_SMILES_keggcmpID) {
print "check hash content $k\t$v\n";
}