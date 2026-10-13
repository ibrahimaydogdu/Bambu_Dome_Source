"""
build_manuscript_full.py
05_Drafts/manuscript/ altindaki bolum dosyalarini tek belgede birlestirir:
  MANUSCRIPT_FULL.md   (VS Code onizlemesi icin; sekiller goreli yolla)
  MANUSCRIPT_FULL.html (tek dosya; sekiller gomulu; denklemler MathJax ile cdnjs'den)
  MANUSCRIPT_FULL.docx (Pandoc ile dogrudan uretim)
Kullanim: python build_manuscript_full.py
"""
from __future__ import annotations
import base64
import html
import os
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MS = ROOT / "05_Drafts" / "manuscript"
FIG = ROOT / "04_Results" / "figures"

# Sirali ve ardisik sekil eslesmesi (Figur 1 -> Figur 7)
FIGS = {
    "1": "method_flowchart.png",
    "2a": "domes/geodesic16_views.png",
    "2b": "domes/kiewitt32_views.png",
    "2c": "domes/ribbed40_views.png",
    "3": "F2_convergence.png",
    "4": "F3_boxplots.png",
    "5": "F1_best_profiles.png",
    "6": "F4_governing_limit_states.png",
    "7a": "F5_material_weight.png",
    "7b": "F5_material_co2.png",
}

# Sekil yerlesim capalari (bolum dosyasi, paragraf baslangici, sekiller)
ANCHORS = [
    ("02_methods.md", "Figure 1 illustrates the overall multi-stage computational workflow", ["1"]),
    ("03_numerical_examples.md", "Figure 2 illustrates the spatial layouts, plan projections", ["2a", "2b", "2c"]),
    ("04_results.md", "Figure 3 shows the mean and best penalized weight", ["3"]),
    ("04_results.md", "The statistical dispersion of the best structural weights", ["4"]),
    ("04_results.md", "The cross-sectional profiles (outer diameter $D$ and wall thickness $t$)", ["5"]),
    ("04_results.md", "Compression buckling governs the largest D/C ratio", ["6"]),
    ("04_results.md", "Figure 7 illustrates the comparative member weight", ["7a", "7b"]),
]


def captions() -> dict[str, str]:
    out = {}
    cap_file = MS / "07_figure_captions.md"
    if not cap_file.exists():
        return out
    for ln in cap_file.read_text(encoding="utf-8").splitlines():
        m = re.match(r"\*\*Figure (\d[ab]?)\.\*\* (.*)", ln)
        if m:
            out[m.group(1)] = m.group(2)
    return out


def with_figures(name: str, text: str, caps: dict[str, str]) -> str:
    paras = text.split("\n\n")
    res = []
    for p in paras:
        res.append(p)
        for fn, start, figs in ANCHORS:
            if fn == name and p.lstrip().startswith(start):
                if figs == ["2a", "2b", "2c"]:
                    res.append(f"![Figure 2a](../../04_Results/figures/{FIGS['2a']})\n\n*(a) 16 m Geodesic dome: (i) 3D view, (ii) plan view, (iii) side view*")
                    res.append(f"![Figure 2b](../../04_Results/figures/{FIGS['2b']})\n\n*(b) 32 m Kiewitt dome: (i) 3D view, (ii) plan view, (iii) side view*")
                    res.append(f"![Figure 2c](../../04_Results/figures/{FIGS['2c']})\n\n*(c) 40 m Ribbed dome: (i) 3D view, (ii) plan view, (iii) side view*")
                    res.append(f"**Figure 2.** {caps.get('2', 'Spatial topology, plan projections, elevation profiles, and optimal cross-sectional diameter allocations across the three benchmark space domes.')}")
                else:
                    for f in figs:
                        cap_text = caps.get(f, "")
                        res.append(f"![Figure {f}](../../04_Results/figures/{FIGS[f]})\n\n**Figure {f}.** {cap_text}")
    return "\n\n".join(res)


def build_md() -> str:
    caps = captions()
    head = (MS / "00_title_abstract_highlights.md").read_text(encoding="utf-8")
    title_m = re.search(r"# Title \(working title\)\s+(.+)", head)
    title = title_m.group(1).strip() if title_m else "Sizing Optimization of Guadua Bamboo Space Domes"
    rest = head.split("\n", 1)[1].split(title, 1)[1].strip() if title in head else head
    rest = rest.replace("## Highlights", "## Highlights").strip()
    
    parts = [f"# {title}", "", rest]
    order = [
        "01_introduction.md",
        "02_methods.md",
        "03_numerical_examples.md",
        "04_results.md",
        "05_discussion.md",
        "06_conclusions.md",
        "07_declarations.md",
        "08_references.md"
    ]
    for name in order:
        fpath = MS / name
        if fpath.exists():
            parts += ["", with_figures(name, fpath.read_text(encoding="utf-8").strip(), caps)]
    return "\n".join(parts) + "\n"


def inline(s: str) -> str:
    s = html.escape(s, quote=False)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![\w*])\*([^*\n]+)\*(?![\w*])", r"<em>\1</em>", s)
    s = re.sub(r"(https?://[^\s<)]+)", r'<a href="\1">\1</a>', s)
    return s


def img_tag(path: str, alt: str) -> str:
    p = (MS / path).resolve()
    if not p.exists():
        return f"[Image not found: {path}]"
    data = base64.b64encode(p.read_bytes()).decode()
    return f'<img alt="{html.escape(alt)}" src="data:image/png;base64,{data}">'


def to_html(md: str) -> str:
    lines = md.split("\n")
    out, i = [], 0
    while i < len(lines):
        ln = lines[i]
        if not ln.strip():
            i += 1
            continue
        m = re.match(r"(#{1,3}) (.*)", ln)
        if m:
            n = len(m.group(1))
            out.append(f"<h{n}>{inline(m.group(2))}</h{n}>")
            i += 1
            continue
        if ln.strip().startswith("$$"):
            buf = [ln]
            if not (ln.strip().endswith("$$") and len(ln.strip()) > 2):
                i += 1
                while i < len(lines) and "$$" not in lines[i]:
                    buf.append(lines[i]); i += 1
                if i < len(lines):
                    buf.append(lines[i])
            out.append("<div class='eq'>" + html.escape("\n".join(buf)) + "</div>")
            i += 1
            continue
        if ln.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                rows.append(lines[i]); i += 1
            cells = [[c.strip() for c in r.strip().strip("|").split("|")] for r in rows if not re.match(r"^\|[-| ]+\|$", r)]
            if cells:
                t = ["<table>", "<thead><tr>" + "".join(f"<th>{inline(c)}</th>" for c in cells[0]) + "</tr></thead><tbody>"]
                for r in cells[1:]:
                    t.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>")
                t.append("</tbody></table>")
                out.append("\n".join(t))
            continue
        if re.match(r"(- |\d+\. )", ln):
            ordered = bool(re.match(r"\d+\. ", ln))
            items = []
            while i < len(lines) and re.match(r"(- |\d+\. )", lines[i]):
                items.append(re.sub(r"^(- |\d+\. )", "", lines[i])); i += 1
            tag = "ol" if ordered else "ul"
            out.append(f"<{tag}>" + "".join(f"<li>{inline(x)}</li>" for x in items) + f"</{tag}>")
            continue
        m = re.match(r"!\[([^\]]*)\]\(([^)]+)\)", ln)
        if m:
            out.append(f"<figure>{img_tag(m.group(2), m.group(1))}")
            i += 1
            while i < len(lines) and not lines[i].strip():
                i += 1
            if i < len(lines) and (lines[i].startswith("**Figure") or lines[i].startswith("*(")):
                out.append(f"<figcaption>{inline(lines[i])}</figcaption>"); i += 1
            out.append("</figure>")
            continue
        if ln.startswith(">"):
            out.append(f"<blockquote>{inline(ln.lstrip('> '))}</blockquote>")
            i += 1
            continue
        buf = [ln]
        i += 1
        while i < len(lines) and lines[i].strip() and not re.match(r"(#|\||- |\d+\. |!\[|\$\$|>)", lines[i]):
            buf.append(lines[i]); i += 1
        out.append(f"<p>{inline(' '.join(buf))}</p>")
        
    css = """body{font-family:'Times New Roman',Times,serif;max-width:48rem;margin:2rem auto;padding:0 1rem;line-height:1.55;font-size:16px;color:#1b1b1b;background:#fff}
h1{font-size:1.5rem}h2{font-size:1.2rem;margin-top:2rem}h3{font-size:1.05rem}
table{border-collapse:collapse;margin:1rem 0;font-size:.85rem;display:block;overflow-x:auto}th,td{border:1px solid #bbb;padding:.3rem .55rem;text-align:left}th{background:#f1f1f1}
figure{margin:1.5rem 0;text-align:center}figure img{max-width:100%;height:auto}figcaption{font-size:.9rem;text-align:left;margin-top:.5rem}code{font-size:.85em;background:#f3f3f3;padding:0 .2em}
blockquote{border-left:4px solid #bbb;margin:1rem 0;padding:.2rem 1rem;color:#444}.eq{overflow-x:auto;text-align:center;margin:1rem 0}
@media (prefers-color-scheme:dark){body{background:#161616;color:#e6e6e6}th{background:#2a2a2a}th,td{border-color:#555}code{background:#2a2a2a}figure img{background:#fff}}"""
    mj = ("<script>window.MathJax={tex:{inlineMath:[['$','$']],displayMath:[['$$','$$']]}};</script>"
          "<script async src='https://cdnjs.cloudflare.com/ajax/libs/mathjax/3.2.2/es5/tex-chtml.js'></script>")
    return f"<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>Manuscript Draft - Stage 5</title><style>{css}</style>{mj}</head><body>\n" + "\n".join(out) + "\n</body></html>\n"


def convert_pandoc(md_path: Path, docx_path: Path):
    pandoc_exe = Path(r"C:\Program Files\Pandoc\pandoc.exe")
    if not pandoc_exe.exists():
        print("Pandoc executable not found at default location.")
        return
    cmd = [
        str(pandoc_exe),
        str(md_path),
        "-o", str(docx_path),
        f"--resource-path={MS}",
        "--toc",
        "--number-sections=false",
    ]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print("Pandoc docx conversion successful:", docx_path.name)
    except subprocess.CalledProcessError as e:
        print("Pandoc error:", e.stderr)


if __name__ == "__main__":
    md = build_md()
    md_file = MS / "MANUSCRIPT_FULL.md"
    html_file = MS / "MANUSCRIPT_FULL.html"
    docx_file = MS / "MANUSCRIPT_FULL.docx"
    
    md_file.write_text(md, encoding="utf-8")
    html_file.write_text(to_html(md), encoding="utf-8")
    print(f"Written: MANUSCRIPT_FULL.md ({len(md.split())} words), MANUSCRIPT_FULL.html")
    
    convert_pandoc(md_file, docx_file)
