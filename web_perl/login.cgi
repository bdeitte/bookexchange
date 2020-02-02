#!/usr/bin/perl

##### start-up #####
use 5.004;
use CGI qw(:standard :html);
require("conf.pl");
require("SbeDisplay.pl");
require("SbeFiles.pl");
require("SbeSafety.pl");
require("SbeKey.pl");
use CGI::Carp qw(fatalsToBrowser set_message);
BEGIN {
   sub handle_errors {
      my $msg = shift;
      print 'Unrecoverable error: ', $msg, '<p>',
            'If you do not understand what is wrong, please see the ',
            '<A HREF=/answers.html>answers</A>.';
  }
  set_message(\&handle_errors);
}
use strict;

my $button_label = 'login';
#####

##### main program #####
# calls password_form(),
# then login()
# Notice print_bottom is not called here, but rather in the subroutines,
# since once logged in, links must be placed.

print_top("no image");

if (param('action') eq $button_label) {
    # don't start_session until know if password is correct
    check_fields() and login();
}
else {
    password_form();
}
#####

sub bail {
    bail_message(@_);
    password_form();
}

sub check_fields {
    my @required = ('email', 'password');
    my $error_text = standard_check(\@required);
    ($error_text) and (bail($error_text), return undef);
    check_email(param('email')) and (bail(&bad_email(param('email'))), 
                                     return undef);
    return 1;
}

##### make sure user ok, then login #####
sub login {
    
    db_connect();

    # get_book_ids also checks on the user info
    my ($status, @booklist);
    ($status, @booklist) = 
      get_book_ids(param('email'), param('password'));
    if ($status eq 'bad_password') {
        my $email = param('email');
        bail(&incorrect_password());
        return undef;
    }
    ($status eq 'new_user') and 
      (bail("You don't have an account here! Please go to " .
       "<A HREF=newuser.cgi>the new user page.</A>"), return undef);

    # everything is ok, so we can create a session key now
    start_session();
    # and save everything to the key file
    param(-name=>'booklist', -value=>\@booklist);
    clear_state();

    # and display the new frameset
    my $skey = get_session_key();

    print "Login complete!<p>";
    print qq!Click <A HREF="controlbar.cgi/$skey" TARGET="controlbar">here</A>!;
    print " to show your options on the left.";

    print_bottom(1);

    db_disconnect();
}
#####

##### form for user to login ####
sub password_form {

    print start_form,
          'Email<br>',
          textfield(-name=>'email', -size=>20, -maxlength=>50),
          p,
          'Password<br>',
          password_field(-name=>'password', -size=>20, -maxlength=>50),
          p,
          submit(-name=>'action', -value=>$button_label, -target=>'_top'),
          end_form, 
          'Welcome back!', p,
          "If you haven't become a user yet, ",
          'you need to do that at the ',
          '<a href="newuser.cgi">new user page</a>.', p;
     print_password_info();
     print '<p></center>';

     print_bottom(1);
}
#####
