"""
Convert CREWAI_REPORT.md to PDF using markdown + browser printing.
Generates an HTML file first, then uses playwright or webbrowser to print.
"""
import markdown
import os
import base64
import re

REPORT_PATH = os.path.join(os.path.dirname(__file__), "CREWAI_REPORT.md")
SCREENSHOTS_DIR = os.path.join(os.path.dirname(__file__), "screenshots")
OUTPUT_HTML = os.path.join(os.path.dirname(__file__), "CREWAI_REPORT.html")

# Read markdown
with open(REPORT_PATH, "r", encoding="utf-8") as f:
    md_content = f.read()

# Convert markdown to HTML
html_body = markdown.markdown(
    md_content,
    extensions=["tables", "fenced_code", "codehilite", "toc"]
)

# Embed images as base64
def embed_images(html, base_dir):
    """Replace image src with base64 embedded data"""
    img_pattern = r'<img\s+[^>]*src="([^"]+)"[^>]*/?\s*>'
    
    def replace_img(match):
        full_tag = match.group(0)
        src = match.group(1)
        
        # Resolve relative path
        if src.startswith("./"):
            src = src[2:]
        img_path = os.path.join(base_dir, src)
        
        if os.path.exists(img_path):
            ext = os.path.splitext(img_path)[1].lower()
            mime = "image/png" if ext == ".png" else "image/jpeg"
            with open(img_path, "rb") as img_f:
                b64 = base64.b64encode(img_f.read()).decode("utf-8")
            return full_tag.replace(match.group(1), f"data:{mime};base64,{b64}")
        return full_tag
    
    return re.sub(img_pattern, replace_img, html)

html_body = embed_images(html_body, os.path.dirname(REPORT_PATH))

# Build full HTML with styling
full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>CrewAI Implementation Report — SmartBasket</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
  
  body {{
    font-family: 'Inter', -apple-system, sans-serif;
    max-width: 900px;
    margin: 0 auto;
    padding: 40px 30px;
    color: #1a1a2e;
    line-height: 1.7;
    font-size: 14px;
  }}
  
  h1 {{ color: #0f3460; font-size: 28px; border-bottom: 3px solid #16213e; padding-bottom: 10px; }}
  h2 {{ color: #16213e; font-size: 22px; margin-top: 35px; border-bottom: 2px solid #e2e8f0; padding-bottom: 8px; }}
  h3 {{ color: #1a1a5e; font-size: 17px; margin-top: 25px; }}
  
  code {{
    background: #f1f5f9;
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 13px;
    font-family: 'Cascadia Code', 'Fira Code', monospace;
  }}
  
  pre {{
    background: #1e293b;
    color: #e2e8f0;
    padding: 16px;
    border-radius: 8px;
    overflow-x: auto;
    font-size: 12px;
    line-height: 1.5;
  }}
  pre code {{
    background: none;
    color: inherit;
    padding: 0;
  }}
  
  table {{
    width: 100%;
    border-collapse: collapse;
    margin: 15px 0;
    font-size: 13px;
  }}
  th {{
    background: #16213e;
    color: white;
    padding: 10px 12px;
    text-align: left;
  }}
  td {{
    padding: 8px 12px;
    border-bottom: 1px solid #e2e8f0;
  }}
  tr:nth-child(even) {{ background: #f8fafc; }}
  
  img {{
    max-width: 100%;
    border-radius: 8px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.15);
    margin: 15px 0;
  }}
  
  hr {{
    border: none;
    border-top: 1px solid #e2e8f0;
    margin: 30px 0;
  }}
  
  strong {{ color: #0f3460; }}
  
  @media print {{
    body {{ padding: 20px; font-size: 12px; }}
    pre {{ font-size: 10px; }}
    img {{ max-width: 85%; }}
    h1, h2 {{ page-break-after: avoid; }}
    pre, img {{ page-break-inside: avoid; }}
  }}
</style>
</head>
<body>
{html_body}
</body>
</html>"""

with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
    f.write(full_html)

print(f"HTML report generated: {OUTPUT_HTML}")
print("Open this file in your browser and press Ctrl+P → Save as PDF")
print(f"File size: {os.path.getsize(OUTPUT_HTML) / 1024:.1f} KB")
