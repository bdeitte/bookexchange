#!/usr/bin/perl
# Copyright 1999  Brian Deitte

##### start-up #####
use 5.004;
use CGI qw(:standard :html);
require("conf.pl");
require("SbeDisplay.pl");
require("SbeData.pl");
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

my $button_label = 'add book';
my $web_address = 'bookexchange.cs.uiowa.edu/';
#####

#### the main program #####
# first calls post_form,
# then add_book
print_top();

if (param('action') eq $button_label) {
    check_fields() and update_session() and add_book();
}
else {
    get_state();
    clear_state();
    post_form();
}

print_bottom();
#####

sub bail {
    bail_message(@_);
    post_form();
}

sub check_fields {
    my @required = ('title');
    my $error_text = standard_check(\@required);
    ($error_text) and (bail($error_text), return undef);
    return 1;
}

##### add the book to both the user and book databases #####
sub add_book {
	
    db_connect();

    # (Checking for '------' department names, which are invalid.)
    (param('dept') =~ /^\s*\-/) and
        (bail("You can't select the departments that begin with" .
              "'-----' such as '------Liberal Arts------'. " .
              "Please select one of the departments below the name."),
         return undef);

    my @book_fields = get_book_fields();    
    # Add the book to the database
    my $book_id = add_item(\@book_fields);

    # Add the book id to the booklist    
    my @booklist = param('booklist');
    push(@booklist, $book_id);
    # Add book id to database
    alter_book_ids(\@booklist);
    # and to the session file
    param(-name=>'booklist', -value=>\@booklist);

    # Tell the user that posting is done, including
    # what books are listed under her account.
    print 'Posting complete!', p;
    print "Here's the information recorded:", p;
    print_new_book(\*STDOUT, 'html');

    print '<p> The added book may not appear immediately.',
          ' Rest assured, though, the changes have been made.<p>';

    # log info into post log 
    #&log_note('addbook', ("$book_id posted by " . param('email') . " at $ENV{REMOTE_ADDR}"));

    # The data of the book just posted is sent to the 
    # user's email address
    #open(MAIL, "<maill");

#  open (MAIL, "|/usr/lib/sendmail -t -n -oi") or die "Couldn't use mail.";
#   print MAIL 
#              'To: ', param('email'), $/,
#              'Subject: Info from the book exchange', $/,
#              'Reply-to: bdeitte@cs.uiowa.edu', $/, $/,
#              'Here is a copy of the book posting you posted to the', $/,
#              "book exchange($web_address):", $/, $/;
#   print_new_book(\*MAIL, 'text');
#   print MAIL $/,
#              'If you have questions or comments, please respond to', $/,
#              'this message or see our answers page', $/,
#              'at ', $web_address, 'answers.html.', $/, $/,
#              'Thanks for using the book exchange!', $/;
#   close(MAIL);

    # clear book information from the CGI object
    clear_state();

    db_disconnect();

    print "If you'd like to add another book, here's the form again: <p>";
    post_form();
}
#####

##### form for user to add a book #####
sub post_form() {
    # This whole form should be the same as the alter book form in editbook.cgi. 
    my $dept = get_areas();
    print  start_form,
          'Title (required) ', '<br>',
          textfield(-name=>'title', -size=>50, -maxlength=>70), '<br>',
          'Author ', '<br>',
          textfield(-name=>'author', -size=>50, -maxlength=>70), '<br>',
          'Area ', '<br>',
          popup_menu(-name=>'dept', -values=>[(split /\n/,$$dept)]),
          '<br>',
          'Class ', '<br>',
          textfield(-name=>'class', -size=>50, -maxlength=>70), '<br>',
          'Condition ', '<br>',
          popup_menu(-name=>'condition', 
                    -values=>["Nothing selected", "Like new", "Excellent", 
                    "Ok"]), '<br>',
          'ISBN ', '<br>',
          textfield(-name=>'isbn', -size=>10, -maxlength=>10), '<br>',
          'Price ', '<br>$',
          textfield(-name=>'price', -size=>10, -maxlength=>10), '<br>',
          'Other Information ', '<br>',
          textfield(-name=>'other', -size=>50, -maxlength=>80), p,
          submit(-name=>'action', -value=>$button_label),
          '<p>The title field must be completed to',
          'post a book.  The remaining fields ',
          'do not need to be filled in, although ',
          'they will help those searching for your book.<p>',
          "After pressing $button_label it may take a few seconds ",
          'for the screen to change.  Pressing it twice will only ',
          'make you post a duplicate of the book you are adding!';
          end_form;
} 
#####
