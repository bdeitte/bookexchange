#!/usr/bin/perl
# part of Quixote's Exchange
# Copyright 1999  Brian Deitte

require("SbeLock.pl");

my $session_key = path_info();
$session_key =~ s/^\///;

my $baseurl = $BASE_URL;
my $cgiurl = $CGI_URL;
my $statefile = "$DATA_DIR/statefile";
my $keyfile = "$DATA_DIR/keyfile";

my $time = time();
# $time is used elsewhere, so don't remove
my $rander=3.14159*($time+$$);
srand($rander);

use strict;

sub get_session_key {
	
	return $session_key;
}

sub update_session {
    unless ($session_key=~/^\d+$/) { # make sure the person supposed to be here
        print redirect("$cgiurl/login.cgi");
        exit 0;
    }
 
    get_state();
    save_state();
}

sub start_session {

    # just pretend this isn't stupid, ok?
    my $num=(int(10*rand));
    remove_old_keys() if ($num == 1);

    $session_key = &generate_session_key();
    # pick a new number if last one already present
    while (&find_key()) {
        $session_key = &generate_session_key();
    }
    param(-name=>'session_key', -value=>$session_key);
    add_key();
    clear_state();
}

sub remove_session {

    remove_state();
    remove_key();
}

# when done with something, we want to get rid of everything in the
# session key except for the email and password and booklist information
sub clear_state() {
    my($password, $email, @booklist, $last_used);
    $password = param('password');
    $email = param('email');
    @booklist = param('booklist');
    $last_used = param('last_used');
    Delete_all();
    param(-name=>'session_key', -value=>$session_key);
    param(-name=>'password', -value=>$password);
    param(-name=>'email', -value=>$email);
    param(-name=>'booklist', -value=>\@booklist);
    param(-name=>'last_used', -value=>$last_used);
    save_state();
}

sub generate_session_key {

    my $num=(1+int(100000000*rand));
    return($num);
}

sub get_state() {
     my($state_file, $state, $found_state);
     $found_state = 0;
     ($state_file = lock($statefile, "read")) or (die "Couldn't get_state: $!");
     while (!eof($state_file)) {
        $state = new CGI($state_file);
        if ($state->param('session_key') eq $session_key) {
            $found_state = 1;
            last;
        }
     }
     unlock($state_file);
     # need this line otherwise if key isn't found, last state in file is defaulted to
     ($found_state) or (die "Couldn't get_state: key not found.");

     # insert old params into current params
     # also overwrites any old params of the same name as a new one
     my($field, @fields, @get_fields);
     @fields = $state->param;
     foreach $field (@fields) {
         @get_fields = $state->param($field);
         param(-name=>$field, value=>\@get_fields);
     }
     return 1;
}

sub save_state {
     remove_state();
     my $date = date_as_number();
     param(-name=>'last_used', -value=>$date);
     (my $state_file = lock($statefile, "append")) or (die "Couldn't save_state: $!");
     save_parameters($state_file);
     unlock($state_file);
}

sub date_as_number {
    my @date = localtime(time);
    return (($date[5] + 1900)*10**8 + ($date[4] + 1)*10**3 + $date[3]);
}

sub remove_state {
     my($state_file, $curr_state, @state);
     ($state_file = lock($statefile, "read")) or (die "Couldn't get_state: $!");
     my $date = date_as_number();
     while (!eof($state_file)) {
        $curr_state = new CGI($state_file);
        (push(@state, $curr_state)) if
             ($curr_state->param('session_key') ne $session_key);
     }
     unlock($state_file);
     ($state_file = &lock($statefile, "overwrite")) or (die "Couldn't get_state: $!");
     while($curr_state = pop(@state)) {
        $curr_state->save($state_file);
     }
     unlock($state_file);
}

sub find_key {

    my($key_file, $key_found, $akey, $atime);
    ($key_file = &lock($keyfile, "read")) or (die "Couldn't find_key:$!");
    while (<$key_file>) {

	($akey, $atime) = split /:/, $_;
        ($session_key eq $akey) and ($key_found = 1, last);
    }
    unlock($key_file);
    return $key_found;
}

sub add_key {

    (my $key_file = &lock($keyfile, "append")) or (die "Couldn't add_key: $!");
    print $key_file "$session_key:$time\n";
    unlock($key_file);
}

sub remove_key {

    my($key_file, $new_info, $akey, $atime);
    ($key_file = &lock($keyfile, "read")) or (die "Couldn't remove_key:$!");
    while (<$key_file>) {
	($akey, $atime) = split /:/, $_;
        ($new_info .= $_ . "\n") if ($akey ne $session_key);
    }
    unlock($key_file);
    ($key_file = &lock($keyfile, "overwrite")) or (die "Couldn't remove_key: $!");
    print $key_file $new_info;
    unlock($key_file);
}

sub remove_old_keys {

    my($key_file, $new_info, $akey, $atime);
    $new_info = ' ';
    ($key_file = &lock("adminfile", "read")) or (die "Couldn't remove_old_keys: $!");
    while (<$key_file>) {
	($akey, $atime) = split /:/, $_;
        ($new_info .= $_ . "\n") if ($time > ($atime + (60 * 60 *24)));
    }
    unlock($key_file);
}

1;
