fname = "./json/quotes.json"
txt = ""

with open(fname, 'r') as file:
    txt = file.read()

print(txt)
    