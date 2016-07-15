f = open('Mobile Chaos List X.txt')
g = open('Chaos Magic Alpha.xml', 'w')

g.write('<?xml version="1.0" encoding="UTF-8"?>\n\n')
g.write('<chaoslist>\n\n')

l = f.readline()

def writeListItem(title, body, special):
	g.write("<roll>\n")
	g.write("\t<name>" + title + "</name>\n")
	g.write("\t<effect>\n")
	g.write(body)
	g.write("\t</effect>\n")
	g.write("</roll>\n\n")
	
list = ['A','B','C','D','E','F']

while l:
	if l[0] in list and l[1:2].isdigit():
		special = []
		if l[4] == '<':
			if
		n = ""
		m = f.readline()
		while m != "\n":
			n += "\t" + m
			m = f.readline()
		
		writeListItem(l[4:-1],n, special)
		
	l = f.readline()
	
g.write('\n</chaoslist>')