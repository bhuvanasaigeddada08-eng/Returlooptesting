import os
import subprocess

BASE_DIR = r"c:\Users\bhuva\OneDrive\Desktop\Returlooptesting"
OUTPUT_DIR = os.path.join(BASE_DIR, "design_thinking_prototype")
WIREFRAMES_DIR = os.path.join(OUTPUT_DIR, "wireframes")
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

os.makedirs(WIREFRAMES_DIR, exist_ok=True)

def render_wireframe(html_content, output_png, width=1280, height=880):
    temp_html = output_png.replace(".png", "_temp.html")
    with open(temp_html, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    cmd = [
        CHROME_PATH,
        "--headless=new",
        "--disable-gpu",
        "--force-device-scale-factor=2",
        f"--screenshot={output_png}",
        f"--window-size={width},{height}",
        f"file:///{os.path.abspath(temp_html).replace(os.sep, '/')}"
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if os.path.exists(temp_html):
        try: os.remove(temp_html)
        except: pass
    
    if res.returncode == 0 and os.path.exists(output_png):
        print(f"[OK] Generated: wireframes/{os.path.basename(output_png)} ({os.path.getsize(output_png):,} bytes)")
        return True
    else:
        print(f"[ERROR] Failed {output_png}: {res.stderr}")
        return False

# Base CSS for clean low-fidelity hand-drawable wireframes
BASE_CSS = """
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    background: #f1f5f9;
    color: #0f172a;
    padding: 24px;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
}
.wf-canvas {
    width: 1200px;
    background: #ffffff;
    border: 3px solid #0f172a;
    border-radius: 16px;
    overflow: hidden;
    box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    display: flex;
    flex-direction: column;
}
.wf-header-bar {
    background: #0f172a;
    color: #ffffff;
    padding: 12px 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 13px;
    font-weight: 700;
}
.wf-header-bar .tag-id {
    background: #ffffff;
    color: #0f172a;
    padding: 3px 10px;
    border-radius: 4px;
    font-weight: 900;
    font-size: 11px;
}
.app-nav {
    border-bottom: 2px solid #0f172a;
    padding: 14px 24px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: #ffffff;
}
.app-logo {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 18px;
    font-weight: 900;
    letter-spacing: -0.5px;
}
.logo-icon {
    width: 26px;
    height: 26px;
    border: 2px solid #0f172a;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 13px;
    font-weight: 900;
}
.badge-lpu {
    font-size: 10px;
    background: #e2e8f0;
    border: 1.5px solid #0f172a;
    padding: 2px 6px;
    border-radius: 4px;
    font-weight: 800;
}
.nav-links {
    display: flex;
    gap: 20px;
    align-items: center;
    font-size: 13px;
    font-weight: 700;
}
.nav-item {
    padding: 6px 12px;
    border-radius: 6px;
    border: 1.5px solid transparent;
}
.nav-item.active {
    border: 1.5px solid #0f172a;
    background: #f8fafc;
}
.app-content {
    padding: 24px;
    flex: 1;
    background: #ffffff;
}

/* UI Elements */
.box {
    border: 2px solid #0f172a;
    border-radius: 8px;
    padding: 16px;
    background: #ffffff;
    margin-bottom: 16px;
}
.box-dark {
    background: #0f172a;
    color: #ffffff;
    border: 2px solid #0f172a;
}
.box-gray {
    background: #f8fafc;
    border: 2px solid #cbd5e1;
}
.box-dashed {
    border: 2px dashed #64748b;
    background: #f8fafc;
    text-align: center;
    padding: 24px;
}
.btn {
    display: inline-block;
    padding: 10px 18px;
    border: 2px solid #0f172a;
    border-radius: 6px;
    font-weight: 800;
    font-size: 13px;
    text-align: center;
    cursor: pointer;
    background: #ffffff;
    color: #0f172a;
}
.btn-dark {
    background: #0f172a;
    color: #ffffff;
}
.input-field {
    border: 2px solid #0f172a;
    border-radius: 6px;
    padding: 10px 12px;
    width: 100%;
    font-size: 12px;
    font-weight: 600;
    color: #334155;
    background: #ffffff;
    margin-top: 5px;
}
.input-label {
    font-size: 11px;
    font-weight: 800;
    text-transform: uppercase;
    color: #475569;
    display: block;
}
.grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
.grid-3 { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 16px; }
.grid-4 { display: grid; grid-template-columns: 1fr 1fr 1fr 1fr; gap: 14px; }

.wf-footer-bar {
    border-top: 2px solid #0f172a;
    padding: 12px 20px;
    background: #f8fafc;
    display: flex;
    justify-content: space-between;
    font-size: 11px;
    font-weight: 700;
    color: #475569;
}
.pill {
    display: inline-block;
    padding: 3px 8px;
    border: 1.5px solid #0f172a;
    border-radius: 12px;
    font-size: 10px;
    font-weight: 800;
}
.pill-dark { background: #0f172a; color: #fff; }
"""

# Screen 1: Landing Page
def wf_01():
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{BASE_CSS}</style></head><body>
<div class="wf-canvas">
  <div class="wf-header-bar">
    <span>INT335 DESIGN THINKING PROTOTYPE • LOW-FIDELITY WIREFRAME</span>
    <span class="tag-id">SCREEN 01 • LANDING PAGE (DESKTOP / MOBILE)</span>
  </div>
  <div class="app-nav">
    <div class="app-logo"><div class="logo-icon">RL</div>ReturnLoop <span class="badge-lpu">LPU</span></div>
    <div class="nav-links">
      <span class="nav-item active">Explore</span>
      <span class="nav-item">My Items</span>
      <span class="nav-item">+ Report</span>
      <span class="nav-item">Notifications</span>
      <span class="btn btn-dark" style="padding: 6px 14px; font-size: 12px;">Sign In</span>
    </div>
  </div>
  <div class="app-content">
    <div class="box box-dark" style="padding: 36px 30px; margin-bottom: 24px;">
      <span class="pill" style="border-color:#fff; color:#fff; margin-bottom: 12px;">Lovely Professional University • Campus Recovery System</span>
      <h1 style="font-size: 32px; font-weight: 900; margin: 12px 0 8px 0; line-height: 1.2;">Lost something on campus?<br>Let's bring it back into the loop.</h1>
      <p style="font-size: 13px; color: #cbd5e1; max-width: 650px; margin-bottom: 24px;">ReturnLoop LPU replaces chaotic WhatsApp chats with a privacy-preserving registry. Report lost or found items, discover algorithmic matches, and verify ownership safely.</p>
      
      <div style="display: flex; gap: 10px; max-width: 700px; margin-bottom: 20px;">
        <input class="input-field" style="margin:0; flex:1; font-size:13px;" value="[ Search lost & found items (e.g. HP laptop, Milton bottle, ID card)... ]">
        <button class="btn btn-dark" style="background:#ffffff; color:#0f172a; border-color:#ffffff;">Search Items</button>
      </div>

      <div style="display: flex; gap: 12px; align-items: center;">
        <span class="btn" style="background:#fee2e2; border-color:#ef4444; color:#991b1b; font-weight:900;">[+] Report Lost Belonging</span>
        <span class="btn" style="background:#dcfce7; border-color:#22c55e; color:#166534; font-weight:900;">[+] Report Found Item</span>
        <span class="btn" style="background:transparent; border-color:#ffffff; color:#ffffff;">Explore All Listings -></span>
      </div>
    </div>

    <div class="grid-3">
      <div class="box">
        <div style="font-weight: 900; font-size: 18px; margin-bottom: 4px;">100% Free</div>
        <div style="font-size: 11px; font-weight: 700; color: #64748b; text-transform: uppercase;">Campus Registry</div>
        <p style="font-size: 12px; color: #334155; margin-top: 8px;">Zero fees for students and staff. Pure university service protocol.</p>
      </div>
      <div class="box">
        <div style="font-weight: 900; font-size: 18px; margin-bottom: 4px;">5-Trait Engine</div>
        <div style="font-size: 11px; font-weight: 700; color: #64748b; text-transform: uppercase;">Algorithmic Matching</div>
        <p style="font-size: 12px; color: #334155; margin-top: 8px;">Scans Category, Brand, Color, Location, and Time window for matches.</p>
      </div>
      <div class="box">
        <div style="font-weight: 900; font-size: 18px; margin-bottom: 4px;">Verified Handover</div>
        <div style="font-size: 11px; font-weight: 700; color: #64748b; text-transform: uppercase;">Physical Security Points</div>
        <p style="font-size: 12px; color: #334155; margin-top: 8px;">Physical handover authorized via Central Security / UniMall Helpdesk.</p>
      </div>
    </div>
  </div>
  <div class="wf-footer-bar">
    <span>PRIMARY ACTION: Search Items / Report Lost or Found</span>
    <span>NEXT NAVIGATION: -> Screen 02 (Report Lost) or -> Screen 04 (Explore)</span>
  </div>
</div>
</body></html>"""
    render_wireframe(html, os.path.join(WIREFRAMES_DIR, "01_landing_page.png"))

# Screen 2: Report Lost Belonging
def wf_02():
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{BASE_CSS}</style></head><body>
<div class="wf-canvas">
  <div class="wf-header-bar">
    <span>INT335 DESIGN THINKING PROTOTYPE • LOW-FIDELITY WIREFRAME</span>
    <span class="tag-id">SCREEN 02 • REPORT LOST BELONGING</span>
  </div>
  <div class="app-nav">
    <div class="app-logo"><div class="logo-icon">RL</div>ReturnLoop <span class="badge-lpu">LPU</span></div>
    <div class="nav-links"><span class="nav-item">Explore</span><span class="nav-item active">+ Report Lost</span><span class="nav-item">Dashboard</span></div>
  </div>
  <div class="app-content">
    <div style="margin-bottom: 16px;">
      <h2 style="font-size: 20px; font-weight: 900;">Report a Lost Belonging</h2>
      <p style="font-size: 12px; color: #64748b;">Enter accurate details to help our 5-trait similarity algorithm find your item across campus.</p>
    </div>

    <div class="grid-2">
      <div>
        <div style="margin-bottom: 12px;">
          <label class="input-label">Item Title *</label>
          <input class="input-field" value="HP Pavilion 14 Laptop (Core i5, 16GB)">
        </div>
        <div class="grid-2" style="margin-bottom: 12px;">
          <div>
            <label class="input-label">Category *</label>
            <input class="input-field" value="Electronics & Laptops [v]">
          </div>
          <div>
            <label class="input-label">Brand / Model</label>
            <input class="input-field" value="HP Pavilion 14">
          </div>
        </div>
        <div class="grid-2" style="margin-bottom: 12px;">
          <div>
            <label class="input-label">Primary Color *</label>
            <input class="input-field" value="Jet Black">
          </div>
          <div>
            <label class="input-label">Campus Location Lost *</label>
            <input class="input-field" value="Block 34 - 3rd Floor Computer Lab [v]">
          </div>
        </div>
        <div style="margin-bottom: 12px;">
          <label class="input-label">Date & Approx Time Lost *</label>
          <input class="input-field" value="2026-10-28 • 16:30 PM">
        </div>
      </div>

      <div>
        <div style="margin-bottom: 12px;">
          <label class="input-label">Detailed Description</label>
          <div class="input-field" style="height: 60px;">Left in a dark gray neoprene sleeve on desk row 3 after CSE practical exam. Mouse and charger inside pouch.</div>
        </div>
        <div style="margin-bottom: 12px;">
          <label class="input-label">Private Traits / Secret Proof (Hidden from Public)</label>
          <div class="input-field" style="height: 50px; border-style: dashed; background: #fffbeb;">Sticker of NASA on top lid; desktop wallpaper is purple nebula; serial no ends in 89B.</div>
        </div>
        <div class="box-dashed" style="padding: 16px; margin-bottom: 12px;">
          <div style="font-weight: 800; font-size: 12px;">[+] Drag & Drop or Upload Photo</div>
          <div style="font-size: 10px; color: #64748b;">PNG, JPG up to 5MB (Optional reference photo)</div>
        </div>
      </div>
    </div>

    <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 10px;">
      <span style="font-size: 11px; color: #64748b;">* Required fields for 5-trait algorithmic matching</span>
      <div style="display: flex; gap: 10px;">
        <span class="btn">[ Cancel ]</span>
        <span class="btn btn-dark">[ Publish Lost Report & Run Match Engine -> ]</span>
      </div>
    </div>
  </div>
  <div class="wf-footer-bar">
    <span>PRIMARY ACTION: Publish Lost Report</span>
    <span>NEXT NAVIGATION: -> Screen 05 (Item Details & AI Match Result)</span>
  </div>
</div>
</body></html>"""
    render_wireframe(html, os.path.join(WIREFRAMES_DIR, "02_report_lost_page.png"))

# Screen 3: Report Found Item
def wf_03():
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{BASE_CSS}</style></head><body>
<div class="wf-canvas">
  <div class="wf-header-bar">
    <span>INT335 DESIGN THINKING PROTOTYPE • LOW-FIDELITY WIREFRAME</span>
    <span class="tag-id">SCREEN 03 • REPORT FOUND ITEM (GOOD SAMARITAN)</span>
  </div>
  <div class="app-nav">
    <div class="app-logo"><div class="logo-icon">RL</div>ReturnLoop <span class="badge-lpu">LPU</span></div>
    <div class="nav-links"><span class="nav-item">Explore</span><span class="nav-item active">+ Report Found</span><span class="nav-item">Dashboard</span></div>
  </div>
  <div class="app-content">
    <div style="margin-bottom: 16px;">
      <h2 style="font-size: 20px; font-weight: 900;">Report a Found Item (Good Samaritan Protocol)</h2>
      <p style="font-size: 12px; color: #64748b;">Thank you for helping keep LPU honest! Register found property without exposing your phone number.</p>
    </div>

    <div class="grid-2">
      <div>
        <div style="margin-bottom: 12px;">
          <label class="input-label">Found Item Title *</label>
          <input class="input-field" value="Milton Thermosteel Water Bottle (1000ml)">
        </div>
        <div class="grid-2" style="margin-bottom: 12px;">
          <div>
            <label class="input-label">Category *</label>
            <input class="input-field" value="Bottles & Tumblers [v]">
          </div>
          <div>
            <label class="input-label">Brand / Model</label>
            <input class="input-field" value="Milton Thermosteel">
          </div>
        </div>
        <div class="grid-2" style="margin-bottom: 12px;">
          <div>
            <label class="input-label">Primary Color *</label>
            <input class="input-field" value="Matte Black">
          </div>
          <div>
            <label class="input-label">Where Was It Found? *</label>
            <input class="input-field" value="Baldev Raj Mittal Unipolis [v]">
          </div>
        </div>
        <div style="margin-bottom: 12px;">
          <label class="input-label">Date & Time Found *</label>
          <input class="input-field" value="2026-10-22 • 14:15 PM">
        </div>
      </div>

      <div>
        <div style="margin-bottom: 12px;">
          <label class="input-label">Current Custody Status *</label>
          <input class="input-field" value="Deposited at UniMall Security Office Room 102 [v]">
        </div>
        <div style="margin-bottom: 12px;">
          <label class="input-label">Verification Challenge Question (For Claimant)</label>
          <input class="input-field" value="What color is the carabiner clip attached to the lid?">
        </div>
        <div class="box-dashed" style="padding: 20px; margin-bottom: 12px;">
          <div style="font-weight: 800; font-size: 12px;">[ Image Uploaded: milton_bottle_unipolis.jpg ]</div>
          <div style="font-size: 10px; color: #64748b;">AI blur applied to private personal stickers</div>
        </div>
      </div>
    </div>

    <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 10px;">
      <span style="font-size: 11px; color: #64748b;">Good Samaritan Protocol: Your identity remains protected.</span>
      <div style="display: flex; gap: 10px;">
        <span class="btn">[ Cancel ]</span>
        <span class="btn btn-dark" style="background:#166534; border-color:#166534;">[ Register Found Item & Alert Matches -> ]</span>
      </div>
    </div>
  </div>
  <div class="wf-footer-bar">
    <span>PRIMARY ACTION: Register Found Item</span>
    <span>NEXT NAVIGATION: -> Screen 07 (Dashboard Confirmation & Instant Notifications)</span>
  </div>
</div>
</body></html>"""
    render_wireframe(html, os.path.join(WIREFRAMES_DIR, "03_report_found_page.png"))

# Screen 4: Explore Campus Listings
def wf_04():
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{BASE_CSS}</style></head><body>
<div class="wf-canvas">
  <div class="wf-header-bar">
    <span>INT335 DESIGN THINKING PROTOTYPE • LOW-FIDELITY WIREFRAME</span>
    <span class="tag-id">SCREEN 04 • EXPLORE CAMPUS LISTINGS</span>
  </div>
  <div class="app-nav">
    <div class="app-logo"><div class="logo-icon">RL</div>ReturnLoop <span class="badge-lpu">LPU</span></div>
    <div class="nav-links"><span class="nav-item active">Explore</span><span class="nav-item">My Items</span><span class="nav-item">+ Report</span><span class="nav-item">Dashboard</span></div>
  </div>
  <div class="app-content">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
      <div>
        <h2 style="font-size: 20px; font-weight: 900;">Explore Campus Listings</h2>
        <p style="font-size: 12px; color: #64748b;">Browse privacy-safe lost belongings and found reports across LPU.</p>
      </div>
      <div style="display: flex; gap: 8px;">
        <span class="btn btn-dark" style="padding: 6px 12px; font-size: 11px;">[ Grid View ]</span>
        <span class="btn" style="padding: 6px 12px; font-size: 11px;">[ List View ]</span>
      </div>
    </div>

    <!-- Filters -->
    <div class="box box-gray" style="padding: 12px; margin-bottom: 16px;">
      <div style="display: flex; gap: 10px; margin-bottom: 10px;">
        <input class="input-field" style="margin:0; flex:1;" value="[ Search by keywords, title, color, block... ]">
        <button class="btn btn-dark">Search</button>
      </div>
      <div style="display: flex; gap: 8px; flex-wrap: wrap; font-size: 11px; font-weight: 700;">
        <span class="pill pill-dark">All Categories</span>
        <span class="pill">Electronics</span>
        <span class="pill">ID & Cards</span>
        <span class="pill">Bags & Wallets</span>
        <span class="pill">Bottles</span>
        <span class="pill" style="margin-left: auto;">Status: [ All Listings v ]</span>
        <span class="pill">Location: [ All LPU Blocks v ]</span>
      </div>
    </div>

    <!-- Cards Grid -->
    <div class="grid-4">
      <div class="box" style="padding: 10px;">
        <div style="height: 100px; border: 1.5px dashed #94a3b8; background: #f8fafc; display:flex; align-items:center; justify-content:center; font-size:10px; font-weight:700; margin-bottom:8px;">[ Item Photo / Milton Flask ]</div>
        <span class="pill" style="background:#dcfce7; border-color:#16a34a; color:#166534; font-size:9px;">FOUND</span>
        <div style="font-weight: 800; font-size: 12px; margin: 4px 0;">Milton Thermosteel 1000ml</div>
        <div style="font-size: 10px; color: #64748b;">Baldev Raj Mittal Unipolis</div>
        <div style="font-size: 9px; color: #94a3b8; margin: 4px 0;">Oct 22, 2026</div>
        <button class="btn btn-dark" style="width: 100%; padding: 6px; font-size: 10px; margin-top: 6px;">View Details & Matches -></button>
      </div>

      <div class="box" style="padding: 10px;">
        <div style="height: 100px; border: 1.5px dashed #94a3b8; background: #f8fafc; display:flex; align-items:center; justify-content:center; font-size:10px; font-weight:700; margin-bottom:8px;">[ Item Photo / HP Laptop ]</div>
        <span class="pill" style="background:#fee2e2; border-color:#dc2626; color:#991b1b; font-size:9px;">LOST</span>
        <div style="font-weight: 800; font-size: 12px; margin: 4px 0;">HP Pavilion 14 Core i5</div>
        <div style="font-size: 10px; color: #64748b;">Block 34 - 3rd Floor Lab</div>
        <div style="font-size: 9px; color: #94a3b8; margin: 4px 0;">Oct 28, 2026</div>
        <button class="btn btn-dark" style="width: 100%; padding: 6px; font-size: 10px; margin-top: 6px;">View Details & Matches -></button>
      </div>

      <div class="box" style="padding: 10px;">
        <div style="height: 100px; border: 1.5px dashed #94a3b8; background: #f8fafc; display:flex; align-items:center; justify-content:center; font-size:10px; font-weight:700; margin-bottom:8px;">[ LPU Identity Card ]</div>
        <span class="pill" style="background:#dcfce7; border-color:#16a34a; color:#166534; font-size:9px;">FOUND</span>
        <div style="font-weight: 800; font-size: 12px; margin: 4px 0;">LPU Student ID Card</div>
        <div style="font-size: 10px; color: #64748b;">Central Library Gate 2</div>
        <div style="font-size: 9px; color: #94a3b8; margin: 4px 0;">Oct 27, 2026</div>
        <button class="btn btn-dark" style="width: 100%; padding: 6px; font-size: 10px; margin-top: 6px;">View Details & Matches -></button>
      </div>

      <div class="box" style="padding: 10px;">
        <div style="height: 100px; border: 1.5px dashed #94a3b8; background: #f8fafc; display:flex; align-items:center; justify-content:center; font-size:10px; font-weight:700; margin-bottom:8px;">[ Wildcraft Backpack ]</div>
        <span class="pill" style="background:#fee2e2; border-color:#dc2626; color:#991b1b; font-size:9px;">LOST</span>
        <div style="font-weight: 800; font-size: 12px; margin: 4px 0;">Wildcraft Navy Backpack</div>
        <div style="font-size: 10px; color: #64748b;">UniMall Food Court</div>
        <div style="font-size: 9px; color: #94a3b8; margin: 4px 0;">Oct 26, 2026</div>
        <button class="btn btn-dark" style="width: 100%; padding: 6px; font-size: 10px; margin-top: 6px;">View Details & Matches -></button>
      </div>
    </div>
  </div>
  <div class="wf-footer-bar">
    <span>PRIMARY ACTION: Filter Listings / Select Item Card</span>
    <span>NEXT NAVIGATION: -> Screen 05 (Item Details & Match Engine)</span>
  </div>
</div>
</body></html>"""
    render_wireframe(html, os.path.join(WIREFRAMES_DIR, "04_explore_items_page.png"))

# Screen 5: Item Details & Match Engine
def wf_05():
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{BASE_CSS}</style></head><body>
<div class="wf-canvas">
  <div class="wf-header-bar">
    <span>INT335 DESIGN THINKING PROTOTYPE • LOW-FIDELITY WIREFRAME</span>
    <span class="tag-id">SCREEN 05 • ITEM DETAILS & MATCH ENGINE</span>
  </div>
  <div class="app-nav">
    <div class="app-logo"><div class="logo-icon">RL</div>ReturnLoop <span class="badge-lpu">LPU</span></div>
    <div class="nav-links"><span class="nav-item">Explore</span><span class="nav-item active">Item #RL-LOST-2026-98742</span><span class="nav-item">Dashboard</span></div>
  </div>
  <div class="app-content">
    <div class="grid-2">
      <!-- Left: Item Info -->
      <div>
        <div style="display:flex; gap:8px; align-items:center; margin-bottom: 8px;">
          <span class="pill" style="background:#fee2e2; border-color:#dc2626; color:#991b1b;">LOST BELONGING</span>
          <span class="pill pill-dark">Ref: #RL-LOST-2026-98742</span>
          <span class="pill">Active</span>
        </div>
        <h2 style="font-size: 22px; font-weight: 900; margin-bottom: 4px;">HP Pavilion 14 Laptop (Core i5, 16GB)</h2>
        <p style="font-size: 12px; color: #64748b; margin-bottom: 14px;">Reported lost on Oct 28, 2026 at Block 34 (3rd Floor Lab)</p>

        <div class="box box-gray" style="padding: 12px; margin-bottom: 12px;">
          <div class="grid-2" style="font-size: 11px;">
            <div><strong>Category:</strong> Electronics</div>
            <div><strong>Brand:</strong> HP Pavilion</div>
            <div><strong>Color:</strong> Jet Black</div>
            <div><strong>Location:</strong> Block 34 Lab</div>
          </div>
        </div>

        <div style="font-size: 12px; margin-bottom: 16px; line-height: 1.4;">
          <strong>Public Description:</strong><br>
          Black HP Pavilion laptop in gray sleeve with green wireless mouse left after evening practical exam.
        </div>

        <div style="display: flex; gap: 10px;">
          <span class="btn btn-dark">[ Claim This Item -> ]</span>
          <span class="btn">[ Download Missing Poster PDF ]</span>
        </div>
      </div>

      <!-- Right: AI Match Result Box -->
      <div>
        <div class="box" style="border: 2px solid #0f172a; background: #f8fafc;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
            <span style="font-weight:900; font-size:13px;">5-TRAIT SIMILARITY MATCH ENGINE</span>
            <span class="pill pill-dark">88% MATCH</span>
          </div>

          <div style="background:#ffffff; border:1.5px solid #0f172a; border-radius:6px; padding:10px; margin-bottom:10px;">
            <div style="font-size:11px; font-weight:800; color:#166534;">[!] High Probability Found Match Detected</div>
            <div style="font-size:11px; font-weight:700; margin-top:4px;">Found Item: "HP Laptop in Gray Sleeve"</div>
            <div style="font-size:10px; color:#64748b;">Reported by Security Guard • Block 34 Custody Desk</div>
            
            <div style="margin-top: 8px; font-size: 10px; border-top: 1px solid #e2e8f0; padding-top: 6px;">
              <div>[✓] Category Match: Electronics (100%)</div>
              <div>[✓] Brand Match: HP (100%)</div>
              <div>[✓] Color Match: Black/Gray (90%)</div>
              <div>[✓] Location Match: Block 34 (100%)</div>
              <div>[~] Time Window: Within 2 hours (80%)</div>
            </div>
          </div>

          <div style="font-size: 11px; color: #475569; margin-bottom: 10px;">
            To maintain zero-trust security, serial numbers and private traits are hidden until physical verification.
          </div>

          <button class="btn btn-dark" style="width: 100%;">Initiate Secure Ownership Claim -></button>
        </div>
      </div>
    </div>
  </div>
  <div class="wf-footer-bar">
    <span>PRIMARY ACTION: Review 88% Trait Match & Click [ Claim This Item ]</span>
    <span>NEXT NAVIGATION: -> Screen 06 (Ownership Claim Submission)</span>
  </div>
</div>
</body></html>"""
    render_wireframe(html, os.path.join(WIREFRAMES_DIR, "05_item_details_page.png"))

# Screen 6: Ownership Claim Submission
def wf_06():
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{BASE_CSS}</style></head><body>
<div class="wf-canvas">
  <div class="wf-header-bar">
    <span>INT335 DESIGN THINKING PROTOTYPE • LOW-FIDELITY WIREFRAME</span>
    <span class="tag-id">SCREEN 06 • CLAIM SUBMISSION & VERIFICATION PROTOCOL</span>
  </div>
  <div class="app-nav">
    <div class="app-logo"><div class="logo-icon">RL</div>ReturnLoop <span class="badge-lpu">LPU</span></div>
    <div class="nav-links"><span class="nav-item">Explore</span><span class="nav-item active">Claim Item</span><span class="nav-item">Dashboard</span></div>
  </div>
  <div class="app-content">
    <div style="margin-bottom: 16px;">
      <h2 style="font-size: 20px; font-weight: 900;">Submit Ownership Claim</h2>
      <p style="font-size: 12px; color: #64748b;">Zero-Trust Campus Protocol: Verify ownership traits before item release at LPU Security.</p>
    </div>

    <div class="grid-2">
      <div>
        <div class="box box-gray" style="padding: 10px; margin-bottom: 14px;">
          <div style="font-size: 11px; font-weight: 800;">Target Item: HP Pavilion 14 Laptop</div>
          <div style="font-size: 10px; color: #64748b;">Item Ref: #RL-LOST-2026-98742 • Custody: Block 34 Security</div>
        </div>

        <div style="margin-bottom: 12px;">
          <label class="input-label">Claimant Full Name & LPU Reg Number *</label>
          <input class="input-field" value="Bhuvanesh • Reg # 12204567">
        </div>
        <div style="margin-bottom: 12px;">
          <label class="input-label">University Email ID *</label>
          <input class="input-field" value="bhuvanesh.12204567@lpu.in">
        </div>
        <div style="margin-bottom: 12px;">
          <label class="input-label">Select Preferred Handover Station *</label>
          <input class="input-field" value="Central Security Office (Near Main Gate 1) [v]">
        </div>
      </div>

      <div>
        <div style="margin-bottom: 12px;">
          <label class="input-label">Private Ownership Proof / Secret Verification Traits *</label>
          <div class="input-field" style="height: 70px;">
            1. Laptop serial number ends in '89B' (visible in BIOS/invoice).<br>
            2. Sticker of NASA with torn left edge on top corner.<br>
            3. Desktop wallpaper is purple deep space.
          </div>
        </div>

        <div class="box-dashed" style="padding: 16px; margin-bottom: 12px;">
          <div style="font-weight: 800; font-size: 11px;">[ Upload Bill / Serial Photo / ID Card ]</div>
          <div style="font-size: 9px; color: #64748b;">Uploaded: hp_purchase_invoice.pdf (1.2 MB)</div>
        </div>

        <div class="box" style="background:#fef2f2; border-color:#ef4444; padding:8px; font-size:10px; color:#991b1b;">
          <strong>Anti-Fraud Warning:</strong> False claims violate LPU Code of Conduct and result in immediate UMC disciplinary committee reporting.
        </div>
      </div>
    </div>

    <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 10px;">
      <span style="font-size: 11px; color: #64748b;">Verification typically processed within 2-4 campus hours.</span>
      <div style="display: flex; gap: 10px;">
        <span class="btn">[ Cancel ]</span>
        <span class="btn btn-dark">[ Submit Claim for Admin Verification -> ]</span>
      </div>
    </div>
  </div>
  <div class="wf-footer-bar">
    <span>PRIMARY ACTION: Submit Ownership Claim Form</span>
    <span>NEXT NAVIGATION: -> Screen 07 (Student Dashboard) & Screen 10 (Admin Verification)</span>
  </div>
</div>
</body></html>"""
    render_wireframe(html, os.path.join(WIREFRAMES_DIR, "06_claim_submission_page.png"))

# Screen 7: Student Dashboard
def wf_07():
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{BASE_CSS}</style></head><body>
<div class="wf-canvas">
  <div class="wf-header-bar">
    <span>INT335 DESIGN THINKING PROTOTYPE • LOW-FIDELITY WIREFRAME</span>
    <span class="tag-id">SCREEN 07 • STUDENT RECOVERY DASHBOARD</span>
  </div>
  <div class="app-nav">
    <div class="app-logo"><div class="logo-icon">RL</div>ReturnLoop <span class="badge-lpu">LPU</span></div>
    <div class="nav-links"><span class="nav-item">Explore</span><span class="nav-item">My Items</span><span class="nav-item active">Dashboard</span><span class="nav-item">Profile</span></div>
  </div>
  <div class="app-content">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
      <div>
        <h2 style="font-size: 20px; font-weight: 900;">Student Recovery Dashboard</h2>
        <p style="font-size: 12px; color: #64748b;">Welcome back, Bhuvanesh (Reg # 12204567) • LPU Campus Network</p>
      </div>
      <span class="btn btn-dark" style="font-size: 11px;">[+] New Report</span>
    </div>

    <!-- 4 KPI Cards -->
    <div class="grid-4" style="margin-bottom: 16px;">
      <div class="box">
        <div style="font-size: 10px; font-weight: 700; color: #64748b; text-transform: uppercase;">Active Lost Reports</div>
        <div style="font-size: 24px; font-weight: 900; margin-top: 4px;">1</div>
      </div>
      <div class="box">
        <div style="font-size: 10px; font-weight: 700; color: #64748b; text-transform: uppercase;">Found Registered</div>
        <div style="font-size: 24px; font-weight: 900; margin-top: 4px;">2</div>
      </div>
      <div class="box">
        <div style="font-size: 10px; font-weight: 700; color: #64748b; text-transform: uppercase;">Pending Claims</div>
        <div style="font-size: 24px; font-weight: 900; margin-top: 4px;">1</div>
      </div>
      <div class="box">
        <div style="font-size: 10px; font-weight: 700; color: #64748b; text-transform: uppercase;">Items Recovered</div>
        <div style="font-size: 24px; font-weight: 900; margin-top: 4px; color: #166534;">1</div>
      </div>
    </div>

    <!-- Active Tracker Table -->
    <div class="box" style="padding: 12px;">
      <div style="font-size: 13px; font-weight: 900; margin-bottom: 10px;">My Active Reports & Verification Status</div>
      
      <div style="border-bottom: 1.5px solid #0f172a; padding-bottom: 6px; display: flex; font-size: 10px; font-weight: 800; color: #64748b;">
        <span style="flex: 2;">ITEM TITLE & ID</span>
        <span style="flex: 1;">TYPE</span>
        <span style="flex: 1.5;">LOCATION</span>
        <span style="flex: 1.5;">MATCH / CLAIM STATUS</span>
        <span style="flex: 1; text-align: right;">ACTION</span>
      </div>

      <div style="border-bottom: 1px solid #e2e8f0; padding: 10px 0; display: flex; align-items: center; font-size: 11px;">
        <span style="flex: 2; font-weight: 800;">HP Pavilion 14 Laptop<br><span style="font-size: 9px; color:#64748b;">#RL-LOST-2026-98742</span></span>
        <span style="flex: 1;"><span class="pill" style="background:#fee2e2; border-color:#dc2626; color:#991b1b; font-size:9px;">LOST</span></span>
        <span style="flex: 1.5; color:#64748b;">Block 34 Lab</span>
        <span style="flex: 1.5;"><span class="pill pill-dark" style="font-size:9px;">88% Match Found</span></span>
        <span style="flex: 1; text-align: right;"><button class="btn btn-dark" style="padding: 4px 8px; font-size: 10px;">View -></button></span>
      </div>

      <div style="padding: 10px 0; display: flex; align-items: center; font-size: 11px;">
        <span style="flex: 2; font-weight: 800;">Milton Thermosteel Flask<br><span style="font-size: 9px; color:#64748b;">#RL-FND-2026-10492</span></span>
        <span style="flex: 1;"><span class="pill" style="background:#dcfce7; border-color:#16a34a; color:#166534; font-size:9px;">FOUND</span></span>
        <span style="flex: 1.5; color:#64748b;">Unipolis</span>
        <span style="flex: 1.5;"><span class="pill" style="background:#dbeafe; border-color:#2563eb; color:#1d4ed8; font-size:9px;">Claim Approved</span></span>
        <span style="flex: 1; text-align: right;"><button class="btn" style="padding: 4px 8px; font-size: 10px;">Handover OTP</button></span>
      </div>
    </div>
  </div>
  <div class="wf-footer-bar">
    <span>PRIMARY ACTION: Track Item Recovery Lifecycle & Claim Updates</span>
    <span>NEXT NAVIGATION: -> Screen 08 (Notifications) or Screen 05 (Item Details)</span>
  </div>
</div>
</body></html>"""
    render_wireframe(html, os.path.join(WIREFRAMES_DIR, "07_student_dashboard.png"))

# Screen 8: Notifications & Alerts
def wf_08():
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{BASE_CSS}</style></head><body>
<div class="wf-canvas">
  <div class="wf-header-bar">
    <span>INT335 DESIGN THINKING PROTOTYPE • LOW-FIDELITY WIREFRAME</span>
    <span class="tag-id">SCREEN 08 • NOTIFICATIONS & MATCH ALERTS</span>
  </div>
  <div class="app-nav">
    <div class="app-logo"><div class="logo-icon">RL</div>ReturnLoop <span class="badge-lpu">LPU</span></div>
    <div class="nav-links"><span class="nav-item">Explore</span><span class="nav-item">My Items</span><span class="nav-item active">Notifications (3)</span><span class="nav-item">Dashboard</span></div>
  </div>
  <div class="app-content">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
      <div>
        <h2 style="font-size: 20px; font-weight: 900;">Notifications & Alerts</h2>
        <p style="font-size: 12px; color: #64748b;">Instant algorithmic updates, claim decisions, and campus security notifications.</p>
      </div>
      <span class="btn" style="font-size: 11px;">[ Mark All Read ]</span>
    </div>

    <div style="display: flex; gap: 8px; margin-bottom: 14px;">
      <span class="pill pill-dark">All (3)</span>
      <span class="pill">Match Alerts (1)</span>
      <span class="pill">Claim Decisions (1)</span>
      <span class="pill">Campus Security (1)</span>
    </div>

    <!-- Notification 1 -->
    <div class="box" style="border-left: 6px solid #0f172a; margin-bottom: 10px; padding: 12px;">
      <div style="display: flex; justify-content: space-between; align-items: flex-start;">
        <div>
          <span class="pill pill-dark" style="font-size: 9px; margin-bottom: 4px;">ALGORITHMIC MATCH ALERT</span>
          <div style="font-weight: 800; font-size: 12px; margin-top: 4px;">Potential Match Found for your HP Pavilion 14 Laptop</div>
          <p style="font-size: 11px; color: #475569; margin-top: 2px;">A found item reported in Block 34 matches your traits with an 88% confidence score.</p>
        </div>
        <div style="text-align: right;">
          <div style="font-size: 10px; color: #94a3b8;">15 mins ago</div>
          <button class="btn btn-dark" style="padding: 4px 10px; font-size: 10px; margin-top: 6px;">Inspect Match -></button>
        </div>
      </div>
    </div>

    <!-- Notification 2 -->
    <div class="box" style="border-left: 6px solid #16a34a; margin-bottom: 10px; padding: 12px;">
      <div style="display: flex; justify-content: space-between; align-items: flex-start;">
        <div>
          <span class="pill" style="background:#dcfce7; border-color:#16a34a; color:#166534; font-size: 9px;">CLAIM APPROVED</span>
          <div style="font-weight: 800; font-size: 12px; margin-top: 4px;">Claim #CLM-1082 Approved by UniMall Security</div>
          <p style="font-size: 11px; color: #475569; margin-top: 2px;">Your ownership claim for Milton Thermosteel Flask has been validated. Visit UniMall Helpdesk Room 102 with your Student ID.</p>
        </div>
        <div style="text-align: right;">
          <div style="font-size: 10px; color: #94a3b8;">2 hours ago</div>
          <button class="btn" style="padding: 4px 10px; font-size: 10px; margin-top: 6px;">View Handover Pass</button>
        </div>
      </div>
    </div>

    <!-- Notification 3 -->
    <div class="box" style="border-left: 6px solid #64748b; margin-bottom: 10px; padding: 12px;">
      <div style="display: flex; justify-content: space-between; align-items: flex-start;">
        <div>
          <span class="pill" style="font-size: 9px;">CAMPUS SECURITY PROTOCOL</span>
          <div style="font-weight: 800; font-size: 12px; margin-top: 4px;">Privacy Reminder: Never Exchange Direct Cash or Contacts</div>
          <p style="font-size: 11px; color: #475569; margin-top: 2px;">All lost and found handovers must occur at designated university security desks for student safety.</p>
        </div>
        <div style="text-align: right;">
          <div style="font-size: 10px; color: #94a3b8;">1 day ago</div>
        </div>
      </div>
    </div>
  </div>
  <div class="wf-footer-bar">
    <span>PRIMARY ACTION: Click Notification to Inspect Match or Download Handover Pass</span>
    <span>NEXT NAVIGATION: -> Screen 05 (Item Details)</span>
  </div>
</div>
</body></html>"""
    render_wireframe(html, os.path.join(WIREFRAMES_DIR, "08_notifications_page.png"))

# Screen 9: Login & Campus Authentication
def wf_09():
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{BASE_CSS}</style></head><body>
<div class="wf-canvas">
  <div class="wf-header-bar">
    <span>INT335 DESIGN THINKING PROTOTYPE • LOW-FIDELITY WIREFRAME</span>
    <span class="tag-id">SCREEN 09 • CAMPUS AUTHENTICATION (LPU LOGIN / REGISTER)</span>
  </div>
  <div class="app-nav">
    <div class="app-logo"><div class="logo-icon">RL</div>ReturnLoop <span class="badge-lpu">LPU</span></div>
    <div class="nav-links"><span class="nav-item">Explore</span><span class="nav-item active">Sign In</span></div>
  </div>
  <div class="app-content" style="display: flex; justify-content: center; align-items: center; padding: 30px;">
    <div class="box" style="width: 480px; padding: 28px; box-shadow: 0 4px 16px rgba(0,0,0,0.06);">
      <div style="text-align: center; margin-bottom: 20px;">
        <div class="logo-icon" style="margin: 0 auto 8px auto; width: 36px; height: 36px; font-size: 16px;">RL</div>
        <h2 style="font-size: 20px; font-weight: 900;">Sign In to ReturnLoop</h2>
        <p style="font-size: 11px; color: #64748b; margin-top: 4px;">Exclusive to Lovely Professional University Students & Faculty</p>
      </div>

      <div style="margin-bottom: 14px;">
        <label class="input-label">University Email Address (@lpu.in) *</label>
        <input class="input-field" value="bhuvanesh.12204567@lpu.in">
      </div>

      <div style="margin-bottom: 14px;">
        <div style="display: flex; justify-content: space-between;">
          <label class="input-label">Password *</label>
          <span style="font-size: 10px; font-weight: 700; color: #64748b; cursor: pointer;">Forgot?</span>
        </div>
        <input class="input-field" type="password" value="••••••••••••••••">
      </div>

      <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 18px; font-size: 11px; font-weight: 600;">
        <input type="checkbox" checked> Remember this campus device for 30 days
      </div>

      <button class="btn btn-dark" style="width: 100%; padding: 10px; font-size: 13px; margin-bottom: 14px;">Sign In to Campus Network -></button>

      <div style="border-top: 1px solid #e2e8f0; padding-top: 14px; text-align: center; font-size: 11px; color: #64748b;">
        First time reporting? <strong style="color: #0f172a; text-decoration: underline;">Register with LPU Registration Number</strong>
      </div>

      <div class="box-gray" style="margin-top: 16px; padding: 10px; text-align: center; font-size: 10px; border-radius: 6px;">
        🔒 <strong>LPU Zero-Trust Protocol:</strong> Your phone number is never exposed to public viewers or search engines.
      </div>
    </div>
  </div>
  <div class="wf-footer-bar">
    <span>PRIMARY ACTION: Authenticate with University Credentials</span>
    <span>NEXT NAVIGATION: -> Screen 07 (Dashboard) or Return to Screen 01 (Landing)</span>
  </div>
</div>
</body></html>"""
    render_wireframe(html, os.path.join(WIREFRAMES_DIR, "09_login_register_page.png"))

# Screen 10: Admin & Security Handover Verification
def wf_10():
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{BASE_CSS}</style></head><body>
<div class="wf-canvas">
  <div class="wf-header-bar">
    <span>INT335 DESIGN THINKING PROTOTYPE • LOW-FIDELITY WIREFRAME</span>
    <span class="tag-id">SCREEN 10 • ADMIN & SECURITY HANDOVER VERIFICATION</span>
  </div>
  <div class="app-nav">
    <div class="app-logo"><div class="logo-icon">RL</div>ReturnLoop <span class="badge-lpu">ADMIN CONSOLE</span></div>
    <div class="nav-links"><span class="nav-item">Live Registry</span><span class="nav-item active">Verification Queue (2)</span><span class="nav-item">Handover Logs</span><span class="nav-item">Security Settings</span></div>
  </div>
  <div class="app-content">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
      <div>
        <h2 style="font-size: 20px; font-weight: 900;">Campus Security Handover Desk</h2>
        <p style="font-size: 12px; color: #64748b;">Central Custody & Ownership Verification Terminal • LPU Security Department</p>
      </div>
      <div style="display: flex; gap: 8px;">
        <span class="btn btn-dark" style="font-size: 11px;">[ Verify Handover Code ]</span>
        <span class="btn" style="font-size: 11px;">[ Print Custody Receipt ]</span>
      </div>
    </div>

    <!-- Filter Bar -->
    <div style="display: flex; gap: 8px; margin-bottom: 12px; font-size: 11px; font-weight: 700;">
      <span class="pill pill-dark">Pending Claims (2)</span>
      <span class="pill">Ready for Physical Pickup (1)</span>
      <span class="pill">Resolved Handaways (48)</span>
      <span class="pill">Flagged Disputes (0)</span>
    </div>

    <!-- Verification Queue -->
    <div class="box" style="padding: 12px;">
      <div style="border-bottom: 1.5px solid #0f172a; padding-bottom: 6px; display: flex; font-size: 10px; font-weight: 800; color: #64748b;">
        <span style="flex: 1;">CLAIM ID</span>
        <span style="flex: 2;">ITEM & CUSTODY LOCATION</span>
        <span style="flex: 2;">CLAIMANT INFO</span>
        <span style="flex: 2;">PRIVATE TRAIT VERIFICATION</span>
        <span style="flex: 1.5; text-align: right;">DECISION</span>
      </div>

      <!-- Queue Item 1 -->
      <div style="border-bottom: 1px solid #e2e8f0; padding: 12px 0; display: flex; align-items: center; font-size: 11px;">
        <span style="flex: 1; font-weight: 800;">#CLM-1082<br><span class="pill pill-dark" style="font-size:8px;">88% MATCH</span></span>
        <span style="flex: 2;"><strong>HP Pavilion 14 Laptop</strong><br><span style="font-size:10px; color:#64748b;">Custody: Block 34 Security Desk</span></span>
        <span style="flex: 2;"><strong>Bhuvanesh</strong> (Reg: 12204567)<br><span style="font-size:10px; color:#64748b;">bhuvanesh.12204567@lpu.in</span></span>
        <span style="flex: 2; font-size: 10px; background: #f8fafc; padding: 6px; border-radius: 4px; border: 1px solid #e2e8f0;">
          Serial: Ends with 89B [MATCHED]<br>
          Wallpaper: Deep Space [MATCHED]
        </span>
        <span style="flex: 1.5; text-align: right;">
          <button class="btn btn-dark" style="padding: 4px 8px; font-size: 10px; background:#166534; border-color:#166534;">Approve Handover</button>
          <button class="btn" style="padding: 4px 6px; font-size: 10px; margin-top: 4px;">Reject</button>
        </span>
      </div>

      <!-- Queue Item 2 -->
      <div style="padding: 12px 0; display: flex; align-items: center; font-size: 11px;">
        <span style="flex: 1; font-weight: 800;">#CLM-1079<br><span class="pill" style="font-size:8px;">MANUAL CLAIM</span></span>
        <span style="flex: 2;"><strong>Wildcraft Navy Backpack</strong><br><span style="font-size:10px; color:#64748b;">Custody: UniMall Helpdesk Room 102</span></span>
        <span style="flex: 2;"><strong>Rohan Sharma</strong> (Reg: 12108821)<br><span style="font-size:10px; color:#64748b;">rohan.12108821@lpu.in</span></span>
        <span style="flex: 2; font-size: 10px; background: #f8fafc; padding: 6px; border-radius: 4px; border: 1px solid #e2e8f0;">
          Contains: Math notes & Casio calculator<br>
          Proof: Class timetable inside notebook
        </span>
        <span style="flex: 1.5; text-align: right;">
          <button class="btn btn-dark" style="padding: 4px 8px; font-size: 10px; background:#166534; border-color:#166534;">Approve Handover</button>
          <button class="btn" style="padding: 4px 6px; font-size: 10px; margin-top: 4px;">Request Proof</button>
        </span>
      </div>
    </div>
  </div>
  <div class="wf-footer-bar">
    <span>PRIMARY ACTION: Validate Trait Matches, Review Physical Proof & Authorize Release</span>
    <span>STATUS: Final Closed-Loop Handover Complete with Digital Timestamp</span>
  </div>
</div>
</body></html>"""
    render_wireframe(html, os.path.join(WIREFRAMES_DIR, "10_admin_claims_page.png"))

def main():
    print("=== Generating 10 Low-Fidelity Wireframes for INT335 Design Thinking Prototype ===")
    wf_01()
    wf_02()
    wf_03()
    wf_04()
    wf_05()
    wf_06()
    wf_07()
    wf_08()
    wf_09()
    wf_10()
    print("=== Wireframes Generation Complete! ===")

if __name__ == "__main__":
    main()
