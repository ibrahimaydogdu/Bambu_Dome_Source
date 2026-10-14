"""
finalize_docx.py
Pandoc ciktisi .docx dosyalarini gonderim icin duzeltir (yalniz bicim; metin ve sayilar degismez):
  1) \\tag{n} ile verilen denklem numaralari pandoc tarafindan atiliyor -> her gosterim denkleminin sonuna "(n)" eklenir
  2) tablolara ust/alt/baslik cizgisi ve 8 pt yazi tipi eklenir
  3) sayfa A4
Kullanim: python finalize_docx.py <kaynak.md> <dosya.docx>
"""
import io
import re
import shutil
import sys
import zipfile


def patch(md_path: str, docx_path: str) -> None:
    md = io.open(md_path, encoding="utf-8").read()
    tags = re.findall(r"tag\{([^}]+)\}", md)
    zin = zipfile.ZipFile(docx_path)
    x = zin.read("word/document.xml").decode("utf-8")
    blocks = len(re.findall(r"<m:oMathPara>", x))
    if blocks != len(tags):
        raise SystemExit(f"denklem sayisi uyusmuyor: docx {blocks}, md {len(tags)}")
    it = iter(tags)

    def add_number(m):
        n = next(it)
        run = ('<m:r><m:t xml:space="preserve">' + "  (" + n + ")</m:t></m:r>")
        return m.group(1) + run + m.group(2)

    x = re.sub(r"(<m:oMathPara>.*?)(</m:oMath>\s*</m:oMathPara>)", add_number, x, flags=re.S)

    border = ('<w:tblBorders><w:top w:val="single" w:sz="8" w:space="0" w:color="000000"/>'
              '<w:bottom w:val="single" w:sz="8" w:space="0" w:color="000000"/>'
              '<w:insideH w:val="single" w:sz="2" w:space="0" w:color="999999"/></w:tblBorders>')

    def fix_table(m):
        t = m.group(0)
        if "<w:tblBorders>" not in t:
            if "<w:tblLayout" in t:
                t = t.replace("<w:tblLayout", border + "<w:tblLayout", 1)
            elif "<w:tblLook" in t:
                t = t.replace("<w:tblLook", border + "<w:tblLook", 1)
            elif "</w:tblPr>" in t:
                t = t.replace("</w:tblPr>", border + "</w:tblPr>", 1)
            else:
                t = t.replace("<w:tbl>", "<w:tbl><w:tblPr>" + border + "</w:tblPr>", 1)
        # 8 pt yazi (w:sz = yarim punto)
        sz = '<w:sz w:val="16"/><w:szCs w:val="16"/>'

        def fix_run(r):
            rpr = r.group(1)
            if rpr is None:
                return "<w:r><w:rPr>" + sz + "</w:rPr>"
            if "<w:sz " in rpr:
                return r.group(0)
            later = ("w:highlight", "w:u ", "w:u/", "w:effect", "w:bdr", "w:shd", "w:fitText", "w:vertAlign", "w:rtl", "w:cs/", "w:em ", "w:lang")
            pos = [rpr.find("<" + k) for k in later if rpr.find("<" + k) >= 0]
            cut = min(pos) if pos else rpr.rfind("</w:rPr>")
            return "<w:r>" + rpr[:cut] + sz + rpr[cut:]

        return re.sub(r"<w:r>(<w:rPr>.*?</w:rPr>)?", fix_run, t, flags=re.S)

    x = re.sub(r"<w:tbl>.*?</w:tbl>", fix_table, x, flags=re.S)
    x = re.sub(r'<w:pgSz [^>]*/>', '<w:pgSz w:w="11906" w:h="16838"/>', x)

    tmp = docx_path + ".tmp"
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == "word/document.xml":
                data = x.encode("utf-8")
            zout.writestr(item, data)
    zin.close()
    shutil.move(tmp, docx_path)
    print(f"{docx_path}: {len(tags)} denklem numarasi eklendi, tablolar bicimlendi, A4")


if __name__ == "__main__":
    patch(sys.argv[1], sys.argv[2])
