#!/usr/bin/perl
# prints the number of books

require("../conf.pl");

use DBI;

$driver = $DB_DRIVER;

$dbh = DBI->connect("DBI:$driver:database=$DB_NAME;", $DB_USER, $DB_PASSWORD);

$drh = DBI->install_driver($DB_DRIVER);

my $sth = $dbh->prepare("SELECT * from books");

(defined $sth) or die "Couldn't select_items: $DBI::errstr";
($sth->execute) or die "Couldn't select_items: $DBI::errstr";

$numRows = $sth->rows;

print $numRows . "\n";
