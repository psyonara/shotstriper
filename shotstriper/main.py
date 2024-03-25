import aggdraw
import random
from pathlib import Path
from rich import print

import typer
from PIL import Image, ImageDraw, ImageFilter, ImageGrab
from typing_extensions import Annotated

from shotstriper.palettes import PALETTES

app = typer.Typer()


def chunk(lst: list, size: int):
    for i in range(0, len(lst), size):
        yield lst[i:i + size]


def get_palettes(category_name=None):
    if category_name and category_name.lower() not in PALETTES:
        raise ValueError("Category not found.")

    for category, palettes in PALETTES.items():
        if category_name and category.lower() != category_name.lower():
            continue

        for name, colors in palettes.items():
            yield name, colors


def get_palette(palette_name: str):
    category, name = palette_name.split(".")
    if not (isinstance(category, str) and isinstance(name, str)):
        raise ValueError("Please specify a category and name, e.g. 'neon.excited-surround'.")

    if category.lower() not in PALETTES:
        raise ValueError("Category not found.")

    category_set = PALETTES[category]
    if name.lower() not in category_set:
        raise ValueError("Palette not found.")

    return category_set[name]


def get_palette_string(name, colors):
    color_string = "".join([f"[on {color}]    [/]" for color in colors])
    return f"{color_string} {name}"


@app.command()
def browse_palettes(category=None):
    row = 0
    print()
    for palettes in chunk(list(get_palettes(category)), 3):
        for n in range(4):
            colors = [c[n] for name, c in palettes]
            for color in colors:
                print(f"[on {color}]            [/]", end="")
                print("            ", end="")
            print()
        for name, _ in palettes:
            name_padding = " " * (24-len(name))
            print(f"{name}{name_padding}", end="")
        print()
        print()
        row += 1
        if row >= 6:
            typer.confirm("View more?", True, abort=True)
            row = 0


@app.command()
def add_background(
    path: Annotated[Path, typer.Argument()] = None,
    from_clipboard: Annotated[bool, typer.Option()] = False,
    palette_name: Annotated[str, typer.Option(prompt="Which color palette would you like to use")] = "",
):
    if path:
        if path.is_file():
            src_img = Image.open(path)
        else:
            raise ValueError("No valid file path was specified.")
    elif from_clipboard:
        try:
            src_img = ImageGrab.grabclipboard()
        except Exception as e:
            raise ValueError(f"Could not grab image from clipboard: {e}")
    else:
        raise ValueError("Please specify either 'path' or 'from_clipboard.")

    # src_img = Image.open(f)
    src_img = src_img.convert("RGBA")
    width = src_img.width
    height = src_img.height

    padding = int(width * 0.1)
    new_width = width + 2 * padding
    new_height = height + 2 * padding

    new_img = Image.new("RGBA", (new_width, new_height), (255, 255, 255))

    draw = aggdraw.Draw(new_img)

    palette = get_palette(palette_name)
    min_width, max_width = int(width * 0.05), int(width * 0.1)
    color_index = 0

    x2_ref = 0
    x1_ref = x2_ref - (new_height * 0.67)

    while x1_ref < new_width:
        stripe_width = random.randint(min_width, max_width)
        if stripe_width % 2 != 0:
            stripe_width += 1

        x1 = x1_ref
        y1 = -1 * stripe_width/2

        x2 = x2_ref + stripe_width
        y2 = new_height + stripe_width/2

        pen = aggdraw.Pen(palette[color_index], stripe_width)
        draw.line((x1, y1, x2, y2), pen)

        x1_ref += stripe_width
        x2_ref += stripe_width

        color_index += 1
        if color_index >= len(palette):
            color_index = 0

    draw.flush()

    # drop shadow
    overlay = Image.new("RGBA", new_img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    draw.rectangle(((padding, padding), (padding + width, padding + height)), fill=(0, 0, 0, 200))
    for _ in range(3):
        overlay = overlay.filter(ImageFilter.GaussianBlur(20))
    new_img = Image.alpha_composite(new_img, overlay)

    # paste source image over new image
    new_img.paste(src_img, (padding, padding), src_img)

    new_img = new_img.convert("RGB")
    new_img.save("new.jpg", quality=95)
