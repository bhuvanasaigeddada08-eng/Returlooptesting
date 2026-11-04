import subprocess
import os

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
html_content = """<!DOCTYPE html>
<html>
<head>
<style>
body { margin: 0; padding: 40px; background: #ffffff; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; }
.card { border: 2px solid #000; padding: 20px; border-radius: 8px; width: 400px; }
h1 { margin-top: 0; font-size: 20px; }
</style>
</head>
<body>
<div class="card">
  <h1>Test Wireframe</h1>
  <p>Testing headless Chrome rendering</p>
</div>
</body>
</html>
"""

temp_html = os.path.abspath("test_render.html")
test_png = os.path.abspath("test_shot.png")

with open(temp_html, "w", encoding="utf-8") as f:
    f.write(html_content)

cmd = [
    chrome_path,
    "--headless=new",
    "--disable-gpu",
    "--force-device-scale-factor=2",
    f"--screenshot={test_png}",
    "--window-size=800,600",
    f"file:///{temp_html.replace(os.sep, '/')}"
]

res = subprocess.run(cmd, capture_output=True, text=True)
print("Return code:", res.returncode)
print("PNG exists:", os.path.exists(test_png), "Size:", os.path.getsize(test_png) if os.path.exists(test_png) else 0)

if os.path.exists(temp_html): os.remove(temp_html)
if os.path.exists(test_png): os.remove(test_png)
