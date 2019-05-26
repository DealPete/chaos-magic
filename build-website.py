import os
from shutil import copyfile
import json
import yaml
from jinja2 import Template

f = open('chaos.yaml')
s = open('scryfall-default-cards.json')
l = open('templates/list.html')
i = open('templates/index.html')

chaos = yaml.safe_load(f)
cards = json.load(s)
page = l.read()
index = i.read()

f.close()
s.close()
l.close()
i.close()

indexTemplate = Template(index)
pageTemplate = Template(page)
cardTemplate = Template('{{ i }}. <a href="{{ uri }}">{{ card }}</a><br>')
listTemplate = Template('{{ i }}. Roll on list {{ list }}.<br>')
effectTemplate = Template('{{ i }}. {{ name }}<br>{{ text }}<br>')

if not os.access("website", os.F_OK):
    os.makedirs("website")

copyfile("templates/rules.html", "website/rules.html")

def write_lists():
    lists = []

    for list in chaos:
        file_name = f"{list['short_name']}.html"
        list_file = open(f"website/{file_name}", 'w')
        preface = f"Roll d{len(list['rolls'])}:"
        rolls = ""

        for i, roll in enumerate(list['rolls']):
            if 'list' in roll:
                rolls += listTemplate.render(i = i+1, list = roll['list'])
            elif 'name' in roll:
                rolls += effectTemplate.render(i = i+1, name = roll['name'], text = roll['text'])
            else:
                card = find_card(roll['card'])
                if card:
                    rolls += cardTemplate.render(i = i+1, uri = card['image_uris']['large'], card = roll['card'])
        output = pageTemplate.render(full_name = list['full_name'], preface = preface, rolls = rolls)
        list_file.write(output)
        list_file.close()
        lists.append({ "url": file_name, "full_name": list['full_name']})

    return lists

def write_index(lists):
    index_file = open("website/index.html", 'w')
    output = indexTemplate.render(lists = lists)
    index_file.write(output)
    index_file.close()

def find_card(card_name):
    for card in cards:
        if card['name'] == card_name:
            return card

    return None

lists = write_lists()
write_index(lists)
