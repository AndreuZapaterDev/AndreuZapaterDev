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


# ---------------------------------------------------------------- stack
# Logos de Simple Icons (CC0) guardados en scripts/icons/
ICON_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icons")


def brand_path(slug):
    import re
    with open(os.path.join(ICON_DIR, f"{slug}.svg"), encoding="utf-8") as f:
        return re.search(r'<path d="([^"]+)"', f.read()).group(1)


# (slug, nombre, color de marca legible sobre fondo oscuro)
STACK = [
    ("FRONTEND", [("html5", "HTML5", "#E34F26"), ("css3", "CSS3", "#2965F1"),
                  ("javascript", "JavaScript", "#F7DF1E"), ("typescript", "TypeScript", "#3178C6"),
                  ("react", "React", "#61DAFB"), ("tailwindcss", "Tailwind CSS", "#06B6D4"),
                  ("angular", "Angular", "#DD0031")]),
    ("BACKEND", [("php", "PHP", "#8892BF"), ("laravel", "Laravel", "#FF2D20"),
                 ("openjdk", "Java", "#ED8B00")]),
    ("DATA", [("mysql", "MySQL", "#5D9CC9"), ("postgresql", "PostgreSQL", "#6B8FE8"),
              ("oracle", "Oracle", "#F80000")]),
    ("DEVOPS", [("git", "Git", "#F05032"), ("github", "GitHub", "#ffffff"),
                ("docker", "Docker", "#2496ED")]),
]


def stack_svg(titles, basic_label):
    color = "#4ade80"
    gap, ph = 12, 126
    # Fila 1: Frontend a todo el ancho · Fila 2: Backend, Datos y DevOps en 3 columnas
    col_w = (1200 - 2 * gap) / 3
    layout = [(0, 0, 1200), (0, ph + gap, col_w), (col_w + gap, ph + gap, col_w),
              (2 * (col_w + gap), ph + gap, col_w)]
    out = []
    for (key, items), (px, py, pw) in zip(STACK, layout):
        out.append(
            f'<rect x="{px + .5:.1f}" y="{py + .5}" width="{pw - 1:.1f}" height="{ph - 1}" rx="16" fill="{BG}" stroke="{color}" stroke-opacity=".28"/>'
            f'<text x="{px + 20:.0f}" y="{py + 36}" font-family="{MONO}" font-size="13" font-weight="700" letter-spacing="2" fill="{color}">{escape(titles[key])}</text>'
            f'<text x="{px + pw - 20:.0f}" y="{py + 36}" text-anchor="end" font-family="{MONO}" font-size="13" fill="#525252">{len(items):02d}</text>'
        )
        cx, cy = px + 20, py + 60
        for slug, name, bc in items:
            extra = f" · {basic_label}" if slug == "angular" else ""
            w = 44 + len(name) * 7.7 + len(extra) * 6.4 + 14
            out.append(
                f'<rect x="{cx:.0f}" y="{cy}" width="{w:.0f}" height="40" rx="10" fill="#111811" stroke="#ffffff" stroke-opacity=".08"/>'
                f'<g transform="translate({cx + 13:.0f} {cy + 10}) scale(.8333)"><path d="{brand_path(slug)}" fill="{bc}"/></g>'
                f'<text x="{cx + 44:.0f}" y="{cy + 26}" font-family="{SANS}" font-size="15" font-weight="600" fill="#f5f5f5">{escape(name)}'
                + (f'<tspan fill="#737373" font-weight="400" font-size="13">{escape(extra)}</tspan>' if extra else "")
                + '</text>'
            )
            cx += w + 8
    h = 2 * ph + gap
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="{h}" viewBox="0 0 1200 {h}" role="img" '
            f'aria-label="Stack: HTML5, CSS3, JavaScript, TypeScript, React, Tailwind CSS, Angular, PHP, Laravel, Java, MySQL, PostgreSQL, Oracle SQL, Git, GitHub, Docker">'
            + "".join(out) + '</svg>\n')


write("stack-es.svg", stack_svg(
    {"FRONTEND": "FRONTEND", "BACKEND": "BACKEND", "DATA": "BASES DE DATOS", "DEVOPS": "DEVOPS & TOOLS"}, "básico"))
write("stack-en.svg", stack_svg(
    {"FRONTEND": "FRONTEND", "BACKEND": "BACKEND", "DATA": "DATABASES", "DEVOPS": "DEVOPS & TOOLS"}, "basic"))


# ---------------------------------------------------------------- trayectoria
def chip(x, y, text, color, filled=False):
    w = len(text) * 7.4 + 24
    fill = f'fill="{color}" fill-opacity=".14"' if filled else 'fill="#111811"'
    return (f'<rect x="{x:.0f}" y="{y}" width="{w:.0f}" height="26" rx="13" {fill} stroke="{color}" stroke-opacity=".5"/>'
            f'<text x="{x + w / 2:.0f}" y="{y + 17}" text-anchor="middle" font-family="{MONO}" font-size="12" font-weight="600" fill="{color}">{escape(text)}</text>'), w


def timeline_svg(entries, label):
    # entries: (pill, título, subtítulo, descripción | None, chips[], color, actual)
    out, y, nodes = [], 20, []
    for pill, title, sub, desc, chips, color, current in entries:
        h = 102 + (30 if desc else 0) + (44 if chips else 0) + 26
        ny = y + 34
        nodes.append(ny)
        out.append(f'<rect x="80.5" y="{y + .5}" width="1119" height="{h - 1}" rx="16" fill="{BG}" stroke="{color}" stroke-opacity=".3"/>')
        if current:
            out.append(
                f'<circle cx="40" cy="{ny}" r="10" fill="none" stroke="{color}" stroke-width="2">'
                f'<animate attributeName="r" values="10;22" dur="2s" repeatCount="indefinite"/>'
                f'<animate attributeName="opacity" values=".8;0" dur="2s" repeatCount="indefinite"/></circle>')
        out.append(f'<circle cx="40" cy="{ny}" r="{9 if current else 7}" fill="{color if current else BG}" stroke="{color}" stroke-width="3"/>')
        p, pw_ = chip(104, y + 20, pill, color, filled=current)
        out.append(p)
        out.append(f'<text x="104" y="{y + 76}" font-family="{SANS}" font-size="24" font-weight="700" fill="#ffffff">{escape(title)}</text>')
        out.append(f'<text x="104" y="{y + 102}" font-family="{SANS}" font-size="15" font-weight="600" fill="{color}">{escape(sub)}</text>')
        ty = y + 102
        if desc:
            ty += 30
            out.append(f'<text x="104" y="{ty}" font-family="{SANS}" font-size="15" fill="#a3a3a3">{escape(desc)}</text>')
        if chips:
            cx = 104
            for c in chips:
                s, w = chip(cx, ty + 18, c, "#d4d4d4")
                out.append(s)
                cx += w + 8
        y += h + 20
    line = (f'<defs><linearGradient id="tl" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="{LIME}"/><stop offset="1" stop-color="#3f3f46"/></linearGradient></defs>'
            f'<rect x="39" y="{nodes[0]}" width="2" height="{nodes[-1] - nodes[0]}" fill="url(#tl)"/>')
    total = y
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="{total}" viewBox="0 0 1200 {total}" role="img" aria-label="{escape(label)}">'
            + line + "".join(out) + '</svg>\n')


write("timeline-es.svg", timeline_svg([
    ("● ACTUALIDAD", "Jefe del Departamento Digital", "OK24Horas · Grupo RODI",
     "Coordinación de proyectos, estrategia digital y supervisión del desarrollo técnico.",
     ["PROMOCIÓN INTERNA", "ASP.NET → REACT + LARAVEL"], LIME, True),
    ("2 AÑOS", "Full Stack Developer", "OK24Horas · Grupo RODI",
     "Desarrollo de aplicaciones web de extremo a extremo, desde la interfaz hasta la base de datos.",
     [], "#65a30d", False),
    ("FORMACIÓN", "Desarrollo de Aplicaciones Web (DAW)", "Ciclo Formativo de Grado Superior",
     None, [], "#a3a3a3", False),
], "Trayectoria: Jefe del Departamento Digital en OK24Horas (actualidad), Full Stack Developer en OK24Horas (2 años), Grado Superior en DAW"))

write("timeline-en.svg", timeline_svg([
    ("● PRESENT", "Head of Digital", "OK24Horas · Grupo RODI",
     "Project coordination, digital strategy and oversight of technical development.",
     ["INTERNAL PROMOTION", "ASP.NET → REACT + LARAVEL"], LIME, True),
    ("2 YEARS", "Full Stack Developer", "OK24Horas · Grupo RODI",
     "End-to-end web application development, from user interface to database.",
     [], "#65a30d", False),
    ("EDUCATION", "Web Application Development (DAW)", "Higher Vocational Training Degree (Spain)",
     None, [], "#a3a3a3", False),
], "Experience: Head of Digital at OK24Horas (present), Full Stack Developer at OK24Horas (2 years), Web Application Development degree"))


# ---------------------------------------------------------------- idiomas
def languages_svg(items, label):
    color = "#10b981"
    w, gap = 392, 12
    out = []
    for i, (code, name, level, score) in enumerate(items):
        x = i * (w + gap)
        out.append(
            f'<rect x="{x + .5}" y=".5" width="{w - 1}" height="149" rx="16" fill="{BG}" stroke="{color}" stroke-opacity=".3"/>'
            f'<text x="{x + w - 22}" y="58" text-anchor="end" font-family="{MONO}" font-size="44" font-weight="800" fill="{color}" fill-opacity=".14">{code}</text>'
            f'<text x="{x + 24}" y="46" font-family="{SANS}" font-size="21" font-weight="700" fill="#ffffff">{escape(name)}</text>'
            f'<text x="{x + 24}" y="74" font-family="{SANS}" font-size="14" fill="#a3a3a3">{escape(level)}</text>'
        )
        sw = (w - 48 - 4 * 8) / 5
        for s in range(5):
            on = s < score
            out.append(
                f'<rect x="{x + 24 + s * (sw + 8):.1f}" y="104" width="{sw:.1f}" height="8" rx="4" '
                f'fill="{color if on else "#1f2a1f"}"/>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="150" viewBox="0 0 1200 150" role="img" aria-label="{escape(label)}">'
            + "".join(out) + '</svg>\n')


write("languages-es.svg", languages_svg([
    ("ES", "Español", "Nativo", 5), ("CA", "Català", "Nativo", 5),
    ("EN", "English", "B2 · EOI  |  C1 · EF SET", 4)],
    "Idiomas: español nativo, catalán nativo, inglés B2 (EOI) y C1 (EF SET)"))
write("languages-en.svg", languages_svg([
    ("ES", "Spanish", "Native", 5), ("CA", "Catalan", "Native", 5),
    ("EN", "English", "B2 · EOI  |  C1 · EF SET", 4)],
    "Languages: Spanish native, Catalan native, English B2 (EOI) and C1 (EF SET)"))

print("ok")
