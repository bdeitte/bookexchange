#!/usr/bin/perl
# part of Quixote's Exchange
# Copyright 1999  Brian Deitte

use strict;

# This file contains standard cgi safety checks.  It never "dies" if it
# finds something wrong, but rather allows someone else to print its 
# error message describing what the user did wrong.

sub standard_check {

    my($required, @missing);
    $required = shift;
    @missing = check_missing($required);
    (@missing) and (return &missing(\@missing));

    my(@param_names, $param, @used_params, @char);
    @param_names = param;
    # foreach loop needed to make check_char work, although it really
    # should be a part of the grep in check_char
    foreach $param (@param_names) {
        (param($param) ne '') and push(@used_params, $param);
    }
    @char = check_char(\@used_params);
    (@char) and (return &bad_char(\@char));

    return undef;
}

sub check_missing {
     my ($req, %p);
     $req = shift;
     grep (param($_) ne '' && $p{$_}++,@$req);
     return grep(!$p{$_},@$req);
}


sub missing {
    my $fields = shift;
    return ("Please fill in the following fields: " .
      em(join(', ',@$fields)) . '.');               
}

sub check_char {
    my ($used, %p, %req);
    $used = shift;

    grep (param($_) !~ /^[\s\w\.\,:\-\+\/'\$;?]+$/ || $p{$_}++, @$used);
    # Since email is dealt with in check_email, these
    # values are kludged in.
    $p{'email'} = 1;
    $p{'sender_email'} = 1;     # from mail.cgi
    $p{'friend_email_1'} = 1;
    $p{'friend_email_2'} = 1;
    $p{'friend_email_3'} = 1;
    $p{'friend_email_4'} = 1;
    $p{'friend_email_5'} = 1;
    $p{'new_email'} = 1;        # from word.cgi

    return grep(!$p{$_},@$used);
}

sub bad_char {
    my $fields = shift;
    return ("The following fields have naughty characters
      (ie strange characters like \^, \&, or even \*) which
      aren't allowed for security reasons: " .
      em(join(', ',"@$fields")) . '.');
}

sub check_email {
    return ("@_" !~ /^[\w\.-]+\@[\w\.-]+$/);
}

sub bad_email {
    return ("@_ is not a recognized email address." .
        "Please enter an email address in standard format.");
}

1; #return true, as required
