#!/usr/bin/perl

##### start-up #####
use 5.004;
use CGI qw(:standard :html);
require("conf.pl");
require("SbeDisplay.pl");
require("SbeKey.pl");
use CGI::Carp qw(fatalsToBrowser set_message);
BEGIN {
   sub handle_errors {
      my $msg = shift;
      print 'Unrecoverable error: ', $msg, '<p>',
            'If you do not understand what is wrong, please see the ',
            '<A HREF=/answers>answers</A>.';
  }
  set_message(\&handle_errors);
}
my $base_url = $BASE_URL;
use strict;

##### main program #####
get_state();      # get CGI object
remove_session(); # remove CGI object

# take user back to the beginning
print redirect(-uri=>'$base_url/newss.html',
               -target=>'_top');
#####
