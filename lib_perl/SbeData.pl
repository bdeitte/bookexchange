#!/usr/bin/perl
# part of Quixote's Exchange
# Copyright 1999  Brian Deitte

require("SbeLock.pl");

my $areasfile = "$DATA_DIR/areas.dat";

use strict;

# the following routines get the current time/date and makes
# the date a number for easier comparison operations

sub get_date {
    my @date = localtime(time);
    return join('/', ($date[4] + 1,$date[3],$date[5] + 1900));
}

sub get_time {
    return (scalar localtime);
}

sub get_book_fields {

    return qw/email title author dept class isbn condition other price date item_id/;
}

sub get_areas {
    
    my($departments, $data);
    ($data = &lock ($areasfile, "read")) or (die "Couldn't get_areas: $!");
    while (<$data>) {
        # s/^\s+$//g;          # remove leading or trailing spaces
        $departments .= $_;  # add to the string
    }
    unlock($data);
    return \$departments;
}

1;
