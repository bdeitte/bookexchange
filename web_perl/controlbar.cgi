#!/usr/bin/perl

##### start-up #####
use 5.004;
use CGI qw(:standard);
require("conf.pl");
require("SbeKey.pl");
use CGI::Carp qw(fatalsToBrowser set_message);
BEGIN {
   sub handle_errors {
      my $msg = shift;
      print 'Unrecoverable error: ', $msg, '<p>';
  }
  set_message(\&handle_errors);
}
use strict;
#####

print header();

##### main program: uses controlbar.html as a template using session_key ####
my $s_key = get_session_key();

my $temp;
(my $template = &lock("controlbar.html", "read")) or (die "Couldn't read controlbar.html: $!");
while (<$template>) {
    # there is probably A Better Way To Do This
    ($temp = $_) =~ s/S_KEY/$s_key/;	
    print $temp;
}
unlock($template);
#####
