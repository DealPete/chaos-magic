import yaml
from jinja2 import Template

f = open('chaos.yaml')
g = open('listA.html', 'w')

g.write('<!DOCTYPE html><html><head><title>Chaos List A</title></head><body>')

chaos = yaml.safe_load(f)

for i, roll in enumerate(chaos['listA']['rolls']):
    cardTemplate = Template('{{ i }}. [{{ card }}]<br>')
    listTemplate = Template('{{ i }}. Roll on list {{ list }}.<br>')
    effectTemplate = Template('{{ i }}. {{ name }}<br>{{ text }}<br>')

    if 'list' in roll:
        g.write(listTemplate.render(i = i, list = roll['list']))
    elif 'name' in roll:
        g.write(effectTemplate.render(i = i, name = roll['name'], text = roll['text']))
    else:
        g.write(cardTemplate.render(i = i, card = roll['card']))

g.write('</body></html>')

f.close()
g.close()
