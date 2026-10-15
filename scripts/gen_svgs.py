"""Genera los SVG del perfil: cabecera, barras de sección y pie (ES/EN)."""
import os
import sys
from xml.sax.saxutils import escape

OUT = sys.argv[1]
os.makedirs(os.path.join(OUT, "sections"), exist_ok=True)

BG = "#0a0f0a"
LIME = "#84cc16"
SANS = "'Segoe UI', -apple-system, BlinkMacSystemFont, 'Helvetica Neue', Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Consolas, 'Liberation Mono', Menlo, monospace"

# Iconos de línea 24x24 (estilo Lucide)
ICONS = {
    "user": '<circle cx="12" cy="8" r="4"/><path d="M4 21v-1a6 6 0 0 1 6-6h4a6 6 0 0 1 6 6v1"/>',
    "briefcase": '<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M8 7V5a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2M3 13h18"/>',
    "code": '<path d="M16 18l6-6-6-6M8 6l-6 6 6 6"/>',
    "rocket": '<path d="M4.5 16.5c-1.5 1.3-2 5-2 5s3.7-.5 5-2c.7-.8.7-2.1-.1-2.9a2.2 2.2 0 0 0-2.9-.1z"/><path d="M12 15l-3-3a22 22 0 0 1 2-3.9A12.9 12.9 0 0 1 22 2c0 2.7-.8 7.5-6 11a22.4 22.4 0 0 1-4 2z"/><path d="M9 12H4s.6-3 2-4c1.6-1.1 5 0 5 0M12 15v5s3-.6 4-2c1.1-1.6 0-5 0-5"/>',
    "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/>',
    "award": '<circle cx="12" cy="9" r="6"/><path d="M8.5 14 7 22l5-3 5 3-1.5-8"/>',
    "activity": '<path d="M22 12h-4l-3 9L9 3l-3 9H2"/>',
}

SECTIONS = [
    ("01", "user", "#a3e635", "Sobre mí", "About me"),
    ("02", "briefcase", "#84cc16", "Trayectoria", "Experience"),
    ("03", "code", "#4ade80", "Stack tecnológico", "Tech stack"),
    ("04", "rocket", "#22c55e", "Proyectos destacados", "Featured projects"),
    ("05", "globe", "#10b981", "Idiomas", "Languages"),
    ("06", "award", "#14b8a6", "Certificaciones", "Certifications"),
    ("07", "activity", "#0d9488", "Actividad en GitHub", "GitHub activity"),
]


def write(path, content):
    with open(os.path.join(OUT, path), "w", encoding="utf-8", newline="\n") as f:
        f.write(content)


# ---------------------------------------------------------------- secciones
def section(num, icon, color, title):
    t = escape(title)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="72" viewBox="0 0 1200 72" role="img" aria-label="{num} — {t}">
  <defs>
    <linearGradient id="g" x1="0" x2="1">
      <stop offset="0" stop-color="{color}" stop-opacity=".22"/>
      <stop offset=".55" stop-color="{color}" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="l" x1="0" x2="1">
      <stop offset="0" stop-color="{color}" stop-opacity="0"/>
      <stop offset="1" stop-color="{color}" stop-opacity=".7"/>
    </linearGradient>
  </defs>
  <rect x=".5" y=".5" width="1199" height="71" rx="14" fill="{BG}" stroke="{color}" stroke-opacity=".35"/>
  <rect x=".5" y=".5" width="1199" height="71" rx="14" fill="url(#g)"/>
  <rect x="18" y="16" width="40" height="40" rx="10" fill="{color}" fill-opacity=".14" stroke="{color}" stroke-opacity=".4"/>
  <g transform="translate(26 24)" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{ICONS[icon]}</g>
  <text x="76" y="44" font-family="{MONO}" font-size="16" font-weight="600" fill="{color}">{num}</text>
  <text x="102" y="44" font-family="{MONO}" font-size="16" fill="#525252">/</text>
  <text x="120" y="45" font-family="{SANS}" font-size="22" font-weight="700" fill="#ffffff">{t}</text>
  <rect x="860" y="35" width="270" height="2" rx="1" fill="url(#l)"/>
  <circle cx="1146" cy="36" r="4" fill="{color}">
    <animate attributeName="opacity" values="1;.35;1" dur="2.4s" repeatCount="indefinite"/>
  </circle>
  <circle cx="1166" cy="36" r="4" fill="{color}" fill-opacity=".55"/>
  <circle cx="1182" cy="36" r="4" fill="{color}" fill-opacity=".25"/>
</svg>
'''


for num, icon, color, es, en in SECTIONS:
    write(f"sections/es-{num}.svg", section(num, icon, color, es))
    write(f"sections/en-{num}.svg", section(num, icon, color, en))


# ---------------------------------------------------------------- cabecera
CHAR_W = 9.0  # ancho aproximado de un carácter monoespaciado a 15px


def header(role, terminal_title, lines, chips):
    # lines: lista de (tipo, texto) con tipo "cmd" | "out" | "hi"
    tx, ty0, lh = 700, 128, 30
    parts, t = [], 0.6
    for i, (kind, text) in enumerate(lines):
        y = ty0 + i * lh
        cid = f"c{i}"
        if kind == "cmd":
            full = (len(text) + 2) * CHAR_W + 4
            dur = max(0.5, len(text) * 0.06)
            content = (f'<tspan fill="{LIME}">$</tspan> '
                       f'<tspan fill="#f5f5f5">{escape(text)}</tspan>')
        else:
            full = len(text) * CHAR_W + 20
            dur = 0.01
            col = LIME if kind == "hi" else "#a3a3a3"
            content = f'<tspan fill="{col}">{escape(text)}</tspan>'
        parts.append(
            f'<clipPath id="{cid}"><rect x="{tx}" y="{y - 18}" width="0" height="26">'
            f'<animate attributeName="width" from="0" to="{full:.0f}" begin="{t:.2f}s" dur="{dur:.2f}s" fill="freeze"/>'
            f'</rect></clipPath>'
            f'<text x="{tx}" y="{y}" clip-path="url(#{cid})" font-family="{MONO}" font-size="15">{content}</text>'
        )
        t += dur + (0.35 if kind == "cmd" else 0.25)
        last_y, last_w = y, full
    cursor = (
        f'<rect x="{tx + last_w + 4:.0f}" y="{last_y - 14}" width="9" height="18" fill="{LIME}" opacity="0">'
        f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.01;.5;.51" dur="1.1s" begin="{t:.2f}s" repeatCount="indefinite"/>'
        f'</rect>'
    )

    chip_svg, cx = [], 60
    for c in chips:
        w = len(c) * 8.6 + 28
        chip_svg.append(
            f'<rect x="{cx}" y="290" width="{w:.0f}" height="30" rx="15" fill="{LIME}" fill-opacity=".1" stroke="{LIME}" stroke-opacity=".45"/>'
            f'<text x="{cx + w / 2:.0f}" y="310" text-anchor="middle" font-family="{SANS}" font-size="14" font-weight="600" fill="#d9f99d">{escape(c)}</text>'
        )
        cx += w + 10

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="360" viewBox="0 0 1200 360" role="img" aria-label="Andreu Zapater Fillat — {escape(role)}">
  <defs>
    <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
      <path d="M40 0H0V40" fill="none" stroke="{LIME}" stroke-opacity=".07"/>
    </pattern>
    <radialGradient id="glow1" cx="1" cy="0" r=".7">
      <stop offset="0" stop-color="{LIME}" stop-opacity=".35"/>
      <stop offset="1" stop-color="{LIME}" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="glow2" cx="0" cy="1" r=".6">
      <stop offset="0" stop-color="#22c55e" stop-opacity=".22"/>
      <stop offset="1" stop-color="#22c55e" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="name" x1="0" x2="1">
      <stop offset="0" stop-color="#d9f99d"/>
      <stop offset="1" stop-color="{LIME}"/>
    </linearGradient>
    <clipPath id="card"><rect width="1200" height="360" rx="20"/></clipPath>
  </defs>

  <g clip-path="url(#card)">
    <rect width="1200" height="360" fill="{BG}"/>
    <rect width="1200" height="360" fill="url(#grid)"/>
    <rect width="1200" height="360" fill="url(#glow1)">
      <animate attributeName="opacity" values=".75;1;.75" dur="6s" repeatCount="indefinite"/>
    </rect>
    <rect width="1200" height="360" fill="url(#glow2)"/>
  </g>
  <rect x=".5" y=".5" width="1199" height="359" rx="20" fill="none" stroke="{LIME}" stroke-opacity=".25"/>

  <!-- Columna izquierda -->
  <rect x="60" y="56" width="236" height="30" rx="15" fill="{LIME}" fill-opacity=".1" stroke="{LIME}" stroke-opacity=".5"/>
  <circle cx="80" cy="71" r="5" fill="{LIME}">
    <animate attributeName="opacity" values="1;.3;1" dur="2s" repeatCount="indefinite"/>
  </circle>
  <text x="94" y="76" font-family="{MONO}" font-size="13" font-weight="600" letter-spacing="2" fill="{LIME}">FULL STACK DEVELOPER</text>

  <text x="58" y="160" font-family="{SANS}" font-size="58" font-weight="800" fill="#ffffff">Andreu Zapater</text>
  <text x="58" y="222" font-family="{SANS}" font-size="58" font-weight="800" fill="url(#name)">Fillat</text>
  <text x="60" y="262" font-family="{SANS}" font-size="18" fill="#a3a3a3">{escape(role)}</text>
  {"".join(chip_svg)}

  <!-- Terminal -->
  <rect x="672" y="56" width="476" height="264" rx="12" fill="#0f150f" fill-opacity=".92" stroke="#ffffff" stroke-opacity=".1"/>
  <path d="M684 56h452a12 12 0 0 1 12 12v24H672V68a12 12 0 0 1 12-12z" fill="#182018"/>
  <circle cx="692" cy="74" r="6" fill="#ff5f57"/>
  <circle cx="712" cy="74" r="6" fill="#febc2e"/>
  <circle cx="732" cy="74" r="6" fill="#28c840"/>
  <text x="910" y="79" text-anchor="middle" font-family="{MONO}" font-size="12" fill="#737373">{escape(terminal_title)}</text>
  {"".join(parts)}
  {cursor}
</svg>
'''


write("header-es.svg", header(
    "Jefe del Departamento Digital · OK24Horas",
    "andreu@ok24horas: ~",
    [("cmd", "whoami"), ("out", "andreu — jefe del departamento digital"),
     ("cmd", "cat stack.txt"), ("out", "React · Laravel · TypeScript · Docker"),
     ("cmd", "git checkout -b migracion"), ("hi", "ASP.NET → React + Laravel")],
    ["React", "Laravel", "TypeScript"],
))
write("header-en.svg", header(
    "Head of Digital · OK24Horas",
    "andreu@ok24horas: ~",
    [("cmd", "whoami"), ("out", "andreu — head of digital"),
     ("cmd", "cat stack.txt"), ("out", "React · Laravel · TypeScript · Docker"),
     ("cmd", "git checkout -b migration"), ("hi", "ASP.NET → React + Laravel")],
    ["React", "Laravel", "TypeScript"],
))


# ---------------------------------------------------------------- pie
def footer(text):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="110" viewBox="0 0 1200 110" role="img" aria-label="{escape(text)}">
  <defs>
    <linearGradient id="line" x1="0" x2="1">
      <stop offset="0" stop-color="{LIME}" stop-opacity="0"/>
      <stop offset=".5" stop-color="{LIME}"/>
      <stop offset="1" stop-color="{LIME}" stop-opacity="0"/>
    </linearGradient>
  </defs>
  <rect x="150" y="20" width="900" height="2" fill="url(#line)"/>
  <text x="600" y="64" text-anchor="middle" font-family="{SANS}" font-size="20" font-weight="700" fill="#65a30d">{escape(text)}</text>
  <text x="600" y="92" text-anchor="middle" font-family="{MONO}" font-size="13" fill="#737373">andreuzapaterdev@gmail.com</text>
</svg>
'''


write("footer-es.svg", footer("Gracias por pasarte"))
write("footer-en.svg", footer("Thanks for stopping by"))
print("ok")
