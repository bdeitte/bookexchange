#!/usr/bin/perl
# part of Quixote's Exchange
# Copyright 1999  Brian Deitte

require("SbeLock.pl");

my $driver = $DB_DRIVER;
my $database = $DB_NAME;
my $user = $DB_USER;
my $password = $DB_PASSWORD;

use DBI;
use strict;

my ($dbh, $drh);

sub db_connect {

    ($dbh = DBI->connect("DBI:$driver:database=$database;", $user, $password))
       or die "Couldn't db_connect: $DBI::errstr";

    $drh = DBI->install_driver($driver)
      or die "Couldn't db_connect: $DBI::errstr";
}

sub db_disconnect {
    
    my $rc = $dbh->disconnect;
    ($rc) or die "Couldn't db_disconnect: $rc->errstr";
}

#####

sub add_item {

    my($item_fields);
    $item_fields = shift;

    my($field, $item_value, @item_values, @item_keys); 
    foreach $field (@$item_fields) {
        $item_value = param($field);
        ($field eq 'item_id') and ($item_value = '');
        # can't put date here, since the function now(), which
        # is used to create the date, can't have quotes around it
        ($field eq 'date') and ($item_value = '');
        if ($item_value) {
            $item_value = escape_string($item_value);
            push(@item_values, $item_value);
            push(@item_keys, $field);
        }
    }

	my $keys_prepared = '(' . join(', ', @item_keys) . 
           ', date' . ')';
	my $values_prepared = "('" . join("', '", @item_values) . 
            "', now())";
	#my $keys_prepared = '(' . join(', ', @item_keys) . ')';
	#my $values_prepared = "('" . join("', '", @item_values) . "')";

	my $sth =
         $dbh->prepare("
             INSERT into books
             $keys_prepared
             VALUES $values_prepared
         ");

    (defined $sth) or die "Couldn't add_item: $DBI::errstr";
    ($sth->execute) or die "Couldn't add_item: $DBI::errstr";

    my $new_id = $sth->{insertid};
	
    return ($new_id);
}

sub remove_items {

    my $itemlist = shift;

	my $items_prepared = "(item_id = '" .
	                     join( "') OR (item_id = '" , @$itemlist) .
                         "')";
	my $sth =
         $dbh->prepare("
             DELETE from books
			 WHERE $items_prepared
         ");

    (defined $sth) or die "Couldn't remove_items: $DBI::errstr";
    ($sth->execute) or die "Couldn't remove_items: $DBI::errstr";
		
	$sth->finish;
}


sub alter_item_field {
    
    my ($field_name, $old_field, $new_field);
    $field_name = shift;
    $old_field = shift;
    $new_field = shift;

	my $sth =
         $dbh->prepare("
             UPDATE books
	     SET $field_name = '$new_field' 
	     WHERE $field_name = '$old_field'
         ");
    (defined $sth) or die "Couldn't alter_item_field: $DBI::errstr";
    ($sth->execute) or die "Couldn't alter_item_field: $DBI::errstr";
		
    $sth->finish;
}

sub alter_item {

    my($item_id, $item_fields);
    $item_id = shift;
    $item_fields = shift;
    

    my($field, $item_value, @item_values); 
    foreach $field (@$item_fields) {
        $item_value = param($field);
        ($field eq 'item_id') and ($item_value = "");
        # can't put date here, since the function now(), which
        # is used to create the date, can't have quotes around it
        ($field eq 'date') and ($item_value = '');
        if ($item_value) {
            $item_value = "$field = '" . escape_string($item_value) . "'";
            push(@item_values, $item_value);
        }
    }
    my $values_prepared = join(", " , @item_values) . ', date = now()';
    #my $values_prepared = join(", " , @item_values);

    my $sth =
         $dbh->prepare("
           UPDATE books
           SET $values_prepared
           WHERE item_id='$item_id'
         ");

    (defined $sth) or die "Couldn't alter_item: $DBI::errstr";
    ($sth->execute) or die "Couldn't remove_items: $DBI::errstr";

}

sub get_items {

    my $itemlist = shift;

    (scalar @$itemlist == 0) and return 0;

    my($item, @matchers);
    foreach $item (@$itemlist) {
        push(@matchers, "item_id = " . $item);
    }
    return &select_items(\@matchers, 'OR');
}

sub search_items {

    my $matchers = shift;

    return &select_items($matchers, 'AND');
}

sub select_items {
    
    my ($matchers, $boolean);
    $matchers = shift;
    $boolean = shift;
	
    my $m_prepared = join(" $boolean ", @$matchers);

    my $sth =
      $dbh->prepare("
         SELECT * from books
         WHERE $m_prepared
      ");

    (defined $sth) or die "Couldn't select_items: $DBI::errstr";
    ($sth->execute) or die "Couldn't select_items: $DBI::errstr";
    
    my (@new_row, @matches);
    while (@new_row = $sth->fetchrow()) {
        push @matches, [@new_row];
    }
	
    $sth->finish;
	
    return (\@matches);
}

#####

sub encrypt_password {

    my $password = shift;

    $password =~ s/^\s+$//;    
    my $sth_encrypt =
         $dbh->prepare("SELECT PASSWORD('$password')");
    (defined $sth_encrypt) or die "Couldn't get_book_ids: $DBI::errstr";
    ($sth_encrypt->execute) or die "Couldn't get_book_ids: $DBI::errstr";

    my $p_encrypt = $sth_encrypt->fetchrow();

    return $p_encrypt;
}


sub get_book_ids {

    my $email = shift; 
    my $password = shift;

    $password = encrypt_password($password);

    my $sth =
         $dbh->prepare("
             SELECT *
             FROM users
             WHERE email = '$email'
         ");
    (defined $sth) or die "Couldn't get_book_ids: $DBI::errstr";
    ($sth->execute) or die "Couldn't get_book_ids: $DBI::errstr";

    my $count = 0;
    my (@therow, $i, $e, $p, $b);
    while (@therow = $sth->fetchrow()) {
        ($i, $e, $p, $b) = @therow;
        $count++;
    }
    ($count == 0) and return "new_user";
    ($count > 1) and log_note('error', "Two people under one email: " . $e);

     if ($p eq $password) {
         return ('success', split(/:/, $b));
     }
     else {

         return 'bad_password';
     }

    $sth->finish;
}

sub alter_book_ids {

    my ($book_array, $email, $password);
    $book_array = shift;
    $email = param('email');
    $password = param('password');
    $password = encrypt_password($password);

    my $booklist = join(':', @$book_array);

    my $sth =
         $dbh->prepare("
             UPDATE users
             SET books = ('$booklist')
	     WHERE (email = '$email') AND
                   (password = '$password')
         ");

    (defined $sth) or die "Couldn't alter_book_ids: $DBI::errstr";
    ($sth->execute) or die "Couldn't alter_book_ids: $DBI::errstr";
		
    $sth->finish;
}

sub alter_user {

    my($old_email, $new_email, $new_password);
    $old_email = shift;
    $new_email = shift;
    $new_password = shift;
    $new_password = encrypt_password($new_password);
 
    my $sth =
         $dbh->prepare("
             UPDATE users
             SET email = '$new_email',
                 password = '$new_password'
             WHERE email = '$old_email'
         ");

    (defined $sth) or die "Couldn't alter_user: $DBI::errstr";
    ($sth->execute) or die "Couldn't alter_user: $DBI::errstr";
		
    $sth->finish;
}

sub add_user {

    my $email = shift;
    my $password = shift;
    $password = encrypt_password($password);
 
    my $sth =
         $dbh->prepare("
             INSERT into users
             VALUES ('', '$email', '$password', 'NULL')
         ");

    (defined $sth) or die "Couldn't add_user: $DBI::errstr";
    ($sth->execute) or die "Couldn't add_user: $DBI::errstr";
	
    $sth->finish;
}

sub remove_user {

    my $email = shift;

	my $sth =
         $dbh->prepare("
             DELETE from users
	     WHERE (email = '$email')
         ");

    (defined $sth) or die "Couldn't remove_user: $DBI::errstr";
    ($sth->execute) or die "Couldn't remove_user: $DBI::errstr";
		
	$sth->finish;
}

sub find_user {
    
    my $email = shift;

    my $sth =
      $dbh->prepare("
         SELECT * from users
         WHERE email='$email'
      ");

    (defined $sth) or die "Couldn't find_user: $DBI::errstr";
    ($sth->execute) or die "Couldn't find_user: $DBI::errstr";
    
    my @match = $sth->fetchrow();
	
    $sth->finish;
	
    return (@match);
}

#####

# for the file "cleanup"
sub db_optimize {

   my ($adder, $sth, $rv);

   $adder = "OPTIMIZE TABLE books";

   ($sth = $dbh->prepare($adder))
      or die "Couldn't optimize: $DBI::errstr";

   ($rv = $sth->execute) 
      or die "Couldn't optimize: $DBI::errstr";

   $adder = "OPTIMIZE TABLE users";

   ($sth = $dbh->prepare($adder))
      or die "Couldn't optimize: $DBI::errstr";

   ($rv = $sth->execute) 
      or die "Couldn't optimize: $DBI::errstr";
}


# since I allow certain "naughty" characters, I have to escape
# them sometimes
sub escape_string {
    
    my $escaped = shift;
    # is there a better way to do this?
    $escaped =~ s/\+/\\\+/g;
    $escaped =~ s/\//\\\//g;
    $escaped =~ s/\./\\\./g;
    $escaped =~ s/\,/\\\,/g;
    $escaped =~ s/\-/\\\-/g;
    $escaped =~ s/\$/\\\$/g;
    $escaped =~ s/\@/\\\@/g;
    $escaped =~ s/\'/\\\'/g;
    $escaped =~ s/\"/\\\"/g;
    return $escaped;
}

# In case bad people try to do bad things and to keep tabs on things.
#sub log_note {

#    my($file_name, $note);
#    $file_name = shift;
#    $note = shift;
#    (my $log = &lock('logs/' . $file_name . '_log', 'append')) or 
#      (die "Couldn't open ${file_name}_log", return undef);

#    my $time = scalar(localtime);
#    print $log "$time: $note\n";
#    unlock($log);
#}

1; #returns true as required
