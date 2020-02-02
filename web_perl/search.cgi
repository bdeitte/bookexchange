#!/usr/bin/perl
# Copyright 1999  Brian Deitte

##### start-up #####
use 5.004;
use CGI qw(:standard :html);
require("conf.pl");
my $base_url = $BASE_URL;
my $cgi_url = $CGI_URL;
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
            '<A HREF=$base_url/answers.html>answers</A>.';
  }
  set_message(\&handle_errors);

}
my $base_dir = $BASE_DIR;
use strict;

my $button_label1 = 'search by word or phrase';
my $button_label2 = 'show books in this area';
my $button_label3 = 'show all books';

my @search_by = ('title', 'author', 'class', 'isbn');
#####

##### the main program #####
print_top();

if ((param('action') eq $button_label1) or 
    (param('action') eq $button_label2) or
    (param('action') eq $button_label3) or
    (param('action') eq 'return to search')) { 
    search();
}
else {
    search_form();
}

print_bottom(1);
#####

sub bail {
    bail_message(@_);
    search_form();
}    

sub check_fields {
    my @required = ();
    my $error_text = standard_check(\@required);
    ($error_text) and (bail($error_text), return undef);
    return 1;
}

##### search for values and print out matched books #####
sub search {
	
    db_connect();

    # (Checking for '------' area names, which are invalid.)
    (param('dept') =~ /^\s*\-/) and
        (bail("You can't select the areas that begin with" .
              "'-----'. " .
              "Please select one of the areas below the name."),
         return undef);

    # Checks to see what the user wishes to search for 
    # (from the information in cgi) and
    # completed after the first submission

    # find matches where ('$search_by =~ /$search_by_value/)
    my($search, @searches);
    #get rid of leading or trailing spaces
    (my $search_value = param('search_by_value')) =~ s/^\s+$//g;
    foreach $search (@search_by) {
        if ((param('search_by') eq $search) and ($search_value ne '')) {
            push(@searches, ('(' . lc($search) . ' LIKE "' . 
                '%' . lc(escape_string($search_value)) . '%")'));
            last;
        }
    }        
    # find matches where 'dept =~ /dept_value/'
    # It would be silly to search through the huge area array
    # simply to see if the user provided a 'correct' area name.
    # If they want to screw with this it doesn't matter, since bad_char
    # would catch any naughty characters.
    (my $d_value = param('dept')) =~ s/^\s+//; # get rid of leading spaces
    if ($d_value ne 'Nothing Selected' and $d_value ne '') {
        push(@searches, 
          ( '(dept="' . escape_string($d_value) . '")' ) );
    }
    # Axed out for now, to be implemented later.
    # find matches where 'date eq date_value'
    #if (defined param('date')) {
    #    push(@searches, "(date eq '" . escape_string(param('date')) . "')");
    #}

    #get everything if button is third one
    if (param('action') eq $button_label3) {
        @searches = ();
        push(@searches, '(title LIKE "%%")');
    }

    (! @searches) and (bail("Nothing asked for."), return undef);

    my $search_data = search_items(\@searches);

    my $matches = scalar(@$search_data);
    if (!$matches) {
        print "Sorry, there were no matches.";
        search_form();
        return undef;
    }

    # let's impress those English majors
    if ($matches==1) {   
        print "<H2>There is $matches match: </H2><br>";
    } else {
        print "<H2>There are $matches matches: </H2><br>";
    }

    my($book);
    foreach $book (@$search_data) {

        # the form for sending email from potential buyer to seller
        # the users.db fields: item_id,email,title,author,dept,class,isbn,condition,other,price,date
        # This hidden form part must go before the printing of the book
        # to the screen.  I would explain why, but it'd be really
        # embarrasing.
        print start_form(-action=>'mail.cgi'),
              hidden(-name=>'email', -value=>"@$book[0]"),
              hidden(-name=>'title', -value=>"@$book[1]"),
              hidden(-name=>'other', -value=>"@$book[7]"),
              hidden(-name=>'price', -value=>"@$book[8]"),
              hidden(-name=>'search_by', -value=>param('search_by')),
              hidden(-name=>'search_by_value', -value=>param('search_by_value')),
              hidden(-name=>'dept', -value=>param('dept')),
              hidden(-name=>'date', -value=>param('date'));

        print_book($book, \*STDOUT, 'html');

        print p, submit(-name=>'email_seller',
                     -value=>'Send this person a message'),
              end_form,
             '<br><hr><br>';
    }
    print p,  start_form(-action=>'search.cgi'),
              submit(-name=>'action', -value=>'new search');

    clear_state();
	
	db_disconnect();
}
#####

##### form for user to search for books #####
sub search_form {

    my $dept = get_areas();
    print start_form,
               '<strong>Three ways to search:</strong>',
               p, '<hr>',

               '<strong>look for a word or phrase in one of the ',
               'book fields:</strong>', p,
               'look for the phrase below by ',
               popup_menu(-'name'=>'search_by',
                          -'values'=>\@search_by), ':<br>',
               textfield(-name=>'search_by_value',
                         -size=>40,
                         -maxlength=>50), p, 
               submit(-name=>'action', -value=>$button_label1), 
               p, '<hr>',

               '<strong>look at all the books in ',
               'a single area:</strong>',
                p,
                popup_menu(-'name'=>'dept',
                           -'values'=>[(split /\n/,$$dept)]), p,
                submit(-name=>'action', -value=>$button_label2), 
                p, '<hr>',

                '<strong>look at all the books on ',
                'the book exchange:</strong>', p,
                submit(-name=>'action', -value=>$button_label3),
                p, '<hr>',

          end_form,
          "<p><a href='$base_url/search_tips.html'>searching tips</a>";

}
######

# This is being axed out for awhile.
# To be implemented someday...
#               '<th align=left>Oldest date to include (blank for all entries):</th>',
#                  textfield(-name=>'date',
#                            -size=>10,
#                            -maxlength=>10),


