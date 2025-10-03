import json
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape
from playwright.sync_api import sync_playwright
import math

ROOT = Path(__file__).parent
DATA = ROOT / "data" / "character.json"
TPL_DIR = ROOT / "templates"
OUT_DIR = ROOT / "out"

def deep_defaults(src: dict) -> dict:
    """Безопасно подмешиваем дефолты под твою схему."""
    defaults = {
        "Basic": {
            "name": "",
            "description": "",
            "hp": 0,
            "money": 0,
            "signs": 0,
            "skills": {},  # dict: name -> text
            "abilities": {
                "agility": 10,
                "presence": 10,
                "strength": 10,
                "toughness": 10,
            },
            "bonus": "",
        },
        "Character": {
            "terrible_trait": "",
            "injuries": "",
            "bad_habbit": "",
            "dangerous_past": "",
            "secret_quest": "",
            "memorie": "",
        },
        "Items": {
            "armor": ["", 0],  # [название, класс/бонус]
            "weapon": "",
            "first_item": "",
            "second_item": "",
            "third_item": "",
        },
    }

    def merge(a, b):
        out = dict(a)
        for k, v in b.items():
            if isinstance(v, dict) and isinstance(out.get(k), dict):
                out[k] = merge(out[k], v)
            else:
                out[k] = v
        return out

    return merge(defaults, src or {})

def ability_mod(score: int) -> int:
    """Если хочешь показывать модификатор из значения (как в MB): округлим вниз по DnD-логике."""
    try:
        return (int(score) - 10) // 2
    except Exception:
        return 0

def build_context(raw: dict) -> dict:
    ctx = deep_defaults(raw)

    # Посчитаем модификаторы отдельно (если пригодится на листе)
    abscores = ctx["Basic"]["abilities"]
    ctx["mods"] = {
        "agility": ability_mod(abscores.get("agility", 10)),
        "presence": ability_mod(abscores.get("presence", 10)),
        "strength": ability_mod(abscores.get("strength", 10)),
        "toughness": ability_mod(abscores.get("toughness", 10)),
    }
    return ctx

def render_html(context: dict) -> Path:
    env = Environment(
        loader=FileSystemLoader(str(TPL_DIR)),
        autoescape=select_autoescape(["html"])
    )
    tpl = env.get_template("sheet.html")

    css_uri = (TPL_DIR / "styles.css").as_uri()
    bg_uri = (ROOT / "assets" / "bg.jpg").as_uri()  # фон (замени при необходимости)

    html = tpl.render(**context, css_uri=css_uri, bg_uri=bg_uri)

    OUT_DIR.mkdir(exist_ok=True)
    out_html = OUT_DIR / "character.html"
    out_html.write_text(html, encoding="utf-8")
    return out_html

def make_png(html_path: Path, width=1240, height=1754) -> Path:
    out_png = OUT_DIR / "character.png"
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(html_path.as_uri(), wait_until="load")
        page.set_viewport_size({"width": width, "height": height})
        page.locator("#sheet").screenshot(path=str(out_png))
        browser.close()
    return out_png

def main():
    raw = json.loads(DATA.read_text(encoding="utf-8"))
    context = build_context(raw)
    html_path = render_html(context)
    png_path = make_png(html_path)
    print(f"✔ HTML: {html_path}")
    print(f"✔ PNG:  {png_path}")

if __name__ == "__main__":
    main()
