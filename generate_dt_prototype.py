import os
import subprocess
import shutil

BASE_DIR = r"c:\Users\bhuva\OneDrive\Desktop\Returlooptesting"
OUTPUT_DIR = os.path.join(BASE_DIR, "design_thinking_prototype")
WIREFRAMES_DIR = os.path.join(OUTPUT_DIR, "wireframes")
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

os.makedirs(WIREFRAMES_DIR, exist_ok=True)

def render(html_content, output_png, width=1400, height=900, scale=2):
    temp_html = output_png.replace(".png", "_temp.html")
    with open(temp_html, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    cmd = [
        CHROME_PATH,
        "--headless=new",
        "--disable-gpu",
        f"--force-device-scale-factor={scale}",
        f"--screenshot={output_png}",
        f"--window-size={width},{height}",
        f"file:///{os.path.abspath(temp_html).replace(os.sep, '/')}"
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if os.path.exists(temp_html):
        os.remove(temp_html)
    
    if res.returncode == 0 and os.path.exists(output_png):
        print(f"✓ Generated: {os.path.basename(output_png)}")
        return True
    else:
        print(f"✗ Error generating {output_png}: {res.stderr}")
        return False

# Base CSS styles for ultra-clean wireframe rendering
BASE_CSS = """
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  background-color: #f8fafc;
  color: #0f172a;
  line-height: 1.4;
  -webkit-font-smoothing: antialiased;
}
.sheet {
  background: #ffffff;
  padding: 30px;
  width: 100%;
  min-height: 100vh;
}
.header-bar {
  border-bottom: 2px solid #0f172a;
  padding-bottom: 14px;
  margin-bottom: 24px;
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
}
.header-bar h1 {
  font-size: 24px;
  font-weight: 800;
  letter-spacing: -0.5px;
  text-transform: uppercase;
}
.header-bar .subtitle {
  font-size: 13px;
  color: #475569;
  font-weight: 500;
}
.header-bar .badge {
  font-size: 11px;
  font-weight: 700;
  background: #0f172a;
  color: #ffffff;
  padding: 4px 10px;
  border-radius: 6px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}
.phone-frame {
  width: 320px;
  height: 640px;
  border: 3px solid #0f172a;
  border-radius: 36px;
  background: #ffffff;
  position: relative;
  overflow: hidden;
  box-shadow: 0 10px 25px rgba(0,0,0,0.08);
  display: flex;
  flex-direction: column;
}
.phone-notch {
  width: 120px;
  height: 18px;
  background: #0f172a;
  margin: 0 auto;
  border-bottom-left-radius: 12px;
  border-bottom-right-radius: 12px;
}
.phone-screen {
  flex: 1;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  padding: 12px 14px;
}
.desktop-frame {
  border: 2px solid #0f172a;
  border-radius: 12px;
  background: #ffffff;
  overflow: hidden;
  box-shadow: 0 10px 25px rgba(0,0,0,0.06);
}
.desktop-titlebar {
  height: 32px;
  background: #f1f5f9;
  border-bottom: 1.5px solid #0f172a;
  display: flex;
  align-items: center;
  padding: 0 12px;
  gap: 6px;
}
.window-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  border: 1px solid #475569;
  background: #cbd5e1;
}
.window-url {
  flex: 1;
  margin: 0 20px;
  background: #ffffff;
  border: 1px solid #cbd5e1;
  border-radius: 4px;
  height: 20px;
  font-size: 10px;
  font-family: monospace;
  display: flex;
  align-items: center;
  padding: 0 8px;
  color: #475569;
}
.wf-nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1.5px solid #0f172a;
  padding: 8px 12px;
  margin-bottom: 12px;
  background: #f8fafc;
}
.wf-logo {
  font-weight: 800;
  font-size: 13px;
  display: flex;
  align-items: center;
  gap: 4px;
}
.wf-logo-box {
  width: 16px;
  height: 16px;
  border: 1.5px solid #0f172a;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 9px;
  font-weight: 900;
}
.wf-btn {
  border: 1.5px solid #0f172a;
  padding: 6px 12px;
  border-radius: 6px;
  font-size: 11px;
  font-weight: 700;
  text-align: center;
  background: #ffffff;
  color: #0f172a;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
}
.wf-btn-primary {
  background: #0f172a;
  color: #ffffff;
}
.wf-btn-secondary {
  background: #e2e8f0;
}
.wf-btn-danger {
  border-color: #0f172a;
  background: #fee2e2;
}
.wf-input {
  border: 1.5px solid #0f172a;
  border-radius: 6px;
  padding: 6px 10px;
  font-size: 11px;
  background: #ffffff;
  width: 100%;
}
.wf-label {
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 3px;
  display: block;
}
.wf-card {
  border: 1.5px solid #0f172a;
  border-radius: 8px;
  padding: 10px;
  background: #ffffff;
  margin-bottom: 8px;
}
.wf-tag {
  display: inline-block;
  padding: 2px 6px;
  border: 1px solid #0f172a;
  border-radius: 4px;
  font-size: 9px;
  font-weight: 700;
  text-transform: uppercase;
}
.wf-img-placeholder {
  border: 1.5px dashed #64748b;
  background: #f1f5f9;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  font-size: 10px;
  color: #475569;
  font-weight: 600;
}
.screen-num-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 26px;
  height: 26px;
  border-radius: 50%;
  background: #0f172a;
  color: #ffffff;
  font-weight: 800;
  font-size: 12px;
  margin-right: 8px;
}
.hand-tip {
  background: #fffbeb;
  border: 1.5px solid #d97706;
  border-radius: 6px;
  padding: 8px 12px;
  font-size: 11px;
  color: #92400e;
  margin-top: 10px;
}
"""

print("Base CSS configured.")
