#!/usr/bin/perl
# part of Quixote's Exchange
# Copyright 1999  Brian Deitte

require("SbeData.pl");
require("SbeKey.pl");

my $base_url = $BASE_URL;
my $email = $ADMIN_EMAIL;

use strict;

sub print_top {

    my $display = shift;

    my ($bg_color, $text_color, $link_color, $vlink_color,
        $keywords, $authors);
    $bg_color ='#003300'; $text_color='#ffffff';
    $link_color='#0080ff'; $vlink_color='#ff0000';
    $keywords = "book, books, buyback, exchange, buy, sell, used";
    $authors = "Brian Deitte, Dave Selden";

    print header(-expires=>'1m'),
          start_html(-'title'=>"$display",
                     -'bgcolor'=>$bg_color, -'text'=>$text_color,
                     -'link'=>$link_color, -'vlink'=>$vlink_color,
                     -'meta'=>{'keywords'=>$keywords,
                               'author'=>$authors});

    print '<font face="Helvetica, Arial"><br>';
}

sub print_bottom {

    print end_html();
}

sub get_the_date {
    my @date = localtime(time);
    return join('/', ($date[4] + 1,$date[3],$date[5] + 1900));
}

# Gets the book from CGI that was just posted, and makes this the one
# book for print_books to print out.
sub print_new_book {
    
    my($fh, $print_type);
    $fh = shift;
    $print_type = shift;

    my @book_fields = get_book_fields();

    my($field, @book, $book_field);
    foreach $field (@book_fields) {

        ($book_field = param($field)) or ($book_field = "");
        push @book, $book_field;
    }
    print_book(\@book, $fh, $print_type);
}

sub print_book {

    my ($book, $fh, $print_type, $newline);
    $book = shift;
    $fh = shift;
    $print_type = shift;
    
    if (lc($print_type) eq "html") {
        $newline = '<br>'; }
    else {
        $newline = $/;
    }

    # This is ugly, unportable, and all the rest.  
    # @display corresponds to the fields in get_book_fields.
    my @display = ('',  'by ',  'Area: ',  'For: ', 'ISBN: ', 
                   'Condition: ',  'Other: ', 'Asking price: $',  
                   'Date posted on: ', 'item_id');

    shift @$book; 
    my($field, $field_info);
    foreach $field (@$book) {

        $field_info = shift @display;
        ((length($field) > 0) and ($field_info ne "item_id")) and
            (print $fh $field_info . $field . $newline);
    }
}

sub default_email {
    return "<a href=mailto:$email>$email</a>.";
}

sub print_password_info {
    print <<"ENDPI";
   
    Note that your password is case sensitive: "ack" is not
    the same as "AcK".
ENDPI
}

sub incorrect_password {
    return "Your password is incorrect.<p>
    The most common mistake is a misspelling.  Please go
    back and try again, even if you don't think you made a mistake.
    Perhaps the dues ex machina will grant you a favor.  
    <p>If you have forgotten your password or believe you have not 
    made an error, please send email to ", default_email();
}

sub bail_message {

    print 'Oops! ', @_, p,
          "If you do not understand what is wrong, please see the ",
          "<A HREF=$base_url/answers.html>answers</A>.";
}

1; #return true
