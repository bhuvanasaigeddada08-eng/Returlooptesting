import os
import subprocess
import shutil

BASE_DIR = r"c:\Users\bhuva\OneDrive\Desktop\Returlooptesting"
OUTPUT_DIR = os.path.join(BASE_DIR, "design_thinking_prototype")
WIREFRAMES_DIR = os.path.join(OUTPUT_DIR, "wireframes")
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

os.makedirs(WIREFRAMES_DIR, exist_ok=True)

def render_html_to_png(html_content, output_png_path, width=1400, height=900, scale=2):
    temp_html = output_png_path.replace(".png", "_temp.html")
    with open(temp_html, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    cmd = [
        CHROME_PATH,
        "--headless=new",
        "--disable-gpu",
        f"--force-device-scale-factor={scale}",
        f"--screenshot={output_png_path}",
        f"--window-size={width},{height}",
        f"file:///{os.path.abspath(temp_html).replace(os.sep, '/')}"
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if os.path.exists(temp_html):
        os.remove(temp_html)
    
    if res.returncode == 0 and os.path.exists(output_png_path):
        print(f"Generated: {os.path.basename(output_png_path)} ({os.path.getsize(output_png_path)} bytes)")
        return True
    else:
        print(f"Error generating {output_png_path}: {res.stderr}")
        return False

print("Setup completed successfully.")
