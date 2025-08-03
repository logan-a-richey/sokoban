#!/bin/perl 

use strict;
use warnings; 
use feature 'say';
use File::Basename;
use Data::Dumper;
use JSON;

# persistent level vars
my $data = {};

# ------------------------------------

# data directory to read
my $level_dir = "leveldata";

# loop over all files in a directory
opendir(my $dh, $level_dir) or die "Cannot opendir $level_dir: $!";
while (my $file_name = readdir($dh)) {
    # skip dot files
    next if ($file_name eq '.' || $file_name eq '..');

    my $file_path = "$level_dir/$file_name";

    # only parse regular text files
    next unless (-f $file_path);

    # extract the filename. this will be the levelset name
    my $current_levelset = basename($file_path, ".txt");

    # keep track of what level we are on in the file
    my $current_level = 0;

    # read all the levels in the levelset file line by line
    open (my $fh, '<', $file_path) or warn "[W] Cannot open file $file_path: $!";
    while (my $line = <$fh>) {
        # skip blank lines
        chomp $line;
        next if ($line =~ /^\s*$/);
        
        # if a line begins with a ;, this marks a new level
        if ($line =~ /^\s*\;/) {
            $current_level++;
            next;
        }

        # append level data line to
        $line =~ s/\s/_/g;
        $data->{$current_levelset}{"level_$current_level"} .= "$line;";
    }
    close($fh);
}
closedir($dh);

# write output level data file
open(my $out_fh, '>', 'out.json') or die "$!";
    my $json_str = encode_json($data);
    my $json_str_pretty = JSON->new->pretty->encode($data);
    say $out_fh $json_str_pretty;
close($out_fh);

