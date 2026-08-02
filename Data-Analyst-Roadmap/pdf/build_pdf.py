"""
Builds the printable handbook, in English or Spanish.

Concatenates every chapter (in order) into one HTML document with a cover
page, a table of contents, running headers/footers, and print-ready
typography, then renders it to PDF.

Usage:
    python pdf/build_pdf.py            # English (default)
    python pdf/build_pdf.py --lang es  # Spanish

Output (English):
    pdf/The_Complete_Data_Analyst_Roadmap.html / .pdf
Output (Spanish):
    pdf/El_Roadmap_Completo_del_Analista_de_Datos.html / .pdf

PDF rendering requires either:
  - WeasyPrint with its system dependencies (Pango/GTK) installed, or
  - Chrome/Edge on PATH or at the default Windows install path (headless print-to-pdf), or
  - manually opening the generated .html and using the browser's
    File > Print > Save as PDF (works everywhere, zero extra installs).
"""
import argparse
import re
import subprocess
import shutil
from pathlib import Path
from datetime import date

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "pdf"

LANGUAGES = {
    "en": {
        "handbook_dir": ROOT / "handbook",
        "title": "The Complete Data Analyst & Data Science Roadmap",
        "subtitle": "A premium, company-grade handbook from beginner/intermediate<br>"
                    "to professional Data Analyst — with a runway into Data Science.",
        "compiled_label": "Compiled",
        "toc_label": "Table of Contents",
        "page_label": "Page",
        "of_label": "of",
        "output_basename": "The_Complete_Data_Analyst_Roadmap",
        "chapters": [
            "01_Introduction.md", "02_How_Companies_Work.md", "03_Databases.md",
            "04_SQL.md", "05_Python.md", "06_Power_BI.md",
            "07_Professional_Projects.md", "08_Machine_Learning.md", "09_Portfolio_Career.md",
        ],
    },
    "es": {
        "handbook_dir": ROOT / "handbook_es",
        "title": "El Roadmap Completo del Analista de Datos y Data Science",
        "subtitle": "Un handbook premium, de nivel empresarial, desde principiante/intermedio<br>"
                    "hasta Data Analyst profesional — con proyección hacia Data Science.",
        "compiled_label": "Compilado el",
        "toc_label": "Tabla de Contenidos",
        "page_label": "Página",
        "of_label": "de",
        "output_basename": "El_Roadmap_Completo_del_Analista_de_Datos",
        "chapters": [
            "01_Introduccion.md", "02_Como_Trabajan_las_Empresas.md", "03_Bases_de_Datos.md",
            "04_SQL.md", "05_Python.md", "06_Power_BI.md",
            "07_Proyectos_Profesionales.md", "08_Machine_Learning.md", "09_Portfolio_Carrera.md",
        ],
    },
}


def build_css(title: str, page_label: str, of_label: str) -> str:
    return f"""
@page {{
    size: A4;
    margin: 2.2cm 1.8cm 2.4cm 1.8cm;
    @top-center {{ content: "{title}"; font-size: 8pt; color: #888; }}
    @bottom-center {{ content: "{page_label} " counter(page) " {of_label} " counter(pages); font-size: 8pt; color: #888; }}
}}
@page cover {{ @top-center {{ content: ""; }} @bottom-center {{ content: ""; }} }}
body {{ font-family: 'Segoe UI', Helvetica, Arial, sans-serif; color: #1a1a1a; line-height: 1.55; font-size: 10.5pt; }}
h1 {{ font-size: 22pt; color: #0b5fff; border-bottom: 3px solid #0b5fff; padding-bottom: 6px; page-break-before: always; }}
h2 {{ font-size: 15pt; color: #111; margin-top: 1.4em; }}
h3 {{ font-size: 12.5pt; color: #333; }}
code {{ background: #f2f4f8; padding: 1px 4px; border-radius: 3px; font-family: 'Cascadia Code', Consolas, monospace; font-size: 9pt; }}
pre {{ background: #0b1021; color: #e6e6e6; padding: 10px 12px; border-radius: 6px; overflow-x: auto; font-size: 8.5pt; }}
pre code {{ background: none; color: inherit; }}
blockquote {{ border-left: 4px solid #0b5fff; background: #f5f8ff; margin: 1em 0; padding: 0.6em 1em; border-radius: 0 4px 4px 0; }}
table {{ border-collapse: collapse; width: 100%; margin: 1em 0; font-size: 9.5pt; }}
th, td {{ border: 1px solid #ddd; padding: 5px 8px; text-align: left; }}
th {{ background: #f2f4f8; }}
a {{ color: #0b5fff; text-decoration: none; }}
.cover {{ page: cover; page-break-after: always; text-align: center; padding-top: 30%; }}
.cover h1 {{ border: none; font-size: 30pt; page-break-before: avoid; }}
.cover p {{ font-size: 12pt; color: #555; }}
.toc {{ page-break-after: always; }}
.toc a {{ display: block; margin: 4px 0; }}
.mermaid, pre.mermaid {{ background: #f9f9fb; border: 1px dashed #ccc; padding: 8px; font-size: 8pt; }}
"""


def md_to_html(md_text: str) -> str:
    """Minimal, dependency-light Markdown -> HTML (headings, bold, code, tables, links, lists, blockquotes)."""
    try:
        import markdown  # type: ignore
        return markdown.markdown(md_text, extensions=["tables", "fenced_code", "toc"])
    except ImportError:
        result = subprocess.run(
            ["pandoc", "-f", "markdown", "-t", "html"],
            input=md_text.encode("utf-8"), capture_output=True, check=True,
        )
        return result.stdout.decode("utf-8")


def build(lang: str):
    cfg = LANGUAGES[lang]
    OUT_DIR.mkdir(exist_ok=True)
    chapters_html = []
    toc_entries = []

    for i, fname in enumerate(cfg["chapters"], start=1):
        path = cfg["handbook_dir"] / fname
        if not path.exists():
            print(f"  [skip] {fname} not found")
            continue
        raw = path.read_text(encoding="utf-8")
        title_match = re.search(r"^#\s+(.+)$", raw, re.MULTILINE)
        title = title_match.group(1) if title_match else fname
        anchor = f"chapter-{i:02d}"
        toc_entries.append(f'<a href="#{anchor}">{title}</a>')
        html = md_to_html(raw)
        chapters_html.append(f'<section id="{anchor}">{html}</section>')
        print(f"  [ok] {fname}")

    cover = f"""
    <div class="cover">
        <h1>{cfg['title']}</h1>
        <p>{cfg['subtitle']}</p>
        <p style="margin-top:3em;">{cfg['compiled_label']} {date.today().isoformat()}</p>
    </div>
    """
    toc = f'<div class="toc"><h1>{cfg["toc_label"]}</h1>{"".join(toc_entries)}</div>'
    css = build_css(cfg["title"], cfg["page_label"], cfg["of_label"])

    full_html = f"""<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8"><title>{cfg['title']}</title>
<style>{css}</style></head>
<body>{cover}{toc}{"".join(chapters_html)}</body></html>"""

    html_path = OUT_DIR / f"{cfg['output_basename']}.html"
    html_path.write_text(full_html, encoding="utf-8")
    print(f"\nHTML written: {html_path}")

    pdf_path = OUT_DIR / f"{cfg['output_basename']}.pdf"
    try:
        from weasyprint import HTML  # type: ignore
        HTML(string=full_html, base_url=str(OUT_DIR)).write_pdf(str(pdf_path))
        print(f"PDF written: {pdf_path}")
        return
    except Exception as e:
        print(f"  [info] WeasyPrint unavailable/failed ({e}); trying a browser fallback...")

    default_edge = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    browser = (
        shutil.which("msedge") or shutil.which("chrome") or shutil.which("google-chrome")
        or (default_edge if Path(default_edge).exists() else None)
    )
    if browser:
        subprocess.run([
            browser, "--headless", "--disable-gpu",
            f"--print-to-pdf={pdf_path}", html_path.as_uri(),
        ], check=False)
        if pdf_path.exists():
            print(f"PDF written via headless browser: {pdf_path}")
            return

    print(
        "\n  [manual step needed] No working PDF engine found on this machine.\n"
        f"  Open {html_path} in any browser and use File > Print > Save as PDF."
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--lang", choices=["en", "es"], default="en")
    args = parser.parse_args()
    print(f"Building handbook ({args.lang})...")
    build(args.lang)
