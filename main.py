from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen
import time
import yaml

FONT_NAME = "squixels"
FONT_STYLE = "Regular"
FONT_VERSION = "Version 1.0"
FONT_MANUFACTURER = "SquareScreamYT"
FONT_DESIGNER = "SquareScreamYT" 
FONT_DESCRIPTION = "A Simple 5x7 Pixel Font"
FONT_URL = "https://sq.is-a.dev"
FONT_LICENSE = "CC BY-ND 4.0"
FONT_LICENSE_URL = "https://creativecommons.org/licenses/by-nd/4.0/"

INPUT_FILE = "C:/Users/KFX/Downloads/squixels.pxf"
OUTPUT_FILE = "C:/Users/KFX/Downloads/squixels.ttf"

with open(INPUT_FILE, 'r') as f:
    content = f.read().replace('\t', '    ')
    font_data = yaml.safe_load(content)

def create_pixel_font():
    fb = FontBuilder(1000, isTTF=True)
    
    fb.setupNameTable({
        "familyName": FONT_NAME,
        "styleName": FONT_STYLE,
        "uniqueFontIdentifier": f"{FONT_NAME}:{FONT_VERSION}",
        "fullName": f"{FONT_NAME} {FONT_STYLE}",
        "version": FONT_VERSION,
        "psName": FONT_NAME.replace(' ', ''),
        "manufacturer": FONT_MANUFACTURER,
        "designer": FONT_DESIGNER,
        "description": FONT_DESCRIPTION,
        "vendorURL": FONT_URL,
        "designerURL": FONT_URL,
        "licenseDescription": FONT_LICENSE,
        "licenseInfoURL": FONT_LICENSE_URL,
        "copyright": f"Copyright (c) 2024 {FONT_MANUFACTURER}"
    })

    current_time = int(time.time())
    fb.setupHead(created=current_time, modified=current_time, flags=0x000B, unitsPerEm=1000)

    glyphs = {'.notdef': TTGlyphPen(None).glyph()}

    for unicode_value, glyph_data in font_data['glyphs'].items():
        glyph_name = f'uni{int(unicode_value):04X}'
        pen = TTGlyphPen(None)
        
        pixels = []
        for pixel_group in glyph_data['pixels'].split(','):
            if pixel_group.strip():
                x, y = map(int, pixel_group.strip().split())
                pixels.append((x, y))
        
        for x, y in pixels:
            x_pos = x * 100
            if glyph_data['advance'] < 0:
                x_pos += abs(glyph_data['advance']) * 100
            
            pen.moveTo((x_pos, y * 100))
            pen.lineTo((x_pos + 100, y * 100))
            pen.lineTo((x_pos + 100, (y + 1) * 100))
            pen.lineTo((x_pos, (y + 1) * 100))
            pen.closePath()
        
        glyphs[glyph_name] = pen.glyph()

    glyph_order = ['.notdef'] + [f'uni{int(k):04X}' for k in font_data['glyphs'].keys()]
    fb.setupGlyphOrder(glyph_order)

    char_map = {int(k): f'uni{int(k):04X}' for k in font_data['glyphs'].keys()}
    fb.setupCharacterMap(char_map)

    fb.setupGlyf(glyphs)
    
    metrics = {'.notdef': (500, 25)}
    for unicode_value, glyph_data in font_data['glyphs'].items():
        glyph_name = f'uni{int(unicode_value):04X}'
        advance = glyph_data['advance'] * 100
        metrics[glyph_name] = (advance, 25)

    fb.setupHorizontalMetrics(metrics)
    
    fb.setupHorizontalHeader(ascent=900, descent=-200, lineGap=100)
    fb.setupOS2(sTypoAscender=900, sTypoDescender=-200, sTypoLineGap=100,
                usWinAscent=900, usWinDescent=200, fsSelection=0x40,
                sxHeight=500, sCapHeight=900)
    
    fb.setupPost()
    fb.save(OUTPUT_FILE)

create_pixel_font()
