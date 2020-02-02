#!/usr/bin/perl

# first, removes keys that have a different date than the current one from
# where they keys and its related information are stored

# second, optimizes the database

#### Make sure this isn't run close after midnight, since current users
#### could then be knocked off.

use CGI qw(:standard);
require("SbeLock.pl");
require("SbeFiles.pl");
use strict;

my $curr_date = date_as_number();
(my $state_file = &lock("data/statefile", "read")) or (die "Couldn't get_state: $!");
my @remove;

while(!eof($state_file)) {

    my $state = new CGI($state_file);

    if ($state->param('last_used') ne $curr_date) {
        push (@remove, $state->param('session_key'));
    }
}
unlock($state_file);

my $session_key;
my $count = 0;
foreach $session_key (@remove) {
    remove_state($session_key);
    remove_key($session_key);
    $count++;
}
print $count . " keys were removed.\n";
log_note("cleanup", "$count keys were removed.");


########## second part

db_connect();
db_optimize();
db_disconnect();
print "Database was optimized.";
log_note("cleanup", "Database was optimized.");

sub date_as_number {
    my @date = localtime(time);
    return (($date[5] + 1900)*10**8 + ($date[4] + 1)*10**3 + $date[3]);
}

sub remove_state {
     my($state_file, $curr_state, @state);
     my $session_key = shift;
     ($state_file = lock("data/statefile", "read")) or (die "Couldn't get_state: $!");
     while (!eof($state_file)) {
        $curr_state = new CGI($state_file);
        (push(@state, $curr_state)) if
             ($curr_state->param('session_key') ne $session_key);
     }
     unlock($state_file);
     ($state_file = &lock("data/statefile", "overwrite")) or (die "Couldn't get_state: $!");
     while($curr_state = pop(@state)) {
        $curr_state->save($state_file);
     }
     unlock($state_file);
}

sub remove_key {
    my($key_file, $new_info); 
    my $session_key = shift;
    ($key_file = &lock("data/keyfile", "read")) or (die "Couldn't remove_key: $!");
    while (<$key_file>) {
        chomp;
        ($new_info .= $_ . "\n") if ($_ ne $session_key);
    }
    unlock($key_file);
    ($key_file = &lock("data/keyfile", "overwrite")) or (die "Couldn't remove_key: $!");
    print $key_file $new_info;
    unlock($key_file);
}
