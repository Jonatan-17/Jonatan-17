"""Genera las tarjetas SVG del perfil (versión clara y oscura).

Uso: python scripts/build_cards.py
Solo usa la biblioteca estándar. Los datos están en PROFILE y PROJECTS.
"""

from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets"

THEMES = {
    "dark": {
        "bg1": "#0B1020", "bg2": "#0F1629", "panel": "#121A2E", "panel2": "#0D1426",
        "border": "#24314D", "grid": "#1A2440", "text": "#F1F5F9", "muted": "#94A3B8",
        "faint": "#5B6B86", "orange": "#FB923C", "blue": "#60A5FA", "green": "#4ADE80",
        "pink": "#F472B6", "chip": "#1A2440", "code_key": "#60A5FA", "code_str": "#FDBA74",
        "code_bool": "#4ADE80", "code_punc": "#94A3B8",
    },
    "light": {
        "bg1": "#FFFFFF", "bg2": "#F6F8FB", "panel": "#FFFFFF", "panel2": "#F1F5F9",
        "border": "#D8E0EA", "grid": "#EEF2F7", "text": "#0F172A", "muted": "#475569",
        "faint": "#94A3B8", "orange": "#EA580C", "blue": "#2563EB", "green": "#16A34A",
        "pink": "#DB2777", "chip": "#EEF2F7", "code_key": "#1D4ED8", "code_str": "#C2410C",
        "code_bool": "#15803D", "code_punc": "#64748B",
    },
}

SANS = "Segoe UI, -apple-system, BlinkMacSystemFont, Helvetica, Arial, sans-serif"
MONO = "SFMono-Regular, Consolas, Menlo, 'Liberation Mono', monospace"

PROFILE = {
    "first": "Jonatan David",
    "last": "Sarmiento",
    "role": "Desarrollador Backend Jr.",
    "focus": "Java · Spring Boot · PostgreSQL",
    "tagline": "Construyo APIs seguras y automatizo procesos con IA.",
    "location": "Piedecuesta, Santander · Colombia",
    "status": "Abierto a oportunidades",
}

PROJECTS = [
    {"slug": "campusdesk", "name": "CampusDesk", "kind": "API REST", "color": "orange",
     "desc": ["Mesa de ayuda de TI con roles, ciclo de", "vida de tickets, SLA y 200+ tests."],
     "chips": ["Spring Boot", "JWT", "PostgreSQL", "Docker"], "note": "Proyecto en equipo"},
    {"slug": "recetas-rag", "name": "Recetas RAG", "kind": "IA · RAG", "color": "blue",
     "desc": ["Escribes tus ingredientes y sugiere", "recetas con búsqueda semántica."],
     "chips": ["Spring Boot", "n8n", "Qdrant", "LLM"], "note": "Proyecto en equipo"},
    {"slug": "smartcity-f", "name": "SmartCity-F", "kind": "IA · Automatización", "color": "green",
     "desc": ["Reportes urbanos con foto y GPS que la", "IA clasifica y prioriza; bot de Telegram."],
     "chips": ["n8n", "Gemini", "Telegram", "Leaflet"], "note": ""},
    {"slug": "SafeGuardian", "name": "SafeGuardian", "kind": "Visión por computador", "color": "pink",
     "desc": ["Detecta fatiga en conductores y alerta", "al supervisor de forma automática."],
     "chips": ["FastAPI", "MediaPipe", "OpenCV", "n8n"], "note": "Hackatón"},
    {"slug": "gamer-jpa", "name": "Gamer JPA", "kind": "Persistencia", "color": "blue",
     "desc": ["Modelo de datos de videojuegos con", "relaciones JPA y pruebas de repositorio."],
     "chips": ["Spring Data JPA", "PostgreSQL", "H2"], "note": ""},
    {"slug": "coworking-db", "name": "CoworkingDB", "kind": "Base de datos", "color": "orange",
     "desc": ["Lógica de negocio dentro de MySQL: 20", "triggers, eventos, funciones y vistas."],
     "chips": ["MySQL 8", "Procedimientos", "Roles"], "note": ""},
]

BUTTONS = [
    {"id": "btn-portafolio", "label": "Portafolio", "sub": "portafolio-jonatan.vercel.app", "icon": "window", "color": "orange"},
    {"id": "btn-linkedin", "label": "LinkedIn", "sub": "Conectemos", "icon": "in", "color": "blue"},
    {"id": "btn-hoja-de-vida", "label": "Hoja de vida", "sub": "Descargar PDF", "icon": "doc", "color": "green"},
    {"id": "btn-carta", "label": "Carta de presentación", "sub": "Leer PDF", "icon": "letter", "color": "pink"},
    {"id": "btn-correo", "label": "Correo", "sub": "jonatandavidsarmientosierra@gmail.com", "icon": "mail", "color": "orange"},
    {"id": "btn-repositorios", "label": "Repositorios", "sub": "Todo mi código", "icon": "code", "color": "blue"},
]

STACK = [
    ("backend", ["Java 21", "Spring Boot", "Spring Security", "JPA / Hibernate", "Python", "FastAPI"]),
    ("datos", ["PostgreSQL", "MySQL", "H2"]),
    ("ia_y_automatizacion", ["n8n", "Gemini", "OpenRouter", "Qdrant", "MediaPipe"]),
    ("frontend", ["HTML", "CSS", "JavaScript"]),
    ("herramientas", ["Git", "Docker", "Gradle", "Maven", "Swagger", "IntelliJ IDEA"]),
]

TIMELINE = [
    ("DIC 2025", "Python", "Lógica y consola", "orange"),
    ("MAR 2026", "Web", "HTML, CSS y JS", "blue"),
    ("JUN 2026", "IA + n8n", "Automatización", "green"),
    ("JUL 2026", "SQL", "MySQL avanzado", "pink"),
    ("AGO 2026", "Java", "POO, JDBC, Maven", "orange"),
    ("OCT 2026", "Spring Boot", "JWT, JPA, RAG", "blue"),
]


def e(text):
    return escape(str(text), quote=True)


def svg_open(w, h, title, desc, t, extra_style=""):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
        f'fill="none" role="img" aria-labelledby="t d">\n'
        f'<title id="t">{e(title)}</title><desc id="d">{e(desc)}</desc>\n'
        f'<style>text{{font-family:{SANS}}}.m{{font-family:{MONO}}}'
        f'.pulse{{animation:p 2.4s ease-in-out infinite}}.blink{{animation:b 1.1s steps(2,end) infinite}}'
        f'@keyframes p{{50%{{opacity:.35}}}}@keyframes b{{50%{{opacity:0}}}}'
        f'@media(prefers-reduced-motion:reduce){{.pulse,.blink{{animation:none}}}}{extra_style}</style>\n'
        f'<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">'
        f'<stop stop-color="{t["bg1"]}"/><stop offset="1" stop-color="{t["bg2"]}"/></linearGradient>'
        f'<linearGradient id="brand" x1="0" x2="1"><stop stop-color="{t["orange"]}"/>'
        f'<stop offset="1" stop-color="{t["blue"]}"/></linearGradient></defs>\n'
    )


def frame(w, h, t, radius=20):
    return (f'<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="{radius}" fill="url(#bg)" '
            f'stroke="{t["border"]}"/>\n')


def dots(x, y, w, h, t, gap=24):
    out = []
    for yy in range(y, y + h, gap):
        for xx in range(x, x + w, gap):
            out.append(f'<circle cx="{xx}" cy="{yy}" r="1.2" fill="{t["grid"]}"/>')
    return "".join(out)


def chip(x, y, label, t, color=None, mono=False, size=14, pad=12, h=28):
    width = int(len(label) * size * (0.62 if mono else 0.56)) + pad * 2
    fg = t[color] if color else t["text"]
    cls = ' class="m"' if mono else ""
    return (f'<rect x="{x}" y="{y}" width="{width}" height="{h}" rx="{h//2}" fill="{t["chip"]}" '
            f'stroke="{t["border"]}"/><text{cls} x="{x + width/2}" y="{y + h/2 + size*0.36}" '
            f'font-size="{size}" fill="{fg}" text-anchor="middle">{e(label)}</text>'), width


# ---------------------------------------------------------------- header

def header(t):
    w, h = 1200, 440
    p = PROFILE
    s = [svg_open(w, h, f'{p["first"]} {p["last"]} — {p["role"]}',
                  f'{p["role"]} enfocado en {p["focus"]}. {p["tagline"]} {p["location"]}.', t)]
    s.append(frame(w, h, t))
    s.append(dots(640, 40, 540, 380, t))
    # left column
    s.append(f'<text class="m" x="56" y="74" font-size="15" fill="{t["faint"]}" letter-spacing="1">~/jonatan-17 <tspan fill="{t["orange"]}">$</tspan> whoami<tspan class="blink" fill="{t["orange"]}"> ▌</tspan></text>')
    s.append(f'<text x="54" y="150" font-size="62" font-weight="700" fill="{t["text"]}" letter-spacing="-1.5">{e(p["first"])}</text>')
    s.append(f'<text x="54" y="218" font-size="62" font-weight="700" fill="url(#brand)" letter-spacing="-1.5">{e(p["last"])}</text>')
    s.append(f'<text x="56" y="266" font-size="24" font-weight="600" fill="{t["text"]}">{e(p["role"])}</text>')
    s.append(f'<text class="m" x="56" y="298" font-size="16" fill="{t["blue"]}">{e(p["focus"])}</text>')
    s.append(f'<text x="56" y="336" font-size="18" fill="{t["muted"]}">{e(p["tagline"])}</text>')
    # status + location pills
    s.append(f'<rect x="56" y="364" width="236" height="36" rx="18" fill="{t["chip"]}" stroke="{t["border"]}"/>')
    s.append(f'<circle class="pulse" cx="78" cy="382" r="6" fill="{t["green"]}"/>')
    s.append(f'<text x="94" y="388" font-size="15" font-weight="600" fill="{t["text"]}">{e(p["status"])}</text>')
    s.append(f'<rect x="304" y="364" width="300" height="36" rx="18" fill="{t["chip"]}" stroke="{t["border"]}"/>')
    s.append(f'<path d="M326 372c-4.4 0-8 3.4-8 7.7 0 5.6 8 12.3 8 12.3s8-6.7 8-12.3c0-4.3-3.6-7.7-8-7.7Zm0 10.6a2.8 2.8 0 1 1 0-5.6 2.8 2.8 0 0 1 0 5.6Z" fill="{t["orange"]}"/>')
    s.append(f'<text x="342" y="388" font-size="15" fill="{t["muted"]}">{e(p["location"])}</text>')
    # right: API response card
    x, y, cw, ch = 660, 56, 484, 328
    s.append(f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" rx="16" fill="{t["panel2"]}" stroke="{t["border"]}"/>')
    s.append(f'<path d="M{x} {y+52}h{cw}" stroke="{t["border"]}"/>')
    s.append(f'<rect x="{x+20}" y="{y+15}" width="48" height="24" rx="6" fill="{t["green"]}" fill-opacity=".16"/>')
    s.append(f'<text class="m" x="{x+44}" y="{y+32}" font-size="13" font-weight="700" fill="{t["green"]}" text-anchor="middle">GET</text>')
    s.append(f'<text class="m" x="{x+80}" y="{y+32}" font-size="14" fill="{t["text"]}">/api/v1/developers/jonatan</text>')
    s.append(f'<text class="m" x="{x+cw-20}" y="{y+32}" font-size="13" fill="{t["green"]}" text-anchor="end">200 OK</text>')
    lines = [
        [("{", "code_punc")],
        [("  ", None), ('"rol"', "code_key"), (": ", "code_punc"), ('"Backend Jr."', "code_str"), (",", "code_punc")],
        [("  ", None), ('"stack"', "code_key"), (": [", "code_punc"), ('"Java"', "code_str"), (", ", "code_punc"),
         ('"Spring Boot"', "code_str"), (",", "code_punc")],
        [("            ", None), ('"PostgreSQL"', "code_str"), ("],", "code_punc")],
        [("  ", None), ('"automatiza"', "code_key"), (": [", "code_punc"), ('"n8n"', "code_str"), (", ", "code_punc"),
         ('"IA"', "code_str"), ("],", "code_punc")],
        [("  ", None), ('"aprende"', "code_key"), (": ", "code_punc"), ('"cada día"', "code_str"), (",", "code_punc")],
        [("  ", None), ('"disponible"', "code_key"), (": ", "code_punc"), ("true", "code_bool")],
        [("}", "code_punc")],
    ]
    ly = y + 90
    for i, line in enumerate(lines):
        spans = "".join(f'<tspan fill="{t[c] if c else t["text"]}">{e(txt)}</tspan>' for txt, c in line)
        s.append(f'<text class="m" x="{x+24}" y="{ly + i*30}" font-size="16" xml:space="preserve">{spans}</text>')
    s.append("</svg>\n")
    return "".join(s)


# ---------------------------------------------------------------- buttons

ICONS = {
    "window": lambda c: f'<rect x="-14" y="-12" width="28" height="24" rx="4" stroke="{c}" stroke-width="2.4"/><path d="M-14 -4h28" stroke="{c}" stroke-width="2.4"/><circle cx="-9" cy="-8" r="1.3" fill="{c}"/><circle cx="-5" cy="-8" r="1.3" fill="{c}"/>',
    "in": lambda c: f'<rect x="-14" y="-14" width="28" height="28" rx="6" stroke="{c}" stroke-width="2.4"/><path d="M-7 -2v10M-7 -7.5v.5M-1 8v-6a4 4 0 0 1 8 0v6" stroke="{c}" stroke-width="2.6" stroke-linecap="round"/>',
    "doc": lambda c: f'<path d="M-10 -15h13l8 8v22h-21z" stroke="{c}" stroke-width="2.4" stroke-linejoin="round"/><path d="M3 -15v8h8M-5 2h11M-5 8h11" stroke="{c}" stroke-width="2.2" stroke-linecap="round"/>',
    "letter": lambda c: f'<path d="M-14 -6v18h28V-6" stroke="{c}" stroke-width="2.4" stroke-linejoin="round"/><path d="M-9 -2v-12h18v12" stroke="{c}" stroke-width="2.2"/><path d="M-5 -9h10M-5 -4h7" stroke="{c}" stroke-width="2" stroke-linecap="round"/><path d="M-14 -6l14 10 14-10" stroke="{c}" stroke-width="2.4" stroke-linejoin="round"/>',
    "mail": lambda c: f'<rect x="-15" y="-11" width="30" height="22" rx="4" stroke="{c}" stroke-width="2.4"/><path d="M-13 -8l13 10 13-10" stroke="{c}" stroke-width="2.4" stroke-linejoin="round"/>',
    "code": lambda c: f'<path d="M-6 -10l-9 10 9 10M6 -10l9 10-9 10" stroke="{c}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>',
}


def button(b, t):
    w, h = 590, 96
    c = t[b["color"]]
    s = [svg_open(w, h, b["label"], f'{b["label"]}: {b["sub"]}', t)]
    s.append(frame(w, h, t, 18))
    s.append(f'<rect x="20" y="20" width="56" height="56" rx="14" fill="{c}" fill-opacity=".14"/>')
    s.append(f'<g transform="translate(48 48)">{ICONS[b["icon"]](c)}</g>')
    s.append(f'<text x="96" y="45" font-size="22" font-weight="700" fill="{t["text"]}">{e(b["label"])}</text>')
    sub_size = 15 if len(b["sub"]) < 34 else 14
    s.append(f'<text class="m" x="96" y="71" font-size="{sub_size}" fill="{t["muted"]}">{e(b["sub"])}</text>')
    s.append(f'<path d="M{w-52} {h/2+9}l18-18M{w-48} {h/2-9}h14v14" stroke="{c}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>')
    s.append("</svg>\n")
    return "".join(s)


# ---------------------------------------------------------------- value strip

def value(t):
    w, h = 1200, 250
    cols = [
        ("orange", "01", "APIs seguras", ["REST con Spring Boot, JWT, roles,", "validación y manejo de errores."]),
        ("blue", "02", "Datos bien modelados", ["PostgreSQL y MySQL, JPA/Hibernate,", "triggers, procedimientos y vistas."]),
        ("green", "03", "Automatización con IA", ["Flujos en n8n, RAG con Qdrant,", "visión por computador y bots."]),
    ]
    s = [svg_open(w, h, "Lo que aporto", "APIs seguras, datos bien modelados y automatización con IA.", t)]
    s.append(frame(w, h, t))
    s.append(f'<text class="m" x="44" y="54" font-size="14" fill="{t["faint"]}" letter-spacing="2">LO QUE APORTO A UN EQUIPO</text>')
    colw = (w - 88 - 40) / 3
    for i, (color, num, title, desc) in enumerate(cols):
        x = 44 + i * (colw + 20)
        s.append(f'<rect x="{x}" y="76" width="{colw}" height="140" rx="14" fill="{t["panel"]}" stroke="{t["border"]}"/>')
        s.append(f'<rect x="{x}" y="76" width="5" height="140" rx="2.5" fill="{t[color]}"/>')
        s.append(f'<text class="m" x="{x+28}" y="112" font-size="14" fill="{t[color]}">{num}</text>')
        s.append(f'<text x="{x+60}" y="113" font-size="22" font-weight="700" fill="{t["text"]}">{e(title)}</text>')
        for j, line in enumerate(desc):
            s.append(f'<text x="{x+28}" y="{152 + j*26}" font-size="16" fill="{t["muted"]}">{e(line)}</text>')
    s.append("</svg>\n")
    return "".join(s)


# ---------------------------------------------------------------- project cards

def project(pj, t):
    w, h = 590, 250
    c = t[pj["color"]]
    s = [svg_open(w, h, pj["name"], f'{pj["name"]} ({pj["kind"]}): {" ".join(pj["desc"])} Tecnologías: {", ".join(pj["chips"])}.', t)]
    s.append(frame(w, h, t, 18))
    s.append(f'<rect x="28" y="28" width="{int(len(pj["kind"])*7.4)+28}" height="26" rx="13" fill="{c}" fill-opacity=".15"/>')
    s.append(f'<text class="m" x="42" y="46" font-size="13" font-weight="700" fill="{c}">{e(pj["kind"].upper())}</text>')
    if pj["note"]:
        s.append(f'<text x="{w-28}" y="46" font-size="14" fill="{t["faint"]}" text-anchor="end">{e(pj["note"])}</text>')
    s.append(f'<text x="28" y="96" font-size="28" font-weight="700" fill="{t["text"]}">{e(pj["name"])}</text>')
    s.append(f'<text class="m" x="28" y="122" font-size="14" fill="{t["faint"]}">github.com/Jonatan-17/{e(pj["slug"])}</text>')
    for j, line in enumerate(pj["desc"]):
        s.append(f'<text x="28" y="{156 + j*24}" font-size="17" fill="{t["muted"]}">{e(line)}</text>')
    x = 28
    for label in pj["chips"]:
        piece, cw = chip(x, 198, label, t, size=13, pad=11, h=26)
        s.append(piece)
        x += cw + 8
    s.append(f'<path d="M{w-46} 112l14-14M{w-43} 98h11v11" stroke="{c}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>')
    s.append("</svg>\n")
    return "".join(s)


# ---------------------------------------------------------------- stack.yml

def stack(t):
    w = 1200
    h = 82 + len(STACK) * 58 + 12
    s = [svg_open(w, h, "Stack técnico", "; ".join(f'{k}: {", ".join(v)}' for k, v in STACK), t)]
    s.append(frame(w, h, t))
    s.append(f'<path d="M0 64h{w}" stroke="{t["border"]}"/>')
    for i, col in enumerate(["#FF5F57", "#FEBC2E", "#28C840"]):
        s.append(f'<circle cx="{36 + i*20}" cy="32" r="6" fill="{col}"/>')
    s.append(f'<text class="m" x="{w/2}" y="38" font-size="15" fill="{t["muted"]}" text-anchor="middle">stack.yml</text>')
    s.append(f'<text class="m" x="{w-32}" y="38" font-size="13" fill="{t["faint"]}" text-anchor="end">YAML</text>')
    y = 108
    for n, (key, items) in enumerate(STACK, start=1):
        s.append(f'<text class="m" x="36" y="{y}" font-size="14" fill="{t["faint"]}" text-anchor="end">{n:02d}</text>')
        s.append(f'<text class="m" x="56" y="{y}" font-size="18" fill="{t["code_key"]}">{e(key)}<tspan fill="{t["code_punc"]}">:</tspan></text>')
        x = 300
        for item in items:
            piece, cw = chip(x, y - 20, item, t, color="code_str", mono=True, size=14, pad=12, h=30)
            s.append(piece)
            x += cw + 10
        y += 58
    s.append("</svg>\n")
    return "".join(s)


# ---------------------------------------------------------------- timeline

def timeline(t):
    w, h = 1200, 300
    s = [svg_open(w, h, "Mi camino", "Aprendizaje en Campuslands: " + "; ".join(f"{d} {n} ({x})" for d, n, x, _ in TIMELINE), t)]
    s.append(frame(w, h, t))
    s.append(f'<text class="m" x="44" y="54" font-size="14" fill="{t["faint"]}" letter-spacing="2">MI CAMINO · CAMPUSLANDS</text>')
    s.append(f'<text x="44" y="92" font-size="26" font-weight="700" fill="{t["text"]}">De Python a Spring Boot + IA en menos de un año.</text>')
    x0, x1, ly = 110, w - 110, 172
    s.append(f'<path d="M{x0} {ly}H{x1}" stroke="url(#brand)" stroke-width="4" stroke-linecap="round"/>')
    step = (x1 - x0) / (len(TIMELINE) - 1)
    for i, (date, name, detail, color) in enumerate(TIMELINE):
        x = x0 + i * step
        s.append(f'<circle cx="{x}" cy="{ly}" r="11" fill="{t["bg1"]}" stroke="{t[color]}" stroke-width="4"/>')
        s.append(f'<text class="m" x="{x}" y="{ly-26}" font-size="13" fill="{t["faint"]}" text-anchor="middle">{e(date)}</text>')
        s.append(f'<text x="{x}" y="{ly+44}" font-size="19" font-weight="700" fill="{t["text"]}" text-anchor="middle">{e(name)}</text>')
        s.append(f'<text x="{x}" y="{ly+70}" font-size="15" fill="{t["muted"]}" text-anchor="middle">{e(detail)}</text>')
    s.append(f'<circle class="pulse" cx="{x1}" cy="{ly}" r="5" fill="{t[TIMELINE[-1][3]]}"/>')
    s.append("</svg>\n")
    return "".join(s)


# ---------------------------------------------------------------- contact

def contact(t):
    w, h = 1200, 260
    s = [svg_open(w, h, "Conectemos", "¿Tienes una vacante o un proyecto? Escríbeme: jonatandavidsarmientosierra@gmail.com", t)]
    s.append(frame(w, h, t))
    s.append(dots(760, 30, 420, 210, t))
    s.append(f'<text class="m" x="48" y="62" font-size="14" fill="{t["faint"]}" letter-spacing="2">POST /contacto</text>')
    s.append(f'<text x="46" y="122" font-size="40" font-weight="700" fill="{t["text"]}">¿Tienes una vacante o un proyecto?</text>')
    s.append(f'<text x="46" y="166" font-size="40" font-weight="700" fill="url(#brand)">Hablemos.</text>')
    s.append(f'<text class="m" x="48" y="214" font-size="17" fill="{t["muted"]}">jonatandavidsarmientosierra@gmail.com</text>')
    cx, cy = 1010, 130
    s.append(f'<circle cx="{cx}" cy="{cy}" r="78" stroke="{t["border"]}" stroke-width="2" fill="{t["panel"]}"/>')
    s.append(f'<circle class="pulse" cx="{cx}" cy="{cy}" r="98" stroke="{t["orange"]}" stroke-opacity=".35" stroke-width="2"/>')
    s.append(f'<g transform="translate({cx} {cy}) scale(2.6)">{ICONS["mail"](t["orange"])}</g>')
    s.append("</svg>\n")
    return "".join(s)


def write(name, builder, *args):
    for theme, t in THEMES.items():
        path = OUT / f"{name}-{theme}.svg"
        path.write_text(builder(*args, t), encoding="utf-8")


def main():
    (OUT / "projects").mkdir(parents=True, exist_ok=True)
    (OUT / "buttons").mkdir(parents=True, exist_ok=True)
    write("header", header)
    write("value", value)
    write("stack", stack)
    write("timeline", timeline)
    write("contact", contact)
    for b in BUTTONS:
        write(f'buttons/{b["id"]}', button, b)
    for pj in PROJECTS:
        write(f'projects/{pj["slug"].lower()}', project, pj)
    print("Tarjetas generadas en", OUT)


if __name__ == "__main__":
    main()
