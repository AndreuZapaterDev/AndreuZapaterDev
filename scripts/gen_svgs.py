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
    # 1) Calcular cuándo empieza y acaba de escribirse cada línea
    t, timed = 0.6, []
    for kind, text in lines:
        if kind == "cmd":
            full = (len(text) + 2) * CHAR_W + 4
            dur = max(0.5, len(text) * 0.06)
        else:
            full = len(text) * CHAR_W + 20
            dur = 0.01
        timed.append((kind, text, full, t, t + dur))
        t += dur + (0.35 if kind == "cmd" else 0.25)
    typed_end = t
    cycle = typed_end + 7  # tiempo con todo escrito antes de "limpiar" y repetir

    # 2) Pintar las líneas: todas las animaciones comparten el mismo ciclo en bucle
    parts = []
    for i, (kind, text, full, start, end) in enumerate(timed):
        y = ty0 + i * lh
        if kind == "cmd":
            content = (f'<tspan fill="{LIME}">$</tspan> '
                       f'<tspan fill="#f5f5f5">{escape(text)}</tspan>')
        else:
            col = LIME if kind == "hi" else "#a3a3a3"
            content = f'<tspan fill="{col}">{escape(text)}</tspan>'
        k1, k2 = start / cycle, end / cycle
        parts.append(
            f'<clipPath id="c{i}"><rect x="{tx}" y="{y - 18}" width="0" height="26">'
            f'<animate attributeName="width" values="0;0;{full:.0f};{full:.0f}" keyTimes="0;{k1:.4f};{k2:.4f};1" '
            f'dur="{cycle:.2f}s" repeatCount="indefinite"/>'
            f'</rect></clipPath>'
            f'<text x="{tx}" y="{y}" clip-path="url(#c{i})" font-family="{MONO}" font-size="15">{content}</text>'
        )
        # El cursor va justo detrás del último carácter (≈8.3 px por carácter a 15 px)
        last_y, last_w = y, len(text) * 8.3 + (18 if kind == "cmd" else 0)
    # Cursor: aparece al terminar de escribir (en cada ciclo) y parpadea
    cursor = (
        f'<g opacity="0"><animate attributeName="opacity" values="0;1" keyTimes="0;{typed_end / cycle:.4f}" '
        f'calcMode="discrete" dur="{cycle:.2f}s" repeatCount="indefinite"/>'
        f'<rect x="{tx + last_w + 4:.0f}" y="{last_y - 14}" width="9" height="18" fill="{LIME}">'
        f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;.5;.51;1" dur="1.1s" repeatCount="indefinite"/>'
        f'</rect></g>'
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
    <!-- Destello que cruza "Fillat" cada 5 s -->
    <linearGradient id="sheen" gradientUnits="userSpaceOnUse" x1="-260" y1="0" x2="-60" y2="0">
      <stop offset="0" stop-color="#ffffff" stop-opacity="0"/>
      <stop offset=".5" stop-color="#ffffff" stop-opacity=".85"/>
      <stop offset="1" stop-color="#ffffff" stop-opacity="0"/>
      <animate attributeName="x1" values="-260;260;260" keyTimes="0;.5;1" dur="5s" repeatCount="indefinite"/>
      <animate attributeName="x2" values="-60;460;460" keyTimes="0;.5;1" dur="5s" repeatCount="indefinite"/>
    </linearGradient>
    <filter id="beamglow" x="-5%" y="-20%" width="110%" height="140%"><feGaussianBlur stdDeviation="4"/></filter>
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
  <!-- Haz de luz que recorre el borde sin parar -->
  <g fill="none" stroke-linecap="round">
    <rect x="1" y="1" width="1198" height="358" rx="20" pathLength="1000" stroke="{LIME}" stroke-width="6" stroke-opacity=".7" stroke-dasharray="90 910" filter="url(#beamglow)">
      <animate attributeName="stroke-dashoffset" from="0" to="-1000" dur="9s" repeatCount="indefinite"/>
    </rect>
    <rect x="1" y="1" width="1198" height="358" rx="20" pathLength="1000" stroke="#d9f99d" stroke-width="2" stroke-dasharray="90 910">
      <animate attributeName="stroke-dashoffset" from="0" to="-1000" dur="9s" repeatCount="indefinite"/>
    </rect>
  </g>

  <!-- Columna izquierda -->
  <rect x="60" y="56" width="236" height="30" rx="15" fill="{LIME}" fill-opacity=".1" stroke="{LIME}" stroke-opacity=".5"/>
  <circle cx="80" cy="71" r="5" fill="{LIME}">
    <animate attributeName="opacity" values="1;.3;1" dur="2s" repeatCount="indefinite"/>
  </circle>
  <text x="94" y="76" font-family="{MONO}" font-size="13" font-weight="600" letter-spacing="2" fill="{LIME}">FULL STACK DEVELOPER</text>

  <text x="58" y="160" font-family="{SANS}" font-size="58" font-weight="800" fill="#ffffff">Andreu Zapater</text>
  <text x="58" y="222" font-family="{SANS}" font-size="58" font-weight="800" fill="url(#name)">Fillat</text>
  <text x="58" y="222" font-family="{SANS}" font-size="58" font-weight="800" fill="url(#sheen)">Fillat</text>
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
    [("cmd", "whoami"), ("out", "Andreu - Full Stack Developer"),
     ("cmd", "cat stack.txt"), ("out", "React · Laravel · TypeScript · Docker"),
     ("cmd", "git checkout -b migracion"), ("hi", "ASP.NET → React + Laravel")],
    ["React", "Laravel", "TypeScript"],
))
write("header-en.svg", header(
    "Head of Digital · OK24Horas",
    "andreu@ok24horas: ~",
    [("cmd", "whoami"), ("out", "Andreu - Full Stack Developer"),
     ("cmd", "cat stack.txt"), ("out", "React · Laravel · TypeScript · Docker"),
     ("cmd", "git checkout -b migration"), ("hi", "ASP.NET → React + Laravel")],
    ["React", "Laravel", "TypeScript"],
))


# ---------------------------------------------------------------- pie
def footer(text):
    # Continúa el degradado de la página: 07 Actividad (#0d9488) → cian (#06b6d4), el último color
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="110" viewBox="0 0 1200 110" role="img" aria-label="{escape(text)}">
  <defs>
    <linearGradient id="line" x1="0" x2="1">
      <stop offset="0" stop-color="#0d9488" stop-opacity="0"/>
      <stop offset=".35" stop-color="#0d9488"/>
      <stop offset=".65" stop-color="#06b6d4"/>
      <stop offset="1" stop-color="#06b6d4" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="txt" gradientUnits="userSpaceOnUse" x1="490" x2="710">
      <stop offset="0" stop-color="#0d9488"/>
      <stop offset="1" stop-color="#0891b2"/>
    </linearGradient>
  </defs>
  <rect x="150" y="20" width="900" height="2" fill="url(#line)"/>
  <text x="600" y="64" text-anchor="middle" font-family="{SANS}" font-size="20" font-weight="700" fill="url(#txt)">{escape(text)}</text>
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
                 ("openjdk", "Java", "#ED8B00"), ("supabase", "Supabase", "#3FCF8E")]),
    ("DATA", [("mysql", "MySQL", "#5D9CC9"), ("postgresql", "PostgreSQL", "#6B8FE8"),
              ("oracle", "Oracle", "#F80000")]),
    ("DEVOPS", [("git", "Git", "#F05032"), ("github", "GitHub", "#ffffff"),
                ("docker", "Docker", "#2496ED")]),
]


def stack_svg(titles, basic_label):
    color = "#4ade80"
    gap, ph = 12, 126
    # Fila 1: Frontend a todo el ancho · Fila 2: Backend, Datos y DevOps en 3 columnas
    # Fila 1: Frontend · Fila 2: Backend y Datos · Fila 3: DevOps
    col_w = (1200 - gap) / 2
    layout = [(0, 0, 1200), (0, ph + gap, col_w), (col_w + gap, ph + gap, col_w),
              (0, 2 * (ph + gap), 1200)]
    out = []
    for (key, items), (px, py, pw) in zip(STACK, layout):
        out.append(
            f'<rect x="{px + .5:.1f}" y="{py + .5}" width="{pw - 1:.1f}" height="{ph - 1}" rx="16" fill="{BG}" stroke="{color}" stroke-opacity=".28"/>'
            f'<text x="{px + 20:.0f}" y="{py + 36}" font-family="{MONO}" font-size="13" font-weight="700" letter-spacing="2" fill="{color}">{escape(titles[key])}</text>'
            f'<text x="{px + pw - 20:.0f}" y="{py + 36}" text-anchor="end" font-family="{MONO}" font-size="13" fill="#525252">{len(items):02d}</text>'
        )
        cx, cy = px + 20, py + 60
        for slug, name, bc in items:
            extra = ""
            w = 44 + len(name) * 7.7 + len(extra) * 6.4 + 14
            out.append(
                f'<rect x="{cx:.0f}" y="{cy}" width="{w:.0f}" height="40" rx="10" fill="#111811" stroke="#ffffff" stroke-opacity=".08"/>'
                f'<g transform="translate({cx + 13:.0f} {cy + 10}) scale(.8333)"><path d="{brand_path(slug)}" fill="{bc}"/></g>'
                f'<text x="{cx + 44:.0f}" y="{cy + 26}" font-family="{SANS}" font-size="15" font-weight="600" fill="#f5f5f5">{escape(name)}'
                + (f'<tspan fill="#737373" font-weight="400" font-size="13">{escape(extra)}</tspan>' if extra else "")
                + '</text>'
            )
            cx += w + 8
    h = 3 * ph + 2 * gap
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="{h}" viewBox="0 0 1200 {h}" role="img" '
            f'aria-label="Stack: HTML5, CSS3, JavaScript, TypeScript, React, Tailwind CSS, Angular, PHP, Laravel, Java, Supabase, MySQL, PostgreSQL, Oracle SQL, Git, GitHub, Docker">'
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
    ("● 2026 – ACTUALIDAD", "Jefe del Departamento Digital", "OK24Horas · Grupo RODI",
     "Coordinación de proyectos, estrategia digital y supervisión del desarrollo técnico.",
     ["PROMOCIÓN INTERNA", "ASP.NET → REACT + LARAVEL"], LIME, True),
    ("2024 – 2025", "Full Stack Developer", "OK24Horas · Grupo RODI",
     "Desarrollo de aplicaciones web de extremo a extremo, desde la interfaz hasta la base de datos.",
     [], "#65a30d", False),
    ("FORMACIÓN", "Desarrollo de Aplicaciones Web (DAW)", "Ciclo Formativo de Grado Superior",
     None, [], "#a3a3a3", False),
], "Trayectoria: Jefe del Departamento Digital en OK24Horas (2026 – actualidad), Full Stack Developer en OK24Horas (2024 – 2025), Grado Superior en DAW"))

write("timeline-en.svg", timeline_svg([
    ("● 2026 – PRESENT", "Head of Digital", "OK24Horas · Grupo RODI",
     "Project coordination, digital strategy and oversight of technical development.",
     ["INTERNAL PROMOTION", "ASP.NET → REACT + LARAVEL"], LIME, True),
    ("2024 – 2025", "Full Stack Developer", "OK24Horas · Grupo RODI",
     "End-to-end web application development, from user interface to database.",
     [], "#65a30d", False),
    ("EDUCATION", "Web Application Development (DAW)", "Higher Vocational Training Degree (Spain)",
     None, [], "#a3a3a3", False),
], "Experience: Head of Digital at OK24Horas (2026 – present), Full Stack Developer at OK24Horas (2024 – 2025), Web Application Development degree"))


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

# ---------------------------------------------------------------- sobre mí
def rich(line):
    """Convierte **negrita** en tspans resaltados."""
    out = []
    for i, chunk in enumerate(line.split("**")):
        if not chunk:
            continue
        out.append(f'<tspan fill="#ffffff" font-weight="700">{escape(chunk)}</tspan>' if i % 2 else escape(chunk))
    return "".join(out)


def count_up(x, y, n, color, delay=0.4, dur=3.2):
    """Número que cuenta de 0 a n al cargar (frena al final). El SVG no puede animar
    el texto en sí, así que se apilan los valores intermedios y se muestran por turnos."""
    style = f'font-family="{SANS}" font-size="34" font-weight="800" fill="{color}"'
    times = [delay + dur * (1 - (1 - k / n) ** (1 / 3)) for k in range(n + 1)] if n else [0]
    out = []
    for k in range(n + 1):
        show = "" if k == 0 else f'<set attributeName="opacity" to="1" begin="{times[k]:.2f}s"/>'
        hide = "" if k == n else f'<set attributeName="opacity" to="0" begin="{times[k + 1]:.2f}s"/>'
        out.append(f'<text x="{x}" y="{y}" {style} opacity="{1 if k == 0 else 0}">{k}{show}{hide}</text>')
    return "".join(out)


def about_svg(paragraphs, stats, code, now_label, now_text, label):
    color = "#a3e635"
    H = 430
    out = [
        f'<rect x=".5" y=".5" width="1199" height="{H - 1}" rx="18" fill="{BG}" stroke="{color}" stroke-opacity=".3"/>',
        f'<rect x=".5" y=".5" width="1199" height="{H - 1}" rx="18" fill="url(#ag)"/>',
    ]
    # Texto
    y = 66
    for para in paragraphs:
        for line in para:
            out.append(f'<text x="40" y="{y}" font-family="{SANS}" font-size="17" fill="#a3a3a3">{rich(line)}</text>')
            y += 28
        y += 14
    # Cifras
    sx = 40
    for num, lab in stats:
        out.append(
            f'<rect x="{sx}" y="262" width="170" height="78" rx="12" fill="#111811" stroke="#ffffff" stroke-opacity=".07"/>'
            + count_up(sx + 18, 304, int(num), color)
            + f'<text x="{sx + 18}" y="326" font-family="{SANS}" font-size="13" fill="#a3a3a3">{escape(lab)}</text>')
        sx += 184
    # Editor
    ex, ey, ew, eh = 640, 40, 520, 300
    out.append(
        f'<rect x="{ex}" y="{ey}" width="{ew}" height="{eh}" rx="12" fill="#0f150f" stroke="#ffffff" stroke-opacity=".1"/>'
        f'<path d="M{ex + 12} {ey}h{ew - 24}a12 12 0 0 1 12 12v28H{ex}V{ey + 12}a12 12 0 0 1 12-12z" fill="#182018"/>'
        f'<circle cx="{ex + 20}" cy="{ey + 20}" r="6" fill="#ff5f57"/><circle cx="{ex + 40}" cy="{ey + 20}" r="6" fill="#febc2e"/><circle cx="{ex + 60}" cy="{ey + 20}" r="6" fill="#28c840"/>'
        f'<rect x="{ex + 84}" y="{ey + 8}" width="100" height="32" rx="6" fill="#0f150f"/>'
        f'<rect x="{ex + 84}" y="{ey + 38}" width="100" height="2" fill="{color}"/>'
        f'<text x="{ex + 134}" y="{ey + 29}" text-anchor="middle" font-family="{MONO}" font-size="12" fill="#d4d4d4">andreu.ts</text>')
    cy = ey + 80
    for n, tokens in enumerate(code, 1):
        spans = "".join(f'<tspan fill="{c}">{escape(t)}</tspan>' for t, c in tokens)
        out.append(
            f'<text x="{ex + 34}" y="{cy}" text-anchor="end" font-family="{MONO}" font-size="13" fill="#3f3f46">{n}</text>'
            f'<text x="{ex + 52}" y="{cy}" font-family="{MONO}" font-size="14" xml:space="preserve">{spans}</text>')
        cy += 30
    # Barra de estado del editor
    out.append(
        f'<path d="M{ex} {ey + eh - 30}h{ew}v18a12 12 0 0 1-12 12H{ex + 12}a12 12 0 0 1-12-12z" fill="#182018"/>'
        f'<text x="{ex + 16}" y="{ey + eh - 11}" font-family="{MONO}" font-size="11" fill="{color}">⎇ main</text>'
        f'<text x="{ex + ew - 16}" y="{ey + eh - 11}" text-anchor="end" font-family="{MONO}" font-size="11" fill="#737373">TypeScript  ·  UTF-8  ·  Ln 6, Col 3</text>')
    # Franja "ahora mismo"
    out.append(
        f'<rect x="20" y="{H - 70}" width="1160" height="50" rx="12" fill="{color}" fill-opacity=".08" stroke="{color}" stroke-opacity=".3"/>'
        f'<circle cx="46" cy="{H - 45}" r="5" fill="{color}"><animate attributeName="opacity" values="1;.25;1" dur="1.6s" repeatCount="indefinite"/></circle>'
        f'<text x="62" y="{H - 40}" font-family="{MONO}" font-size="13" font-weight="700" letter-spacing="2" fill="{color}">{escape(now_label)}</text>'
        f'<text x="{62 + len(now_label) * 9.8 + 18:.0f}" y="{H - 40}" font-family="{SANS}" font-size="15" fill="#e5e5e5">{rich(now_text)}</text>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="{H}" viewBox="0 0 1200 {H}" role="img" aria-label="{escape(label)}">'
            f'<defs><radialGradient id="ag" cx="0" cy="0" r=".8"><stop offset="0" stop-color="{color}" stop-opacity=".12"/>'
            f'<stop offset="1" stop-color="{color}" stop-opacity="0"/></radialGradient></defs>'
            + "".join(out) + '</svg>\n')


KW, KEY, STR, PUN, ID = "#c084fc", "#7dd3fc", "#a3e635", "#737373", "#f5f5f5"


def code_lines(focus):
    def arr(items):
        toks = [("[", PUN)]
        for i, it in enumerate(items):
            toks.append((f'"{it}"', STR))
            if i < len(items) - 1:
                toks.append((", ", PUN))
        return toks + [("],", PUN)]
    return [
        [("const ", KW), ("andreu", ID), (" = {", PUN)],
        [("  frontend", KEY), (": ", PUN)] + arr(["React", "TypeScript", "Tailwind"]),
        [("  backend", KEY), (":  ", PUN)] + arr(["PHP", "Laravel"]),
        [("  data", KEY), (":     ", PUN)] + arr(["MySQL", "PostgreSQL"]),
        [("  focus", KEY), (":    ", PUN), (f'"{focus}"', STR), (",", PUN)],
        [("};", PUN)],
    ]


write("about-es.svg", about_svg(
    [["Desarrollador **Full Stack** con **3 años de experiencia** diseñando",
      "y construyendo aplicaciones web de extremo a extremo:",
      "interfaz, lógica de negocio y base de datos."],
     ["Lidero el **Departamento Digital de OK24Horas** (Grupo RODI),",
      "combinando desarrollo técnico, gestión de proyectos",
      "y estrategia digital."]],
    [("3", "años de experiencia"), ("17", "tecnologías"), ("3", "idiomas")],
    code_lines("producto web de extremo a extremo"),
    "AHORA MISMO",
    "Migrando una aplicación web de **ASP.NET** a **React + Laravel** en OK24Horas",
    "Sobre mí: desarrollador Full Stack con 3 años de experiencia. Lidero el Departamento Digital de OK24Horas "
    "(Grupo RODI). Ahora mismo: migrando una aplicación web de ASP.NET a React + Laravel."))

write("about-en.svg", about_svg(
    [["**Full Stack** developer with **3 years of experience** designing",
      "and building end-to-end web applications:",
      "user interface, business logic and database."],
     ["I lead the **Digital Department at OK24Horas** (Grupo RODI),",
      "combining hands-on development, project management",
      "and digital strategy."]],
    [("3", "years of experience"), ("17", "technologies"), ("3", "languages")],
    code_lines("end-to-end web products"),
    "CURRENTLY",
    "Migrating a web application from **ASP.NET** to **React + Laravel** at OK24Horas",
    "About me: Full Stack developer with 3 years of experience. I lead the Digital Department at OK24Horas "
    "(Grupo RODI). Currently migrating a web application from ASP.NET to React + Laravel."))


# ---------------------------------------------------------------- proyecto
CHECK = '<path d="M20 6 9 17l-5-5"/>'


def project_svg(status, kind, title, subtitle, desc_lines, stack_label, stack, feat_label, features, label):
    color = "#22c55e"
    # Alto según el número de filas de funcionalidades (4 filas caben en 280 px)
    rows_needed = (len(features) + 1) // 2 if len(features) > 3 else len(features)
    H = 280 + max(0, rows_needed - 4) * 28
    out = [
        f'<rect x=".5" y=".5" width="1199" height="{H - 1}" rx="18" fill="{BG}" stroke="{color}" stroke-opacity=".3"/>',
        f'<rect x=".5" y=".5" width="1199" height="{H - 1}" rx="18" fill="url(#pg)"/>',
    ]
    # Píldoras de estado y tipo
    sw = len(status) * 7.6 + 44
    out.append(
        f'<rect x="40" y="36" width="{sw:.0f}" height="28" rx="14" fill="{color}" fill-opacity=".16" stroke="{color}" stroke-opacity=".6"/>'
        f'<circle cx="58" cy="50" r="4.5" fill="{color}"><animate attributeName="opacity" values="1;.25;1" dur="1.6s" repeatCount="indefinite"/></circle>'
        f'<text x="70" y="55" font-family="{MONO}" font-size="12" font-weight="700" letter-spacing="1.5" fill="{color}">{escape(status)}</text>')
    kw = len(kind) * 7.6 + 28
    out.append(
        f'<rect x="{40 + sw + 8:.0f}" y="36" width="{kw:.0f}" height="28" rx="14" fill="#111811" stroke="#ffffff" stroke-opacity=".15"/>'
        f'<text x="{40 + sw + 8 + kw / 2:.0f}" y="55" text-anchor="middle" font-family="{MONO}" font-size="12" font-weight="700" letter-spacing="1.5" fill="#d4d4d4">{escape(kind)}</text>')
    # Título y descripción
    out.append(
        f'<text x="38" y="114" font-family="{SANS}" font-size="40" font-weight="800" fill="#ffffff">{escape(title)}</text>'
        f'<text x="40" y="142" font-family="{SANS}" font-size="15" font-weight="600" fill="{color}">{escape(subtitle)}</text>')
    y = 186
    for line in desc_lines:
        out.append(f'<text x="40" y="{y}" font-family="{SANS}" font-size="16" fill="#a3a3a3">{rich(line)}</text>')
        y += 26
    # Panel derecho
    px = 770
    out.append(f'<rect x="{px - 30}" y="30" width="1" height="{H - 60}" fill="#ffffff" fill-opacity=".08"/>')
    out.append(f'<text x="{px}" y="52" font-family="{MONO}" font-size="12" font-weight="700" letter-spacing="2" fill="{color}">{escape(stack_label)}</text>')
    cx = px
    for slug, name, bc in stack:
        w = 44 + len(name) * 7.7 + 14
        out.append(
            f'<rect x="{cx:.0f}" y="66" width="{w:.0f}" height="38" rx="10" fill="#111811" stroke="#ffffff" stroke-opacity=".08"/>'
            f'<g transform="translate({cx + 13:.0f} 75) scale(.8333)"><path d="{brand_path(slug)}" fill="{bc}"/></g>'
            f'<text x="{cx + 44:.0f}" y="91" font-family="{SANS}" font-size="15" font-weight="600" fill="#f5f5f5">{escape(name)}</text>')
        cx += w + 8
    out.append(f'<text x="{px}" y="144" font-family="{MONO}" font-size="12" font-weight="700" letter-spacing="2" fill="{color}">{escape(feat_label)}</text>')
    two_cols = len(features) > 3
    rows = (len(features) + 1) // 2 if two_cols else len(features)
    step = 28 if two_cols else 30
    for i, f in enumerate(features):
        fx = px + (200 if two_cols and i >= rows else 0)
        fy = 174 + (i % rows) * step
        out.append(
            f'<circle cx="{fx + 10}" cy="{fy - 5}" r="10" fill="{color}" fill-opacity=".15"/>'
            f'<g transform="translate({fx + 3} {fy - 12}) scale(.5833)" fill="none" stroke="{color}" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round">{CHECK}</g>'
            f'<text x="{fx + 30}" y="{fy}" font-family="{SANS}" font-size="15" fill="#e5e5e5">{escape(f)}</text>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="{H}" viewBox="0 0 1200 {H}" role="img" aria-label="{escape(label)}">'
            f'<defs><radialGradient id="pg" cx="0" cy="0" r=".8"><stop offset="0" stop-color="{color}" stop-opacity=".12"/>'
            f'<stop offset="1" stop-color="{color}" stop-opacity="0"/></radialGradient></defs>'
            + "".join(out) + '</svg>\n')


REACT = [("react", "React", "#61DAFB")]

write("project-xixauxas-es.svg", project_svg(
    "EN PRODUCCIÓN", "PROYECTO PERSONAL", "Xixauxas", "League of Legends · Plataforma de coaching",
    ["Plataforma web para un **streamer y coach de League of Legends**",
     "que le permite **gestionar y promocionar sus sesiones de coaching**",
     "entre su comunidad de seguidores."],
    "STACK", REACT, "FUNCIONALIDADES",
    ["Reserva de sesiones de coaching", "Web bilingüe ES / EN", "Vídeos y redes sociales integrados"],
    "Xixauxas: proyecto personal en producción desarrollado con React. Plataforma web para un streamer y coach de "
    "League of Legends para gestionar y promocionar sus sesiones de coaching. Reserva de coachings, web bilingüe ES/EN, vídeos y redes sociales."))

write("project-xixauxas-en.svg", project_svg(
    "LIVE", "PERSONAL PROJECT", "Xixauxas", "League of Legends · Coaching platform",
    ["Web platform for a **League of Legends streamer and coach**",
     "to **manage and promote coaching sessions**",
     "to their community of followers."],
    "STACK", REACT, "FEATURES",
    ["Coaching session booking", "Bilingual site ES / EN", "Integrated videos and social media"],
    "Xixauxas: live personal project built with React. Web platform for a League of Legends streamer and coach "
    "to manage and promote coaching sessions. Coaching booking, bilingual ES/EN site, videos and social media."))


ZENSU_STACK = [("react", "React", "#61DAFB"), ("supabase", "Supabase", "#3FCF8E")]

write("project-zensu-es.svg", project_svg(
    "EN PRODUCCIÓN", "PROYECTO PERSONAL", "Zensu", "Gestión de tareas inteligente",
    ["Gestor de tareas con **React** en el frontend y **Supabase**",
     "como backend: **autenticación, base de datos y seguridad**",
     "a nivel de fila (RLS)."],
    "STACK", ZENSU_STACK, "FUNCIONALIDADES",
    ["Prioridades", "Etiquetas", "Fechas límite", "Arrastrar y soltar", "Calendario y reuniones",
     "Método Pomodoro", "Estadísticas", "Auth + RLS (Supabase)", "Bilingüe ES / EN", "Tema claro / oscuro"],
    "Zensu: gestor de tareas en producción desarrollado con React y Supabase. Prioridades, etiquetas, fechas límite, "
    "arrastrar y soltar, calendario para tareas y reuniones, método Pomodoro, estadísticas, autenticación y Row Level Security, bilingüe ES/EN y tema claro/oscuro."))

write("project-zensu-en.svg", project_svg(
    "LIVE", "PERSONAL PROJECT", "Zensu", "Smart task management",
    ["Task manager with a **React** frontend and **Supabase**",
     "as the backend: **authentication, database and row-level**",
     "**security** (RLS)."],
    "STACK", ZENSU_STACK, "FEATURES",
    ["Priorities", "Tags", "Due dates", "Drag and drop", "Calendar & meetings",
     "Pomodoro timer", "Statistics", "Auth + RLS (Supabase)", "Bilingual ES / EN", "Light / dark theme"],
    "Zensu: live task manager built with React and Supabase. Priorities, tags, due dates, drag and drop, calendar for tasks and meetings, Pomodoro timer, statistics, "
    "authentication and Row Level Security, bilingual ES/EN and light/dark theme."))

# ---------------------------------------------------------------- frase de posicionamiento
# Fondo transparente: versión clara y oscura (README usa <picture> según el tema de GitHub)
def tagline_svg(parts, line2, theme):
    main = "#0a0f0a" if theme == "light" else "#f5f5f5"
    accent = "#4d7c0f" if theme == "light" else "#a3e635"
    sub = "#525252" if theme == "light" else "#a3a3a3"
    spans = "".join(
        f'<tspan fill="{accent}" font-weight="800">{escape(t)}</tspan>' if hi else escape(t)
        for t, hi in parts)
    label = "".join(t for t, _ in parts) + " " + line2
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="120" viewBox="0 0 1200 120" role="img" aria-label="{escape(label)}">
  <defs>
    <linearGradient id="u" x1="0" x2="1">
      <stop offset="0" stop-color="{LIME}" stop-opacity="0"/>
      <stop offset=".5" stop-color="{LIME}"/>
      <stop offset="1" stop-color="{LIME}" stop-opacity="0"/>
    </linearGradient>
  </defs>
  <text x="600" y="46" text-anchor="middle" font-family="{SANS}" font-size="27" font-weight="700" fill="{main}">{spans}</text>
  <text x="600" y="82" text-anchor="middle" font-family="{SANS}" font-size="19" fill="{sub}">{escape(line2)}</text>
  <rect x="540" y="104" width="120" height="3" rx="1.5" fill="url(#u)"/>
</svg>
'''


TAGLINES = {
    "es": ([("Construyo y modernizo aplicaciones web de negocio con ", False), ("React", True),
            (" y ", False), ("Laravel", True)], "y lidero el área digital de OK24Horas."),
    "en": ([("I build and modernize business web applications with ", False), ("React", True),
            (" and ", False), ("Laravel", True)], "and lead the digital department at OK24Horas."),
}
for lang, (parts, line2) in TAGLINES.items():
    for theme in ("light", "dark"):
        write(f"tagline-{lang}-{theme}.svg", tagline_svg(parts, line2, theme))


# ---------------------------------------------------------------- botones de contacto
MAIL_ICON = '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/>'


def text_width(text, size, bold=True):
    """Ancho aproximado de un texto en una fuente sans-serif (em por carácter)."""
    em = 0
    for ch in text:
        if ch in "iljtf.,:;!|'I":
            em += .30
        elif ch in "r ":
            em += .38
        elif ch in "mwMW@":
            em += .86
        elif ch.isupper():
            em += .64
        elif ch.isdigit():
            em += .56
        else:
            em += .54
    return em * size * (1.04 if bold else 1)


def button_svg(text, icon_svg, primary, color=LIME):
    pad, icon, gap = 26, 24, 12
    tw = text_width(text, 16)
    w = pad + icon + gap + tw + pad
    fill = color if primary else BG
    fg = BG if primary else "#f5f5f5"
    stroke = "" if primary else f' stroke="{color}" stroke-opacity=".55"'
    # textLength fija el ancho del texto: los márgenes izquierdo y derecho quedan iguales con cualquier fuente
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w:.0f}" height="52" viewBox="0 0 {w:.0f} 52" role="img" aria-label="{escape(text)}">
  <rect x=".75" y=".75" width="{w - 1.5:.1f}" height="50.5" rx="25.25" fill="{fill}"{stroke}/>
  <g transform="translate({pad} 14)">{icon_svg(BG if primary else color)}</g>
  <text x="{pad + icon + gap}" y="32" textLength="{tw:.1f}" lengthAdjust="spacing" font-family="{SANS}" font-size="16" font-weight="700" fill="{fg}">{escape(text)}</text>
</svg>
'''


write("btn-email.svg", button_svg(
    "andreuzapaterdev@gmail.com",
    lambda c: f'<g fill="none" stroke="{c}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{MAIL_ICON}</g>',
    primary=True))
write("btn-linkedin.svg", button_svg(
    "LinkedIn",
    lambda c: f'<path d="{brand_path("linkedin")}" fill="{c}"/>',
    primary=False))

# ---------------------------------------------------------------- certificaciones
AWARD = ICONS["award"]


def cert_svg(issuer, title, footer, linked, icon, level=None):
    color = "#14b8a6"
    W, H = 590, 150
    fs = min(18, 476 / (len(title) * 0.56))
    if icon == "google":
        ic = f'<g transform="translate(36 36) scale(1)"><path d="{brand_path("google")}" fill="{color}"/></g>'
    else:
        ic = (f'<g transform="translate(36 36)" fill="none" stroke="{color}" stroke-width="2" '
              f'stroke-linecap="round" stroke-linejoin="round">{AWARD}</g>')
    mark = (f'<text x="{W - 24}" y="66" text-anchor="end" font-family="{MONO}" font-size="46" font-weight="800" '
            f'fill="{color}" fill-opacity=".16">{level}</text>') if level else ""
    if linked:
        foot = (f'<text x="24" y="{H - 22}" font-family="{SANS}" font-size="14" font-weight="700" fill="{color}">{escape(footer)}</text>'
                f'<g transform="translate({24 + len(footer) * 6.9 + 6:.0f} {H - 36}) scale(.6667)" fill="none" stroke="{color}" '
                f'stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M7 17 17 7M7 7h10v10"/></g>')
    else:
        foot = (f'<g transform="translate(24 {H - 36}) scale(.6667)" fill="none" stroke="#a3a3a3" stroke-width="3" '
                f'stroke-linecap="round" stroke-linejoin="round">{CHECK}</g>'
                f'<text x="46" y="{H - 22}" font-family="{SANS}" font-size="14" font-weight="600" fill="#a3a3a3">{escape(footer)}</text>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{escape(title)} — {escape(issuer)}">
  <defs><radialGradient id="cg" cx="0" cy="0" r=".9"><stop offset="0" stop-color="{color}" stop-opacity=".14"/><stop offset="1" stop-color="{color}" stop-opacity="0"/></radialGradient></defs>
  <rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="16" fill="{BG}" stroke="{color}" stroke-opacity=".32"/>
  <rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="16" fill="url(#cg)"/>
  {mark}
  <rect x="24" y="24" width="48" height="48" rx="12" fill="{color}" fill-opacity=".14" stroke="{color}" stroke-opacity=".4"/>
  {ic}
  <text x="88" y="42" font-family="{MONO}" font-size="12" font-weight="700" letter-spacing="1.5" fill="{color}">{escape(issuer.upper())}</text>
  <text x="88" y="68" font-family="{SANS}" font-size="{fs:.1f}" font-weight="700" fill="#ffffff">{escape(title)}</text>
  <rect x="24" y="{H - 52}" width="{W - 48}" height="1" fill="#ffffff" fill-opacity=".08"/>
  {foot}
</svg>
'''


os.makedirs(os.path.join(OUT, "certs"), exist_ok=True)
CERTS = {
    # id: (emisor, título ES, título EN, enlazada, icono, nivel)
    "efset-c1": ("EF SET", "Inglés C1", "English C1", True, "award", "C1"),
    "eoi-b2": ("Escuela Oficial de Idiomas", "Inglés B2", "English B2", False, "award", "B2"),
    "google-digital": ("Google Skillshop", "Competencias digitales para profesionales", "Digital skills for professionals", True, "google", None),
    "google-productivity": ("Google Skillshop", "Productividad personal", "Personal productivity", True, "google", None),
    "google-web-1": ("Google Skillshop", "Introducción al desarrollo web: HTML y CSS (1/2)", "Introduction to web development: HTML & CSS (1/2)", True, "google", None),
    "google-web-2": ("Google Skillshop", "Introducción al desarrollo web: HTML y CSS (2/2)", "Introduction to web development: HTML & CSS (2/2)", True, "google", None),
}
for cid, (issuer, es, en, linked, icon, level) in CERTS.items():
    en_issuer = "Official School of Languages (EOI)" if cid == "eoi-b2" else issuer
    write(f"certs/es-{cid}.svg", cert_svg(issuer, es, "Ver credencial" if linked else "Certificado oficial", linked, icon, level))
    write(f"certs/en-{cid}.svg", cert_svg(en_issuer, en, "View credential" if linked else "Official certificate", linked, icon, level))


ARROW = '<path d="M7 17 17 7M7 7h10v10"/>'
for lang, txt in (("es", "Visitar xixauxas.es"), ("en", "Visit xixauxas.es")):
    write(f"btn-visit-{lang}.svg", button_svg(
        txt,
        lambda c: f'<g fill="none" stroke="{c}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">{ARROW}</g>',
        primary=True, color="#22c55e"))

for lang, txt in (("es", "Visitar zensu.vercel.app"), ("en", "Visit zensu.vercel.app")):
    write(f"btn-visit-zensu-{lang}.svg", button_svg(
        txt,
        lambda c: f'<g fill="none" stroke="{c}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">{ARROW}</g>',
        primary=True, color="#22c55e"))

print("ok")
