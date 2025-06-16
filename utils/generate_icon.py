from PIL import Image, ImageDraw

def generate_3d_pen_letter_icon(path="icon.ico", size=64):
    img = Image.new("RGBA", (size, size), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)

    shadow_color = (30, 30, 60, 180)        # Dark blue shadow (semi-transparent)
    letter_color = (70, 70, 110, 255)       # Main bright blue
    highlight_color = (150, 150, 200, 255)  # Light highlight for bevel

    pen_color = (50, 50, 50, 255)
    pen_highlight = (140, 140, 170, 180)

    # Shadow offset (for 3D depth)
    offset = 2

    # Draw "F" shadow (offset down-right)
    # Vertical bar shadow
    draw.line([(size*0.3 + offset, size*0.2 + offset), (size*0.3 + offset, size*0.75 + offset)], fill=shadow_color, width=6)
    # Top horizontal bar shadow
    draw.line([(size*0.3 + offset, size*0.2 + offset), (size*0.65 + offset, size*0.2 + offset)], fill=shadow_color, width=6)
    # Middle horizontal bar shadow
    draw.line([(size*0.3 + offset, size*0.45 + offset), (size*0.55 + offset, size*0.45 + offset)], fill=shadow_color, width=6)

    # Draw main "F"
    draw.line([(size*0.3, size*0.2), (size*0.3, size*0.75)], fill=letter_color, width=6)
    draw.line([(size*0.3, size*0.2), (size*0.65, size*0.2)], fill=letter_color, width=6)
    draw.line([(size*0.3, size*0.45), (size*0.55, size*0.45)], fill=letter_color, width=6)

    # Add highlight
    draw.line([(size*0.3 + 1, size*0.2), (size*0.3 + 1, size*0.75)], fill=highlight_color, width=2)
    draw.line([(size*0.3, size*0.2 + 1), (size*0.65, size*0.2 + 1)], fill=highlight_color, width=2)
    draw.line([(size*0.3, size*0.45 + 1), (size*0.55, size*0.45 + 1)], fill=highlight_color, width=2)

    # Draw ink pen
    nib_base = size * 0.75
    draw.polygon([
        (size*0.48, nib_base),
        (size*0.52, nib_base),
        (size*0.55, size*0.85),
        (size*0.45, size*0.85)
    ], fill=pen_color)

    draw.rectangle([size*0.47, size*0.6, size*0.53, nib_base], fill=pen_color)

    draw.line([(size*0.5, size*0.85), (size*0.5, size*0.9)], fill=pen_color, width=2)

    # Highlights on pen shaft
    draw.line([(size*0.48, size*0.6), (size*0.48, nib_base)], fill=pen_highlight, width=2)

    img.save(path, format="ICO")

generate_3d_pen_letter_icon()
