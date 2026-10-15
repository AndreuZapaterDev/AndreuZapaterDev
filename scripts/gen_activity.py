"""Genera la tarjeta de actividad de GitHub (ES/EN) con el estilo del perfil.

Uso:
  GITHUB_TOKEN=... USERNAME=AndreuZapaterDev python scripts/gen_activity.py <carpeta_salida>
  python scripts/gen_activity.py <carpeta_salida> --demo   # datos de ejemplo, sin token

Lo ejecuta .github/workflows/profile-assets.yml cada día y publica el resultado
en la rama `output`.
"""
import datetime as dt
import json
import os
import random
import sys
import urllib.request
from xml.sax.saxutils import escape

OUT = sys.argv[1]
DEMO = "--demo" in sys.argv
os.makedirs(OUT, exist_ok=True)

BG = "#0a0f0a"
COLOR = "#14b8a6"
LEVELS = ["#151c17", "#134e4a", "#0f766e", "#14b8a6", "#5eead4"]
SANS = "'Segoe UI', -apple-system, BlinkMacSystemFont, 'Helvetica Neue', Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Consolas, 'Liberation Mono', Menlo, monospace"

QUERY = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount } }
      }
    }
    repositories(ownerAffiliations: OWNER, isFork: false, privacy: PUBLIC, first: 100) {
      totalCount
      nodes {
        languages(first: 10, orderBy: {field: SIZE, direction: DESC}) {
          edges { size node { name color } }
        }
      }
    }
  }
}
"""


def fetch(login, token):
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": login}}).encode(),
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.load(r)
    if "errors" in data:
        raise SystemExit(f"GraphQL: {data['errors']}")
    u = data["data"]["user"]
    cal = u["contributionsCollection"]["contributionCalendar"]
    days = [(d["date"], d["contributionCount"]) for w in cal["weeks"] for d in w["contributionDays"]]
    langs = {}
    for repo in u["repositories"]["nodes"]:
        for e in repo["languages"]["edges"]:
            name = e["node"]["name"]
            size, color = langs.get(name, (0, e["node"]["color"]))
            langs[name] = (size + e["size"], color or "#737373")
    return days, cal["totalContributions"], u["repositories"]["totalCount"], langs


def demo():
    random.seed(7)
    today = dt.date.today()
    start = today - dt.timedelta(days=364 + (today.weekday() + 1) % 7)
    days = []
    for i in range((today - start).days + 1):
        d = start + dt.timedelta(days=i)
        n = 0 if random.random() < .35 else random.choice([1, 2, 3, 4, 6, 9, 12])
        days.append((d.isoformat(), n))
    langs = {"TypeScript": (52000, "#3178c6"), "PHP": (41000, "#4F5D95"), "JavaScript": (23000, "#f1e05a"),
             "Blade": (9000, "#f7523f"), "CSS": (7000, "#563d7c"), "HTML": (4000, "#e34c26")}
    return days, sum(n for _, n in days), 12, langs


def streaks(days):
    counts = [n for _, n in days]
    longest = cur = 0
    for n in counts:
        cur = cur + 1 if n > 0 else 0
        longest = max(longest, cur)
    # Racha actual: si hoy aún no hay contribuciones, se cuenta desde ayer
    i = len(counts) - 1
    if counts and counts[i] == 0:
        i -= 1
    current = 0
    while i >= 0 and counts[i] > 0:
        current += 1
        i -= 1
    return current, longest


def level(n, mx):
    if n == 0:
        return 0
    q = n / mx
    return 1 if q <= .25 else 2 if q <= .5 else 3 if q <= .75 else 4


T = {
    "es": {"total": "contribuciones · último año", "cur": "días · racha actual", "long": "días · racha más larga",
           "repos": "repositorios públicos", "less": "Menos", "more": "Más", "langs": "LENGUAJES MÁS USADOS",
           "months": "Ene Feb Mar Abr May Jun Jul Ago Sep Oct Nov Dic".split(), "dows": ["Lun", "Mié", "Vie"],
           "other": "Otros", "label": "Actividad en GitHub"},
    "en": {"total": "contributions · last year", "cur": "days · current streak", "long": "days · longest streak",
           "repos": "public repositories", "less": "Less", "more": "More", "langs": "MOST USED LANGUAGES",
           "months": "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split(), "dows": ["Mon", "Wed", "Fri"],
           "other": "Other", "label": "GitHub activity"},
}


def render(lang, days, total, repos, langs):
    t = T[lang]
    W, H = 1200, 470
    cur, longest = streaks(days)
    out = [
        f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="18" fill="{BG}" stroke="{COLOR}" stroke-opacity=".3"/>',
        f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="18" fill="url(#ag)"/>',
    ]
    # Cifras
    tw = (1120 - 3 * 16) / 4
    for i, (num, lab) in enumerate([(f"{total:,}".replace(",", "."), t["total"]), (cur, t["cur"]),
                                    (longest, t["long"]), (repos, t["repos"])]):
        x = 40 + i * (tw + 16)
        out.append(
            f'<rect x="{x:.0f}" y="32" width="{tw:.0f}" height="84" rx="12" fill="#111811" stroke="#ffffff" stroke-opacity=".07"/>'
            f'<text x="{x + 20:.0f}" y="76" font-family="{SANS}" font-size="32" font-weight="800" fill="{COLOR}">{num}</text>'
            f'<text x="{x + 20:.0f}" y="100" font-family="{SANS}" font-size="13" fill="#a3a3a3">{escape(lab)}</text>')
    # Mapa de contribuciones (semanas en columnas, domingo arriba como en GitHub)
    first = dt.date.fromisoformat(days[0][0])
    offset = (first.weekday() + 1) % 7
    mx = max((n for _, n in days), default=1) or 1
    gx, gy, cell, gap = 80, 172, 16, 4
    last_month = None
    for idx, (date, n) in enumerate(days):
        pos = idx + offset
        col, row = pos // 7, pos % 7
        x, y = gx + col * (cell + gap), gy + row * (cell + gap)
        d = dt.date.fromisoformat(date)
        if row == 0 or idx == 0:
            if d.month != last_month and d.day <= 7:
                out.append(f'<text x="{x}" y="{gy - 12}" font-family="{SANS}" font-size="12" fill="#737373">{t["months"][d.month - 1]}</text>')
                last_month = d.month
        out.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="4" fill="{LEVELS[level(n, mx)]}">'
                   f'<title>{date}: {n}</title></rect>')
    for i, name in zip((1, 3, 5), t["dows"]):
        out.append(f'<text x="{gx - 12}" y="{gy + i * (cell + gap) + 12}" text-anchor="end" font-family="{SANS}" font-size="12" fill="#737373">{name}</text>')
    # Leyenda
    ly = gy + 7 * (cell + gap) + 14
    lx = 1160 - 5 * (cell - 2 + 4) - 40
    out.append(f'<text x="{lx - 10}" y="{ly + 12}" text-anchor="end" font-family="{SANS}" font-size="12" fill="#737373">{t["less"]}</text>')
    for i, c in enumerate(LEVELS):
        out.append(f'<rect x="{lx + i * 18}" y="{ly}" width="14" height="14" rx="3" fill="{c}"/>')
    out.append(f'<text x="{lx + 5 * 18 + 6}" y="{ly + 12}" font-family="{SANS}" font-size="12" fill="#737373">{t["more"]}</text>')
    # Lenguajes
    by = H - 78
    out.append(f'<text x="40" y="{by - 14}" font-family="{MONO}" font-size="12" font-weight="700" letter-spacing="2" fill="{COLOR}">{t["langs"]}</text>')
    items = sorted(langs.items(), key=lambda kv: -kv[1][0])
    top, rest = items[:5], sum(v[0] for _, v in items[5:])
    if rest:
        top.append((t["other"], (rest, "#525252")))
    tot = sum(v[0] for _, v in top) or 1
    bx = 40
    segs = []
    for name, (size, c) in top:
        w = 1120 * size / tot
        segs.append(f'<rect x="{bx:.1f}" y="{by}" width="{w:.1f}" height="12" fill="{c}"/>')
        bx += w
    out.append(f'<clipPath id="pill"><rect x="40" y="{by}" width="1120" height="12" rx="6"/></clipPath>'
               f'<g clip-path="url(#pill)">{"".join(segs)}</g>')
    lx = 40
    for name, (size, c) in top:
        label = f"{name} {100 * size / tot:.1f}%"
        out.append(f'<circle cx="{lx + 5}" cy="{by + 37}" r="5" fill="{c}"/>'
                   f'<text x="{lx + 16}" y="{by + 42}" font-family="{SANS}" font-size="13" fill="#d4d4d4">{escape(name)} '
                   f'<tspan fill="#737373">{100 * size / tot:.1f}%</tspan></text>')
        lx += 16 + len(label) * 6.8 + 22
    desc = f'{t["label"]}: {total} {t["total"]}, {cur} {t["cur"]}, {longest} {t["long"]}, {repos} {t["repos"]}'
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{escape(desc)}">'
            f'<defs><radialGradient id="ag" cx="1" cy="0" r=".8"><stop offset="0" stop-color="{COLOR}" stop-opacity=".12"/>'
            f'<stop offset="1" stop-color="{COLOR}" stop-opacity="0"/></radialGradient></defs>'
            + "".join(out) + '</svg>\n')


if DEMO:
    data = demo()
else:
    data = fetch(os.environ["USERNAME"], os.environ["GITHUB_TOKEN"])

for lang in ("es", "en"):
    with open(os.path.join(OUT, f"activity-{lang}.svg"), "w", encoding="utf-8", newline="\n") as f:
        f.write(render(lang, *data))
print("ok")
