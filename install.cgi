#!/usr/bin/perl
# Parts of this install script are copyrighted by Perlfect Solutions, http://www.perlfect.com
use strict;
use DBI;

my $VERSION = "0.1";

print "
BookExchange $VERSION Setup Utility

NOTE: You must have 

access to an SQL database
access to the DBI driver for the database
a created database for the bookexchange

Without these pieces, the bookexchange can't run!  Please take special note to
the third piece, the only unautomatic part of this installation: you need to create
the database (but not its tables) before installation.

If you don't know if have 
these, please ask your system administrator.  (Also ask for a user name and 
password for connecting to the database, and that the user can create tables.)

";

exit if (input("Do you want to continue? [y/n]", "y", ["y","n"]) eq "n");

print "
BookExchange
Copyright 1999 Brian Deitte (except as noted below)
Original Installer: Copyright 1999 Perlfect Solutions
All Images: Copyright 1999 David Selden

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

";

exit if (input("Do you want to continue? [y/n]", "y", ["y","n"]) eq "n");

my $os = input("What operating system is your site running on? [unix/nt]", "", ["unix", "nt"]);

my $perl;
if($os eq 'unix')
{
    $perl = `which perl`;
    chomp $perl;
    $perl='/usr/bin/perl' unless ($perl);
    $perl = input("Where is perl? [$perl]", "$perl");
    print "Ok, I will configure the scripts to run with $perl\n";

my @perlfiles;
my @sfile = &get_files('web_perl');
foreach (@sfile)
{
	set_perl_path("web_perl/$_", $perl);
}

@sfile = &get_files('admin_perl');
foreach (@sfile)
{
	set_perl_path("admin_perl/$_", $perl);
}

@sfile = &get_files('lib_perl');
foreach (@sfile)
{
	set_perl_path("lib_perl/$_", $perl);
}

print "\n";
}

my ($instdir, $insturl, $cgidir, $cgiurl, $sendmail, $adminemail,
    $dbdriver, $dbname, $dbuser, $dbpassword);
do 
{

$instdir = input("
  Where would you like the bookexchange to be installed?
  (e.g. /home/httpd/html/bookexchange)
  If the folder does not exist, it will be created.");

$insturl = input("
  What is the URL of the above directory?
  (e.g. http://www.yoursite.edu/bookexchange)");

$cgidir = input("
   Where would you like the cgi files to be installed?
   (e.g. /home/httpd/cgi-bin/bookexchange)
   If the folder does not exist, it will be created.");

$cgiurl = input("
   What is the URL of the above directory?
   (e.g.http://www.yoursite.edu/cgi-bin/bookexchange)");

$sendmail = input("
   Where is sendmail (or the equivalent) located?
   (e.g. /usr/lib/sendmail");
  
$adminemail = input("
   What is the email users should use if they need help with the bookexchange?");

$dbdriver = input("
   What kind of database are you using? (e.g. mysql)");

$dbname = input("
   What is the database named? (e.g. bookexchange)
   Remember, this install script will not work if the
   database has not already been created.");

$dbuser = input("
   What name will be used to connect to the database?");

$dbpassword = input("
   What is the password for this name?");

}
while (input("End of custom information.  Is the information you provided ok? [y/n]", "y", ["y","n"]) eq "n");

foreach ($instdir, $insturl, $cgidir, $cgiurl)
  {
    $_ =~ s/[\/:\\]$//;
  }


print "
I will now set up the database... 
";

(my $dbh = DBI->connect("DBI:$dbdriver:database=$dbname;", $dbuser, $dbpassword))
       or die "Couldn't connect to the database by DBI: $DBI::errstr";

my $drh = DBI->install_driver($dbdriver)
      or die "Couldn't install the database driver: $DBI::errstr";

my $sth = $dbh->prepare("
	create table books (
		item_id		integer AUTO_INCREMENT PRIMARY KEY,
		email		varchar (60),
		title     	varchar(100),
		author		varchar(100),
		dept      	varchar(100),
		class     	varchar(100),
		isbn      	varchar(20),
		condition 	varchar(50),
		other     	varchar(255),
		price     	varchar(10),
		date      	date
	)
    ");

(defined $sth) or die "Couldn't create table: $DBI::errstr";
($sth->execute) or die "Couldn't create table: $DBI::errstr";
		
$sth->finish;

$sth = $dbh->prepare("

	create table users (
		ID		integer AUTO_INCREMENT PRIMARY KEY,
		email		varchar(60),
		password	varchar(50),
		books		varchar(255)
	)
    ");

(defined $sth) or die "Couldn't create table: $DBI::errstr";
($sth->execute) or die "Couldn't create table: $DBI::errstr";
		
$sth->finish;

my $rc = $dbh->disconnect;
($rc) or die "Couldn't disconnect from database: $rc->errstr";


print "
I will now install the files...

";

install_dir($instdir, "0755");
install_dir_files('html/', "$instdir/", "0644");
html_install($instdir, $cgiurl);

install_dir($cgidir, "0755");
install_dir_files('web_perl/', "$cgidir/", "0755");
install_dir_files('lib_perl/', "$cgidir/", "0755");

my $admindir = $instdir . "/admin";
install_dir($admindir, "0700");
install_dir_files('admin_perl/', "$admindir/", "0700");

my $imagedir = $instdir . "/images";
install_dir($imagedir, "0755");
install_dir_files("images/", "$imagedir/", "0644");

my $datadir = $instdir . "/data";
install_dir($datadir, "0755");
install_dir_files("data/", "$datadir/", "0666");

my $configdir = $instdir . "/config";
install_dir($configdir, "0750");

print "Configuring BookExchange...\n";
open(CONF, ">$cgidir/conf.pl")
  or die "\n** Could not open $cgidir/conf.pl: $!\n";
print CONF "
# Configuration for the BookExchange $VERSION

#The system running under
\$OS = '$os';

#The url of the site
\$BASE_URL = '$insturl';

#The url of the cgis
\$CGI_URL = '$cgiurl';

#The base directory
\$BASE_DIR = '$instdir';

#The directory of the cgi files
\$CGI_DIR   = '$cgidir';

#The directory of the data
\$DATA_DIR   = '$datadir';

#The location of sendmail or equivalent
\$SENDMAIL = '$sendmail';

#the contact-email
\$ADMIN_EMAIL = '$adminemail';

\$DB_DRIVER = '$dbdriver';
\$DB_USER = '$dbuser';
\$DB_NAME = '$dbname';
\$DB_PASSWORD = '$dbpassword';

1;
";
close CONF;

unless(chmod(oct("0755"), "$cgidir/conf.pl"))
{
	print "**Cannot set permissions!\n**Aborting.\n";
	exit(1);
}


print "
BookExchange $VERSION has been installed on your system.

Note: the files in 
$datadir 
have been set up as world-readable and world-writable for unix systems.  
This isn't a good idea, however.  Try to change it so that it only needs 
to be in the web-browsing 'group'.

";

press_enter();

system('clear') if($os eq 'unix');

print "
The exchange divides books into different areas.  The names (and number)
of the areas is up to you.

You can set up the areas now by entering one area per line.  Just enter a blank
line when you're done.  Otherwise, you should edit the area file by yourself:
its located at $datadir/areas.dat

";

if (input("Would you like to set up the areas now? [y/n]", "y", ["y","n"]) eq "y")
{
	print "Enter one area per line, and a blank line when you're done.\n\n";
	my $areas = "Nothing Selected\n";
	my $line = <>;
        chomp $line;
	while (defined $line && $line ne '')
	{
		$areas .= "$line\n";

	        $line = <>;
        	chomp $line;
	}

	my $areafile = "$datadir/areas.dat";
	open(CONF, ">$areafile")
	  or die "\n** Could not open $areafile: $!\n";
		
	print CONF $areas;
	close CONF;

	unless(chmod(oct("0644"), "$areafile"))
	{
		print "**Cannot set permissions!\n**Aborting.\n";
		exit(1);
	}
	print "Area setup complete! \n";
}

print "

Thanks for choosing the BookExchange for your site.
For more information on this program, please see
http://cs.uiowa.edu/~bdeitte/bookexchange

";

sub html_install
{
	my $inst_dir = shift;
	my $cgi_url = shift;

	my @allfiles = get_files($inst_dir);
	my @htmlfiles = grep /[\.html]$/, @allfiles;
	my($file, $temp, $text);

	foreach $file (@htmlfiles)
	{
		$file = "$inst_dir/$file";
		open (HTML, $file) or (die "Couldn't open $file: $!");

		$text = '';
    		while (<HTML>) 
		{
			$temp = $_;
        		$temp =~ s/CGI_URL/$cgiurl/;
			$temp =~ s/BASE_URL/$insturl/;
			$text .= $temp;
    		}
    		close HTML;
		open (NEWH, ">$file");
		print NEWH $text;
		close NEWH;

		(chmod(oct("0644"), "$file")) or die "Couldn't set permissions on $file.";
	}
}

sub install_dir
  {
    my ($dir, $permissions) = @_;
    print "Setting up $dir\n";
    if(-e $dir)
      {
	if(-d $dir)
	  {
	    print "**Directory already exists.\n";
	  }
	else
	  {
	    print "**$dir is not a directory.\n";
	    print "**I'd better not touch it then\n**Aborting!\n";
	    exit(1);
	  }
      }
    else
      {
	unless(mkdir($dir, oct($permissions)))
	  {
	    print "**Cannot create $dir\n";
	    print "**Aborting!\n";
	    exit(1);
	  }
      }
    unless(chmod(oct($permissions), $dir))
      {
	print "**Cannot set permissions!\n**Aborting.\n";
	exit(1);
      }
  }

sub install_file
  {
    my ($source, $destination, $permissions, $keepold) = @_;
    my $uninstall;
    if(-e $destination)
      {
	print "**$destination already exists.\n";
	if($keepold)
	  {
	    print "**Preserving existing $destination\n";
	    return;
	  }
	if(rename("$destination", "$destination.bak"))
	  {
	    print "**I kept a backup in $destination.bak\n";
	  }
	else
	  {
	    print "**Cannot backup the file\n**Aborting.\n";
	    exit(1);
	  }
      }
      if ($os eq 'unix')
      {
	    if(system("cp $source $destination"))
      	    {
		print "**Cannot copy $source to $destination\n**Aborting.";
		exit(1);
      	    }
      }
      elsif ($os eq 'nt')
      {
            $source =~ s/\//\\/g;
            $destination =~ s/\//\\/g;
	    if(system("copy $source $destination"))
      	    {
		print "**Cannot copy $source to $destination\n**Aborting.";
		exit(1);
      	    }
      }

    unless(chmod(oct($permissions), $destination))
    {
	print "**Cannot set permissions!\n**Aborting.\n";
	exit(1);
    }
  }

sub install_dir_files {

    my ($source, $destination, $permissions, $keepold) = @_;

    print "Installing files in $source to $destination\n";

    my @files = get_files($source);
    foreach (@files) {
    	install_file($source . $_, $destination . $_, $permissions, $keepold);
    }
}

sub get_files {

    my $dir = shift;

    if (! opendir(THISDIR, $dir))
    {
	print "Can't open the directory $dir\n**Aborting";
	exit(1);
    }

    # gets all files in directory (other than '.', '..')
    my @shortfiles = grep !/^\.\.?$/, readdir THISDIR;
    closedir THISDIR;

    return @shortfiles;
}

sub set_perl_path
  {
    my ($file, $path) = @_;
    print "Setting perl path in $file.\n";
    my $source = "#!$path\n";
    open(SRC, "$file") or die "Cannot open $file: $!\n";
    my $dump = <SRC>;
    while(<SRC>)
      {
	$source .= $_;
      }
    close SRC;
    open(DST, ">$file") or die "Cannot open $file: $!\n";
    print DST $source;
    close DST;
  }


sub input
  {
    my ($question, $default, $options) = @_;

    my $answer = '';

    while ($answer eq "")
    {
    	print "$question\n";
    	$answer = <>;
    	chomp $answer;
    	print "\n";
   
    	$answer = $default unless $answer;
    }


    unless(!defined $options or scalar(@$options)==0 or member($options, $answer))
      {
	print "Invalid option. Please select one of: ";
	print join(",", @$options)."\n";
	return input($question, $default, $options);
      }
    return $answer;
  }


sub press_enter
{
    print "-- press enter to continue --";
    my $blah = <>;
}

sub member
  {
    my ($ary, $el) = @_;
    foreach (@$ary)
      {
	return 1 if($_ eq $el);
      }
    return 0;
  }
