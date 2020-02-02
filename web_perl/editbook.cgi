#!/usr/bin/perl

##### start-up  #####
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
      print 'Unrecoverable error: ', $msg, '<p>',
            'If you do not understand what is wrong, please see the ',
            '<A HREF=/answers.html>answers</A>.';
  }
  set_message(\&handle_errors);
}
use strict;
#####

##### the main program #####

print_top();

my $action = param('action');

if ($action eq 'edit') {
    check_fields() and get_state() and alter_book(); }
elsif ($action eq 'save changes') {
    check_fields() and get_state() and save_book(); }
else {
    get_state();
    clear_state();
    list_books();
}

print_bottom();
#####

sub bail {
    bail_message(@_); 
}

sub check_fields {
    my @required = ();
    my $error_text = standard_check(\@required);
    ($error_text) and (bail($error_text), return undef);
    return 1;
}

##### save the changes made to the book #####
sub save_book {
	
    db_connect();

    # (Checking for '------' department names, which are invalid.)
    (param('dept') =~ /^\s*\-/) and
        (bail("You can't select the departments that begin with" .
              "'-----' such as '------Liberal Arts------'. " .
              "Please select one of the departments below the name."),
         return undef);

    # Get the id of the book that the user wants to alter
    (my $alter_book = param('bookn')) or 
       (bail("You haven't identified a book to alter!."), 
              return undef);

    my @booklist = param('booklist');
    
    # make sure user owns the book they wish to alter
    my($own_book, $var);
    $own_book = 0;
    foreach $var (@booklist){
        ($alter_book eq $var) and ($own_book = 1, last);
    }
    (!$own_book) and (bail("You don't own the book you wish to alter."), return undef);

    # the actual altering of the book
    my @book_fields = get_book_fields();
    alter_item($alter_book, \@book_fields);
    
    clear_state();
    
    print '<p>Changes saved!  The changes may not appear immediately.',
          ' Rest assured, though, the changes have been made.<p>';
	
    db_disconnect();

    list_books();
}
######

##### Let the user alter the book they chose
sub alter_book {

    db_connect();
	
    # Get the id of the book that the user wants to alter
    (my $alter_book = param('bookn')) or 
       (bail("You haven't identified a book to alter!."), 
              return undef);

    my @booklist = param('booklist');

    my($own_book, $book);
    $own_book = 0;
    foreach $book (@booklist){
        $own_book = 1 if ($alter_book eq $book);
    }
    (!$own_book) and (bail("You don't own the book you wish to alter."), return undef);

    # Get the book's information
    my $book_array = get_items([$alter_book]);
    (! scalar(@$book_array)) and (bail("Couldn't find book id."), return undef);
    my $book = shift @$book_array;

    # Print the information to a form like in post.cgi to allow the
    # user to alter the information
    my (@book_fields, $field, $value);
    @book_fields = get_book_fields();
    foreach $field (@book_fields) {
        $value = shift @$book;
        param(-'name'=>$field, -'value'=>$value);
    }

    # This whole form should be the same as the long form in addbook.cgi,
	# except for the added hidden value that transfers the book id
    my $dept = get_departments();
    print start_form,
          'Title (required) ', '<br>',
          textfield(-name=>'title', -size=>50, -maxlength=>70), '<br>',
          'Author ', '<br>',
          textfield(-name=>'author', -size=>50, -maxlength=>70), '<br>',
          'Department ', '<br>',
          popup_menu(-name=>'dept', -values=>[(split /\n/, $$dept)]),
'<br>',
          'Class ', '<br>',
          textfield(-name=>'class', -size=>50, -maxlength=>70), '<br>',
          'Condition ', '<br>',
          popup_menu(-name=>'condition', 
                    -values=>["Nothing selected", "Like new", "Excellent", 
                    "Ok"]), '<br>',
          'ISBN ', '<br>',
          textfield(-name=>'isbn', -size=>10, -maxlength=>10), '<br>',
          'Price', '<br> $',
          textfield(-name=>'price', -size=>10, -maxlength=>10), '<br>',
          'Other Information ', '<br>',
          textfield(-name=>'other', -size=>50, -maxlength=>80), p,
          hidden(-name=>'bookn', -value=>param('bookn')),
          submit(-name=>'action', -value=>"save changes"),
          '<p>The title field must be completed to<br>',
          'post a book.  The remaining fields <br>',
          'do not need to be filled in, although<br>',
          'they may help those searching for your book.',
          end_form;
		  
    db_disconnect();
}
#####

##### list the books under the user's account for picking to alter #####
sub list_books {

    db_connect();
	
    my @booklist = param('booklist');

    my $books = get_items(\@booklist);

    (!$books) and (bail("Please Add a book before editing."), return undef);

    # List the books under the user's account
    # print '<center><table border=0 width=100>';

    my($book);
    print '<table border=0 width=300>';
    foreach $book (@$books) {

        print start_form,
              '<tr>',
                  '<td align=left>',
                      submit(-name=>'action',
                             -value=>'edit'), '&nbsp&nbsp&nbsp&nbsp',
                      hidden(-name=>'bookn',
                             -value=>@$book[10]),
                  '</td>',
                  '<td align=left>';
                      print_book($book, \*STDOUT, 'html');
        print         '<br>',
                  '</td>',
              '</tr>',
              end_form;
    }
    print '</table>';
	
	db_disconnect();
}
#####
