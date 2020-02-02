# Copyright 1999  Brian Deitte

#!/usr/bin/perl

##### set-up #####
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
      print 'Unrecoverable error: ', $msg, '<p>',
            'If you do not understand what is wrong, please see the ',
            '<A HREF=$base_url/answers.html>answers</A>.';
  }
  set_message(\&handle_errors);
}
use strict;

my $button_label = 'remove selected books';
#####

##### main program #####
print_top();

if (param('action') eq $button_label) {
    check_fields() and update_session() and remove_selected_books(); 
}
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
    my $error_text = standard_check();
    ($error_text) and (bail($error_text), return undef);
    return 1;
}

##### remove selected books from user's account #####
sub remove_selected_books {
	
    db_connect();

    # Find the books to remove
    my @param_names = param;
    my($key, @removebooks);
    foreach $key (@param_names) {
        if ($key =~ /^\d+$/) {
            push(@removebooks,$key);
        }
    }
    (scalar(@removebooks)) or 
        (bail("You didn't select any books to remove.<p>"), return undef);

    my @booklist = param('booklist');
    
    my($not_owner, $book, $owner, $check_book);
    $not_owner = 0;
    foreach $book (@removebooks) {
        $owner = 0;
        foreach $check_book (\@booklist) {
            ($book == $check_book) and ($owner = 1, last);
        }
        $owner and ($not_owner = 1, last);
    }
    # checked to see if anybody's trying to be naughty and remove other
    # people's books by posting their own form information.
    if ($not_owner) {
        log_note('naughty', ($ENV{REMOTE_ADDR} . ", aka " . param('email') .
                 "tried to remove books @removebooks"));
        bail("You don't own one of the books you want to remove.");
        return undef;
    }

    # Make an array of the books left after the removebooks have
    # been removed from the books the user owns.
    my($book, $not_found, $match_book, @booksleft);
    foreach $book (@booklist) {
        $not_found = 1;
        foreach $match_book (@removebooks) {
            $not_found = 0 if ($book == $match_book);
        }
        push(@booksleft, $book) if ($not_found);
    }


    # remove the selected books by rewriting the book ids minus the removebooks
    alter_book_ids(\@booksleft);    
    # remove the books from the books database.
    remove_items(\@removebooks);
    # and from the session file
    param(-name=>'booklist', -value=>\@booksleft);
    clear_state();
        
    # Note the removal in the remove log.
    log_note('remove', join(':', @removebooks) . " removed by " .
             param('email') . " at " . $ENV{REMOTE_ADDR});
    
    my $nob = scalar(@removebooks);
    if ($nob == 1) {
        print "The book has been removed. The book ";
    } else {
        print "$nob books have been removed. The books ";
    }
    print 'may not immediately appear to have been removed.',
          ' The changes, though, have been made.<p>';
    print "Thank you for using the book exchange!<br>";

    db_disconnect();
}
#####

##### list books user can select to remove #####
sub list_books {
	
    db_connect();

    my @booklist = param('booklist');

    my $books = get_items(\@booklist);
    
    (!$books) and (bail("You need to add a book before removing a book!"),
return undef);

    # Print out the books the user can remove.
    print 'Click on the checkbox to the left of any ',
          'books you wish to delete, then click on the button at ',
          'the bottom to remove the books.<br>',
          start_form,
          '<table border=0 width=300>';

    # Prints each book in a table with a checkbox to its left.
    my($book);
    foreach $book (@$books) {
        print '<tr>',
                  '<td align=left>',
                      checkbox(-name=>@$book[10], -label=>''),
                  '</td>',
                  '<td align=left>';
                      print_book($book, \*STDOUT, 'html'); 
        print     '</td>',
              '</tr>';
    }
    print '</table><p>',
          submit(-name=>'action', -value=>$button_label),
         '</center>',
          end_form;
		  
    db_disconnect();
} 
