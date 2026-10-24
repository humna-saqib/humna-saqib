"""Builds the static pink panels (about + focus) and adds a light sheen to every asset."""
import base64, re, urllib.request, pathlib

A = pathlib.Path(__file__).resolve().parents[2] / "assets"
ICONS = ["python", "fastapi", "django", "pytorch", "tensorflow", "sklearn",
         "js", "ts", "mysql", "git", "docker", "linux"]

DEFS = """<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#2a0b20"/><stop offset=".55" stop-color="#1c0716"/><stop offset="1" stop-color="#14060f"/></linearGradient>
<linearGradient id="edge" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f9a8d4" stop-opacity=".55"/><stop offset=".5" stop-color="#f472b6" stop-opacity=".12"/><stop offset="1" stop-color="#f9a8d4" stop-opacity=".4"/></linearGradient>
<radialGradient id="glow"><stop offset="0" stop-color="#ec4899" stop-opacity=".35"/><stop offset="1" stop-color="#ec4899" stop-opacity="0"/></radialGradient>"""

FONT = "'Segoe UI',Inter,Helvetica,Arial,sans-serif"


def sheen(w, h, rx, uid):
    return f"""<defs><linearGradient id="sh{uid}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".09"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient><clipPath id="sc{uid}"><rect width="{w}" height="{h}" rx="{rx}"/></clipPath></defs>
<g clip-path="url(#sc{uid})"><rect x="-{w}" y="0" width="{w // 3}" height="{h}" fill="url(#sh{uid})" transform="skewX(-20)"><animate attributeName="x" values="-{w};{w * 1.6:.0f}" dur="6s" repeatCount="indefinite"/></rect>
<rect width="{w}" height="{h * .5:.0f}" fill="#fff" fill-opacity=".025"/></g>"""


def icon(name):
    req = urllib.request.Request(f"https://skillicons.dev/icons?i={name}", headers={"User-Agent": "Mozilla/5.0"})
    svg = urllib.request.urlopen(req).read()
    return "data:image/svg+xml;base64," + base64.b64encode(svg).decode()


def about():
    w, h = 1000, 250
    tiles = []
    for i, n in enumerate(ICONS):
        x, y = 560 + (i % 6) * 68, 52 + (i // 6) * 76
        d = .15 + i * .06
        tiles.append(f'<g class="ic" style="animation-delay:{d:.2f}s"><image href="{icon(n)}" x="{x}" y="{y}" width="56" height="56"/></g>')
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
<defs>{DEFS}</defs>
<style>.k{{font:700 12px Consolas,monospace;fill:#f472b6;letter-spacing:2.5px}}.h{{font:800 30px {FONT};fill:#fdf2f8;letter-spacing:-.5px}}.b{{font:400 15px {FONT};fill:#e9c9da}}.s{{font:700 15px {FONT};fill:#f9a8d4}}
.ic{{opacity:0;animation:in .6s ease forwards}}@keyframes in{{to{{opacity:1}}}}</style>
<rect width="{w}" height="{h}" rx="22" fill="url(#bg)"/>
<circle cx="120" cy="10" r="230" fill="url(#glow)"/>
<rect x=".75" y=".75" width="{w - 1.5}" height="{h - 1.5}" rx="21.5" fill="none" stroke="url(#edge)" stroke-width="1.5"/>
<text x="48" y="62" class="k">ABOUT ME</text>
<text x="48" y="104" class="h">I build AI systems that ship.</text>
<text x="48" y="140" class="b">Reinforcement-learning agents, transformer NLP and</text>
<text x="48" y="162" class="b">LLM-powered apps — wrapped in clean, production-grade</text>
<text x="48" y="184" class="b"><tspan class="s">Django / FastAPI</tspan> backends.</text>
<text x="48" y="214" class="s" style="font:600 13px Consolas,monospace">data → model → API → product</text>
<line x1="525" y1="44" x2="525" y2="206" stroke="#f472b6" stroke-opacity=".18"/>
{''.join(tiles)}
{sheen(w, h, 22, 'a')}
</svg>"""


def focus():
    cards = [("AI / ML", "Intelligent systems", ["Reinforcement learning, transformer", "NLP and LLM agents, from research", "idea to a model that works."]),
             ("BACKEND", "Production APIs", ["Django and FastAPI services with", "clean architecture, built to serve", "models reliably at scale."]),
             ("QUALITY", "Tested &amp; maintainable", ["End-to-end automation with", "Playwright and a strong grounding", "in data structures &amp; algorithms."])]
    out = []
    for i, (k, t, lines) in enumerate(cards):
        body = "".join(f'<text x="26" y="{120 + j * 20}" class="b">{l}</text>' for j, l in enumerate(lines))
        out.append(f"""<g transform="translate({i * 340},0)"><g class="c" style="animation-delay:{i * .2:.1f}s">
<rect width="320" height="200" rx="18" fill="url(#bg)"/><circle cx="300" cy="0" r="150" fill="url(#glow)"/>
<rect x=".75" y=".75" width="318.5" height="198.5" rx="17.5" fill="none" stroke="url(#edge)" stroke-width="1.5"/>
<text x="26" y="44" class="n">0{i + 1}</text><text x="56" y="44" class="n">{k}</text>
<rect x="26" y="58" width="36" height="3" rx="1.5" fill="#f472b6"/>
<text x="26" y="94" class="h">{t}</text>{body}{sheen(320, 200, 18, f'f{i}')}</g></g>""")
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="200" viewBox="0 0 1000 200">
<defs>{DEFS}</defs>
<style>.n{{font:700 12px Consolas,monospace;fill:#f472b6;letter-spacing:2px}}.h{{font:700 21px {FONT};fill:#fdf2f8}}.b{{font:400 14px {FONT};fill:#d9b8c9}}
.c{{opacity:0;animation:in .7s ease forwards}}@keyframes in{{to{{opacity:1}}}}</style>
{''.join(out)}
</svg>"""


def add_sheen(name, w, h, rx):
    p = A / name
    s = re.sub(r"<!--sheen-->.*?<!--/sheen-->", "", p.read_text(encoding="utf-8"), flags=re.S)
    s = s.replace("</svg>", f"<!--sheen-->{sheen(w, h, rx, name[:2])}<!--/sheen-->\n</svg>")
    p.write_text(s, encoding="utf-8")


(A / "about.svg").write_text(about(), encoding="utf-8")
(A / "focus.svg").write_text(focus(), encoding="utf-8")
add_sheen("hero.svg", 1000, 340, 24)
for c in ("intelliroads.svg", "email.svg", "ner.svg"):
    add_sheen(c, 320, 200, 16)
