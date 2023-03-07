import os
from shutil import copyfile
import json
import yaml
from jinja2 import Template

f = open('chaos.yaml')
h = open('templates/header.html')
s = open('templates/sidebar.html')
c = open('scryfall-default-cards.json')
l = open('templates/list.html')
i = open('templates/index.html')

chaos = yaml.safe_load(f)
header = h.read()
sidebar = s.read()
cards = json.load(c)
page = l.read()
index = i.read()

f.close()
s.close()
c.close()
l.close()
i.close()

headerTemplate = Template(header)
sidebarTemplate = Template(sidebar)
indexTemplate = Template(index)
pageTemplate = Template(page)
cardCell = Template('<td class="roll-title"><a class="magic-card" href="{{ uri }}">{{ card }}</a></td>')
listCell = Template('<td class="roll-title"><a class="chaos-list" href="{{ uri }}">{{ name }}</a></td>')
effectCell = Template('<td class="roll-title"><span class="chaos-effect">{{ name }}</span></td>')
emptyRollTextCell = '<td class="roll-text"></td>'

if not os.access("website", os.F_OK):
    os.makedirs("website")

copyfile("templates/rules.html", "website/rules.html")
copyfile("templates/chaos.css", "website/chaos.css")

def get_lists():
    lists = []

    for list in chaos:
        file_name = f"{list['short_name']}.html"
        lists.append({ "url": file_name, "short_name": list['short_name'], "full_name": list['full_name'], "body": list})

    return lists

def write_lists(lists, preface):
    for list in lists:
        body = list['body']
        list_file = open(f"website/{list['url']}", 'w')
        heading = f"<h3>{body['dice']}:</h3><table>"
        rolls = ""
        offset = body['first_index']

        for i, roll in enumerate(body['rolls']):
            rolls += f'<tr class="chaos-roll"><td class="index">{i + offset}</td>'

            if 'list' in roll:
                cell = '<td class="roll-totle"></td>'

                for l in lists:
                    if l['short_name'] == roll['list']:
                        uri = f"{list['short_name']}.html"
                        cell = listCell.render(uri = uri, name = l['full_name'])
                        break

                rolls += cell + emptyRollTextCell

            elif 'name' in roll:
                rolls += effectCell.render(name = roll['name'])
                rolls += f"<td class='roll-text'>{roll['text']}</td>"
            else:
                card = find_card(roll['card'])
                if card:
                    rolls += cardCell.render(uri = card['image_uris']['large'], card = roll['card'])
                else:
                    rolls += effectCell.render(name = roll['card']) 

                if 'Xdice' in roll:
                    rolls += Template('<td class="roll-text"><span>X = d{{ dice }}</span></td>').render(dice = roll['Xdice'])
                else:
                    rolls += emptyRollTextCell

            rolls += '</tr>'

        rolls += '</table>'

        output = preface + pageTemplate.render(full_name = list['full_name'], heading = heading, rolls = rolls)
        list_file.write(output)
        list_file.close()

    return lists

def write_index(preface):
    index_file = open("website/index.html", 'w')
    output = preface + indexTemplate.render()
    index_file.write(output)
    index_file.close()

def find_card(card_name):
    return None
    for card in cards:
        if card['name'] == card_name:
            return card

    return None

lists = get_lists()
preface = headerTemplate.render() + sidebarTemplate.render(lists = lists)
write_lists(lists, preface)
write_index(preface)
