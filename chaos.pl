
open CHAOS, "<Chaos List X.txt"
	or die "Can't open chaos list: $!";

#open ORACLE, "<oracle-all_091018.txt"
open ORACLE, "<All Sets-2014-02-01.txt"
	or die "Can't open oracle text: $!";
	
my $entireList, $oracleText;

$entireList .= $_
	foreach (<CHAOS>);

$oracleText .= $_
	foreach (<ORACLE>);

my %listName = ("a" => "Chaos List A",
				"b" => "Chaos List B",
				"c" => "Chaos List C",
				"d" => "Chaos List D",
				"e" => "Chaos List E",
				"f" => "Chaos List F",
				"v" => "The Vortex",
				"g" => "Global",
				"ex" => "Extreme Chaos",
				"cs1" => "Mild Creature",
				"cs2" => "Strong Creature",
				"cs3" => "Exceptional Creature",
				"cs4" => "Treacherous Creature",
				"cs5" => "Synthetic Creature",
				"a1" => "Acquisition",
				"a2" => "Acquisition II",
				"mus" => "Musical",
				"neg" => "Negative Feedback",
				"pl" => "Planeswalker",
				"res" => "Response",
				"dire" => "Dire Misfortune",);
@listName = sort values %listName; #@listname can be used instead of "keys %chaoslist" as chaoslist never changes once made, and is made from this
@shortName = sort keys %listName;

my @creatureTypes = qw/ Soldier Spirit Wizard Goblin Beast Cleric Wall Elf Zombie Bird Human Knight Elemental Dragon Insect Merfolk Angel Golem Cat Druid Horror Drake Warrior Rat Giant Wurm Minion Ogre Shaman Snake Dwarf Illusion Mercenary Orc Spellshaper Kavu Lord Samurai Sliver Djinn Rebel Elephant Imp Ape Barbarian Minotaur Treefolk Thrull Serpent Demon /;

my @colours = qw/ Blue Green Red White Black Pink /;

my %optionalMechanics = ("Pink" => 'no', "Vanguard" => 'yes', "Ante" => 'no');

my %chaosList;

foreach (@listName) {
	if ( $entireList =~ /\_\_$_\_\_(.*?)\[=+\]/s ) {
		$chaosList{ $_ } = [ $1 ];
	} else {
		die "Something is awry.  Can't find " . $_ . " on Chaos List.\n";
	}
}

foreach $name (@listName) {
	my $index, $begin;
	if ($name =~ /Chaos List ([ABCDEF])/) {
		my $ltr = $1;
		$index = $begin = 10;
		while (${ $chaosList{ $name } }[0] =~ /\n($ltr$index.*?\n)\n/s ) {
			${ $chaosList{ $name } }[++$index - $begin] = &preParse($1);
#			print ${ $chaosLIst{ $name } }[$index - $begin];
		}
	} elsif ($name =~ /(Synthetic Creature)|(Negative Feedback)/) {
		$index = $begin = 1;
		while (${ $chaosList{ $name } }[0] =~ /\n$index\s(.*?)\n\d/s ) {
			${ $chaosList{ $name } }[++$index - $begin] = &preParse($1);
		}
	} else {
		$index = $begin = 	($name eq "The Vortex") ? 3 :
							($name eq "Global") ? 10 :
							($name eq "Extreme Chaos") ? 2 : 1;
		while (${ $chaosList{ $name } }[0] =~ /\n\n($index.*?\n)\n/s ) {
			${ $chaosList{ $name } }[++$index - $begin] = &preParse($1);
		}
	}
	
	print "Parsed $name with " . ($index - $begin) . " elements.\n";
}

&listMechanics;

for (my $name, $chaosRoll;;) {
	my $previousRoll = $name;
	print "\nEnter a list or command (info end toggle help): ";
	chomp($name = <>);
	print '=' x 80;
	$name = $listName{$name} if exists $listName{$name};
	$name = $previousRoll if ($name eq "");
	if ($name =~ /help/i) {
		print "Type the name of a list (case sensitive) to make a roll on that list.\n";
		print "Type the name of a magic card to see the text of that card.\n";
		print "\nThe commands are:\n";
		print "(end)         Ends the program.\n";
		print "(info)        Displays available lists and optional gameplay mechanics.\n";
		print "(toggle)      Toggles an optional gameplay mechanic.\n";
		print "\nPressing enter will repeat previous command.\n";
	} elsif ($name =~ /end/i) {
		last;
	} elsif ($name =~ /info/i) {
		print "Available lists are:\n";
		#TODO: make the nextline a printf to make the colons line up
		print "$_ : $listName{ $_ } \n" foreach (@shortName);
		&listMechanics;
	} elsif ($name =~ /toggle (.*)/i) {
		if (!$optionalMechanics{ $1 }) {
			print "Cannot find optional gameplay mechanic $1:\n";
			&listMechanics;
		} elsif ($optionalMechanics{ $1 } eq 'yes') {
			$optionalMechanics{ $1 } = 'no';
			print "Turned off $1.\n";
		} else {
			$optionalMechanics{ $1 } = 'yes';
			print "Turned on $1.\n";
		}
	} elsif ($chaosList{$name}) {
ROLL:	while () {
			if ($name eq "The Vortex") {
				$chaosRoll = &Parse( ${ $chaosList{ "The Vortex" }}[ &d(8) + &d(8) + &d(8) - 2 ] );
			} elsif ($name eq "Extreme Chaos") {
				$chaosRoll = &Parse( ${ $chaosList{ "Extreme Chaos" }}[ &d(12) + &d(12) - 1 ] );
			} elsif ($name eq "Synthetic Creature") {
				print "I am generating a random creature for you.  You will have to give it a name.\n";
				my $creatureType = $creatureTypes[ &d( scalar @creatureTypes ) - 1];
				print "It is a(n) " . &d(8) . "/" . &d(8) . " " . $colours[ &d($optionalMechanics{ "Pink" } eq "yes" ? 6 : 5) - 1] . " " . $creatureType . " with the following abilities:\n\n";
				#my $abilities = &d(4);
				#if ($creatureType eq "Wall") {
				#	print "Defender\n";
				#}
				my %rolled, $roll;
				for (1..&d(4)) {
					while ($rolled{ $roll = &d( @{$chaosList{ $name }} - 1) }) {};
					$rolled{ $roll } = 'yes';
					if (${ $chaosList{ $name } }[ $roll ] =~ /Threshold: Ability d/) {
						while ($rolled{ $roll = &d( @{$chaosList{ $name }} - 1) }) {};
						$rolled{ $roll } = 'yes';
						print "Threshold: ";
					}
					print &Parse( ${ $chaosList{ $name } }[ $roll ]) . "\n";
				}
				last;
			} else {
            	$chaosRoll = Parse( ${ $chaosList{ $name } }[ &d( @{$chaosList{ $name }} - 1) ] );
			}
			print "\n\n" . $chaosRoll . "\n";
			if ($chaosRoll =~ /{(.*?)}/) {
				$bracedtext = $1;
				last unless exists $chaosList{$bracedtext}; #only want to jump for a list
				print "Press enter to roll on $temp, or anything else to abort.\n";
				chomp($nextline = <>);
				last ROLL if ($nextline ne '');
				$name = $bracedtext; #this will make the named list the default on the next loop
			} else { last; }
		}
	} elsif ($oracleText =~ /\n\n($name.*?\n)\n/is) {
		print $1;
	} else {
		print "I can find no list, card, or command matching $name.  Please re-enter.\n";
	}
	print '=' x 80;
}

sub d ($) {
    my ($max) = @_;
	# Assumes that the argument is an integer itself!
    1 + int rand($max);
}

sub preParse ($) {
	my ($parseText) = @_;
	#$parseText =~ s/\n(\(.*?\))//sg; #removed to stop removing the oracle text
	return $parseText;
}
	
sub Parse ($) {
	my $replaceText, ($parseText) = @_;
	while ($parseText =~ /(\d*)d(\d+)/s) {
		$replaceText = 0;
		$replaceText += &d($2) for (1..(!$1 ? 1 : $1));
		$parseText =~ s/(\d*)d(\d+)/$replaceText/s;
		#print $parseText;
	}
	return $parseText;
}

sub listMechanics {
	@keys = keys %optionalMechanics;
	print "\nOptional gameplay mechanics: @keys\n";
	print "Optional gameplay mechanics in use: ";
	foreach (@keys) {
		if ($optionalMechanics{ $_ } eq "yes") {
			print $_ . " ";
		}
	}
	print "\n";
}

