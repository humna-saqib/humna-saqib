"""Generates dist/pulse.svg: pink stats panel with the contribution snake embedded. Runs daily in Actions."""
import base64, datetime, json, os, pathlib, urllib.request

USER = os.environ.get("GH_USER", "humna-saqib")
DIST = pathlib.Path("dist")
FONT = "'Segoe UI',Inter,Helvetica,Arial,sans-serif"

Q = """query($u:String!){user(login:$u){
 contributionsCollection{contributionCalendar{totalContributions weeks{contributionDays{date contributionCount}}}}
 repositories(ownerAffiliations:OWNER,isFork:false,privacy:PUBLIC,first:100){totalCount nodes{stargazerCount
  languages(first:10,orderBy:{field:SIZE,direction:DESC}){edges{size node{name color}}}}}}}"""


def fetch():
    req = urllib.request.Request("https://api.github.com/graphql",
                                 data=json.dumps({"query": Q, "variables": {"u": USER}}).encode(),
                                 headers={"Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}"})
    return json.load(urllib.request.urlopen(req))["data"]["user"]


def streaks(days):
    today = datetime.date.today().isoformat()
    longest = run = 0
    for d in days:
        run = run + 1 if d["contributionCount"] else 0
        longest = max(longest, run)
    current = 0
    for d in reversed(days):
        if d["contributionCount"]:
            current += 1
        elif d["date"] != today:
            break
    return current, longest


def main():
    u = fetch()
    cal = u["contributionsCollection"]["contributionCalendar"]
    days = [d for w in cal["weeks"] for d in w["contributionDays"]]
    cur, best = streaks(days)
    repos = u["repositories"]
    stars = sum(r["stargazerCount"] for r in repos["nodes"])
    langs = {}
    for r in repos["nodes"]:
        for e in r["languages"]["edges"]:
            n = e["node"]["name"]
            langs.setdefault(n, [0, e["node"]["color"] or "#f472b6"])[0] += e["size"]
    top = sorted(langs.items(), key=lambda kv: -kv[1][0])[:6]
    total = sum(v[0] for _, v in top) or 1

    w = 1000
    tiles = [(cal["totalContributions"], "CONTRIBUTIONS", "last 12 months"),
             (cur, "CURRENT STREAK", "days in a row"),
             (best, "LONGEST STREAK", "days"),
             (repos["totalCount"], "PUBLIC PROJECTS", f"{stars} stars")]
    tile_svg = ""
    for i, (v, k, sub) in enumerate(tiles):
        x = 40 + i * 235
        tile_svg += f"""<g><rect x="{x}" y="86" width="215" height="112" rx="14" fill="#fff" fill-opacity=".04" stroke="#f472b6" stroke-opacity=".18"/>
<text x="{x + 22}" y="140" class="v">{v}</text><text x="{x + 22}" y="164" class="k">{k}</text><text x="{x + 22}" y="183" class="s">{sub}</text></g>"""

    bar, legend, x = "", "", 40.0
    for i, (n, (size, color)) in enumerate(top):
        bw = 920 * size / total
        bar += f'<rect x="{x:.1f}" y="262" width="{max(bw, 2):.1f}" height="10" fill="{color}"/>'
        x += bw
        lx, ly = 40 + (i % 3) * 310, 302 + (i // 3) * 26
        legend += f'<circle cx="{lx + 5}" cy="{ly - 4}" r="5" fill="{color}"/><text x="{lx + 18}" y="{ly}" class="l">{n} <tspan class="s">{100 * size / total:.1f}%</tspan></text>'

    snake = (DIST / "snake-dark.svg").read_bytes()
    snake_uri = "data:image/svg+xml;base64," + base64.b64encode(snake).decode()
    h = 590
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#2a0b20"/><stop offset=".55" stop-color="#1c0716"/><stop offset="1" stop-color="#14060f"/></linearGradient>
<linearGradient id="edge" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f9a8d4" stop-opacity=".55"/><stop offset=".5" stop-color="#f472b6" stop-opacity=".12"/><stop offset="1" stop-color="#f9a8d4" stop-opacity=".4"/></linearGradient>
<radialGradient id="glow"><stop offset="0" stop-color="#ec4899" stop-opacity=".3"/><stop offset="1" stop-color="#ec4899" stop-opacity="0"/></radialGradient>
<linearGradient id="sh" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".07"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<clipPath id="c"><rect width="{w}" height="{h}" rx="22"/></clipPath><clipPath id="bc"><rect x="40" y="262" width="920" height="10" rx="5"/></clipPath></defs>
<style>.t{{font:700 12px Consolas,monospace;fill:#f472b6;letter-spacing:2.5px}}.v{{font:800 34px {FONT};fill:#fdf2f8}}
.k{{font:700 11px Consolas,monospace;fill:#f9a8d4;letter-spacing:1.5px}}.s{{font:400 12.5px {FONT};fill:#b993a8}}.l{{font:500 14px {FONT};fill:#ecd5e1}}</style>
<g clip-path="url(#c)"><rect width="{w}" height="{h}" fill="url(#bg)"/><circle cx="900" cy="40" r="300" fill="url(#glow)"/><circle cx="80" cy="560" r="260" fill="url(#glow)"/></g>
<rect x=".75" y=".75" width="{w - 1.5}" height="{h - 1.5}" rx="21.5" fill="none" stroke="url(#edge)" stroke-width="1.5"/>
<text x="40" y="58" class="t">GITHUB PULSE</text>
{tile_svg}
<text x="40" y="244" class="t">TOP LANGUAGES</text>
<g clip-path="url(#bc)">{bar}</g>{legend}
<text x="40" y="386" class="t">CONTRIBUTION GRAPH</text>
<image href="{snake_uri}" x="40" y="400" width="920" height="170"/>
<g clip-path="url(#c)"><rect x="-1000" y="0" width="330" height="{h}" fill="url(#sh)" transform="skewX(-20)"><animate attributeName="x" values="-1000;1600" dur="7s" repeatCount="indefinite"/></rect></g>
</svg>"""
    (DIST / "pulse.svg").write_text(svg, encoding="utf-8")


main()
