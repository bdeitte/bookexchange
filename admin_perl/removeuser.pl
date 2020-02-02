#!/usr/bin/perl
require("../SbeFiles.pl");

my $question = 'Enter the email of the user you wish to remove: ";
my $answer = '';

while ($answer eq "")
{
  	print "$question\n";
    	$answer = <>;
    	chomp $answer;
    	print "\n";
}

db_connect();
remove_user($answer);
print "$email has been removed. \n";
db_disconnect();

