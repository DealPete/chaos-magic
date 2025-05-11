import os
from shutil import copyfile
import json
import yaml
from jinja2 import Template

y = open('chaos.yaml')
h = open('templates/header.html')
f = open('templates/footer.html')
s = open('templates/sidebar.html')
l = open('templates/list.html')
i = open('templates/index.html')
r = open('templates/rules.html')
m = open('templates/music.html')

chaos = yaml.safe_load(y)
header = h.read()
footer = f.read()
sidebar = s.read()
page = l.read()
index = i.read()
rules = r.read()
musical = m.read()

y.close()
h.close()
f.close()
s.close()
l.close()
i.close()
r.close()
m.close()

headerTemplate = Template(header)
footerTemplate = Template(footer)
sidebarTemplate = Template(sidebar)
indexTemplate = Template(index)
pageTemplate = Template(page)
rulesTemplate = Template(rules)
musicTemplate = Template(musical)
cardCell = Template('<td class="roll-title hover"><auto-card>{{ card }}</auto-card></td>')
cardCellNoHover = Template('<td class="roll-title no-hover"><a href="https://scryfall.com/search?q=name:{{ card }}">{{ card }}</a></td>')
listCell = Template('<td class="roll-title"><a class="chaos-list" href="{{ uri }}">{{ name }}</a></td>')
effectCell = Template('<td class="roll-title"><span class="chaos-effect">{{ name }}</span></td>')
emptyRollTextCell = '<td class="roll-text"></td>'

if not os.access("website", os.F_OK):
    os.makedirs("website")

copyfile("templates/chaos.css", "website/chaos.css")
copyfile("templates/github-mark.svg", "website/github-mark.svg")
copyfile("templates/mozart.mp3", "website/mozart.mp3")
copyfile("templates/magmed.woff2", "website/magmed.woff2")
copyfile("templates/mplantin.woff2", "website/mplantin.woff2")

def get_lists():
    lists = []

    for chaos_list in chaos:
        file_name = f"{chaos_list['short_name']}.html"
        lists.append({ "url": file_name, "short_name": chaos_list['short_name'], "full_name": chaos_list['full_name'], "body": chaos_list})

    return lists

def write_lists():
    for chaos_list in lists:
        preface = headerTemplate.render() + sidebarTemplate.render(lists = lists, cur_list = chaos_list['short_name'])
        body = chaos_list['body']

        heading = f'<header><h3>{body["desc"]}</h3></header>'
        list_file = open(f"website/{chaos_list['url']}", 'w')

        if body['format'] == 'List':
            parsed = parse_as_list(body)
        else:
            parsed = parse_as_table(body)

        parsed = replace_embedded_links(parsed)
        output = preface + pageTemplate.render(full_name = chaos_list['full_name'], heading = heading, rolls = parsed)
        if chaos_list['short_name'] == 'musical': output += musicTemplate.render()
        output += footerTemplate.render()
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
        index = i + offset

        if 'index' in roll:
            index = roll['index']

        rolls += f'<tr class="chaos-roll"><td class="roll-index">{index}</td>'

        if 'list' in roll:
            cell = get_list_cell(roll['list'])
            rolls += cell + emptyRollTextCell
        elif 'name' in roll:
            rolls += effectCell.render(name = roll['name'])

            text = []
            if 'mana_cost' in roll:
                top_line = roll["mana_cost"]
                if 'type' in roll:
                    top_line += f', {roll["type"]}'
                text.append(top_line)
            if 'power' in roll:
                text.append(f'{roll["power"]}/{roll["toughness"]}')

            text = text + roll['text'].split('\n')
            markup = '<br>'.join([ f'<span>{t}</span>' for t in text ])
            rolls += f"<td class='roll-text'>{markup}</td>"
        elif 'text' in roll:
            rolls += f'<td class="roll-text"><span>{roll["text"]}</span></td>'
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
        ( '{X}', 'ms-x' ),
        ( '{0}', 'ms-0' ),
        ( '{1}', 'ms-1' ),
        ( '{2}', 'ms-2' ),
        ( '{3}', 'ms-3' ),
        ( '{4}', 'ms-4' ),
        ( '{5}', 'ms-5' ),
        ( '{6}', 'ms-6' ),
        ( '{7}', 'ms-7' ),
        ( '{8}', 'ms-8' ),
        ( '{9}', 'ms-9' ),
        ( '{10}', 'ms-10' ),
        ( '{11}', 'ms-11' ),
        ( '{15}', 'ms-15' ),
        ( '{T}', 'ms-tap' ),
        ( '{Q}', 'ms-untap' ),
        ( '{B}', 'ms-b' ),
        ( '{U}', 'ms-u' ),
        ( '{G}', 'ms-g' ),
        ( '{hG}', 'ms-g ms-half' ),
        ( '{R}', 'ms-r' ),
        ( '{W}', 'ms-w' ),
        ( '{R/U}', 'ms-ur' ),
        ( '{G/W}', 'ms-gw' )
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

def find_card(card_name):
    return None
    for card in cards:
        if card['name'] == card_name:
            return card

    return None

lists = get_lists()
write_lists()

index_file = open("website/index.html", 'w')
output = headerTemplate.render() + sidebarTemplate.render(lists = lists, cur_list = 'Home') + indexTemplate.render() + footerTemplate.render()
index_file.write(output)
index_file.close()

rules_file = open("website/rules.html", 'w')
output = headerTemplate.render() + sidebarTemplate.render(lists = lists, cur_list = 'Rules') + rulesTemplate.render() + footerTemplate.render()
rules_file.write(output)
rules_file.close()
