#!/usr/bin/perl
# Prints out the email addresses of all users.

require("../conf.pl");

use DBI;

$driver = $DB_DRIVER;

$dbh = DBI->connect("DBI:$driver:database=$DB_NAME;", $DB_USER, $DB_PASSWORD);

$drh = DBI->install_driver($DB_DRIVER);

my $sth = $dbh->prepare("SELECT email from users");

(defined $sth) or die "Couldn't select_items: $DBI::errstr";
($sth->execute) or die "Couldn't select_items: $DBI::errstr";

while (@new_row = $sth->fetchrow()) {
    print @new_row;
    print "\n";
}

print "\n";
