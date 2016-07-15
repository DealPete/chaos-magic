while (<>) {
	chomp;
	$abba = "B";
	$index = 52;
	if (/===.*===/s) {
		print "Matched: |$`<$&>$'|\n";
	} else {
		print "No match.\n";
	}
}
