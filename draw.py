"""Render the supplied news digest as a deterministic 1024 × 1024 PNG."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
FONTS = Path('/usr/share/fonts/truetype/dejavu')
STORIES = (
    ('DIPLOMACY', 'Xi, Trump and Putin meet in Shenzhen',
     "China's Xi Jinping welcomed US President Donald Trump to Shenzhen for a trilateral summit with Russia's Vladimir Putin, the three leaders' first three-way meeting.", '#6D929B'),
    ('MIDDLE EAST', 'Three tankers hit mines near Hormuz',
     "Three oil tankers caught fire after striking mines east of the Strait of Hormuz, Iran's Revolutionary Guard said, warning that passage through the waterway must be coordinated with Tehran.", '#A7806C'),
    ('ENTERTAINMENT', 'Grand Theft Auto VI launches worldwide',
     'Grand Theft Auto VI launched worldwide to near-perfect reviews, ending a 13-year wait since the last entry in the series set in Vice City.', '#9383A5'),
    ('JUSTICE', 'World Court rules on Rohingya genocide',
     'The International Court of Justice delivers its judgment today on whether Myanmar committed genocide against the Rohingya, a case followed by 1.2 million refugees in Bangladesh.', '#758C71'),
    ('CULTURE', 'Van Gogh sells for record $190.4m',
     "A Van Gogh painting sold for a record $190.4 million at auction, the most ever paid for the artist's work, after a dispute over its Nazi-era history.", '#A48D58'),
)


def font(size, bold=False):
    name = 'DejaVuSans-Bold.ttf' if bold else 'DejaVuSans.ttf'
    return ImageFont.truetype(str(FONTS / name), size)


def wrap(draw, text, face, width):
    lines = []
    line = ''
    for word in text.split():
        candidate = f'{line} {word}' if line else word
        if draw.textlength(candidate, font=face) > width:
            lines.append(line)
            line = word
        else:
            line = candidate
    if line:
        lines.append(line)
    return lines


def main():
    image = Image.new('RGB', (1024, 1024), '#F5F3EF')
    draw = ImageDraw.Draw(image)
    title_font = font(43, bold=True)
    tag_font = font(18, bold=True)
    headline_font = font(29, bold=True)
    body_font = font(22)
    footer_font = font(18)

    draw.rectangle((0, 0, 1023, 125), fill='#152739')
    title = 'THURSDAY 19 NOVEMBER 2026'
    assert draw.textlength(title, font=title_font) <= 944
    draw.text((40, 43), title, font=title_font, fill='white', anchor='lt')

    for index, (tag, headline, body, accent) in enumerate(STORIES):
        top = 146 + index * 163
        draw.rectangle((36, top, 41, top + 141), fill=accent)
        draw.text((60, top), tag, font=tag_font, fill=accent, anchor='lt')
        assert draw.textlength(headline, font=headline_font) <= 924
        draw.text((60, top + 27), headline, font=headline_font,
                  fill='#182A3B', anchor='lt')
        lines = wrap(draw, body, body_font, 924)
        assert len(lines) <= 3, f'Story body exceeds its block: {tag}'
        for line_index, line in enumerate(lines):
            draw.text((60, top + 67 + line_index * 27), line,
                      font=body_font, fill='#35424D', anchor='lt')
        if index < len(STORIES) - 1:
            draw.line((60, top + 151, 984, top + 151), fill='#DFDFDA')

    draw.line((36, 974, 988, 974), fill='#D7D9D8')
    draw.text((40, 989), 'Events of 19 November 2026, as reported.',
              font=footer_font, fill='#737A80', anchor='lt')
    image.save(ROOT / 'entry.png', format='PNG', optimize=False,
               compress_level=9)


if __name__ == '__main__':
    main()
