from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject, BooleanObject, TextStringObject, ArrayObject, FloatObject

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

page1 = writer.pages[0]
page2 = writer.pages[1]


def _normalize_rects(page):
    """Заменяет /Rect у аннотаций на прямые числа (вместо IndirectObject)."""
    for ref in page.get("/Annots", []):
        annot = ref.get_object()
        rect = annot.get("/Rect")
        if rect:
            def num(v):
                try:
                    v = v.get_object()
                except AttributeError:
                    pass
                return float(v)
            vals = [num(v) for v in rect]
            annot.update({NameObject("/Rect"): ArrayObject([FloatObject(v) for v in vals])})

def create_new_character_list(character):
    data1 = {
        "name" : character.name,
        "description" : character.description,
        "clas" : character.clas,
        "hp_current" : character.hp,
        "hp_max" : character.hp,
        "weapon_1" : character.weapon,
        "armor" : character.armor[0],
        f"armor_{character.armor[1]}" : "0",
        "item_1" : character.first_item,
        "item_2" : character.second_item,
        "item_3" : character.third_item,
        "strength" : character.strength,
        "agility" : character.agility,
        "presence" : character.presence,
        "toughness" : character.toughness,
        "money" : character.money,
        "signs" : character.signs,
    }
    data2 = {
        "terrible_trait" : character.terrible_trait,
        "injuries" : character.injuries,
        "bad_habbits" : character.bad_habbits,
        "dangerous_past" : character.dangerous_past,
        "secret_quest" : character.secret_quest,
        "memmories" : character.memories
    }
    x = 1
    for key, value in character.skills.items():
        data1[f"skill{x}"] = f"{key}: {value}"
        x += 1

    writer.update_page_form_field_values(page1, data1)

    _normalize_rects(page2)
    writer.update_page_form_field_values(page2, data2)

    with open(DST, "wb") as f:
        writer.write(f)
