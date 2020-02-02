#!/usr/bin/perl
# part of Quixote's Exchange
# Copyright 1999  Brian Deitte

##### start-up #####
use 5.004;
use CGI qw(:standard :html);
require("conf.pl");
my $base_url = $BASE_URL;
my $cgi_url = $CGI_URL;
require("SbeDisplay.pl");
require("SbeFiles.pl");
require("SbeSafety.pl");
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

my $button_label = 'create account';
#####

##### main program #####
# first password_form(),
# then new_user()
# Notice that print_bottom is not called from here.  This is because
# the links are shown after the login.

print_top();

if (param('action') eq $button_label) {
    # don't start_session until know if password is correct
    check_fields() and new_user();
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

##### create the user #####
sub new_user {

    db_connect(); # connect to database

    # check to make sure the email address is not already in use
    my ($status, @junk);
    ($status, @junk) = get_book_ids(param('email'), param('password'));

    ($status eq 'bad_password') and (bail("Your email address already has an account here."), return undef);
    ($status ne 'new_user') and (bail("Not a new user.  Just login!"), return undef);

    # everything is ok, so we can create a session key now
    start_session();
    # and save everything to the key file
    param(-name=>'booklist', -value=>\@junk);
    clear_state();

    # add user to database
    add_user(param('email'), param('password'));
    
    print p, 'Thanks for trying the book exchange!', p,
          'An account has been created for you.', p,
          'Email address: ', param('email'), p,
          'Password: ', param('password'), p;
		  
    my $skey = get_session_key();

	print qq!<A HREF="controlbar.cgi/$skey" target="controlbar">
	         Click here</A> to show your options on the left.!;

    print_bottom(1);

    db_disconnect();
}
#####

##### password form for the new user to fill out #####
sub password_form {

    print start_form,
          'Email<br>',
          textfield(-name=>'email', -size=>20, -maxlength=>50),
          p,
          'Password<br>',
          password_field(-name=>'password', -size=>20, -maxlength=>50),
          p,
          submit(-name=>'action', -value=>$button_label),
          end_form,
          'First time visiting?  You may want to check out the ',
          '<a href="$base_url/answers.html">answers</a> or ',
          '<a href="$cgi_url/search.cgi">search</a> pages first. ',
          '<italic>Becoming a user is needed only when you want to add books ',
          'to the book exchange. You can search for books ',
          'without becoming a user.', p,
          'All you have to do here is ',
          ' enter your email address and a password. An account will ',
          'then be created for you so you can have your books on the ',
          'book exchange.', p,
          'Your email address will be shown to people ',
          'who wish to buy your posted books, but in no ',
          'other case will your email be given to others.';

     print_bottom(1);
}
#####
