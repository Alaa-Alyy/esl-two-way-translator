"""Build PDFs from the Markdown sources in docs/en and docs/ar.

Usage:  python docs/build.py
Needs:  pip install markdown   +   Microsoft Edge or Google Chrome installed.
Output: docs/pdf/en/*.pdf and docs/pdf/ar/*.pdf
"""
import pathlib
import subprocess
import markdown

ROOT = pathlib.Path(__file__).resolve().parent
BROWSERS = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "/usr/bin/google-chrome",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
]

CSS = """
@page { size: A4; margin: 18mm 16mm 18mm 16mm; }
* { box-sizing: border-box; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { font-family: "Segoe UI", "Tahoma", "Arial", sans-serif; font-size: 10.5pt;
       line-height: 1.55; color: #1d2433; background: #fff; margin: 0; }
h1 { font-size: 20pt; color: #0b3d5c; border-bottom: 3px solid #1a7f8e; padding-bottom: 6px;
     margin: 28px 0 12px; page-break-after: avoid; }
h1:not(:first-of-type) { page-break-before: always; }
h2 { font-size: 14pt; color: #0b3d5c; margin: 22px 0 8px; page-break-after: avoid; }
h3 { font-size: 11.5pt; color: #1a7f8e; margin: 16px 0 6px; page-break-after: avoid; }
p { margin: 6px 0 8px; }
ul, ol { margin: 4px 0 10px; padding-inline-start: 22px; }
li { margin: 2px 0; }
table { border-collapse: collapse; width: 100%; margin: 8px 0 14px; font-size: 9.5pt;
        page-break-inside: auto; }
tr { page-break-inside: avoid; }
th { background: #0b3d5c; color: #fff; text-align: start; padding: 6px 8px; }
td { border-bottom: 1px solid #d6dde6; padding: 5px 8px; vertical-align: top; }
tr:nth-child(even) td { background: #f3f6f9; }
code { font-family: "Cascadia Mono", "Consolas", monospace; font-size: 9pt; background: #eef2f6;
       padding: 1px 4px; border-radius: 3px; direction: ltr; unicode-bidi: embed; }
pre { background: #f3f6f9; border: 1px solid #d6dde6; border-inline-start: 4px solid #1a7f8e;
      padding: 10px 12px; border-radius: 4px; overflow: hidden; white-space: pre-wrap;
      direction: ltr; text-align: left; page-break-inside: avoid; }
pre code { background: none; padding: 0; font-size: 8.6pt; }
blockquote { margin: 10px 0; padding: 8px 14px; background: #eaf6f7;
             border-inline-start: 4px solid #1a7f8e; color: #0b3d5c; }
strong { color: #0b3d5c; }
hr { border: none; border-top: 1px solid #d6dde6; margin: 18px 0; }
.cover { height: 250mm; display: flex; flex-direction: column; justify-content: center;
         page-break-after: always; }
.cover .kicker { color: #1a7f8e; font-weight: 600; letter-spacing: 0.06em; font-size: 11pt; }
.cover .title { font-size: 30pt; font-weight: 700; color: #0b3d5c; line-height: 1.2; margin: 10px 0; }
.cover .subtitle { font-size: 14pt; color: #3c4a5e; margin-bottom: 30px; }
.cover .meta { font-size: 10.5pt; color: #3c4a5e; border-top: 2px solid #1a7f8e; padding-top: 12px; }
.cover .meta div { margin: 3px 0; }
.box { border: 1px solid #1a7f8e; background: #f3fafb; border-radius: 6px; padding: 10px 14px;
       margin: 10px 0; page-break-inside: avoid; }
"""

TEMPLATE = """<!doctype html>
<html lang="{lang}" dir="{dir}"><head><meta charset="utf-8">
<title>{title}</title><style>{css}</style></head>
<body>{body}</body></html>"""


def find_browser():
    for b in BROWSERS:
        if pathlib.Path(b).exists():
            return b
    raise SystemExit("No Edge/Chrome found. Edit BROWSERS in build.py.")


def build(lang):
    src = ROOT / lang
    html_dir = ROOT / "build" / lang
    pdf_dir = ROOT / "pdf" / lang
    html_dir.mkdir(parents=True, exist_ok=True)
    pdf_dir.mkdir(parents=True, exist_ok=True)
    browser = find_browser()
    for md_file in sorted(src.glob("*.md")):
        text = md_file.read_text(encoding="utf-8")
        body = markdown.markdown(text, extensions=["tables", "fenced_code", "sane_lists", "md_in_html"])
        html = TEMPLATE.format(lang=lang, dir="rtl" if lang == "ar" else "ltr",
                               title=md_file.stem, css=CSS, body=body)
        html_file = html_dir / (md_file.stem + ".html")
        html_file.write_text(html, encoding="utf-8")
        pdf_file = pdf_dir / (md_file.stem + ".pdf")
        subprocess.run([browser, "--headless", "--disable-gpu", "--no-pdf-header-footer",
                        f"--print-to-pdf={pdf_file}", html_file.as_uri()],
                       check=True, capture_output=True)
        print("built", pdf_file.relative_to(ROOT))


if __name__ == "__main__":
    for lang in ("en", "ar"):
        if (ROOT / lang).exists():
            build(lang)
