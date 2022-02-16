import json

with open('storage.json', mode = 'r') as file:
    storage = json.load(file)

id = '211960973253279744'
try: 
    person = storage[id]
except:
    with open('template.json', mode = 'r') as file:
        person = json.load(file)['id']
person['tries'].append(1)
storage[id] = person

with open('storage.json', mode = 'w', encoding = 'utf-8') as f:
    json.dump(storage, f, ensure_ascii = False, indent = 4)