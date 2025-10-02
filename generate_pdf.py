from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject, BooleanObject, TextStringObject

SRC = "pdf_files/prepare_sheet.pdf"
DST = "pdf_files/new.pdf"

reader = PdfReader(SRC)
writer = PdfWriter()
writer.append(reader)

# чтобы значения гарантированно отрисовывались
if "/AcroForm" in writer._root_object:
    writer._root_object["/AcroForm"].update(
        {NameObject("/NeedAppearances"): BooleanObject(True)}
    )


page = writer.pages[0]

for ref in page.get("/Annots", []):
    annot = ref.get_object()
    if annot.get("/FT") == "/Tx":  # только текстовые поля
        annot.update({NameObject("/DA"): TextStringObject("/Helv 8 Tf 0 g")})
        annot.pop(NameObject("/AP"), None)  # удалить старый вид, чтобы перерисовалось

def create_new_character_list(character):
    data = {
        "name" : character.name,
        "description" : character.description,
        "clas" : character.clas,
        "hp_current" : character.hp,
        "hp_max" : character.hp,
        "weapon_1" : character.weapon,
        "armor" : character.armor[0],
        f"armor_{character.armor[1]}" : '/0',
        "item_1" : character.first_item,
        "item_2" : character.second_item,
        "item_3" : character.third_item,
        "strength" : character.strength,
        "agility" : character.agility,
        "presence" : character.presence,
        "toughness" : character.toughness,
        "money" : character.money,
        "signs" : character.signs,
        
        # Вторая страница
        "terrible_trait" : character.terrible_trait,
        "injuries" : character.injuries,
        "bad_habbits" : character.bad_habbits,
        "dangerous_past" : character.dangerous_past,
        "secret_quest" : character.secret_quest,
        "memmories" : character.memories
    }
    x = 1
    for key, value in character.skills.items():
        data[f"skill{x}"] = f"{key}: {value}"
        x += 1
    
    writer.update_page_form_field_values(page, data)

    with open(DST, "wb") as f:
        writer.write(f)
