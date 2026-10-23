"""Regenerate index.html from every <app>/meta.json in the repo root."""
import html
import json
import os
from pathlib import Path

base = os.environ["BASE_URL"].rstrip("/")
root = Path(__file__).resolve().parent.parent

apps = []
for meta_path in sorted(root.glob("*/meta.json")):
    apps.append(json.loads(meta_path.read_text(encoding="utf-8")))

def notes_html(notes):
    lines = [line.strip() for line in notes.splitlines() if line.strip()]
    if not lines:
        return ""
    body = "<br>".join(html.escape(line) for line in lines)
    return f"<p><strong>What's new:</strong> {body}</p>"


items = []
for app in apps:
    manifest = f"{base}/{app['slug']}/manifest.plist"
    link = "itms-services://?action=download-manifest&url=" + manifest
    items.append(
        "<li>"
        f'<a href="{html.escape(link)}">Install {html.escape(app["name"])}</a>'
        f'<p>Version {html.escape(app["version"])}, built {html.escape(app["built"])}</p>'
        + notes_html(app.get("notes", ""))
        + "</li>"
    )

body = "\n".join(items) if items else "<li><p>Nothing here yet.</p></li>"

page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light dark">
<title>Bucket</title>
<style>
  body {{ font: 18px/1.5 -apple-system, system-ui, sans-serif; margin: 0 auto; max-width: 36rem; padding: 1.5rem 16px; }}
  ul {{ list-style: none; padding: 0; }}
  li {{ margin: 0 0 1.5rem; }}
  a {{ display: inline-block; padding: 0.75rem 0; font-weight: 600; }}
  p {{ margin: 0; opacity: 0.75; }}
</style>
</head>
<body>
<main>
<h1>Bucket</h1>
<ul>
{body}
</ul>
</main>
</body>
</html>
"""

(root / "index.html").write_text(page, encoding="utf-8")
print(f"Wrote index.html with {len(apps)} app(s)")
