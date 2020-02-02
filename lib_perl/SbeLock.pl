#!/usr/bin/perl
# part of Quixote's Exchange
# Copyright 1999  Brian Deitte

sub LOCK_SH { 1 }
sub LOCK_EX { 2 }
sub LOCK_UN { 8 }

my $flock = ($OS ne 'nt');

# opens and locks a file of type 'append', 'overwrite', or 'read'
sub lock {

    my ($path, $type);
    $path = shift;
    $type = shift;

    my ($lock_type, $path_name, $description);
    if ($type eq 'append') {
        $lock_type = LOCK_EX;
        $path_name = ">>$path";
        $description = 'appending';
    } else {
        if ($type eq 'overwrite') {
            $lock_type = LOCK_EX;
            $path_name = ">$path";
            $description = 'overwriting';
        }
        else {
            $lock_type = LOCK_SH;
            $path_name = "<$path";
            $description = 'reading';
        }
    }

    if ($flock)
    {
        my($handler, $msg,$oldsig);
        $handler = sub { $msg='timed out'; $SIG{ALRM}=$oldsig; };
        ($oldsig,$SIG{ALRM}) = ($SIG{ALRM},$handler);
        alarm(10);   # wait for up to 10 seconds for a flock
    }
    open (FH, $path_name) or (warn("Couldn't open $path for $description: $!"), return undef);

    if ($flock)
    {
        unless (flock (FH, $lock_type)) {
            warn("Couldn't get lock for $description (".($msg or "$!") . ")");
            alarm(0);
            close FH;
            return undef;
        }
        alarm(0);
    }

    return \*FH;
}

# close and unlock a file
# takes in a file handle
sub unlock {
    my $fh = shift;

    flock($fh, LOCK_UN) if ($flock);
    close $fh;
}

1;
