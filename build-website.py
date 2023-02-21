import os
from shutil import copyfile
import json
import yaml
from jinja2 import Template

f = open('chaos.yaml')
h = open('templates/header.html')
s = open('templates/sidebar.html')
#s = open('scryfall-default-cards.json')
l = open('templates/list.html')
i = open('templates/index.html')

chaos = yaml.safe_load(f)
header = h.read()
sidebar = s.read()
#cards = json.load(s)
page = l.read()
index = i.read()

f.close()
#s.close()
l.close()
i.close()

headerTemplate = Template(header)
sidebarTemplate = Template(sidebar)
indexTemplate = Template(index)
pageTemplate = Template(page)
cardTemplate = Template('<h4>{{ i }}. <a href="{{ uri }}">{{ card }}</a></h4><p>{{ text }}</p>')
listTemplate = Template('<h4>{{ i }}. Roll on list {{ list }}.</h4>')
effectTemplate = Template('<h4>{{ i }}. {{ name }}</h4><p>{{ text }}</p>')

if not os.access("website", os.F_OK):
    os.makedirs("website")

copyfile("templates/rules.html", "website/rules.html")

def get_lists():
    lists = []

    for list in chaos:
        file_name = f"{list['short_name']}.html"
        lists.append({ "url": file_name, "full_name": list['full_name'], "body": list})

    return lists

def write_lists(lists, preface):
    for list in lists:
        body = list['body']
        list_file = open(f"website/{list['url']}", 'w')
        heading = f"<h3>Roll d{len(body['rolls'])}:</h3>"
        rolls = ""

        for i, roll in enumerate(body['rolls']):
            if 'list' in roll:
                rolls += listTemplate.render(i = i+1, list = roll['list'])
            elif 'name' in roll:
                rolls += effectTemplate.render(i = i+1, name = roll['name'], text = roll['text'])
            else:
                card = find_card(roll['card'])
                if card:
                    text = ""
                    if 'Xdice' in roll:
                        text += Template('X = d{{ dice }}').render(dice = roll['Xdice'])

                    rolls += cardTemplate.render(i = i+1, uri = card['image_uris']['large'], card = roll['card'], text = text)
                else:
                    rolls += effectTemplate.render(i = i+1, name = roll['card'], text = "") 

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
