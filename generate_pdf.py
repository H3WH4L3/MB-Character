from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject, BooleanObject, TextStringObject

SRC = "character_sheet.pdf"
DST = "new.pdf"

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
        "Text1" : character.name,
        "Text2" : character.description,
        "Text3" : character.clas,
        "Text8" : character.hp,
        "Text9" : character.hp,
        "Text10" : character.weapon,
        "Text12" : character.armor[0],
        f"Check Box{34 + character.armor[1]}" : '/0',
        "Text13" : character.first_item,
        "Text14" : character.second_item,
        "Text15" : character.third_item,
        "Text29" : character.strength,
        "Text30" : character.agility,
        "Text31" : character.presence,
        "Text32" : character.toughness,
        "Money" : character.money,
        "Omen" : character.signs
    }
    x = 4
    for key, value in character.skills.items():
        data[f"Text{x}"] = f"{key}: {value}"
        x += 1
    
    writer.update_page_form_field_values(page, data)

    with open(DST, "wb") as f:
        writer.write(f)
