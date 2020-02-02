require("../SbeFiles.pl");

my $question = 'Enter the email of the user you wish to find: ";
my $answer = '';

while ($answer eq "")
{
  	print "$question\n";
    	$answer = <>;
    	chomp $answer;
    	print "\n";
}

db_connect();
@user = find_user($answer);
if (@user) {
    print @user;
} else {
    print 'not found';
}
print "\n";
db_disconnect();
