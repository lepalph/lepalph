"""Génère les images du README de profil (terminal + ASCII), en clair et en sombre, dans assets/.
Usage : uv run --with pyfiglet python gen.py"""
import html
from pathlib import Path

import pyfiglet

A = Path(__file__).parent / "assets"
A.mkdir(exist_ok=True)
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'DejaVu Sans Mono', monospace"
SANS = "system-ui, -apple-system, 'Segoe UI', Helvetica, Arial, sans-serif"
CW = 0.602  # largeur d'un caractère mono en em (Menlo, SF Mono, Consolas tombent à ±2 %)

T = {
    "dark": dict(win="#0d1117", bar="#161b22", line="#30363d", ink="#e6edf3", dim="#8b949e",
                 g1="#7ee787", g2="#56d4dd", prompt="#7ee787", dir="#79c0ff", inset="#010409", art="#c9d1d9"),
    "light": dict(win="#ffffff", bar="#f6f8fa", line="#d0d7de", ink="#1f2328", dim="#59636e",
                  g1="#1a7f37", g2="#0a6c7a", prompt="#1a7f37", dir="#0969da", inset="#f6f8fa", art="#24292f"),
}
STYLE = """<style>
  .c { animation: b 1.1s steps(1) infinite }
  @keyframes b { 50% { opacity: 0 } }
  @media (prefers-reduced-motion: reduce) { .c { animation: none } }
</style>"""


def esc(s):
    return html.escape(s, quote=False)


def lines(x, y, rows, size, lh, fill, extra=""):
    """Bloc de texte mono, une <tspan> par ligne (espaces conservés)."""
    sp = "".join(f'<tspan x="{x}" dy="{0 if i == 0 else lh}">{esc(r)}</tspan>' for i, r in enumerate(rows))
    return f'<text x="{x}" y="{y}" font-family="{MONO}" font-size="{size}" fill="{fill}" xml:space="preserve" {extra}>{sp}</text>'


def ascii_cells(art, x0, y0, cw, ch, t):
    """Dessine l'ASCII art cellule par cellule : █ = carré plein, traits doubles = ombre fine.
    Aucun joint entre caractères, quel que soit le moteur de rendu ou la police."""
    full, shade = [], []
    for r, line in enumerate(art):
        for c, k in enumerate(line):
            x, y = x0 + c * cw, y0 + r * ch
            mx, my = x + cw / 2, y + ch / 2
            if k == "█":
                full.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{cw + .4:.1f}" height="{ch + .4:.1f}"/>')
            elif k in "═╗╔╝╚║":
                d = {"═": f"M{x:.1f} {my:.1f}h{cw}", "║": f"M{mx:.1f} {y:.1f}v{ch}",
                     "╗": f"M{x:.1f} {my:.1f}H{mx:.1f}V{y + ch:.1f}", "╔": f"M{x + cw:.1f} {my:.1f}H{mx:.1f}V{y + ch:.1f}",
                     "╝": f"M{x:.1f} {my:.1f}H{mx:.1f}V{y:.1f}", "╚": f"M{x + cw:.1f} {my:.1f}H{mx:.1f}V{y:.1f}"}[k]
                shade.append(f'<path d="{d}"/>')
    return (f'<g fill="url(#g)">{"".join(full)}</g>'
            f'<g fill="none" stroke="url(#g)" stroke-width="1.6" opacity=".55">{"".join(shade)}</g>')


INFO = [("role", "AI engineer · IT consultant"), ("school", "EPITA, class of 2028"), ("based", "Paris"),
        ("stack", "TypeScript · Rust · Swift · Python"), ("focus", "automation · AI · web apps")]


def banner():
    art = [l.rstrip() for l in pyfiglet.figlet_format("RALPH BITAR", font="ansi_shadow", width=200).splitlines() if l.strip()]
    W, H, X = 1200, 372, 56
    for mode, t in T.items():
        info = [f'<text x="772" y="112" font-family="{MONO}" font-size="16" font-weight="700" fill="{t["prompt"]}">ralph<tspan fill="{t["dim"]}">@</tspan>lepalph</text>',
                f'<rect x="772" y="124" width="{13 * 16 * CW:.0f}" height="1.5" fill="{t["line"]}"/>']
        for i, (k, v) in enumerate(INFO):
            info.append(f'<text x="772" y="{156 + i * 27}" font-family="{MONO}" font-size="14.5" xml:space="preserve">'
                        f'<tspan fill="{t["dir"]}" font-weight="600">{k:<8}</tspan><tspan fill="{t["ink"]}">{esc(v)}</tspan></text>')
        cmd = 254
        body = [
            ascii_cells(art, X, 92, 8.4, 17, t),
            *info,
            f'<text x="{X}" y="{cmd}" font-family="{MONO}" font-size="17" xml:space="preserve"><tspan fill="{t["prompt"]}">❯</tspan><tspan fill="{t["ink"]}"> ls ~/projects</tspan></text>',
            f'<text x="{X}" y="{cmd + 30}" font-family="{MONO}" font-size="17" font-weight="600" fill="{t["dir"]}" xml:space="preserve">notch-ram/   tactile-touch-bar/   CVLove/</text>',
            f'<text x="{X}" y="{cmd + 70}" font-family="{MONO}" font-size="17" fill="{t["prompt"]}">❯</text>',
            f'<rect class="c" x="{X + 17 * CW * 2:.0f}" y="{cmd + 55}" width="{17 * CW:.0f}" height="20" fill="{t["ink"]}"/>',
        ]
        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="Ralph Bitar, AI engineer and IT consultant in Paris, EPITA">
{STYLE}
<defs><linearGradient id="g" gradientUnits="userSpaceOnUse" x1="{X}" y1="0" x2="{X + 680}" y2="0"><stop offset="0" stop-color="{t['g1']}"/><stop offset="1" stop-color="{t['g2']}"/></linearGradient></defs>
<rect x="0.75" y="0.75" width="{W - 1.5}" height="{H - 1.5}" rx="14" fill="{t['win']}" stroke="{t['line']}" stroke-width="1.5"/>
<path d="M0.75 14.75 A14 14 0 0 1 14.75 0.75 H{W - 14.75} A14 14 0 0 1 {W - 0.75} 14.75 V44 H0.75 Z" fill="{t['bar']}"/>
<rect x="0.75" y="44" width="{W - 1.5}" height="1.5" fill="{t['line']}"/>
<circle cx="30" cy="22.5" r="7" fill="#ff5f57"/><circle cx="54" cy="22.5" r="7" fill="#febc2e"/><circle cx="78" cy="22.5" r="7" fill="#28c840"/>
<text x="{W / 2}" y="28" text-anchor="middle" font-family="{MONO}" font-size="14" fill="{t['dim']}">ralph@lepalph: ~</text>
{chr(10).join(body)}
</svg>"""
        (A / f"banner-{mode}.svg").write_text(svg)


ART = {
    "notch-ram": dict(w=29, rows=["██████████████░░░░░░░░   62 %", "---", "Safari             1.46 GB  ×",
                                  "kitty              0.96 GB  ×", "Xcode              0.83 GB  ×"]),
    "tactile": dict(w=44, rows=["[ esc ]  [ ▸ play ]  [ ⌘ build ]", "", "vol  ━━━━━━━━━━━━━━━━━●━━━━━━━━━━━━━━━━━━━"]),
    "cvlove": dict(w=24, rows=["CAMILLE MARCHAND", "Product designer · Lyon", "---", "▪ Experience   ·········",
                               "▪ Skills       ███████░░", "▪ Languages    FR EN ES"], tail="──▸ cv.pdf"),
}
FS, LH = 15, 21


def art_svg(spec, cx, cy, t):
    cw = FS * CW
    w, rows = spec["w"], spec["rows"]
    bw, bh = (w + 2) * cw, len(rows) * LH + 18
    x0, y0 = cx - bw / 2 - (len(spec.get("tail", "")) * cw / 2 + 10 if "tail" in spec else 0), cy - bh / 2
    out = [f'<rect x="{x0:.1f}" y="{y0:.1f}" width="{bw:.1f}" height="{bh:.1f}" rx="6" fill="none" stroke="{t["art"]}" stroke-width="1.4" opacity=".9"/>']
    for i, r in enumerate(rows):
        y = y0 + 9 + i * LH
        if r == "---":
            out.append(f'<rect x="{x0 + cw:.1f}" y="{y + LH / 2 - .7:.1f}" width="{bw - 2 * cw:.1f}" height="1.4" fill="{t["art"]}" opacity=".5"/>')
        elif r:
            out.append(f'<text x="{x0 + cw:.1f}" y="{y + LH * .72:.1f}" font-family="{MONO}" font-size="{FS}" fill="{t["art"]}" xml:space="preserve">{esc(r)}</text>')
    if "tail" in spec:
        out.append(f'<text x="{x0 + bw + 14:.1f}" y="{y0 + bh - 6:.1f}" font-family="{MONO}" font-size="{FS}" fill="{t["prompt"]}" xml:space="preserve">{esc(spec["tail"])}</text>')
    return "\n".join(out)


def row(slug, path, name, desc, lang, color, meta, art):
    W, H = 1200, 230
    for mode, t in T.items():
        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(name)}: {esc(desc)}">
<rect x="0.75" y="0.75" width="{W - 1.5}" height="{H - 1.5}" rx="14" fill="{t['win']}" stroke="{t['line']}" stroke-width="1.5"/>
<rect x="630" y="16" width="554" height="{H - 32}" rx="10" fill="{t['inset']}"/>
<text x="40" y="58" font-family="{MONO}" font-size="15" fill="{t['dim']}" xml:space="preserve"><tspan fill="{t['prompt']}">❯</tspan> cd ~/projects/{esc(path)}</text>
<text x="40" y="106" font-family="{SANS}" font-size="38" font-weight="700" letter-spacing="-0.8" fill="{t['ink']}">{esc(name)}</text>
<text x="40" y="142" font-family="{SANS}" font-size="19" fill="{t['dim']}">{esc(desc)}</text>
<circle cx="47" cy="185" r="7" fill="{color}"/>
<text x="62" y="190" font-family="{SANS}" font-size="16" fill="{t['dim']}" xml:space="preserve">{esc(lang)}    {esc(meta)}</text>
{art_svg(art, 907, H / 2, t)}
</svg>"""
        (A / f"{slug}-{mode}.svg").write_text(svg)


banner()
row("notch-ram", "notch-ram", "notch-ram", "A RAM gauge that lives in the MacBook notch.", "Swift", "#F05138", "v0.1.0 · macOS · MIT", ART["notch-ram"])
row("tactile", "tactile-touch-bar", "tactile-touch-bar", "A Touch Bar you set up in one TOML file.", "Rust", "#dea584", "v0.4.1 · macOS · MIT", ART["tactile"])
row("cvlove", "CVLove", "CVLove", "Free CV builder. Your data never leaves the browser.", "TypeScript", "#3178c6", "7 languages · 36 templates · MIT", ART["cvlove"])
print("ok", sorted(p.name for p in A.glob("*.svg")))
