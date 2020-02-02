#!/usr/bin/perl

##### start-up #####
use 5.004;
use CGI qw(:standard :html);
require("conf.pl");
require("SbeDisplay.pl");
require("SbeSafety.pl");
require("SbeKey.pl");
require("SbeFiles.pl");
use CGI::Carp qw(fatalsToBrowser set_message);
BEGIN {
   sub handle_errors {
      my $msg = shift;
      print 'Unrecoverable error: ', $msg, '<p>',
            'If you do not understand what is wrong, please see the ',
            '<A HREF=/faq.html>FAQ</A>';
  }
  set_message(\&handle_errors);
}

my $sendmail = $SENDMAIL;

use strict;

my $button_label = 'send the message';
#####

##### main program #####
# calls print_mail(),
# then send_mail()
print_top();  # from SbeDisplay.pl

if (param('action') eq $button_label) { 
    check_fields(['title', 'price', 'email', 'sender_email', 'sender_name']) 
    and send_mail(); 
}
else {
    check_fields(['title']) and print_mail();
}

print_bottom(1);
#####

sub bail {
    bail_message(@_);
    print_mail();
}    

sub check_fields {

    my($required, $error_text);
    $required = shift;
    $error_text = standard_check($required);
    ($error_text) and (bail($error_text), return undef);
    
    if (defined param('sender_email')) {
        (check_email(param('sender_email'))) and 
            (bail(&bad_email(param('sender_email'))), return undef);
    }
    return 1;
}

# use some hidden passing for returning to search.cgi
sub print_hidden_info {

    my $sb = param('search_by');
    my $sbv = param('search_by_value');
    my $dept = param('dept');
    my $date = param('date');
    print hidden(-name=>'search_by', -value=>$sb),
          hidden(-name=>'search_by_value', -value=>$sbv),
          hidden(-name=>'dept', -value=>$dept),
          hidden(-name=>'date', -value=>$date);
}

sub send_mail {

    # Make variables for the parameters that may not be filled.
    my($sprice, $sother, $tprice, $sname);
    $sprice = param('sender_price');
    $sother = param('sender_other');
    $tprice = param('price');
    $sname = param('sender_name');

    ($sprice eq "") and
      ($sprice = 'an unspecified price');  # that kind of rhymes
    ($tprice eq 'Not given.') and ($tprice = 'an unspecified price');
    ($sother ne "") and 
        $sother = 'The person also had this to say: ' . $/ . $sother . $/;
    ($sname eq '') and ($sname = 'Somebody');

    my $web_address = 'bookexchange.cs.uiowa.edu';

    # Send the email
    open (MAIL, "|$SENDMAIL -t -n -oi") or die "Couldn't send mail.";
    print MAIL 'From:', param('sender_email'), $/,
               'To:', param('email'), $/,
               'Subject: ', $sname, ' wishes to buy ', param('title'), $/, $/,
               'Hello there!  This is a message for you ', $/,
               'sent from the book exchange, at ', $web_address, $/, $/,
               $sname, ' wants to buy your book entitled', $/,
               param('title'), $/,
               "for $sprice. (You asked for $tprice.)", $/,
               $sother, $/;
    print MAIL
               'Please remember, the book exchange does not take', $/,
               'part in the actual transaction of selling books.  We just', $/,
               'provide an easy way to get in touch with people who have', $/,
               'something you may need.  So if you want to sell this book', $/,
               'to this person, reply to this message or compose a message to', $/,
               param('sender_email'), $/, $/,
               'Thanks, and good luck book hunting!', $/,
               '-the book exchange';

    close(MAIL);
    print 'The email has been sent!<p>',
          'Thank you for using the book exchange.<p>';

   # log_note('mail', "mail sent by $ENV{REMOTE_ADDR}");

    # From the saved information of where the user came from,
    # allow them to go back to that place in search
    print start_form(-action=>'search.cgi');
    print_hidden_info();
    print submit(-name=>'action', -value=>'return to search'),
          end_form, p,
          start_form(-action=>'search.cgi'),
          submit(-name=>'action', -value=>'new search');
    
}

sub print_mail {

    # Print the form for email information, but
    # fill in fields that would look empty otherwise.
    (param('other') ne '') or param(-'name'=>'other', -'value'=>"None");
    my($temp);
    if (param('price') ne '') {
        $temp = '$' . param('price'); }
    else {
        $temp = 'Not given.'; }
    param(-name=>'price', -value=>$temp);

    #print the form
    print start_form;
    my @form_data = ('title', 'Book Name', 'other', 'Other Info', 
                     'price', 'Asking Price', 'email', 'Email');
    my($field_name, $name);
    while($field_name = shift @form_data) {
        $name = shift @form_data;
        print $name, ': ', param($field_name), '<br>',
              hidden(-name=>$field_name, -value=>param($field_name));
    }
    print_hidden_info();
    print p, 'Your Name: ', 
          textfield(-name=>'sender_name', -size=>'20', -maxlength=>'40'), p,
          'Your Email: ',
          textfield(-name=>'sender_email', -size=>'20', -maxlength=>'40'), p,
          'Your Asking Price: $',
          textfield(-'name'=>'sender_price', -size=>'8', -maxlength=>'8'), p,
          'Other: ',
          textarea(-'wrap'=>'physical', -'name'=>'sender_other',
                   -rows=>'5', -columns=>'30'),
          p,
          submit(-name=>'action', -value=>$button_label),
          end_form(), p;

    print start_form(-action=>'search.cgi');
    print_hidden_info();
    print submit(-name=>'action', -value=>'return to search'),
          end_form, p,
}
