require("../SbeFiles.pl");

my $question = 'Enter the email of the user who's password you want to change: ";
my $answer = '';

while ($answer eq "")
{
  	print "$question\n";
    	$answer = <>;
    	chomp $answer;
    	print "\n";
}

my $question2 = 'Enter the email of the user who's password you want to change: ";
my $answer2 = '';

while ($answer2 eq "")
{
  	print "$question2\n";
    	$answer2 = <>;
    	chomp $answer2;
    	print "\n";
}

db_connect();
alter_user($answer, $answer, $answer2);
print "$answer password changed to $answer2 \n";
db_disconnect();
