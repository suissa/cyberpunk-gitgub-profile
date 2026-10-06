#!/usr/bin/env python3
"""Generate the cyberpunk GitHub profile SVG interface from one profile.json."""
from __future__ import annotations
import argparse, html, json, re
from pathlib import Path

W, CARD_W, CARD_H = 880, 220, 80
CARD_X = (52, 35.75, 19.5, 3.25)
CARD_END = (217, 200.5, 184.25, 168)

def esc(v): return html.escape(str(v), quote=True)

def rgb(h):
    h=h.lstrip("#")
    if len(h)!=6: raise ValueError(f"Invalid hex color: {h}")
    return tuple(int(h[i:i+2],16) for i in (0,2,4))

def mix(a,b,t):
    ar,ag,ab=rgb(a); br,bg,bb=rgb(b)
    return "#{:02X}{:02X}{:02X}".format(
        round(ar+(br-ar)*t), round(ag+(bg-ag)*t), round(ab+(bb-ab)*t)
    )

def colors(p):
    t=p.get("theme",{})
    accent=t.get("accent","#00D9FF")
    return {
        "accent":accent,
        "bright":t.get("accent_bright",mix(accent,"#FFFFFF",.58)),
        "bg":t.get("background","#03040A"),
        "fg":t.get("foreground","#F0FBFF"),
        "muted":t.get("muted","#8B949E"),
        "grid":float(t.get("grid_opacity",.06)),
    }

def defs(t):
    return f"""<defs>
<pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="{t['accent']}" stroke-opacity="{t['grid']}"/></pattern>
<filter id="glow" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="5"/></filter>
<filter id="soft" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="2.5"/></filter>
</defs>"""

def svg(w,h,title,desc,t,body):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="t d">
<title id="t">{esc(title)}</title><desc id="d">{esc(desc)}</desc>
<style>text{{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,"Liberation Mono",monospace}}.dim{{fill:{t['muted']}}}.cy{{fill:{t['accent']}}}.fg{{fill:{t['fg']}}}.bright{{fill:{t['bright']}}}</style>
{defs(t)}
{body}
</svg>"""

def header(p,t):
    x=p["profile"]; name=x.get("display_name",x["name"]).upper()
    bio=x.get("bio",""); chunks=[bio[i:i+78] for i in range(0,len(bio),78)]
    body=f"""<rect width="880" height="360" fill="{t['bg']}"/><rect width="880" height="360" fill="url(#grid)"/>
<path d="M40 0V360M840 0V360" stroke="{t['accent']}" stroke-opacity=".16"/>
<path d="M56 54H824M56 306H824" stroke="{t['accent']}" stroke-opacity=".25"/>
<text x="56" y="96" font-size="54" font-weight="700" class="bright">{esc(name)}</text>
<text x="58" y="125" font-size="14" class="cy">{esc(x.get('handle',''))}</text>
<text x="58" y="166" font-size="20" font-weight="700" class="fg">{esc(x.get('title',''))}</text>
<text x="58" y="193" font-size="13" class="dim">{esc(x.get('subtitle',''))}</text>"""
    for i,line in enumerate(chunks[:4]):
        body+=f'<text x="58" y="{238+i*18}" font-size="12" class="dim">// {esc(line)}</text>'
    body+=f'<text x="58" y="326" font-size="11" class="cy">BORN {esc(x.get("born",""))}  ·  DIED {esc(x.get("died",""))}  ·  {esc(x.get("location",""))}</text>'
    return svg(880,360,name,f"{name}. {x.get('title','')}",t,body)

def section(title,desc,t):
    body=f"""<rect width="880" height="120" fill="{t['bg']}"/><rect width="880" height="120" fill="url(#grid)"/>
<path d="M32 0V120M848 0V120" stroke="{t['accent']}" stroke-opacity=".32"/>
<text x="56" y="62" font-size="30" font-weight="700" class="bright">~/{esc(title)}</text>
<text x="58" y="88" font-size="12" class="dim">{esc(desc)}</text><path d="M56 102H824" stroke="{t['accent']}" stroke-opacity=".28"/>"""
    return svg(880,120,title,desc,t,body)

def link_card(link,t,i):
    col=i%4; x0=CARD_X[col]; x1=CARD_END[col]
    label=link.get("label",link.get("id","LINK")).upper()[:16]
    glyph=link.get("glyph","↗")[:3]
    handle=link.get("handle","")[:28]
    body=f'<rect width="220" height="80" fill="{t["bg"]}"/><rect width="220" height="80" fill="url(#grid)"/>'
    if col==0: body+=f'<path d="M16 -40V120" stroke="{t["accent"]}" stroke-width="3" opacity=".42" filter="url(#glow)"/><path d="M16 0V80" stroke="{t["accent"]}" stroke-width="1.2"/>'
    if col==3: body+=f'<path d="M204 -40V120" stroke="{t["accent"]}" stroke-width="3" opacity=".42" filter="url(#glow)"/><path d="M204 0V80" stroke="{t["accent"]}" stroke-width="1.2"/>'
    body+=f"""<path d="M{x0} 12H{x1-12}L{x1} 24V68H{x0}Z" fill="{t['accent']}" fill-opacity=".06"/>
<path d="M{x0} 12H{x1-12}L{x1} 24V68H{x0}Z" fill="none" stroke="{t['accent']}" stroke-opacity=".58"/>
<path d="M{x1-12} 12L{x1} 24" stroke="{t['accent']}" stroke-width="2"/>
<text x="{x0+12}" y="38" font-size="20" font-weight="700" class="bright">{esc(glyph)}</text>
<text x="{x0+42}" y="37" font-size="13" font-weight="700" class="cy">{esc(label)}</text>
<text x="{x0+12}" y="58" font-size="10" class="dim">{esc(handle)}</text>"""
    return svg(220,80,label,link.get("description",label),t,body)

def stats(p,t):
    body=f'<rect width="880" height="560" fill="{t["bg"]}"/><rect width="880" height="560" fill="url(#grid)"/><text x="56" y="58" font-size="30" font-weight="700" class="bright">~/stats</text>'
    for i,s in enumerate(p.get("stats",[])[:8]):
        col=i%2; row=i//2; x=56+col*392; y=100+row*100
        body+=f'<text x="{x}" y="{y}" font-size="11" class="dim">{esc(s.get("label",""))}</text><text x="{x}" y="{y+31}" font-size="25" font-weight="700" class="cy">{esc(s.get("value",""))}</text><text x="{x}" y="{y+64}" font-size="10" class="fg">{esc(s.get("detail",""))}</text><path d="M{x} {y+78}H{x+330}" stroke="{t["accent"]}" stroke-opacity=".14"/>'
    return svg(880,560,"Stats","Profile statistics",t,body)

def stack(p,t):
    body=f'<rect width="880" height="360" fill="{t["bg"]}"/><rect width="880" height="360" fill="url(#grid)"/><text x="56" y="58" font-size="30" font-weight="700" class="bright">~/stack</text>'
    for i,c in enumerate(p.get("stack",{}).get("categories",[])[:5]):
        y=96+i*50
        body+=f'<text x="56" y="{y}" font-size="11" class="cy">{esc(c.get("name",""))}</text><text x="190" y="{y}" font-size="11" class="fg">{esc(" · ".join(c.get("items",[])))}</text><path d="M56 {y+12}H824" stroke="{t["accent"]}" stroke-opacity=".1"/>'
    return svg(880,360,"Stack","Technical profile",t,body)

def footer(p,t):
    msg=p.get("footer","connection closed.")
    return svg(880,80,"End of profile",msg,t,f'<rect width="880" height="80" fill="{t["bg"]}"/><rect width="880" height="80" fill="url(#grid)"/><path d="M56 40H824" stroke="{t["accent"]}" stroke-opacity=".25"/><text x="440" y="45" text-anchor="middle" font-size="12" class="dim">{esc(msg)}</text>')

def safe_id(v,i):
    s=re.sub(r"[^a-z0-9]+","-",v.lower()).strip("-")
    return f"{i:02d}-{s or 'link'}"

def write_readme(out,p):
    lines=['<p align="center">','<img src="./header.svg" width="100%" align="top" alt="Profile">','<img src="./links.svg" width="100%" align="top" alt="Links">']
    links=p.get("links",[])[:8]
    for start in range(0,len(links),4):
        row=[]
        for i,l in enumerate(links[start:start+4],start+1):
            f=safe_id(l.get("id","link"),i)+".svg"
            row.append(f'<a href="{esc(l.get("url","#"))}"><img src="./links/{f}" width="25%" align="top" alt="{esc(l.get("label",l.get("id","Link")))}"></a>')
        lines.append("".join(row))
    lines += ['<img src="./stats.svg" width="100%" align="top" alt="Stats">','<img src="./stack.svg" width="100%" align="top" alt="Stack">','<img src="./footer.svg" width="100%" align="top" alt="Footer">','</p>']
    (out/"README.generated.md").write_text("\n".join(lines)+"\n",encoding="utf-8")

def validate(out,p):
    errors=[]
    for name,w,h in [("header.svg",880,360),("links.svg",880,120),("stats.svg",880,560),("stack.svg",880,360),("footer.svg",880,80)]:
        s=(out/name).read_text(encoding="utf-8")
        if not re.search(fr'<svg[^>]*width="{w}" height="{h}" viewBox="0 0 {w} {h}"',s): errors.append(f"{name}: dimensions are not {w}x{h}")
    links=list((out/"links").glob("*.svg")); expected=min(8,len(p.get("links",[])))
    if len(links)!=expected: errors.append(f"links: expected {expected}, found {len(links)}")
    if expected and expected<=8 and expected%4==0 and expected*CARD_W//2 != expected//4*W: pass
    for f in links:
        s=f.read_text(encoding="utf-8")
        if not re.search(r'<svg[^>]*width="220" height="80" viewBox="0 0 220 80"',s): errors.append(f"{f.name}: dimensions are not 220x80")
    # The canonical two-row layout is four 220px cards = exactly 880px.
    if expected>4 and expected%4==0 and 4*CARD_W != W: errors.append("link row width mismatch")
    if expected>=4:
        first=(out/"links"/safe_id(p["links"][0].get("id","link"),1)+".svg").read_text(encoding="utf-8")
        fourth=(out/"links"/safe_id(p["links"][3].get("id","link"),4)+".svg").read_text(encoding="utf-8")
        if 'M16 0V80' not in first: errors.append("first card is missing the outer left rail")
        if 'M204 0V80' not in fourth: errors.append("fourth card is missing the outer right rail")
    if errors: raise SystemExit("VALIDATION FAILED\n"+"\n".join(errors))
    print(f"VALIDATION OK · section=880px · row=4×220px=880px · links={expected}")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("profile"); ap.add_argument("-o","--output",default="generated-profile")
    ap.add_argument("--validate",action="store_true"); ap.add_argument("--render",action="store_true")
    a=ap.parse_args(); p=json.loads(Path(a.profile).read_text(encoding="utf-8")); out=Path(a.output); (out/"links").mkdir(parents=True,exist_ok=True); t=colors(p)
    (out/"header.svg").write_text(header(p,t),encoding="utf-8")
    (out/"links.svg").write_text(section("links","Where to find "+p["profile"].get("display_name",p["profile"]["name"]),t),encoding="utf-8")
    for i,l in enumerate(p.get("links",[])[:8]): (out/"links"/(safe_id(l.get("id","link"),i+1)+".svg")).write_text(link_card(l,t,i),encoding="utf-8")
    (out/"stats.svg").write_text(stats(p,t),encoding="utf-8"); (out/"stack.svg").write_text(stack(p,t),encoding="utf-8"); (out/"footer.svg").write_text(footer(p,t),encoding="utf-8"); write_readme(out,p)
    if a.validate: validate(out,p)
    if a.render:
        try: import cairosvg
        except ImportError: raise SystemExit("Rendering requires cairosvg: python -m pip install cairosvg")
        r=out/"rendered"; r.mkdir(exist_ok=True)
        for f in list(out.glob("*.svg"))+list((out/"links").glob("*.svg")): cairosvg.svg2png(url=str(f),write_to=str(r/(f.stem+".png")))
        print(f"RENDER OK · previews={r}")

if __name__=="__main__": main()
