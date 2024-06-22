## Chaos Magic

This is a multi-player variant of Magic the Gathering for long-time players looking to add a bit of excitement and wackiness to the game. The basic idea is that at the beginning of each player's turn he rolls some dice and consults a list of spells, resolving that spell as if it had just been cast. We usually play with our Commander decks, and sometimes with <a href="https://magic.wizards.com/en/vanguard">Vanguard cards</a>.

There have been many versions of Chaos Magic over the years; it was the inspiration for Wizards of the Coast's <a href="https://en.wikipedia.org/wiki/Planechase">Planechase product</a>. This version is rather complex and is not for the faint of heart.

To compile the website youself, run

`$ python3 build-website.py`

then open the file `website/index.html`.

### Files

The file `Chaos List X.txt` contains the complete game as a text file that can be printed out and enjoyed in the old fashioned way. It was created back before mobile devices and other conveniences, when the only way to play was to have a paper copy in front of you.

The web list is contained in the file `chaos.yaml`. The html and css files to create the website are in `/templates`.

There is also an android version. The source files are found in `MobileChaos`. It uses `Chaos Magic.xml` as a source file. The file `Chaos Magic.xml` is generated from the text file `Mobile Chaos List X.txt` by the python script `mobilechaos2xml.py`.

The file `chaos.pl` is a Perl command line program that looks up chaos rolls from `Chaos List X.txt`. It should still work, but requires a plain-text oracle listing of every card on the list, which I'm no longer sure where to obtain.

The directory `MSE` contains cards created in [Magic Set Editor](http://magicseteditor.sourceforge.net). These cards can be printed out to form decks that replace some of the lists that generate tokens.

`Ron's Chaos Program.rar` is an old Windows GUI application created by a friend.

`Chaos Magic Stats.ods` is a spreadsheet that helps me keep track of how often various kinds of effects come up on the list.
