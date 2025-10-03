import random
import json

# Выгружаем базу
with open("mork_borg_cache.json", "r", encoding="UTF-8") as file:
    data = json.load(file)

class Character:
    def __init__(self, character, items, narrative):
        #region Базовые
        self.name = random.choice(data["Names"])
        self.age = random.randint(16, 55)
        self.sex = random.choice(["Male", "Female"])
        #endregion

        #region Класс 
        self.clas = character["Name"]
        self.description = character["Description"]
        #endregion

        #region Атрибуты : agility, presence, strength, toughness
        for ability, value in character["Abilities"].items():
            setattr(self, ability, value[0] * random.randint(1, value[1]) + value[2])
        #endregion

        #region Главные значения
        self.hp =  + self.toughness + character["Traits"]["HP"]
        self.money = sum([random.randint(1, character["Traits"]["Money"][1]) for _ in range(character["Traits"]["Money"][0])])
        self.skills = character["Traits"]["Skills"]
        self.signs = random.randint(1, character["Traits"]["Signs"])
        self.bonus = random.choice(character["Bonus"])
        #endregion

        #region Наратив
        self.memorie = random.choice(character["Memories"])
        self.terrible_trait = random.choice(narrative["Terrible_trait"])
        self.injuries = random.choice(narrative["Injuries"])
        self.bad_habbit = random.choice(narrative["Bad_habbits"])
        self.dangerous_past = random.choice(narrative["Dangerous_past"])
        self.secret_quest = random.choice(narrative["Secret_quest"])
        #endregion

        #region Предметы
        self.weapon = self.make_weapon(items)
        self.armor = random.choice(items["Armor"])
        self.first_item = random.choice(items["First"])
        self.second_item = self.check_to_scroll(items, "Second")
        self.third_item = self.check_to_scroll(items, "Third")
        #endregion

    def make_weapon(self, items):
        weapon = random.choice(items["Weapon"])
        if len(weapon) == 3:
            weapon_result =  f"{weapon[0]}, Урон: {weapon[1]} (Количество снарядов: {weapon[2]})"
        else:
            weapon_result = f"{weapon[0]}, Урон: {weapon[1]}"
        return weapon_result
    
    def check_to_scroll(self, items, tir):
        while True:
            item = random.choice(items[tir])
            if item in ("СВИТОК", "СВЯЩЕННЫЙ СВИТОК") and "Неграмотный" in self.skills:
                continue
            elif item == "СВИТОК":
                chose_scroll_tir = random.choice(list(items["Scrolls"]))
                return random.choice(items["Scrolls"][chose_scroll_tir])
            elif item == "СВЯЩЕННЫЙ СВИТОК":
                return random.choice(items["Scrolls"]["Sacred_scroll"])
            else:
                return item

    def __str__(self):
        return f"{self.armor}"

def create_character():
    # Выбираем класс
    choosen_class = data["Classes"][random.choice(list(data["Classes"]))]
    
    # Копируем информацию о предметах
    all_items = data["Items"]

    # Копируем информацию о нарративе
    all_narrative = data["Character"] 

    # Создаем персонажа
    new_character = Character(choosen_class, all_items, all_narrative)
    return new_character

def create_json_character(character):
    data = {
        "Basic" : {
            "name" : character.name,
            "description" : character.description,
            "hp" : character.hp,
            "money" : character.money,
            "signs" : character.signs,
            "skills" : character.skills,
            "abilities" : {
                "agility" : character.agility,
                "presence" : character.presence,
                "strength" : character.strength,
                "toughness" : character.toughness
            },
            "bonus" : character.bonus
        },
        "Character" : {
            "terrible_trait" : character.terrible_trait,
            "injuries" : character.injuries,
            "bad_habbit" : character.bad_habbit,
            "dangerous_past" : character.dangerous_past,
            "secret_quest" : character.secret_quest,
            "memorie" : character.memorie
        },
        "Items" : {
            "armor" : character.armor,
            "weapon" : character.weapon,
            "first_item" : character.first_item,
            "second_item" : character.second_item,
            "third_item" : character.third_item,
        }
    }
    with open("character.json", "w", encoding="UTF-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

new_character = create_character()
create_json_character(new_character)