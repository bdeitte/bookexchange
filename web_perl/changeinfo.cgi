#!/usr/bin/perl

##### start up #####
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

my $button_label = 'change user info';
#####

##### the main program #####
# user_info_form() is called first,
# then change_user_info()

print_top();  # from sbe-display.pl

if (param('action') eq $button_label) {
    check_fields() and update_session() and change_user_info();
}
else {
    get_state();
    clear_state();
    user_info_form();
}

print_bottom();
#####

sub bail {    
    bail_message(@_);
    user_info_form();
}    

sub check_fields {
    my @required = ('new_email', 'new_password');
    my $error_text = standard_check(\@required);
    ($error_text) and (bail($error_text), return undef);
    return 1;
}

##### changes info about user #####
sub change_user_info {
	
    db_connect();

    my $echange = 0; 
    my $pchange = 0;
    #check if a new email value is given
    if (param('new_email') ne param('email')) {
        (check_email(param('new_email'))) and 
            (bail(&bad_email(param('new_email'))), return undef);
        $echange = 1;
    }
    #check if a new password value given
    if (param('new_password') ne param('password')) {
        $pchange = 1;
    }
    # just for clarity
    my $new_email = param('new_email');
    my $new_password = param('new_password');

    # send user back if nothing was changed
    if (!$echange and !$pchange) {

        print "No changes made.<p>";
        user_info_form();
        return undef;
    }
      
    # Need to make sure the new email isn't already being used
    if ($echange) {
        my ($status, @junk);
        ($status, @junk) = get_book_ids(param('new_email'), "junk");
        ($status eq 'new_user') or (bail("Redundant email choice. (Choice" .
            " of email was redundant.)<br> The new email address you have " .
            " chosen is already in use."), return undef);
    }

    # This is where the change is actually made.
    alter_user(param('email'), $new_email, $new_password);
    # Update the book database if the email was changed
    $echange and 
      alter_item_field('email', param('email'), $new_email);
    # and update session file
    ($echange) and 
          param(-name=>'email', -value=>$new_email);
    ($pchange) and 
          param(-name=>'password', -value=>$new_password);
    clear_state(); 

    # Print results of the validation to HTML    
    $echange and 
        (print 'Your email has been changed<br>' ,
        'Your new email address is: ' , param('email'),  p);
    $pchange and 
        (print 'Your password has been changed.<br>' , 
        'Your new password is: ' , param('password'),  p);

	db_disconnect();
}
#####

##### form to change user info #####
sub user_info_form {

    my $email = param('email');
    my $password = param('password');

    print start_form,
          '<table border=0 width=30>',
          '<tr>',
              '<th align=left>Email</th>',
          '</tr>',
          '<tr>',
              '<td>',
                  textfield(-name=>'new_email',
                            -value=>$email,                          
                            -size=>20,
                            -maxlength=>50),
              '</td>',
          '</tr>',
          '<tr>',
              '<th align=left>Password</th>',
          '</tr>',
          '<tr>',
              '<td>',
                  password_field(-name=>'new_password',
                                 -value=>$password,
                                 -size=>20,
                                 -maxlength=>50),
              '</td>',
          '</tr>',
          '</table>',
          p,
          submit(-name=>'action',
                 -value=>$button_label),
          end_form;
}
#####
