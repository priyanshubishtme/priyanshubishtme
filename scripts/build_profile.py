from __future__ import annotations

import base64
import html
import json
import re
import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
NAVY = "#070b16"
BLUE = "#247bff"
RED = "#ff354f"
WHITE = "#f4f6fb"
MUTED = "#9da8bc"


def data(path: Path, mime: str) -> str:
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode()


def svg(name: str, width: int, height: int, body: str, title: str) -> str:
    display = data(ASSETS / "fonts/BarlowCondensed-ExtraBold.woff2", "font/woff2")
    mono = data(ASSETS / "fonts/JetBrainsMono-Regular.woff2", "font/woff2")
    return f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="{name}-title {name}-desc">
<title id="{name}-title">{html.escape(title)}</title><desc id="{name}-desc">{html.escape(title)} for Priyanshu Bisht. Built from the profile README and embedded assets.</desc>
<defs>
 <linearGradient id="{name}-edge" x1="0" y1="0" x2="1" y2="1"><stop stop-color="{BLUE}"/><stop offset=".55" stop-color="#39476a"/><stop offset="1" stop-color="{RED}"/></linearGradient>
 <linearGradient id="{name}-glow" x1="0" y1="0" x2="1" y2="0"><stop stop-color="{BLUE}" stop-opacity=".25"/><stop offset="1" stop-color="{RED}" stop-opacity=".2"/></linearGradient>
 <linearGradient id="{name}-metal" x1="0" y1="0" x2="1" y2="0"><stop stop-color="#536078"/><stop offset=".22" stop-color="#dce4f0"/><stop offset=".48" stop-color="#7d8aa1"/><stop offset=".72" stop-color="#f2f5fa"/><stop offset="1" stop-color="#657188"/></linearGradient>
 <pattern id="{name}-dots" width="18" height="18" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="1" fill="#8092b5" opacity=".15"/></pattern>
 <style><![CDATA[
 @font-face{{font-family:BC;src:url('{display}') format('woff2');font-weight:800}}
 @font-face{{font-family:JB;src:url('{mono}') format('woff2');font-weight:400}}
 text{{fill:{WHITE};font-family:Arial,sans-serif}} .display{{font-family:BC,'Arial Narrow',sans-serif;font-weight:800;letter-spacing:.2px}} .mono{{font-family:JB,monospace}} .muted{{fill:{MUTED}}}
 .in{{animation:rise .8s cubic-bezier(.2,.8,.2,1) both}} .in2{{animation:rise .8s .16s cubic-bezier(.2,.8,.2,1) both}} .in3{{animation:rise .8s .3s cubic-bezier(.2,.8,.2,1) both}}
 @keyframes rise{{from{{opacity:0;transform:translateY(24px)}}to{{opacity:1;transform:translateY(0)}}}}
 @media(prefers-reduced-motion:reduce){{.in,.in2,.in3{{animation:none;opacity:1;transform:none}} .motion{{display:none}} .orbit-motion animateTransform{{display:none}} .static{{display:inline}} .slide{{display:none!important}} .reduced-type{{clip-path:none!important}}}}
 ]]></style>
 <filter id="{name}-shadow" x="-30%" y="-30%" width="160%" height="170%"><feGaussianBlur in="SourceAlpha" stdDeviation="14"/><feOffset dy="12"/><feComponentTransfer><feFuncA type="linear" slope=".28"/></feComponentTransfer><feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs>
<rect width="{width}" height="{height}" rx="28" fill="{NAVY}"/><rect width="{width}" height="{height}" rx="28" fill="url(#{name}-dots)"/>
<rect x="1" y="1" width="{width-2}" height="{height-2}" rx="27" fill="none" stroke="url(#{name}-edge)" stroke-opacity=".72"/>
{body}</svg>'''


def write_svg(name: str, width: int, height: int, body: str, title: str) -> None:
    (ASSETS / name).write_text(svg(name.replace(".", "-"), width, height, body, title), encoding="utf-8")


def png_href(file: str) -> str:
    return data(ASSETS / file, "image/png")


def build() -> None:
    portrait = png_href("id.png")
    write_svg("hero.svg", 960, 440, f'''
<text x="54" y="60" class="mono" font-size="14" fill="{BLUE}">PROFILE / 01 <tspan fill="{MUTED}">— FRONTEND DEVELOPER &amp; BUILDER</tspan></text>
<defs><clipPath id="hero-svg-type-clip"><rect x="50" y="95" width="220" height="42"><animate attributeName="width" values="0;18;36;54;72;90;108;126;144;162;180;198;220" keyTimes="0;.08;.16;.24;.32;.4;.48;.56;.64;.72;.8;.88;1" calcMode="discrete" dur="1.3s" repeatCount="1" fill="freeze" begin="0s"/></rect></clipPath><clipPath id="hero-svg-name-mask"><rect x="38" y="104" width="470" height="211"><animateTransform attributeName="transform" type="translate" values="0 240;0 0" keyTimes="0;1" dur="1.1s" fill="freeze" begin="0s"/></rect></clipPath></defs>
<text x="52" y="128" class="display in reduced-type" font-size="29" clip-path="url(#hero-svg-type-clip)">HELLO, WORLD.</text>
<g class="reduced-type" clip-path="url(#hero-svg-name-mask)"><text x="48" y="220" class="display in2" font-size="82">PRIYANSHU</text>
<text x="49" y="291" class="display in2" font-size="82" fill="{BLUE}">BISHT</text></g>
<rect x="49" y="306" width="390" height="4" rx="2" fill="url(#hero-svg-edge)"/>
<text x="54" y="344" class="mono" font-size="16" fill="{BLUE}">I'M A</text>
<g class="motion"><text x="122" y="344" class="mono" font-size="16">FRONTEND DEVELOPER<animate attributeName="opacity" values="1;1;0;0;0;0;1" keyTimes="0;.24;.25;.49;.5;.99;1" dur="8s" repeatCount="indefinite" begin="0s"/></text><text x="122" y="344" class="mono" font-size="16" opacity="0">PRODUCT BUILDER<animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="0;.24;.25;.49;.5;1" dur="8s" repeatCount="indefinite" begin="0s"/></text><text x="122" y="344" class="mono" font-size="16" opacity="0">CREATOR<animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="0;.49;.5;.74;.75;1" dur="8s" repeatCount="indefinite" begin="0s"/></text><text x="122" y="344" class="mono" font-size="16" opacity="0">AUTONOMOUS SYSTEMS BUILDER<animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;.74;.75;.99;1" dur="8s" repeatCount="indefinite" begin="0s"/></text></g><text x="122" y="344" class="mono static" font-size="16" display="none">FRONTEND DEVELOPER</text>
<text x="54" y="378" font-size="14" fill="{MUTED}">Turning ideas into scalable experiences.</text>
<g transform="translate(54 410)"><circle cx="5" cy="-5" r="4" fill="{RED}"/><text x="18" y="0" font-size="12" fill="{MUTED}">Curious about tech, people, ideas &amp; life</text><text x="340" y="0" class="mono" font-size="11" fill="{MUTED}">PORTFOLIO ↗</text></g>
<circle cx="744" cy="240" r="160" fill="url(#hero-svg-glow)"/><circle cx="744" cy="240" r="137" fill="none" stroke="url(#hero-svg-edge)" stroke-opacity=".6" stroke-width="1.5"/>
<image href="{portrait}" x="600" y="65" width="290" height="340" preserveAspectRatio="xMidYMid meet"/>
<g transform="translate(600 382)"><rect width="290" height="34" rx="17" fill="#10192a" stroke="#34415c"/><circle cx="18" cy="17" r="4" fill="{BLUE}"/><text x="31" y="21" class="mono" font-size="11">BUILDER · CREATOR · 19</text></g>
''', "Priyanshu Bisht — frontend developer and builder")

    slides = []
    topics = [
        ("01", "PRODUCTS THAT FEEL", "EFFORTLESS", "Frontend craft · from interface to checkout"),
        ("02", "MACHINES THAT", "LEARN", "Arena Self-Driving · tabular SARSA"),
        ("03", "IDEAS, PEOPLE", "& LIFE", "Curiosity that keeps the next build moving"),
    ]
    for i, (num, line1, line2, sub) in enumerate(topics):
        opacity = "1" if i == 0 else "0"
        values = ["1;1;0;0;0;0;1", "0;0;1;1;0;0;0", "0;0;0;0;1;1;0"][i]
        slides.append(f'''<g class="slide slide-{i}" opacity="{opacity}"><text x="542" y="124" class="mono" font-size="12" fill="{BLUE}">INTEREST / {num}</text><text x="542" y="178" class="display" font-size="36">{html.escape(line1)}</text><text x="542" y="222" class="display" font-size="36" fill="{RED}">{html.escape(line2)}</text><text x="542" y="260" font-size="14" fill="{MUTED}">{html.escape(sub)}</text><animate attributeName="opacity" values="{values}" keyTimes="0;.32;.34;.65;.67;.98;1" dur="12s" repeatCount="indefinite" begin="0s"/></g>''')
    write_svg("about-life.svg", 960, 370, f'''
<text x="50" y="56" class="mono" font-size="13" fill="{BLUE}">PROFILE / 02 — WHAT I BRING</text><text x="50" y="108" class="display" font-size="38">MAKE THE COMPLEX</text><text x="50" y="149" class="display" font-size="38" fill="{BLUE}">FEEL SIMPLE.</text>
<rect x="42" y="178" width="420" height="148" rx="20" fill="#0d1423" stroke="#222e45"/>
<g font-size="14"><circle cx="70" cy="216" r="4" fill="{BLUE}"/><text x="88" y="221">Frontend development</text><circle cx="70" cy="252" r="4" fill="{RED}"/><text x="88" y="257">Full-stack product building</text><circle cx="70" cy="288" r="4" fill="{BLUE}"/><text x="88" y="293">Autonomous systems · SARSA</text></g>
<rect x="500" y="78" width="410" height="248" rx="22" fill="#0d1423" stroke="#2a3550"/>{''.join(slides)}
<g class="motion" transform="translate(542 298)"><rect width="96" height="3" rx="2" fill="#303a50"/><rect width="0" height="3" rx="2" fill="{BLUE}"><animate attributeName="width" values="0;96;96;0" keyTimes="0;.32;.66;1" dur="12s" repeatCount="indefinite" begin="0s"/></rect><rect x="112" width="96" height="3" rx="2" fill="#303a50"/><rect x="112" width="0" height="3" rx="2" fill="{RED}"><animate attributeName="width" values="0;0;96;96;0" keyTimes="0;.32;.34;.65;1" dur="12s" repeatCount="indefinite" begin="0s"/></rect><rect x="224" width="96" height="3" rx="2" fill="#303a50"/><rect x="224" width="0" height="3" rx="2" fill="{BLUE}"><animate attributeName="width" values="0;0;0;96;96;0" keyTimes="0;.32;.34;.65;.98;1" dur="12s" repeatCount="indefinite" begin="0s"/></rect></g>
<g class="static" display="none"><text x="542" y="124" class="mono" font-size="12" fill="{BLUE}">INTEREST / 01</text><text x="542" y="178" class="display" font-size="36">PRODUCTS THAT FEEL</text><text x="542" y="222" class="display" font-size="36" fill="{RED}">EFFORTLESS</text></g>
''', "About Priyanshu: product craft, autonomous systems and curiosity")

    labels = ["Java", "Python", "JavaScript", "TypeScript", "React", "Next.js", "Node.js", "Express", "MongoDB", "MySQL", "Git", "GitHub", "Figma", "Postman", "FastAPI", "Gymnasium"]
    import xml.etree.ElementTree as ET
    def icon_path(slug: str) -> str:
        return ET.parse(ASSETS / f"icons/{slug}.svg").getroot().find("{http://www.w3.org/2000/svg}path").attrib["d"]
    orbit_labels = ["Python", "JavaScript", "TypeScript", "React", "Next.js", "Node.js", "Express", "MongoDB", "MySQL", "Git", "GitHub", "Figma"]
    orbit_slugs = ["python", "javascript", "typescript", "react", "nextdotjs", "nodedotjs", "express", "mongodb", "mysql", "git", "github", "figma"]
    orbit_items = [[], [], []]
    for i, (label, slug) in enumerate(zip(orbit_labels, orbit_slugs)):
        import math
        ring = i % 3
        rx, ry, tilt = [(356, 75, -10), (292, 54, 12), (222, 38, -20)][ring]
        angle = (i // 3 / 4) * 6.28318 + math.radians([0, 30, 60][ring])
        # The parent group scales a circle into the visible ellipse. The inner
        # inverse scale keeps each icon round while it follows that ellipse.
        x, y = rx * math.cos(angle), rx * math.sin(angle)
        inverse_y = rx / ry
        orbit_items[ring].append(f'<g transform="translate({x:.1f} {y:.1f})"><g transform="scale(1 {inverse_y:.4f})"><circle r="22" fill="#101a2c" stroke="{BLUE if i%2==0 else RED}" stroke-opacity=".65"/><path d="{icon_path(slug)}" transform="translate(-8 -8) scale(.67)" fill="{WHITE}"/><title>{html.escape(label)}</title></g></g>')
    chips = []
    for i, label in enumerate(labels):
        x = 52 + (i % 8) * 108
        y = 382 + (i // 8) * 38
        chips.append(f'<g><rect x="{x}" y="{y}" width="96" height="27" rx="13.5" fill="#101a2c" stroke="#26334c"/><text x="{x+48}" y="{y+18}" text-anchor="middle" font-size="11">{html.escape(label)}</text></g>')
    ring_specs = [(356, 75, -10), (292, 54, 12), (222, 38, -20)]
    orbit_svg_markup = "".join(
        f'<g transform="translate(480 250) rotate({tilt}) scale(1 {ry/rx:.4f})">{"".join(items)}</g>'
        for items, (rx, ry, tilt) in zip(orbit_items, ring_specs)
    )
    write_svg("stack.svg", 960, 490, f'''
<text x="50" y="55" class="mono" font-size="13" fill="{BLUE}">PROFILE / 03 — THE TOOLKIT</text><text x="50" y="105" class="display" font-size="42">TOOLS IN ORBIT.</text><text x="52" y="136" font-size="13" fill="{MUTED}">Grouped by the work they help me ship.</text>
<ellipse cx="480" cy="250" rx="356" ry="75" fill="none" stroke="#293650" stroke-width="1.5" transform="rotate(-10 480 250)"/><ellipse cx="480" cy="250" rx="291" ry="54" fill="none" stroke="url(#stack-svg-edge)" stroke-opacity=".4" transform="rotate(12 480 250)"/><ellipse cx="480" cy="250" rx="222" ry="38" fill="none" stroke="#293650" stroke-opacity=".72" transform="rotate(-20 480 250)"/>{orbit_svg_markup}
<g transform="translate(442 225)"><circle cx="38" cy="25" r="48" fill="url(#stack-svg-glow)" stroke="#3d4e70"/><text x="38" y="22" text-anchor="middle" class="display" font-size="25">BUILD</text><text x="38" y="42" text-anchor="middle" class="mono" font-size="9" fill="{MUTED}">SHIP / LEARN</text></g>
<text x="52" y="365" class="mono" font-size="10" fill="{MUTED}">LANGUAGES · FRAMEWORKS · DATA · WORKFLOW</text>{''.join(chips)}
''', "Priyanshu's technology stack")

    # GitHub profile README uses repo-relative assets and real HTML links below the image.
    readme = '''<div align="center">\n\n![Priyanshu Bisht — frontend developer and builder](assets/hero.svg?v=1)\n\n![About Priyanshu](assets/about-life.svg?v=1)\n\n![Priyanshu's technology stack](assets/stack.svg?v=1)\n\n</div>\n\n## Selected projects\n\n| Project | Focus | Technical implementation |\n|---|---|---|\n| [AshaPure](https://github.com/priyanshubishtme/ashapur_customer) | Dairy commerce with shopping, checkout, subscriptions, and role-based access. | React frontend, Node.js backend, MongoDB data store. |\n| [Arena Self-Driving](https://github.com/priyanshubishtme/arena-self-driving) | Autonomous highway-driving simulator with a tabular SARSA agent. | Python, Gymnasium environment, FastAPI control surface. |\n| [ZenAlert — SIH26178](https://github.com/priyanshubishtme/zen-alert) | Environmental early-warning dashboard plus sensor-node simulation. | FastAPI, MapLibre, Three.js; ESP32-S2 node and KiCad PCB design. |\n| [LinkPulse](https://github.com/priyanshubishtme/pulse) | Governed short links, campaigns, QR generation, analytics, and admin controls. | React, Express, TypeScript, PostgreSQL, Prisma; Redis is optional. |\n| [Stardela](https://github.com/priyanshubishtme/stardela) | Daily Colour Binary and Guzzle puzzles across three difficulty levels. | React 19, TypeScript, Vite, Vitest. |\n| [Little Universe Portfolio](https://github.com/priyanshubishtme/cool-website) | Route-based portfolio inside an explorable foothill town with a visual fallback. | Three.js, Rapier physics, Vite. |\n\n## Contribution activity\n\n![GitHub contribution activity](https://raw.githubusercontent.com/priyanshubishtme/priyanshubishtme/output/github-snake.svg?v=1)\n\n## Connect\n\n| [Portfolio](https://priyanshubishtme.netlify.app/) | [LinkedIn](https://linkedin.com/in/priyanshubishtme) | [YouTube](https://youtube.com/@priyanshubishtme) | [Email](mailto:priyanshubisht.me@gmail.com) |\n|---|---|---|---|\n\n'''
    (ROOT / "README.md").write_text(readme, encoding="utf-8")

    preview_images = "\n".join(
        f'    <img src="assets/{file}" alt="{file.removesuffix(".svg").replace("-", " ")}">'
        for file in ["hero.svg", "about-life.svg", "stack.svg"]
    )
    preview = f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Priyanshu Bisht — README preview</title>
  <style>
    body {{ margin: 0; background: #070b16; color: #f4f6fb; font: 16px/1.5 Arial, sans-serif; }}
    .wrap {{ max-width: 980px; margin: 32px auto; padding: 0 16px; }}
    img {{ display: block; width: 100%; height: auto; margin: 0 0 18px; border-radius: 20px; }}
    h1 {{ margin: 28px 0 8px; color: #9da8bc; font-size: 16px; font-weight: 400; }}
    a {{ color: #77aaff; }}
    .table {{ width: 100%; border-collapse: collapse; }}
    td, th {{ padding: 10px; border-bottom: 1px solid #2a3550; text-align: left; }}
    @media (max-width: 560px) {{
      .table, .table tbody, .table tr, .table td {{ display: block; width: 100%; box-sizing: border-box; }}
      .table th {{ display: none; }}
      .table tr {{ padding: 8px 0; }}
      .table td {{ padding: 4px 0; border: 0; }}
      .table tr + tr {{ border-top: 1px solid #2a3550; }}
    }}
  </style>
</head>
<body>
  <main class="wrap">
    <h1>README preview · five self-contained SVGs</h1>
{preview_images}
    <h1>Selected projects</h1>
    <table class="table">
      <thead><tr><th>Project</th><th>Focus</th><th>Technical implementation</th></tr></thead>
      <tbody>
        <tr><td><a href="https://github.com/priyanshubishtme/ashapur_customer">AshaPure</a></td><td>Dairy commerce</td><td>React / Node.js / MongoDB</td></tr>
        <tr><td><a href="https://github.com/priyanshubishtme/arena-self-driving">Arena Self-Driving</a></td><td>Tabular SARSA simulator</td><td>Python / Gymnasium / FastAPI</td></tr>
        <tr><td><a href="https://github.com/priyanshubishtme/zen-alert">ZenAlert</a></td><td>Early-warning dashboard</td><td>FastAPI / MapLibre / Three.js</td></tr>
        <tr><td><a href="https://github.com/priyanshubishtme/pulse">LinkPulse</a></td><td>Governed short links</td><td>React / Express / PostgreSQL / Prisma</td></tr>
        <tr><td><a href="https://github.com/priyanshubishtme/stardela">Stardela</a></td><td>Daily puzzle collection</td><td>React 19 / TypeScript / Vite</td></tr>
        <tr><td><a href="https://github.com/priyanshubishtme/cool-website">Little Universe</a></td><td>Explorable 3D portfolio</td><td>Three.js / Rapier / Vite</td></tr>
      </tbody>
    </table>
    <p>
      <a href="https://priyanshubishtme.netlify.app/">Portfolio</a> /
      <a href="https://linkedin.com/in/priyanshubishtme">LinkedIn</a> /
      <a href="https://youtube.com/@priyanshubishtme">YouTube</a> /
      <a href="mailto:priyanshubisht.me@gmail.com">Email</a>
    </p>
  </main>
</body>
</html>
'''
    (ROOT / "preview.html").write_text(preview, encoding="utf-8")

    sources = '''# Asset sources and licenses\n\n- Display face: Barlow Condensed ExtraBold, SIL Open Font License 1.1. License: `assets/fonts/OFL-BarlowCondensed.txt`. Source: https://github.com/google/fonts/tree/main/ofl/barlowcondensed\n- Mono face: JetBrains Mono Regular, SIL Open Font License 1.1. License: `assets/fonts/OFL-JetBrainsMono.txt`. Source: https://github.com/google/fonts/tree/main/ofl/jetbrainsmono\n- Orbit and YouTube brand paths: Simple Icons, embedded from its SVG icon files at https://github.com/simple-icons/simple-icons/tree/develop/icons (Python, JavaScript, TypeScript, React, Next.js, Node.js, Express, MongoDB, MySQL, Git, GitHub, Figma, YouTube). Java and Gymnasium remain text chips because Simple Icons has no matching icon file in the selected set.\n- LinkedIn and email symbols are inline text/envelope marks. No external icon assets are loaded.\n- Portrait: the original RGBA file `assets/id.png` is embedded byte-for-byte into the hero SVG; no mask or redraw is applied.\n'''
    (ROOT / "ASSET-SOURCES.md").write_text(sources, encoding="utf-8")

    # Make a clean upload archive while leaving source artwork and builder in the working repo.
    zip_path = ROOT / "profile-readme-upload.zip"
    entries = [ROOT / "README.md", ROOT / "preview.html", ROOT / "ASSET-SOURCES.md", ROOT / ".github/workflows/snake.yml", ROOT / "scripts/build_profile.py"]
    entries += [ASSETS / name for name in ["hero.svg", "about-life.svg", "stack.svg", "id.png"]]
    entries += list((ASSETS / "fonts").glob("*.txt")) + list((ASSETS / "fonts").glob("*.woff2"))
    entries += list((ASSETS / "icons").glob("*.svg")) + [ASSETS / "icons/LICENSE.txt"]
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED, compresslevel=8) as zf:
        for path in entries:
            zf.write(path, path.relative_to(ROOT))


if __name__ == "__main__":
    build()
