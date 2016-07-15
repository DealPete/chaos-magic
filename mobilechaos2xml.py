f = open('Mobile Chaos List X.txt')
g = open('Chaos Magic.xml', 'w')

g.write('<?xml version="1.0" encoding="UTF-8"?>\n\n')
g.write('<chaoslist>\n\n')

l = f.readline()

def writeListItem(title, body, chaosList, weight):
	g.write("<roll>\n")
	g.write("\t<list>" + chaosList + "</list>\n")
	g.write("\t<name>" + title + "</name>\n")
	g.write("\t<effect>")
	g.write(body)
	g.write("</effect>\n")
	g.write("\t<weight>")
	g.write(str(weight))
	g.write("</weight>\n")
	g.write("</roll>\n\n")
	
list = {'A':'Chaos List A',
		'B':'Chaos List B',
		'C':'Chaos List C',
		'D':'Chaos List D',
		'E':'Chaos List E',
		'F':'Chaos List F',
		'G':'Global Chaos',
		'S':'Spite',
		'X':'Extreme Chaos'}
		
while l:
	if l[0] in list:
		listName = list[l[0]]
		firstLine = l.split(None, 1);
		
		n = ""
		m = f.readline()
		while m != "\n":
			n += m
			m = f.readline()
		
		if l[0] == 'S':
			weight = int(firstLine[0][1:])
			rollName = 'Spite'
		else:
			weight = 1
			rollName = firstLine[1][:-1]
			
		writeListItem(rollName, n[:-1], listName, weight)
		
	l = f.readline()
	
g.write('\n</chaoslist>')