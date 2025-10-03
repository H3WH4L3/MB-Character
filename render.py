from jinja2 import Environment, FileSystemLoader
import json

env = Environment(loader=FileSystemLoader("templates/"))
template = env.get_template("sheet.html")

def make_new_sheet():
    with open("data/character.json", "r", encoding="UTF-8") as file:
        data = json.load(file)
    
    new_html = template.stream(**data)
    new_html.dump("character.html", encoding="UTF-8")