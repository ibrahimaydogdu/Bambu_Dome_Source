"""
build_manuscript_full.py
05_Drafts/manuscript/ altindaki bolum dosyalarini tek belgede birlestirir:
  MANUSCRIPT_FULL.md   (VS Code onizlemesi icin; sekiller goreli yolla)
  MANUSCRIPT_FULL.html (tek dosya; sekiller gomulu; denklemler MathJax ile cdnjs'den)
Hicbir sayi uretmez; yalnizca mevcut bolum dosyalarini ve 04_Results/figures/ sekillerini kullanir.
Kullanim: python build_manuscript_full.py
"""
from __future__ import annotations
import base64
import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MS = ROOT / "05_Drafts" / "manuscript"
FIG = ROOT / "04_Results" / "figures"

FIGS = {  # numara -> dosya
    "1": "F1_best_profiles.png", "2": "F2_convergence.png", "3": "F3_boxplots.png",
    "4": "F4_governing_limit_states.png", "5a": "F5_material_weight.png", "5b": "F5_material_co2.png"}
# sekil, ilgili paragrafin baslangicindan sonra yerlestirilir (bolum dosyasi, paragraf baslangici)
ANCHORS = [
    ("04_results.md", "**Table 9.**", ["3"]),
    ("04_results.md", "Figure 2 shows the mean", ["2"]),
    ("04_results.md", "Compression determines the largest D/C ratio", ["4", "1"]),
    ("04_results.md", "Figure 5 shows the member weight", ["5a", "5b"]),
]


def captions() -> dict[str, str]:
    out = {}
    for ln in (MS / "07_figure_captions.md").read_text(encoding="utf-8").splitlines():
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
                for f in figs:
                    res.append(f"![Figure {f}](../../04_Results/figures/{FIGS[f]})\n\n**Figure {f}.** {caps[f]}")
    return "\n\n".join(res)


def build_md() -> str:
    caps = captions()
    head = (MS / "00_title_abstract_highlights.md").read_text(encoding="utf-8")
    title = re.search(r"# Title \(working title\)\s+(.+)", head).group(1).strip()
    rest = head.split("\n", 1)[1].split(title, 1)[1].strip()
    rest = rest.replace("## Highlights", "## Highlights").strip()
    n_open = re.search(r"Count: (\d+)", (MS / "OPEN_ITEMS.md").read_text(encoding="utf-8"))
    status = ("> Working draft. Open placeholders in the text: " + (n_open.group(1) if n_open else "?") +
              ". Sources of numbers: `NUMBERS_TRACE.md`. Open decisions and data requests: `OPEN_ITEMS.md`. Source search instructions: `REFERENCE_SEARCH_GUIDE.md`.")
    parts = [f"# {title}", "", status, "", rest]
    for name in ["01_introduction.md", "02_methods.md", "03_numerical_examples.md", "04_results.md", "05_discussion.md", "06_conclusions.md"]:
        parts += ["", with_figures(name, (MS / name).read_text(encoding="utf-8").strip(), caps)]
    parts += ["", (MS / "08_references.md").read_text(encoding="utf-8").strip()]
    return "\n".join(parts) + "\n"


# ---------------------------------------------------------------- HTML (kucuk markdown alt kumesi)
def inline(s: str) -> str:
    s = html.escape(s, quote=False)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![\w*])\*([^*\n]+)\*(?![\w*])", r"<em>\1</em>", s)
    s = re.sub(r"(https?://[^\s<)]+)", r'<a href="\1">\1</a>', s)
    return s


def img_tag(path: str, alt: str) -> str:
    p = (MS / path).resolve()
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
        if ln.strip().startswith("$$"):                       # gosterim denklemi
            buf = [ln]
            if not (ln.strip().endswith("$$") and len(ln.strip()) > 2):
                i += 1
                while i < len(lines) and "$$" not in lines[i]:
                    buf.append(lines[i]); i += 1
                buf.append(lines[i])
            out.append("<div class='eq'>" + html.escape("\n".join(buf)) + "</div>")
            i += 1
            continue
        if ln.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                rows.append(lines[i]); i += 1
            cells = [[c.strip() for c in r.strip().strip("|").split("|")] for r in rows if not re.match(r"^\|[-| ]+\|$", r)]
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
            if i < len(lines) and lines[i].startswith("**Figure"):
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
    css = """body{font-family:'Times New Roman',Times,serif;max-width:46rem;margin:2rem auto;padding:0 1rem;line-height:1.5;font-size:16px;color:#1b1b1b;background:#fff}
h1{font-size:1.5rem}h2{font-size:1.2rem;margin-top:2rem}h3{font-size:1.05rem}
table{border-collapse:collapse;margin:1rem 0;font-size:.85rem;display:block;overflow-x:auto}th,td{border:1px solid #bbb;padding:.25rem .5rem;text-align:left}th{background:#f1f1f1}
figure{margin:1.5rem 0}figure img{max-width:100%}figcaption{font-size:.9rem}code{font-size:.85em;background:#f3f3f3;padding:0 .2em}
blockquote{border-left:4px solid #bbb;margin:1rem 0;padding:.2rem 1rem;color:#444}.eq{overflow-x:auto}
@media (prefers-color-scheme:dark){body{background:#161616;color:#e6e6e6}th{background:#2a2a2a}th,td{border-color:#555}code{background:#2a2a2a}figure img{background:#fff}}"""
    mj = ("<script>window.MathJax={tex:{inlineMath:[['$','$']],displayMath:[['$$','$$']]}};</script>"
          "<script async src='https://cdnjs.cloudflare.com/ajax/libs/mathjax/3.2.2/es5/tex-chtml.js'></script>")
    return f"<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>Manuscript draft</title><style>{css}</style>{mj}</head><body>\n" + "\n".join(out) + "\n</body></html>\n"


if __name__ == "__main__":
    md = build_md()
    (MS / "MANUSCRIPT_FULL.md").write_text(md, encoding="utf-8")
    (MS / "MANUSCRIPT_FULL.html").write_text(to_html(md), encoding="utf-8")
    print("yazildi: MANUSCRIPT_FULL.md,", len(md.split()), "sozcuk; MANUSCRIPT_FULL.html")
