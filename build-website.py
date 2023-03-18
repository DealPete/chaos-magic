import os
from shutil import copyfile
import json
import yaml
from jinja2 import Template

y = open('chaos.yaml')
h = open('templates/header.html')
f = open('templates/footer.html')
s = open('templates/sidebar.html')
#c = open('scryfall-default-cards.json')
l = open('templates/list.html')
i = open('templates/index.html')

chaos = yaml.safe_load(y)
header = h.read()
footer = f.read()
sidebar = s.read()
#cards = json.load(c)
page = l.read()
index = i.read()

y.close()
h.close()
f.close()
s.close()
#c.close()
l.close()
i.close()

headerTemplate = Template(header)
footerTemplate = Template(footer)
sidebarTemplate = Template(sidebar)
indexTemplate = Template(index)
pageTemplate = Template(page)
cardCell = Template('<td class="roll-title hover"><auto-card>{{ card }}</auto-card></td>')
cardCellNoHover = Template('<td class="roll-title no-hover"><a href="https://scryfall.com/search?q=name:{{ card }}">{{ card }}</a></td>')
listCell = Template('<td class="roll-title"><a class="chaos-list" href="{{ uri }}">{{ name }}</a></td>')
effectCell = Template('<td class="roll-title"><span class="chaos-effect">{{ name }}</span></td>')
emptyRollTextCell = '<td class="roll-text"></td>'

if not os.access("website", os.F_OK):
    os.makedirs("website")

copyfile("templates/rules.html", "website/rules.html")
copyfile("templates/chaos.css", "website/chaos.css")

def get_lists():
    lists = []

    for chaos_list in chaos:
        file_name = f"{chaos_list['short_name']}.html"
        lists.append({ "url": file_name, "short_name": chaos_list['short_name'], "full_name": chaos_list['full_name'], "body": chaos_list})

    return lists

def write_lists():
    for chaos_list in lists:
        body = chaos_list['body']

        heading = f"<h3>{body['desc']}</h3>"
        list_file = open(f"website/{chaos_list['url']}", 'w')

        if body['format'] == 'List':
            parsed = parse_as_list(body)
        else:
            parsed = parse_as_table(body)

        parsed = replace_embedded_links(parsed)
        output = preface + pageTemplate.render(full_name = chaos_list['full_name'], heading = heading, rolls = parsed) + footerTemplate.render()
        list_file.write(parse_mana_symbols(output))
        list_file.close()

def parse_as_list(body):
    rolls = f"<ol start={body['first_index']}>"

    for roll in body['rolls']:
        if 'list' in roll:
            cell = get_list_cell(roll['list'])
            rolls += f'<li class="roll-text">{cell}</li>'
        else:
            rolls += f'<li class="roll-text">{roll["text"]}</li>'

    rolls += '</ol>'
    return rolls

def parse_as_table(body):
    rolls = "<table>"

    offset = body['first_index']

    for i, roll in enumerate(body['rolls']):
        rolls += f'<tr class="chaos-roll"><td class="index">{i + offset}</td>'

        if 'list' in roll:
            cell = get_list_cell(roll['list'])
            rolls += cell + emptyRollTextCell

        elif 'name' in roll:
            rolls += effectCell.render(name = roll['name'])
            text = roll['text'].split('\n')
            markup = '<br>'.join([ f'<span>{t}</span>' for t in text ])
            rolls += f"<td class='roll-text'>{markup}</td>"
        else:
            rolls += cardCell.render(card = roll['card']) + cardCellNoHover.render(card = roll['card'])

            if 'Xdice' in roll:
                roll_dice = parse_dice(roll['Xdice'])
                rolls += Template('<td class="roll-text"><span>X = {{ dice }}</span></td>').render(dice = roll_dice)
            else:
                rolls += emptyRollTextCell

        rolls += '</tr>'

    rolls += '</table>'

    return rolls

def replace_embedded_links(parsed):
    for l in lists:
        short_name = l["short_name"]
        full_name = l["full_name"]
        replacement = f'<a href="{short_name}.html">{full_name}</a>'
        parsed = parsed.replace(f'[{short_name}]', replacement)

    return parsed

def parse_mana_symbols(markup):
    mana_symbols = [
        ( '{0}', 'ms-0' ),
        ( '{1}', 'ms-1' ),
        ( '{2}', 'ms-2' ),
        ( '{3}', 'ms-3' ),
        ( '{T}', 'ms-tap' ),
        ( '{B}', 'ms-b' ),
        ( '{U}', 'ms-u' ),
        ( '{G}', 'ms-g' ),
        ( '{R}', 'ms-u' ),
        ( '{W}', 'ms-w' ),
        ( '{R/U}', 'ms-ur' )
    ]

    for ( m, r ) in mana_symbols:
        markup = markup.replace( m, f'<i class="ms ms-cost {r}"></i>' )

    return markup

def get_list_cell(list_name):
    cell = '<td class="roll-title"></td>'
    for l in lists:
        if l['short_name'] == list_name:
            uri = f"{l['short_name']}.html"
            cell = listCell.render(uri = uri, name = l['full_name'])
            break

    return cell
    
def parse_dice(xdice):
    dice = []

    if xdice[0] == 1:
        dice.append(f"d{xdice[1]}")
    elif xdice[0] > 1:
        dice.append(f"{xdice[0]}d{xdice[1]}")

    if xdice[2] > 0:
        dice.append(f"{xdice[2]}")

    return " + ".join(dice)

def write_index():
    index_file = open("website/index.html", 'w')
    output = preface + indexTemplate.render() + footerTemplate.render()
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
write_lists()
write_index()
