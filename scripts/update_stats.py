"""Genera el panel 'GitHub en números' (claro y oscuro) con datos públicos de GitHub.

Uso: python scripts/update_stats.py            -> consulta GitHub y escribe los SVG
     python scripts/update_stats.py data.json  -> usa datos guardados (para pruebas)

Solo usa la biblioteca estándar. Si algo falla al consultar o leer los datos,
el script termina con error y NO reemplaza las imágenes existentes.
"""

import json
import os
import re
import sys
from datetime import date, datetime, timedelta, timezone
from html import escape
from html.parser import HTMLParser
from pathlib import Path
from urllib.request import Request, urlopen

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_cards import MONO, SANS, THEMES  # noqa: E402  (misma paleta que las tarjetas)

USER = "Jonatan-17"
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "stats"
SKIP_LANG_REPOS = {USER.lower()}  # el repo del perfil no cuenta para lenguajes
LANG_COLORS = ["orange", "blue", "green", "pink", "faint"]
MONTHS = ["ENE", "FEB", "MAR", "ABR", "MAY", "JUN", "JUL", "AGO", "SEP", "OCT", "NOV", "DIC"]


def get(url, api=True):
    headers = {"User-Agent": f"{USER}-profile-stats"}
    if api:
        headers["Accept"] = "application/vnd.github+json"
        token = os.environ.get("GITHUB_TOKEN")
        if token:
            headers["Authorization"] = f"Bearer {token}"
    with urlopen(Request(url, headers=headers), timeout=40) as r:
        body = r.read().decode("utf-8")
    return json.loads(body) if api else body


class CalendarParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.days = {}

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "td" and "data-date" in a and "data-level" in a:
            self.days[a["data-date"]] = int(a["data-level"])


def fetch_data():
    user = get(f"https://api.github.com/users/{USER}")
    repos = get(f"https://api.github.com/users/{USER}/repos?per_page=100&type=owner")
    own = [r for r in repos if not r["fork"]]
    langs = {}
    for r in own:
        if r["name"].lower() in SKIP_LANG_REPOS:
            continue
        for lang, size in get(r["languages_url"]).items():
            langs[lang] = langs.get(lang, 0) + size
    html = get(f"https://github.com/users/{USER}/contributions", api=False)
    cal = CalendarParser()
    cal.feed(html)
    if len(cal.days) < 300:
        raise SystemExit(f"Calendario incompleto ({len(cal.days)} días); no se actualiza el panel.")
    m = re.search(r"([\d,]+)\s+contributions?\s+in the last year", html)
    if not m:
        raise SystemExit("No se encontró el total de contribuciones; no se actualiza el panel.")
    return {
        "public_repos": user["public_repos"],
        "followers": user["followers"],
        "stars": sum(r["stargazers_count"] for r in own),
        "languages": langs,
        "total": int(m.group(1).replace(",", "")),
        "days": cal.days,
        "updated": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
    }


def streaks(days):
    ordered = sorted(days.items())
    longest = run = 0
    for _, level in ordered:
        run = run + 1 if level > 0 else 0
        longest = max(longest, run)
    current = 0
    items = ordered[::-1]
    if items and items[0][1] == 0:  # hoy todavía sin contribuciones no rompe la racha
        items = items[1:]
    for _, level in items:
        if level == 0:
            break
        current += 1
    active = sum(1 for _, level in ordered if level > 0)
    return current, longest, active


def e(text):
    return escape(str(text), quote=True)


def render(data, t):
    w, h = 1200, 560
    current, longest, active = streaks(data["days"])
    kpis = [
        (f'{data["total"]}', "Contribuciones", "en el último año", "orange"),
        (f"{active}", "Días activos", "con al menos una contribución", "blue"),
        (f"{longest}", "Racha más larga", f"días seguidos · actual: {current}", "green"),
        (f'{data["public_repos"]}', "Repos públicos", "proyectos para revisar", "pink"),
    ]
    upd = datetime.strptime(data["updated"], "%Y-%m-%d").strftime("%d/%m/%Y")
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" fill="none" role="img" aria-labelledby="t d">',
         f'<title id="t">GitHub en números</title>',
         f'<desc id="d">{data["total"]} contribuciones en el último año, {active} días activos, racha más larga de {longest} días, '
         f'{data["public_repos"]} repositorios públicos. Actualizado el {upd}.</desc>',
         f'<style>text{{font-family:{SANS}}}.m{{font-family:{MONO}}}</style>',
         f'<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop stop-color="{t["bg1"]}"/><stop offset="1" stop-color="{t["bg2"]}"/></linearGradient></defs>',
         f'<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="20" fill="url(#bg)" stroke="{t["border"]}"/>',
         f'<text class="m" x="44" y="54" font-size="14" fill="{t["faint"]}" letter-spacing="2">GITHUB EN NÚMEROS</text>',
         f'<text class="m" x="{w-44}" y="54" font-size="13" fill="{t["faint"]}" text-anchor="end">Actualizado {upd} · se renueva a diario</text>']
    # KPI tiles
    tw = (w - 88 - 3 * 16) / 4
    for i, (num, label, sub, color) in enumerate(kpis):
        x = 44 + i * (tw + 16)
        s.append(f'<rect x="{x}" y="74" width="{tw}" height="112" rx="14" fill="{t["panel"]}" stroke="{t["border"]}"/>')
        s.append(f'<text x="{x+22}" y="126" font-size="38" font-weight="700" fill="{t[color]}">{e(num)}</text>')
        s.append(f'<text x="{x+22}" y="152" font-size="15" font-weight="600" fill="{t["text"]}">{e(label)}</text>')
        s.append(f'<text x="{x+22}" y="173" font-size="13" fill="{t["muted"]}">{e(sub)}</text>')
    # heatmap
    days = sorted(data["days"].items())[-371:]
    first = date.fromisoformat(days[0][0])
    offset = (first.weekday() + 1) % 7  # columnas empiezan en domingo, como GitHub
    cell, gap = 16, 4
    x0, y0 = 72, 248
    s.append(f'<text x="44" y="222" font-size="17" font-weight="700" fill="{t["text"]}">Actividad del último año</text>')
    seen_months = set()
    alpha = {1: .35, 2: .6, 3: .82, 4: 1}
    for idx, (d, level) in enumerate(days):
        pos = idx + offset
        col, row = pos // 7, pos % 7
        x, y = x0 + col * (cell + gap), y0 + row * (cell + gap)
        if level:
            s.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="4" fill="{t["orange"]}" fill-opacity="{alpha.get(level, 1)}"/>')
        else:
            s.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="4" fill="{t["grid"]}"/>')
        dd = date.fromisoformat(d)
        key = (dd.year, dd.month)
        if dd.day <= 7 and row == 0 and key not in seen_months:
            seen_months.add(key)
            s.append(f'<text class="m" x="{x}" y="{y0-10}" font-size="12" fill="{t["faint"]}">{MONTHS[dd.month-1]}</text>')
    for row, label in ((1, "L"), (3, "X"), (5, "V")):
        s.append(f'<text class="m" x="50" y="{y0 + row*(cell+gap) + 12}" font-size="12" fill="{t["faint"]}">{label}</text>')
    ly = y0 + 7 * (cell + gap) + 22
    s.append(f'<text x="{w-210}" y="{ly}" font-size="12" fill="{t["faint"]}" text-anchor="end">Menos</text>')
    for i, a in enumerate([0, .35, .6, .82, 1]):
        fill = f'fill="{t["grid"]}"' if a == 0 else f'fill="{t["orange"]}" fill-opacity="{a}"'
        s.append(f'<rect x="{w-200 + i*20}" y="{ly-12}" width="14" height="14" rx="3" {fill}/>')
    s.append(f'<text x="{w-92}" y="{ly}" font-size="12" fill="{t["faint"]}">Más</text>')
    # languages
    langs = sorted(data["languages"].items(), key=lambda kv: -kv[1])
    total = sum(v for _, v in langs) or 1
    top = langs[:4]
    rest = sum(v for _, v in langs[4:])
    if rest:
        top.append(("Otros", rest))
    by = ly + 44
    s.append(f'<text x="44" y="{by}" font-size="17" font-weight="700" fill="{t["text"]}">Lenguajes en mis repositorios</text>')
    s.append(f'<text x="{w-44}" y="{by}" font-size="13" fill="{t["muted"]}" text-anchor="end">por volumen de código · repos propios públicos</text>')
    bx, bw, bar_y = 44, w - 88, by + 18
    s.append(f'<clipPath id="bar"><rect x="{bx}" y="{bar_y}" width="{bw}" height="14" rx="7"/></clipPath><g clip-path="url(#bar)">')
    x = bx
    for i, (lang, size) in enumerate(top):
        seg = bw * size / total
        s.append(f'<rect x="{x:.1f}" y="{bar_y}" width="{seg:.1f}" height="14" fill="{t[LANG_COLORS[i]]}"/>')
        x += seg
    s.append("</g>")
    lx = 44
    for i, (lang, size) in enumerate(top):
        pct = 100 * size / total
        s.append(f'<circle cx="{lx+6}" cy="{bar_y+44}" r="6" fill="{t[LANG_COLORS[i]]}"/>')
        s.append(f'<text x="{lx+20}" y="{bar_y+49}" font-size="15" font-weight="600" fill="{t["text"]}">{e(lang)} <tspan font-weight="400" fill="{t["muted"]}">{pct:.1f}%</tspan></text>')
        lx += 220
    s.append("</svg>\n")
    return "\n".join(s)


def main():
    if len(sys.argv) > 1:
        data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    else:
        data = fetch_data()
    OUT.mkdir(parents=True, exist_ok=True)
    for theme, t in THEMES.items():
        (OUT / f"github-{theme}.svg").write_text(render(data, t), encoding="utf-8")
    print(f'Panel actualizado: {data["total"]} contribuciones, {len(data["languages"])} lenguajes.')


if __name__ == "__main__":
    main()
