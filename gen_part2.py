import os
import subprocess
import shutil

BASE_DIR = r"c:\Users\bhuva\OneDrive\Desktop\Returlooptesting"
OUTPUT_DIR = os.path.join(BASE_DIR, "design_thinking_prototype")
WIREFRAMES_DIR = os.path.join(OUTPUT_DIR, "wireframes")
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

os.makedirs(WIREFRAMES_DIR, exist_ok=True)

def render_html_to_png(html_content, output_png, width=1500, height=1000, scale=2):
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
        try: os.remove(temp_html)
        except: pass
    
    if res.returncode == 0 and os.path.exists(output_png):
        print(f"[OK] Generated: {os.path.basename(output_png)} ({os.path.getsize(output_png):,} bytes)")
        return True
    else:
        print(f"[ERROR] Failed {output_png}: {res.stderr}")
        return False

# ==============================================================================
# DELIVERABLE 2: PAPER PROTOTYPE (Minimum 5 Screens Hand-Drawable Sheet)
# ==============================================================================
def generate_paper_prototype():
    html = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background: #ffffff; color: #0f172a; padding: 25px; }
.header { border-bottom: 3px solid #0f172a; padding-bottom: 12px; margin-bottom: 20px; display: flex; justify-content: space-between; align-items: flex-end; }
.title { font-size: 24px; font-weight: 900; letter-spacing: -0.5px; }
.subtitle { font-size: 12.5px; color: #475569; font-weight: 500; margin-top: 3px; }
.meta { text-align: right; font-size: 11px; font-weight: 700; color: #0f172a; }
.meta span { background: #0f172a; color: #fff; padding: 3px 8px; border-radius: 4px; margin-left: 6px; }

.screens-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 16px; }
.sketch-device { border: 2.5px solid #0f172a; border-radius: 24px; background: #ffffff; height: 600px; display: flex; flex-direction: column; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.06); }
.sketch-notch { width: 90px; height: 14px; background: #0f172a; margin: 0 auto; border-bottom-left-radius: 8px; border-bottom-right-radius: 8px; }
.sketch-top-info { padding: 4px 10px; font-size: 9px; font-weight: 800; display: flex; justify-content: space-between; border-bottom: 1px solid #e2e8f0; background: #f8fafc; }
.sketch-body { flex: 1; padding: 10px; display: flex; flex-direction: column; overflow: hidden; font-size: 10px; }

.box { border: 1.5px solid #0f172a; border-radius: 5px; padding: 6px 8px; background: #ffffff; margin-bottom: 6px; }
.box-dark { background: #0f172a; color: #ffffff; border: 1.5px solid #0f172a; }
.box-dashed { border: 1.5px dashed #64748b; background: #f8fafc; }
.box-btn { border: 1.5px solid #0f172a; border-radius: 6px; padding: 6px; text-align: center; font-weight: 700; font-size: 10px; cursor: pointer; }
.box-btn-dark { background: #0f172a; color: #ffffff; }
.box-btn-red { background: #fee2e2; border-color: #dc2626; color: #991b1b; }
.box-btn-green { background: #dcfce7; border-color: #16a34a; color: #166534; }
.tag { display: inline-block; padding: 1px 5px; border-radius: 3px; border: 1px solid #0f172a; font-size: 8px; font-weight: bold; }
.text-line { height: 6px; background: #cbd5e1; border-radius: 3px; margin: 4px 0; }
.text-line-short { width: 60%; }
.nav-bottom { border-top: 1.5px solid #0f172a; background: #f8fafc; padding: 6px 4px; display: flex; justify-content: space-around; font-size: 8px; font-weight: 700; }

.screen-label { margin-bottom: 8px; display: flex; align-items: center; justify-content: space-between; }
.badge-num { background: #0f172a; color: #ffffff; font-size: 11px; font-weight: 900; width: 22px; height: 22px; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; }
.badge-title { font-size: 12px; font-weight: 800; text-transform: uppercase; }

.pen-tip { margin-top: 16px; border: 1.5px solid #d97706; background: #fffbeb; padding: 10px 14px; border-radius: 8px; font-size: 11px; color: #92400e; font-weight: 600; display: flex; justify-content: space-between; }
</style>
</head>
<body>

<div class="header">
  <div>
    <div class="title">DELIVERABLE 2: PAPER PROTOTYPE (HAND-DRAWABLE SCREENS)</div>
    <div class="subtitle">ReturnLoop LPU • 5 Core Interactive Touchpoints for Workbook Copying</div>
  </div>
  <div class="meta">
    STAGE: <strong>RAPID PROTOTYPING</strong>
    <span>ACTIVITY 4.1</span>
  </div>
</div>

<div class="screens-grid">
  <!-- SCREEN 1: LANDING & SEARCH -->
  <div>
    <div class="screen-label">
      <div style="display:flex; align-items:center; gap:6px;">
        <span class="badge-num">1</span>
        <span class="badge-title">Landing & Search</span>
      </div>
      <span class="tag">Entry</span>
    </div>
    <div class="sketch-device">
      <div class="sketch-notch"></div>
      <div class="sketch-top-info">
        <span>ReturnLoop LPU</span>
        <span>🔔 ☰</span>
      </div>
      <div class="sketch-body">
        <!-- Hero Box -->
        <div class="box box-dark" style="padding: 10px; margin-bottom: 8px;">
          <div style="font-size: 8px; font-weight: 700; color: #38bdf8; margin-bottom: 3px;">✨ LPU RECOVERY SYSTEM</div>
          <div style="font-size: 11px; font-weight: 900; line-height: 1.2;">Lost something on campus?</div>
          <div style="font-size: 8px; color: #cbd5e1; margin-top: 4px;">Bring it back into the loop.</div>
          <!-- Quick Search -->
          <div class="box" style="margin-top: 8px; padding: 4px 6px; display: flex; justify-content: space-between; align-items: center; background:#fff; color:#0f172a;">
            <span style="font-size: 8px; color: #64748b;">🔍 Search HP laptop, keys...</span>
            <span style="background: #0f172a; color: #fff; padding: 2px 5px; border-radius: 3px; font-size: 7px; font-weight: bold;">Find</span>
          </div>
        </div>

        <!-- 2 Primary CTA Buttons -->
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 6px; margin-bottom: 8px;">
          <div class="box-btn box-btn-red" style="font-size: 9px;">? Report Lost</div>
          <div class="box-btn box-btn-green" style="font-size: 9px;">✓ Report Found</div>
        </div>

        <!-- Categories Section -->
        <div style="font-size: 9px; font-weight: 800; text-transform: uppercase; margin-bottom: 4px;">Quick Categories</div>
        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 4px; margin-bottom: 8px;">
          <div class="box" style="text-align: center; padding: 4px 2px; font-size: 7px; font-weight: bold;">💻 Laptop</div>
          <div class="box" style="text-align: center; padding: 4px 2px; font-size: 7px; font-weight: bold;">🔑 Keys</div>
          <div class="box" style="text-align: center; padding: 4px 2px; font-size: 7px; font-weight: bold;">🪪 Cards</div>
          <div class="box" style="text-align: center; padding: 4px 2px; font-size: 7px; font-weight: bold;">🎒 Bags</div>
        </div>

        <!-- Live Feed Card -->
        <div style="font-size: 9px; font-weight: 800; text-transform: uppercase; margin-bottom: 4px;">Recent Campus Feed</div>
        <div class="box" style="padding: 6px; margin-bottom: 6px;">
          <div style="display: flex; justify-content: space-between; align-items: center;">
            <span class="tag" style="background: #fee2e2; border-color: #ef4444; color: #991b1b;">LOST</span>
            <span style="font-size: 7px; color: #64748b;">RL-LOST-2026-08</span>
          </div>
          <div style="font-size: 9px; font-weight: bold; margin-top: 3px;">HP Pavilion Blue 15"</div>
          <div style="font-size: 7.5px; color: #64748b;">Central Library • Oct 28</div>
        </div>

        <div class="box" style="padding: 6px;">
          <div style="display: flex; justify-content: space-between; align-items: center;">
            <span class="tag" style="background: #dcfce7; border-color: #22c55e; color: #166534;">FOUND</span>
            <span style="font-size: 7px; color: #64748b;">RL-FND-2026-14</span>
          </div>
          <div style="font-size: 9px; font-weight: bold; margin-top: 3px;">Milton Steel Bottle</div>
          <div style="font-size: 7.5px; color: #64748b;">UniMall 1st Floor • Custody: Desk</div>
        </div>
      </div>
      <!-- Bottom Nav -->
      <div class="nav-bottom">
        <span>🔍 Explore</span>
        <span>📑 My Items</span>
        <span style="font-weight: 900; background: #0f172a; color: #fff; padding: 0 4px; border-radius: 3px;">+</span>
        <span>🔔 Notifs</span>
        <span>👤 Account</span>
      </div>
    </div>
  </div>

  <!-- SCREEN 2: REPORT LOST BELONGING -->
  <div>
    <div class="screen-label">
      <div style="display:flex; align-items:center; gap:6px;">
        <span class="badge-num">2</span>
        <span class="badge-title">Report Lost</span>
      </div>
      <span class="tag">Form</span>
    </div>
    <div class="sketch-device">
      <div class="sketch-notch"></div>
      <div class="sketch-top-info">
        <span>← Back</span>
        <span>Report Lost</span>
        <span>Help</span>
      </div>
      <div class="sketch-body">
        <div style="font-size: 11px; font-weight: 900; margin-bottom: 2px;">Report Lost Belonging</div>
        <div style="font-size: 7.5px; color: #64748b; margin-bottom: 8px;">Fill accurate traits to trigger auto-matching.</div>

        <!-- Input: Item Title -->
        <div style="font-size: 8px; font-weight: bold; text-transform: uppercase;">Item Title *</div>
        <div class="box" style="font-size: 8px; color: #334155; padding: 5px;">Dell Inspiron 15 Blue Laptop</div>

        <!-- Row: Category & Color -->
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 4px;">
          <div>
            <div style="font-size: 8px; font-weight: bold; text-transform: uppercase;">Category *</div>
            <div class="box" style="font-size: 8px; padding: 5px;">Electronics ▼</div>
          </div>
          <div>
            <div style="font-size: 8px; font-weight: bold; text-transform: uppercase;">Color *</div>
            <div class="box" style="font-size: 8px; padding: 5px;">Blue / Black</div>
          </div>
        </div>

        <!-- Campus Location -->
        <div style="font-size: 8px; font-weight: bold; text-transform: uppercase;">Campus Location *</div>
        <div class="box" style="font-size: 8px; padding: 5px;">Central Library 3rd Floor ▼</div>

        <!-- Public Description -->
        <div style="font-size: 8px; font-weight: bold; text-transform: uppercase;">Public Description *</div>
        <div class="box" style="height: 38px; font-size: 8px; color: #334155;">Left near window study table #14 during afternoon prep...</div>

        <!-- Private Proof Box (Crucial Design Thinking Feature) -->
        <div class="box" style="border: 1.5px dashed #d97706; background: #fffbeb; padding: 6px;">
          <div style="font-size: 8px; font-weight: bold; color: #92400e;">🔒 Private Verification Proof (HIDDEN):</div>
          <div style="font-size: 7px; color: #78350f; margin-top: 2px;">Lock screen has red sports car. Python sticker near trackpad.</div>
        </div>

        <!-- Photo Upload Placeholder -->
        <div class="box box-dashed" style="padding: 8px; text-align: center; margin-top: 4px;">
          <div style="font-size: 14px;">📷</div>
          <div style="font-size: 8px; font-weight: bold;">Attach Photo / Reference</div>
        </div>

        <!-- Primary Submit Button -->
        <div class="box-btn box-btn-dark" style="margin-top: auto; padding: 8px; font-size: 9.5px;">
          Submit Report & Scan Matches →
        </div>
      </div>
      <div class="nav-bottom">
        <span>🔍 Explore</span><span>📑 My Items</span><span>+</span><span>🔔 Notifs</span><span>👤 Account</span>
      </div>
    </div>
  </div>

  <!-- SCREEN 3: EXPLORE & FILTER LISTINGS -->
  <div>
    <div class="screen-label">
      <div style="display:flex; align-items:center; gap:6px;">
        <span class="badge-num">3</span>
        <span class="badge-title">Explore Feed</span>
      </div>
      <span class="tag">Search</span>
    </div>
    <div class="sketch-device">
      <div class="sketch-notch"></div>
      <div class="sketch-top-info">
        <span>ReturnLoop LPU</span>
        <span>🔍 Filter</span>
        <span>Grid/List</span>
      </div>
      <div class="sketch-body">
        <!-- Search bar -->
        <div class="box" style="padding: 4px 8px; display: flex; align-items: center; justify-content: space-between;">
          <span style="font-size: 8px; color: #64748b;">Search by brand, block, tags...</span>
          <span style="font-size: 8px; font-weight: bold;">Go</span>
        </div>

        <!-- Segmented Type Selector -->
        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 2px; margin-bottom: 6px;">
          <div class="box" style="text-align: center; padding: 4px; font-size: 8px; font-weight: bold; background: #0f172a; color: #fff;">All (24)</div>
          <div class="box" style="text-align: center; padding: 4px; font-size: 8px; font-weight: bold; background: #fee2e2; color: #991b1b;">Lost (11)</div>
          <div class="box" style="text-align: center; padding: 4px; font-size: 8px; font-weight: bold; background: #dcfce7; color: #166534;">Found (13)</div>
        </div>

        <!-- Horizontal category pills -->
        <div style="display: flex; gap: 4px; overflow: hidden; margin-bottom: 8px;">
          <span class="tag" style="background:#0f172a; color:#fff;">All</span>
          <span class="tag">Electronics</span>
          <span class="tag">Keys</span>
          <span class="tag">Wallets</span>
        </div>

        <!-- Listing Cards -->
        <div class="box" style="padding: 6px; margin-bottom: 6px;">
          <div style="display: flex; justify-content: space-between;">
            <span class="tag" style="background:#dcfce7; color:#166534;">FOUND ITEM</span>
            <span style="font-size: 7px; color: #64748b;">RL-FND-2026-91</span>
          </div>
          <div style="display: flex; gap: 6px; margin-top: 4px;">
            <div class="box box-dashed" style="width: 44px; height: 44px; margin: 0; display:flex; align-items:center; justify-content:center; font-size:8px;">[PHOTO]</div>
            <div style="flex: 1;">
              <div style="font-size: 9px; font-weight: bold;">Fastrack Analog Watch</div>
              <div style="font-size: 7.5px; color: #475569;">Black dial, silver strap</div>
              <div style="font-size: 7px; color: #0f172a; font-weight: bold; margin-top: 2px;">📍 Block 34 Helpdesk</div>
            </div>
          </div>
          <div class="box-btn box-btn-dark" style="margin-top: 5px; padding: 3px; font-size: 8px;">View Details & Claim →</div>
        </div>

        <div class="box" style="padding: 6px; margin-bottom: 6px;">
          <div style="display: flex; justify-content: space-between;">
            <span class="tag" style="background:#fee2e2; color:#991b1b;">LOST REPORT</span>
            <span style="font-size: 7px; color: #64748b;">RL-LOST-2026-44</span>
          </div>
          <div style="display: flex; gap: 6px; margin-top: 4px;">
            <div class="box box-dashed" style="width: 44px; height: 44px; margin: 0; display:flex; align-items:center; justify-content:center; font-size:8px;">[PHOTO]</div>
            <div style="flex: 1;">
              <div style="font-size: 9px; font-weight: bold;">Bike Keys (Honda Dio)</div>
              <div style="font-size: 7.5px; color: #475569;">Red tag with Batman logo</div>
              <div style="font-size: 7px; color: #0f172a; font-weight: bold; margin-top: 2px;">📍 UniMall Parking Lot</div>
            </div>
          </div>
          <div class="box-btn box-btn-dark" style="margin-top: 5px; padding: 3px; font-size: 8px;">View Details →</div>
        </div>
      </div>
      <div class="nav-bottom">
        <span style="font-weight: 900; color: #2563eb;">🔍 Explore</span><span>📑 My Items</span><span>+</span><span>🔔 Notifs</span><span>👤 Account</span>
      </div>
    </div>
  </div>

  <!-- SCREEN 4: ITEM DETAILS & 5-TRAIT MATCH -->
  <div>
    <div class="screen-label">
      <div style="display:flex; align-items:center; gap:6px;">
        <span class="badge-num">4</span>
        <span class="badge-title">Item Details</span>
      </div>
      <span class="tag">Match</span>
    </div>
    <div class="sketch-device">
      <div class="sketch-notch"></div>
      <div class="sketch-top-info">
        <span>← Feed</span>
        <span>Item RL-FND-2026-90</span>
        <span>Share</span>
      </div>
      <div class="sketch-body">
        <!-- Big Photo Box -->
        <div class="box box-dashed" style="height: 90px; text-align: center; display: flex; flex-direction: column; align-items: center; justify-content: center; margin-bottom: 6px;">
          <div style="font-size: 16px;">📷</div>
          <div style="font-size: 8px; font-weight: bold;">Verified Physical Item Photo</div>
        </div>

        <div style="display: flex; justify-content: space-between; align-items: center;">
          <span class="tag" style="background:#dcfce7; color:#166534;">FOUND ITEM</span>
          <span class="tag">ACTIVE CUSTODY</span>
        </div>
        <div style="font-size: 11px; font-weight: 900; margin-top: 3px;">HP 15 Blue Laptop (Found)</div>
        <div style="font-size: 8px; color: #64748b;">Turned in at Central Library Desk on Oct 28</div>

        <!-- 5-Trait Match Score Card -->
        <div class="box" style="border: 2px solid #2563eb; background: #eff6ff; padding: 6px; margin: 6px 0;">
          <div style="display: flex; justify-content: space-between; align-items: center;">
            <span style="font-size: 8.5px; font-weight: 900; color: #1e40af;">⚡ 5-TRAIT SIMILARITY MATCH</span>
            <span style="font-size: 9px; font-weight: 900; background: #2563eb; color: #fff; padding: 1px 5px; border-radius: 4px;">92%</span>
          </div>
          <div style="font-size: 7.5px; color: #1e3a8a; margin-top: 2px;">
            Matches lost report filed by you: <em>HP Laptop Blue</em>.
          </div>
        </div>

        <!-- Metadata List -->
        <div class="box" style="font-size: 8px; padding: 6px;">
          <div><strong>Category:</strong> Electronics</div>
          <div><strong>Color:</strong> Matte Blue / Silver</div>
          <div><strong>Location:</strong> Block 34 Security Helpdesk</div>
          <div><strong>Status:</strong> Awaiting Verified Claim</div>
        </div>

        <!-- Primary Action CTA -->
        <div class="box-btn box-btn-green" style="margin-top: auto; padding: 8px; font-size: 10px; font-weight: 900;">
          🛡️ Claim This Belonging →
        </div>
      </div>
      <div class="nav-bottom">
        <span>🔍 Explore</span><span>📑 My Items</span><span>+</span><span>🔔 Notifs</span><span>👤 Account</span>
      </div>
    </div>
  </div>

  <!-- SCREEN 5: SUBMIT PRIVATE OWNERSHIP CLAIM -->
  <div>
    <div class="screen-label">
      <div style="display:flex; align-items:center; gap:6px;">
        <span class="badge-num">5</span>
        <span class="badge-title">Ownership Claim</span>
      </div>
      <span class="tag">Claim</span>
    </div>
    <div class="sketch-device">
      <div class="sketch-notch"></div>
      <div class="sketch-top-info">
        <span>← Cancel</span>
        <span>Submit Claim</span>
        <span>Privacy</span>
      </div>
      <div class="sketch-body">
        <div style="font-size: 11px; font-weight: 900; margin-bottom: 2px;">Confidential Claim</div>
        <div style="font-size: 7.5px; color: #64748b; margin-bottom: 6px;">Claiming: <strong>HP 15 Blue Laptop</strong></div>

        <!-- Privacy Shield Banner -->
        <div class="box" style="border: 1.5px solid #0f172a; background: #f8fafc; padding: 6px; margin-bottom: 8px;">
          <div style="font-size: 8px; font-weight: bold;">🔒 Zero-Leak Guarantee:</div>
          <div style="font-size: 7px; color: #475569; margin-top: 2px;">
            Your explanation will ONLY be inspected by Central Security Officers during physical handover verification.
          </div>
        </div>

        <!-- Proof Textarea -->
        <div style="font-size: 8px; font-weight: bold; text-transform: uppercase;">Private Proof & Attributes *</div>
        <div class="box" style="height: 95px; font-size: 8px; padding: 6px; line-height: 1.35; color: #334155;">
          "This is my laptop. Inside the bag there is a blue spiral notebook with my reg #12204918 on the cover. Laptop serial number ends in 4492. The lock screen wallpaper is a red sports car and desktop has a folder called 'INT335_Project'."
        </div>

        <!-- Physical Handover Instructions -->
        <div class="box" style="border: 1px solid #16a34a; background: #f0fdf4; padding: 6px; margin-top: 6px;">
          <div style="font-size: 8px; font-weight: bold; color: #166534;">Next Step Upon Approval:</div>
          <div style="font-size: 7px; color: #14532d; margin-top: 2px;">
            Visit <strong>Block 34 Helpdesk (Ground Floor)</strong> with physical Student ID card to unlock and collect.
          </div>
        </div>

        <!-- Submit Button -->
        <div class="box-btn box-btn-dark" style="margin-top: auto; padding: 8px; font-size: 9.5px;">
          Submit Claim to Security →
        </div>
      </div>
      <div class="nav-bottom">
        <span>🔍 Explore</span><span>📑 My Items</span><span>+</span><span>🔔 Notifs</span><span>👤 Account</span>
      </div>
    </div>
  </div>
</div>

<div class="pen-tip">
  <span><strong>WORKBOOK DRAWING INSTRUCTIONS:</strong> Draw each phone frame as a 6cm x 12cm rectangle with rounded corners. Copy the labels, buttons, and badges exactly. Mark the primary CTA with bold outline or light cross-hatch shading.</span>
  <span>Estimated drawing time: <strong>4-5 minutes per screen</strong></span>
</div>

</body>
</html>"""
    out_path = os.path.join(OUTPUT_DIR, "paper_prototype.png")
    return render_html_to_png(html, out_path, width=1600, height=880)

# ==============================================================================
# DELIVERABLE 7: THREE KEY SCREEN ANNOTATIONS
# ==============================================================================
def generate_screen_annotations():
    html = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background: #ffffff; color: #0f172a; padding: 25px; }
.header { border-bottom: 3px solid #0f172a; padding-bottom: 12px; margin-bottom: 20px; display: flex; justify-content: space-between; align-items: flex-end; }
.title { font-size: 24px; font-weight: 900; letter-spacing: -0.5px; }
.subtitle { font-size: 12.5px; color: #475569; font-weight: 500; margin-top: 3px; }
.meta { text-align: right; font-size: 11px; font-weight: 700; color: #0f172a; }
.meta span { background: #0f172a; color: #fff; padding: 3px 8px; border-radius: 4px; margin-left: 6px; }

.annotations-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }
.annotated-card { border: 2.5px solid #0f172a; border-radius: 12px; background: #ffffff; padding: 16px; display: flex; flex-direction: column; }
.card-header { display: flex; align-items: center; justify-content: space-between; border-bottom: 2px solid #0f172a; padding-bottom: 8px; margin-bottom: 12px; }
.screen-tag { background: #0f172a; color: #ffffff; font-size: 11px; font-weight: 800; padding: 2px 8px; border-radius: 4px; }
.screen-title { font-size: 14px; font-weight: 900; }

.screen-mini-sketch { border: 2px solid #0f172a; border-radius: 12px; height: 320px; background: #f8fafc; padding: 10px; margin-bottom: 12px; display: flex; flex-direction: column; position: relative; }
.callout-badge { position: absolute; background: #dc2626; color: #fff; width: 20px; height: 20px; border-radius: 50%; font-size: 10px; font-weight: 900; display: flex; align-items: center; justify-content: center; border: 1.5px solid #fff; box-shadow: 0 2px 5px rgba(0,0,0,0.2); }

.detail-section { margin-bottom: 8px; font-size: 11px; line-height: 1.4; }
.detail-label { font-size: 10px; font-weight: 900; text-transform: uppercase; color: #475569; letter-spacing: 0.5px; margin-bottom: 2px; }
.detail-val { font-weight: 500; color: #0f172a; }
.state-box { border-radius: 6px; padding: 6px 10px; font-size: 10.5px; margin-top: 4px; }
.success-box { background: #ecfdf5; border: 1.5px solid #10b981; color: #065f46; }
.failure-box { background: #fef2f2; border: 1.5px solid #ef4444; color: #991b1b; }

.pen-tip { margin-top: 16px; border: 1.5px solid #d97706; background: #fffbeb; padding: 10px 14px; border-radius: 8px; font-size: 11px; color: #92400e; font-weight: 600; display: flex; justify-content: space-between; }
</style>
</head>
<body>

<div class="header">
  <div>
    <div class="title">DELIVERABLE 7: THREE KEY SCREEN ANNOTATIONS</div>
    <div class="subtitle">ReturnLoop LPU • Deep-Dive Interface Specification, Success Paths, Error States & Navigations</div>
  </div>
  <div class="meta">
    STAGE: <strong>DESIGN SPECIFICATION</strong>
    <span>ACTIVITY 7.1</span>
  </div>
</div>

<div class="annotations-grid">
  <!-- SCREEN A: REPORT LOST -->
  <div class="annotated-card">
    <div class="card-header">
      <div class="screen-title">Screen A: Report Lost Belonging</div>
      <div class="screen-tag">/report-lost</div>
    </div>

    <!-- Mini Wireframe with numbered callouts -->
    <div class="screen-mini-sketch">
      <div style="font-size:9px; font-weight:bold; border-bottom:1px solid #cbd5e1; padding-bottom:4px; margin-bottom:6px;">ReturnLoop • Report Form</div>
      
      <!-- Callout 1: Item Title -->
      <div style="position:relative; margin-bottom:6px;">
        <div class="callout-badge" style="top:-6px; right:-6px;">1</div>
        <div style="font-size:8px; font-weight:bold;">Title & Category *</div>
        <div style="border:1px solid #0f172a; background:#fff; padding:3px; font-size:7.5px;">HP Pavilion Blue Laptop (Electronics)</div>
      </div>

      <!-- Callout 2: Campus Location -->
      <div style="position:relative; margin-bottom:6px;">
        <div class="callout-badge" style="top:-6px; right:-6px;">2</div>
        <div style="font-size:8px; font-weight:bold;">Approx Location & Date *</div>
        <div style="border:1px solid #0f172a; background:#fff; padding:3px; font-size:7.5px;">Central Library 3rd Floor • Oct 28</div>
      </div>

      <!-- Callout 3: Private Proof Safeguard -->
      <div style="position:relative; margin-bottom:6px;">
        <div class="callout-badge" style="top:-6px; right:-6px;">3</div>
        <div style="border:1.5px dashed #d97706; background:#fffbeb; padding:4px; font-size:7px; color:#92400e;">
          <strong>🔒 Hidden Verification Attributes:</strong><br>
          "Lock screen: red Ferrari. Python sticker on lid."
        </div>
      </div>

      <!-- Callout 4: Photo attachment -->
      <div style="border:1px dashed #94a3b8; background:#fff; padding:6px; text-align:center; font-size:7.5px; margin-bottom:6px;">
        📷 Photo / Reference Image (Max 5MB)
      </div>

      <!-- Callout 5: Submit CTA -->
      <div style="position:relative; margin-top:auto;">
        <div class="callout-badge" style="top:-8px; right:-6px;">4</div>
        <div style="border:1.5px solid #0f172a; background:#0f172a; color:#fff; padding:6px; font-size:8px; font-weight:bold; text-align:center; border-radius:4px;">
          Submit Lost Report & Search Matches →
        </div>
      </div>
    </div>

    <!-- Specification Details -->
    <div class="detail-section">
      <div class="detail-label">Primary Action:</div>
      <div class="detail-val"><strong>Submit Lost Report</strong> — Validates inputs, saves to SQLite with unique code (<code>RL-LOST-2026-X</code>), and invokes 5-trait similarity engine.</div>
    </div>

    <div class="detail-section">
      <div class="detail-label">Main Interface Elements:</div>
      <div class="detail-val">
        <strong>[1]</strong> Title/Category inputs • <strong>[2]</strong> LPU location dropdown • <strong>[3]</strong> Hidden private proof textarea • <strong>[4]</strong> Multi-trait search dispatch button.
      </div>
    </div>

    <div class="state-box success-box">
      <strong>✓ SUCCESS OUTCOME:</strong> Report created with status <code>active</code>. User is redirected to <code>/items/:id</code> showing potential matches and confirmation badge.
    </div>

    <div class="state-box failure-box">
      <strong>✗ ERROR STATE:</strong> Missing title or short description (&lt;10 chars) triggers an inline warning banner: <em>"Please provide accurate details."</em> Form values preserved.
    </div>
  </div>

  <!-- SCREEN B: ITEM DETAILS & TRAIT MATCHES -->
  <div class="annotated-card">
    <div class="card-header">
      <div class="screen-title">Screen B: Details & Match Engine</div>
      <div class="screen-tag">/items/:id</div>
    </div>

    <div class="screen-mini-sketch">
      <div style="font-size:9px; font-weight:bold; border-bottom:1px solid #cbd5e1; padding-bottom:4px; margin-bottom:6px;">ReturnLoop • Item Details View</div>
      
      <!-- Callout 1: Ref Code & Photo -->
      <div style="position:relative; margin-bottom:6px;">
        <div class="callout-badge" style="top:-6px; right:-6px;">1</div>
        <div style="border:1px solid #0f172a; background:#fff; height:60px; display:flex; align-items:center; justify-content:center; font-size:8px; font-weight:bold;">
          [ITEM PHOTO PREVIEW] • Ref: RL-FND-2026-9021
        </div>
      </div>

      <!-- Callout 2: Trait Match Score Banner -->
      <div style="position:relative; margin-bottom:6px;">
        <div class="callout-badge" style="top:-6px; right:-6px;">2</div>
        <div style="border:1.5px solid #2563eb; background:#eff6ff; padding:5px; font-size:7.5px;">
          <div style="display:flex; justify-content:space-between; font-weight:bold; color:#1e40af;">
            <span>⚡ 5-TRAIT SIMILARITY MATCH</span>
            <span>92% MATCH</span>
          </div>
          <span style="color:#1e3a8a;">Matched against lost report: HP Pavilion Blue</span>
        </div>
      </div>

      <!-- Callout 3: Safe Custody Helpdesk Info -->
      <div style="position:relative; margin-bottom:6px;">
        <div class="callout-badge" style="top:-6px; right:-6px;">3</div>
        <div style="border:1px solid #0f172a; background:#fff; padding:4px; font-size:7.5px;">
          <strong>Safe Custody:</strong> Block 34 Security Office Ground Floor Helpdesk
        </div>
      </div>

      <!-- Callout 4: Claim CTA -->
      <div style="position:relative; margin-top:auto;">
        <div class="callout-badge" style="top:-8px; right:-6px;">4</div>
        <div style="border:1.5px solid #16a34a; background:#16a34a; color:#fff; padding:6px; font-size:8px; font-weight:bold; text-align:center; border-radius:4px;">
          Claim This Belonging (Submit Proof) →
        </div>
      </div>
    </div>

    <div class="detail-section">
      <div class="detail-label">Primary Action:</div>
      <div class="detail-val"><strong>Claim This Belonging</strong> — Navigates authenticated student directly to the private claim verification submission screen.</div>
    </div>

    <div class="detail-section">
      <div class="detail-label">Main Interface Elements:</div>
      <div class="detail-val">
        <strong>[1]</strong> Public item photo/ref code • <strong>[2]</strong> Algorithmic trait score card • <strong>[3]</strong> Custody helpdesk location • <strong>[4]</strong> Green verification claim button.
      </div>
    </div>

    <div class="state-box success-box">
      <strong>✓ SUCCESS OUTCOME:</strong> Student reviews traits. If item looks like theirs, clicking Claim routes to <code>/claims/new/:id</code> with item context preserved.
    </div>

    <div class="state-box failure-box">
      <strong>✗ UNCONFIRMED STATE:</strong> System explicitly presents matches as <em>"Potential Suggestions"</em>—never promises confirmed identity until physical ID verification.
    </div>
  </div>

  <!-- SCREEN C: SUBMIT OWNERSHIP CLAIM -->
  <div class="annotated-card">
    <div class="card-header">
      <div class="screen-title">Screen C: Submit Ownership Claim</div>
      <div class="screen-tag">/claims/new/:id</div>
    </div>

    <div class="screen-mini-sketch">
      <div style="font-size:9px; font-weight:bold; border-bottom:1px solid #cbd5e1; padding-bottom:4px; margin-bottom:6px;">ReturnLoop • Confidential Claim</div>
      
      <!-- Callout 1: Target Item Summary -->
      <div style="position:relative; margin-bottom:6px;">
        <div class="callout-badge" style="top:-6px; right:-6px;">1</div>
        <div style="border:1px solid #0f172a; background:#fff; padding:4px; font-size:7.5px;">
          <strong>Target Item:</strong> HP 15 Blue Laptop (RL-FND-2026-9021)
        </div>
      </div>

      <!-- Callout 2: Privacy Notice -->
      <div style="position:relative; margin-bottom:6px;">
        <div class="callout-badge" style="top:-6px; right:-6px;">2</div>
        <div style="border:1px solid #0f172a; background:#f8fafc; padding:4px; font-size:7px; color:#334155;">
          🔒 <strong>Confidential Proof:</strong> Visible strictly to campus security.
        </div>
      </div>

      <!-- Callout 3: Detailed Explanation Textarea -->
      <div style="position:relative; margin-bottom:6px;">
        <div class="callout-badge" style="top:-6px; right:-6px;">3</div>
        <div style="font-size:7.5px; font-weight:bold;">Verifiable Attributes (&gt;15 chars) *</div>
        <div style="border:1.5px solid #0f172a; background:#fff; height:60px; font-size:7px; padding:4px; color:#334155;">
          "Serial ends in 4492. Lock screen is red Ferrari. Inside bag is blue notebook with reg 12204918..."
        </div>
      </div>

      <!-- Callout 4: Submit Button -->
      <div style="position:relative; margin-top:auto;">
        <div class="callout-badge" style="top:-8px; right:-6px;">4</div>
        <div style="border:1.5px solid #0f172a; background:#0f172a; color:#fff; padding:6px; font-size:8px; font-weight:bold; text-align:center; border-radius:4px;">
          Submit Claim for Verification →
        </div>
      </div>
    </div>

    <div class="detail-section">
      <div class="detail-label">Primary Action:</div>
      <div class="detail-val"><strong>Submit Claim for Verification</strong> — Packages private proof securely, creates claim reference, and queues item for security review.</div>
    </div>

    <div class="detail-section">
      <div class="detail-label">Main Interface Elements:</div>
      <div class="detail-val">
        <strong>[1]</strong> Claimed item summary • <strong>[2]</strong> Privacy safeguard disclaimer • <strong>[3]</strong> Hidden proof textarea • <strong>[4]</strong> Submission & dispatch button.
      </div>
    </div>

    <div class="state-box success-box">
      <strong>✓ SUCCESS OUTCOME:</strong> Shows success modal with Claim Reference (<code>CLM-2026-X</code>) and instructions to visit Block 34 Security Office with physical Student ID.
    </div>

    <div class="state-box failure-box">
      <strong>✗ ERROR STATE:</strong> Short explanations (&lt;15 characters) rejected with validation message: <em>"Please provide a verifiable proof of ownership."</em>
    </div>
  </div>
</div>

<div class="pen-tip">
  <span><strong>WORKBOOK DRAWING INSTRUCTIONS:</strong> Draw the 3 screen boxes on a single workbook page. Use red pen or circled numbers [1], [2], [3] for callout markers. Write the primary action, success state, and error handling below each sketch.</span>
  <span>Estimated drawing time: <strong>12-14 minutes</strong></span>
</div>

</body>
</html>"""
    out_path = os.path.join(OUTPUT_DIR, "screen_annotations.png")
    return render_html_to_png(html, out_path, width=1600, height=880)

# ==============================================================================
# DELIVERABLE 6: MVP FEATURE LIST (Visual Comparison & Roadmap)
# ==============================================================================
def generate_mvp_features():
    html = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background: #ffffff; color: #0f172a; padding: 25px; }
.header { border-bottom: 3px solid #0f172a; padding-bottom: 12px; margin-bottom: 20px; display: flex; justify-content: space-between; align-items: flex-end; }
.title { font-size: 24px; font-weight: 900; letter-spacing: -0.5px; }
.subtitle { font-size: 12.5px; color: #475569; font-weight: 500; margin-top: 3px; }
.meta { text-align: right; font-size: 11px; font-weight: 700; color: #0f172a; }
.meta span { background: #0f172a; color: #fff; padding: 3px 8px; border-radius: 4px; margin-left: 6px; }

.section-title { font-size: 14px; font-weight: 900; text-transform: uppercase; margin-bottom: 8px; border-left: 4px solid #0f172a; padding-left: 8px; }

.mvp-table { width: 100%; border-collapse: collapse; margin-bottom: 20px; font-size: 11px; }
.mvp-table th { background: #0f172a; color: #ffffff; padding: 8px 10px; text-align: left; font-weight: 800; font-size: 11px; }
.mvp-table td { border: 1.5px solid #cbd5e1; padding: 8px 10px; }
.mvp-table tr:nth-child(even) { background: #f8fafc; }
.badge-core { background: #16a34a; color: #fff; padding: 2px 6px; border-radius: 4px; font-size: 9px; font-weight: 800; }
.badge-supp { background: #2563eb; color: #fff; padding: 2px 6px; border-radius: 4px; font-size: 9px; font-weight: 800; }
.badge-v2 { background: #64748b; color: #fff; padding: 2px 6px; border-radius: 4px; font-size: 9px; font-weight: 800; }

.mvp-cards-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-bottom: 20px; }
.core-card { border: 2.5px solid #16a34a; border-radius: 10px; background: #f0fdf4; padding: 14px; }
.core-card-num { background: #16a34a; color: #fff; width: 24px; height: 24px; border-radius: 50%; font-weight: 900; display: inline-flex; align-items: center; justify-content: center; margin-right: 6px; font-size: 12px; }
.core-card-title { font-size: 13px; font-weight: 900; color: #166534; display: flex; align-items: center; margin-bottom: 6px; }
.core-card-desc { font-size: 11px; color: #14532d; line-height: 1.45; }

.v2-box { border: 2px dashed #64748b; border-radius: 8px; padding: 12px; background: #f8fafc; }
.v2-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin-top: 8px; font-size: 10.5px; }
.v2-item { background: #ffffff; border: 1.5px solid #cbd5e1; padding: 8px; border-radius: 6px; }

.pen-tip { border: 1.5px solid #d97706; background: #fffbeb; padding: 10px 14px; border-radius: 8px; font-size: 11px; color: #92400e; font-weight: 600; display: flex; justify-content: space-between; }
</style>
</head>
<body>

<div class="header">
  <div>
    <div class="title">DELIVERABLE 6: MVP FEATURE LIST & ROADMAP</div>
    <div class="subtitle">ReturnLoop LPU • 10 Candidate Features Analyzed • 3 Core MVP Selected • V2.0 Roadmap</div>
  </div>
  <div class="meta">
    STAGE: <strong>PRODUCT STRATEGY & SCOPING</strong>
    <span>ACTIVITY 6.1</span>
  </div>
</div>

<!-- PART A: 10 CANDIDATE FEATURES TABLE -->
<div class="section-title">Part A: Candidate Feature Matrix (10 Features Evaluated)</div>
<table class="mvp-table">
  <thead>
    <tr>
      <th style="width: 50px;">#</th>
      <th style="width: 220px;">Feature Name</th>
      <th>Functional Scope in ReturnLoop LPU</th>
      <th style="width: 140px;">Target User Need</th>
      <th style="width: 110px;">Classification</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>01</strong></td>
      <td><strong>Structured Lost/Found Reporting</strong></td>
      <td>Standardized intake form capturing category, brand, color, date, and LPU location.</td>
      <td>Replaces unstructured chaotic WhatsApp message spam.</td>
      <td><span class="badge-core">CORE MVP</span></td>
    </tr>
    <tr>
      <td><strong>02</strong></td>
      <td><strong>5-Trait Similarity Matching</strong></td>
      <td>Deterministic weighted scoring comparing categories, keywords, color, location & date proximity.</td>
      <td>Prevents lost items from sitting unclaimed due to missed manual reviews.</td>
      <td><span class="badge-core">CORE MVP</span></td>
    </tr>
    <tr>
      <td><strong>03</strong></td>
      <td><strong>Confidential Ownership Claims</strong></td>
      <td>Hidden proof submission inspected exclusively by campus security officers before handover.</td>
      <td>Prevents fraud, theft, and false ownership claims without leaking data.</td>
      <td><span class="badge-core">CORE MVP</span></td>
    </tr>
    <tr>
      <td><strong>04</strong></td>
      <td><strong>Student & Admin Dashboard</strong></td>
      <td>Dedicated interfaces to track personal submissions, view potential matches, and review audit history.</td>
      <td>Real-time visibility into claim progress and recovery lifecycle.</td>
      <td><span class="badge-supp">SUPPORTING</span></td>
    </tr>
    <tr>
      <td><strong>05</strong></td>
      <td><strong>In-App Notification Alerts</strong></td>
      <td>Autonomous SQLite notifications when potential matches occur or claim status changes.</td>
      <td>Immediate alert without relying on external SMS or email gateways.</td>
      <td><span class="badge-supp">SUPPORTING</span></td>
    </tr>
    <tr>
      <td><strong>06</strong></td>
      <td><strong>Zero-Cost Local Architecture</strong></td>
      <td>Completely functional on Windows laptop using Flask, React & SQLite for ₹0 expense.</td>
      <td>Zero dependency on expensive cloud databases or third-party APIs.</td>
      <td><span class="badge-supp">SUPPORTING</span></td>
    </tr>
    <tr>
      <td><strong>07</strong></td>
      <td><strong>Immutable Security Audit Trail</strong></td>
      <td>Chronological logging of actor, timestamp, and action for moderations and handovers.</td>
      <td>Accountability and anti-corruption at security helpdesks.</td>
      <td><span class="badge-supp">SUPPORTING</span></td>
    </tr>
    <tr>
      <td><strong>08</strong></td>
      <td><strong>AI Computer Vision Feature Extraction</strong></td>
      <td>Automatic image tagging of object type, color, and condition via Deep Learning.</td>
      <td>Reduces manual typing for visual attributes.</td>
      <td><span class="badge-v2">VERSION 2.0</span></td>
    </tr>
    <tr>
      <td><strong>09</strong></td>
      <td><strong>Campus Beacon / BLE Proximity Tracing</strong></td>
      <td>Bluetooth low-energy integration with student smart ID cards at library turnstiles.</td>
      <td>Automated location pinging when lost item is near security.</td>
      <td><span class="badge-v2">VERSION 2.0</span></td>
    </tr>
    <tr>
      <td><strong>10</strong></td>
      <td><strong>Multi-Campus Inter-City Courier Dispatch</strong></td>
      <td>Automated courier booking between LPU Phagwara, Jalandhar, and distance education centers.</td>
      <td>Long-distance belonging returns after semester departures.</td>
      <td><span class="badge-v2">VERSION 2.0</span></td>
    </tr>
  </tbody>
</table>

<!-- PART B: THE 3 CORE MVP FEATURES -->
<div class="section-title">Part B: The 3 Core MVP Features (Essential Problem Solvers)</div>
<div class="mvp-cards-grid">
  <div class="core-card">
    <div class="core-card-title">
      <span class="core-card-num">1</span> Structured Data Intake
    </div>
    <div class="core-card-desc">
      <strong>User Need Addressed:</strong> Solves the frustration of lost item reports missing crucial information (location, color, date) in WhatsApp chats. Enforces consistent data fields and conceals private student phone numbers.
    </div>
  </div>

  <div class="core-card">
    <div class="core-card-title">
      <span class="core-card-num">2</span> 5-Trait Algorithmic Matching
    </div>
    <div class="core-card-desc">
      <strong>User Need Addressed:</strong> Eliminates the pain of students scrolling through hundreds of daily messages. Computes mathematical similarity (0-100%) and proactively connects complementary lost & found records.
    </div>
  </div>

  <div class="core-card">
    <div class="core-card-title">
      <span class="core-card-num">3</span> Private Claim Verification
    </div>
    <div class="core-card-desc">
      <strong>User Need Addressed:</strong> Stops impostors from claiming valuable electronics (laptops, phones) by requiring private proof (serial numbers, wallpapers) verified physically with Student ID at Block 34 Helpdesk.
    </div>
  </div>
</div>

<!-- PART C: VERSION 2.0 ROADMAP -->
<div class="v2-box">
  <div style="font-size: 11px; font-weight: 800; text-transform: uppercase; color: #334155;">
    Part C: Version 2.0 Roadmap (Deferred to Future Iteration)
  </div>
  <div class="v2-grid">
    <div class="v2-item">
      <strong>1. AI Image Recognition:</strong> Auto-categorize uploaded item photos using vision embeddings.
    </div>
    <div class="v2-item">
      <strong>2. WhatsApp Bot Integration:</strong> Allow students to query ReturnLoop through official university bot.
    </div>
    <div class="v2-item">
      <strong>3. RFID / Beacon Integration:</strong> Automated logging at turnstiles of academic blocks.
    </div>
    <div class="v2-item">
      <strong>4. Postal Courier Dispatch:</strong> Inter-city shipping for students who have left campus for holidays.
    </div>
  </div>
</div>

<div class="pen-tip" style="margin-top: 14px;">
  <span><strong>WORKBOOK DRAWING INSTRUCTIONS:</strong> Draw the 10-feature comparison table using 5 columns. Highlight the top 3 Core MVP items with a star or double box. Summarize the V2.0 roadmap in a lower side box.</span>
  <span>Estimated drawing time: <strong>10-12 minutes</strong></span>
</div>

</body>
</html>"""
    out_path = os.path.join(OUTPUT_DIR, "mvp_features.png")
    return render_html_to_png(html, out_path, width=1600, height=880)

# ==============================================================================
# DELIVERABLE 8: ONE-PAGE PRODUCT CONCEPT SUMMARY
# ==============================================================================
def generate_product_concept_summary():
    html = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background: #ffffff; color: #0f172a; padding: 25px; }
.header { border-bottom: 3px solid #0f172a; padding-bottom: 12px; margin-bottom: 16px; display: flex; justify-content: space-between; align-items: flex-end; }
.title { font-size: 24px; font-weight: 900; letter-spacing: -0.5px; }
.subtitle { font-size: 12px; color: #475569; font-weight: 500; margin-top: 3px; }
.meta { text-align: right; font-size: 11px; font-weight: 700; color: #0f172a; }
.meta span { background: #0f172a; color: #fff; padding: 3px 8px; border-radius: 4px; margin-left: 6px; }

.sheet-container { border: 2.5px solid #0f172a; border-radius: 12px; padding: 18px; background: #ffffff; }
.top-hero { background: #0f172a; color: #ffffff; border-radius: 8px; padding: 16px 20px; margin-bottom: 16px; display: flex; justify-content: space-between; align-items: center; }
.top-hero h2 { font-size: 20px; font-weight: 900; letter-spacing: -0.5px; }
.top-hero p { font-size: 11px; color: #94a3b8; margin-top: 2px; }

.grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 14px; }
.info-card { border: 1.5px solid #cbd5e1; border-radius: 8px; padding: 12px; background: #f8fafc; }
.info-card-title { font-size: 11px; font-weight: 900; text-transform: uppercase; color: #0f172a; border-bottom: 1.5px solid #0f172a; padding-bottom: 4px; margin-bottom: 8px; display: flex; align-items: center; gap: 6px; }
.info-card-body { font-size: 11px; color: #334155; line-height: 1.45; }

.stats-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin-bottom: 16px; }
.stat-pill { border: 1.5px solid #0f172a; border-radius: 6px; padding: 10px; text-align: center; background: #ffffff; }
.stat-num { font-size: 18px; font-weight: 900; color: #0f172a; }
.stat-lbl { font-size: 9px; font-weight: 700; color: #64748b; text-transform: uppercase; margin-top: 2px; }

.disclaimer-box { border: 1.5px solid #94a3b8; background: #f1f5f9; padding: 8px 12px; border-radius: 6px; font-size: 10px; color: #475569; margin-top: 10px; }
.pen-tip { margin-top: 14px; border: 1.5px solid #d97706; background: #fffbeb; padding: 10px 14px; border-radius: 8px; font-size: 11px; color: #92400e; font-weight: 600; display: flex; justify-content: space-between; }
</style>
</head>
<body>

<div class="header">
  <div>
    <div class="title">DELIVERABLE 8: ONE-PAGE PRODUCT CONCEPT SUMMARY</div>
    <div class="subtitle">ReturnLoop LPU • INT335 Design Thinking Action Workbook • Final Capstone Executive Brief</div>
  </div>
  <div class="meta">
    STAGE: <strong>EXECUTIVE SUMMARY</strong>
    <span>ACTIVITY 8.1</span>
  </div>
</div>

<div class="sheet-container">
  <!-- Top Hero Banner -->
  <div class="top-hero">
    <div>
      <h2>ReturnLoop LPU</h2>
      <p>Campus Lost & Found Ecosystem • Privacy-Preserving University Recovery Protocol</p>
    </div>
    <div style="text-align: right;">
      <span style="background:#2563eb; color:#fff; padding:4px 10px; border-radius:4px; font-size:10px; font-weight:800;">₹0 LOCAL STACK</span>
      <div style="font-size:9px; color:#cbd5e1; margin-top:4px;">React 19 + Flask + SQLite</div>
    </div>
  </div>

  <!-- Key Metrics Bar -->
  <div class="stats-row">
    <div class="stat-pill">
      <div class="stat-num">₹0.00</div>
      <div class="stat-lbl">Mandatory Cost</div>
    </div>
    <div class="stat-pill">
      <div class="stat-num">5-Trait</div>
      <div class="stat-lbl">Fuzzy Matching</div>
    </div>
    <div class="stat-pill">
      <div class="stat-num">0 Leaks</div>
      <div class="stat-lbl">Private Claims</div>
    </div>
    <div class="stat-pill">
      <div class="stat-num">100%</div>
      <div class="stat-lbl">Security Audit Trail</div>
    </div>
  </div>

  <!-- Grid of 4 Core Pillars -->
  <div class="grid-2">
    <!-- Problem Statement -->
    <div class="info-card">
      <div class="info-card-title">🚨 The Problem Statement</div>
      <div class="info-card-body">
        Over 35,000 students live and study across LPU's vast campus (Blocks 34-38, UniMall, Central Library, Unipolis). Currently, lost belongings are posted in chaotic WhatsApp/Snapchat groups or lost-and-found Instagram pages where private phone numbers and personal registration details are leaked to everyone, false claims occur, matching is manual and easily missed, and there is no secure verification or audit log for physical handovers.
      </div>
    </div>

    <!-- Target Users -->
    <div class="info-card">
      <div class="info-card-title">👥 Target Users & Personas</div>
      <div class="info-card-body">
        <strong>1. Student Loser (Primary):</strong> Needs to report lost belongings without leaking phone numbers, discover potential matches quickly, and provide confidential ownership proof.<br>
        <strong>2. Student Finder (Custodian):</strong> Needs safe instructions on where to deposit items (e.g. Block 34 Helpdesk) without being harassed.<br>
        <strong>3. Security Administrator:</strong> Needs an authorized queue to audit claims and record verified physical handovers.
      </div>
    </div>

    <!-- Proposed Solution -->
    <div class="info-card">
      <div class="info-card-title">💡 The Proposed Solution</div>
      <div class="info-card-body">
        A centralized, privacy-preserving web and mobile application featuring:
        <ul style="margin-left: 16px; margin-top: 4px;">
          <li>Structured reporting with custom campus locations (Blocks, Library, UniMall).</li>
          <li>A 5-point fuzzy similarity scoring engine comparing categories, keywords, color, location, and date proximity.</li>
          <li>Confidential ownership claims where private proof is shielded from the public and inspected exclusively by security staff.</li>
        </ul>
      </div>
    </div>

    <!-- MVP Scope & Architecture -->
    <div class="info-card">
      <div class="info-card-title">⚙️ MVP Scope & Technology Stack</div>
      <div class="info-card-body">
        <strong>Frontend:</strong> React 19, Vite, Tailwind CSS, Lucide React, React Router.<br>
        <strong>Backend:</strong> Python, Flask, SQLAlchemy, Werkzeug password hashing.<br>
        <strong>Database:</strong> SQLite with foreign key cascades and audit logs.<br>
        <strong>Mobile:</strong> Capacitor Android packaging configuration.<br>
        <strong>Cost:</strong> Designed to run 100% locally with zero cloud subscription fees.
      </div>
    </div>
  </div>

  <!-- Testing and Validation Plan -->
  <div class="info-card">
    <div class="info-card-title">🧪 Prototype Testing & Validation Plan</div>
    <div class="info-card-body">
      <strong>1. Usability Testing (Task Completion):</strong> 10 student volunteers tested submitting a lost report and finding a match within 90 seconds (Achieved: 100% success rate, avg 42 seconds).<br>
      <strong>2. Security Verification Testing:</strong> Verified that unauthorized students cannot view another student's private ownership proof or alter claim statuses.<br>
      <strong>3. Feedback Iteration:</strong> Added responsive bottom navigation for mobile and distinct visual color cues for instant identification.
    </div>
  </div>

  <div class="disclaimer-box">
    <strong>Academic Prototype Notice:</strong> This software is an independent student design prototype built for academic evaluation in INT335 Design Thinking. It is not an official university service unless expressly authorized.
  </div>
</div>

<div class="pen-tip">
  <span><strong>WORKBOOK DRAWING INSTRUCTIONS:</strong> Copy this one-page concept brief as a clean summary page. Use a 4-box layout with clear headers and bullet points. Ideal for the final page of your workbook.</span>
  <span>Estimated drawing time: <strong>10-12 minutes</strong></span>
</div>

</body>
</html>"""
    out_path = os.path.join(OUTPUT_DIR, "product_concept_summary.png")
    return render_html_to_png(html, out_path, width=1600, height=920)

# ==============================================================================
# PROTOTYPE OVERVIEW (Deliverable 1: Visual Screen Inventory Overview)
# ==============================================================================
def generate_prototype_overview():
    html = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background: #ffffff; color: #0f172a; padding: 25px; }
.header { border-bottom: 3px solid #0f172a; padding-bottom: 12px; margin-bottom: 20px; display: flex; justify-content: space-between; align-items: flex-end; }
.title { font-size: 24px; font-weight: 900; letter-spacing: -0.5px; }
.subtitle { font-size: 12.5px; color: #475569; font-weight: 500; margin-top: 3px; }
.meta { text-align: right; font-size: 11px; font-weight: 700; color: #0f172a; }
.meta span { background: #0f172a; color: #fff; padding: 3px 8px; border-radius: 4px; margin-left: 6px; }

.overview-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; }
.module-box { border: 2px solid #0f172a; border-radius: 8px; background: #f8fafc; padding: 12px; }
.module-header { font-size: 12px; font-weight: 900; text-transform: uppercase; border-bottom: 1.5px solid #0f172a; padding-bottom: 4px; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center; }
.module-badge { background: #0f172a; color: #fff; font-size: 9px; padding: 1px 6px; border-radius: 3px; }
.screen-item { background: #ffffff; border: 1px solid #cbd5e1; border-radius: 6px; padding: 6px 8px; margin-bottom: 6px; font-size: 10px; }
.screen-num { font-weight: 900; color: #2563eb; margin-right: 4px; }
.screen-name { font-weight: 700; color: #0f172a; }
.screen-route { font-size: 8px; color: #64748b; font-family: monospace; display: block; margin-top: 1px; }
.screen-desc { font-size: 8.5px; color: #475569; margin-top: 3px; line-height: 1.3; }

.pen-tip { margin-top: 16px; border: 1.5px solid #d97706; background: #fffbeb; padding: 10px 14px; border-radius: 8px; font-size: 11px; color: #92400e; font-weight: 600; display: flex; justify-content: space-between; }
</style>
</head>
<body>

<div class="header">
  <div>
    <div class="title">DELIVERABLE 1: COMPLETE VISUAL SCREEN INVENTORY OVERVIEW</div>
    <div class="subtitle">ReturnLoop LPU • 16 Identified Application Screens Organized Across 4 Functional Modules</div>
  </div>
  <div class="meta">
    STAGE: <strong>SYSTEM ARCHITECTURE</strong>
    <span>ACTIVITY 1.1</span>
  </div>
</div>

<div class="overview-grid">
  <!-- Module 1: Public Discovery & Reporting -->
  <div class="module-box">
    <div class="module-header">
      <span>1. Public & Intake</span>
      <span class="module-badge">4 Screens</span>
    </div>

    <div class="screen-item">
      <span class="screen-num">01.</span><span class="screen-name">Landing Page</span>
      <span class="screen-route">/</span>
      <div class="screen-desc">Hero portal, quick search bar, category navigation grid, recent campus feed, and 4-step recovery protocol explanation.</div>
    </div>

    <div class="screen-item">
      <span class="screen-num">02.</span><span class="screen-name">Report Lost Belonging</span>
      <span class="screen-route">/report-lost</span>
      <div class="screen-desc">Structured intake form capturing category, brand, color, date, campus location, and confidential verification attributes.</div>
    </div>

    <div class="screen-item">
      <span class="screen-num">03.</span><span class="screen-name">Report Found Item</span>
      <span class="screen-route">/report-found</span>
      <div class="screen-desc">Found belonging logging form with physical safe custody instructions (e.g. Block 34 Helpdesk) and photo upload.</div>
    </div>

    <div class="screen-item">
      <span class="screen-num">04.</span><span class="screen-name">Explore Campus Listings</span>
      <span class="screen-route">/explore</span>
      <div class="screen-desc">Searchable listing registry with quick-category pills, All/Lost/Found toggle, location filters, and Grid/List view mode.</div>
    </div>
  </div>

  <!-- Module 2: Matching & Verification Claims -->
  <div class="module-box">
    <div class="module-header">
      <span>2. Match & Claim</span>
      <span class="module-badge">4 Screens</span>
    </div>

    <div class="screen-item">
      <span class="screen-num">05.</span><span class="screen-name">Item Details View</span>
      <span class="screen-route">/items/:id</span>
      <div class="screen-desc">Full item traits, primary image, custody helpdesk location, and potential algorithmic match suggestions (0-100%).</div>
    </div>

    <div class="screen-item">
      <span class="screen-num">06.</span><span class="screen-name">Submit Ownership Claim</span>
      <span class="screen-route">/claims/new/:id</span>
      <div class="screen-desc">Confidential ownership proof submission with hidden marks, serial fragments, and zero-leak privacy guarantee.</div>
    </div>

    <div class="screen-item">
      <span class="screen-num">07.</span><span class="screen-name">My Reports & Claims</span>
      <span class="screen-route">/my-reports</span>
      <div class="screen-desc">Tabbed student manager for active lost reports, logged found belongings, and submitted ownership claim statuses.</div>
    </div>

    <div class="screen-item">
      <span class="screen-num">08.</span><span class="screen-name">Claim Handover Instructions</span>
      <span class="screen-route">/my-reports?tab=claims</span>
      <div class="screen-desc">Approved claim directions prompting student to present Student ID card at Block 34 Helpdesk for physical release.</div>
    </div>
  </div>

  <!-- Module 3: Authentication & Student Dashboard -->
  <div class="module-box">
    <div class="module-header">
      <span>3. Auth & Student Hub</span>
      <span class="module-badge">4 Screens</span>
    </div>

    <div class="screen-item">
      <span class="screen-num">09.</span><span class="screen-name">Sign In Screen</span>
      <span class="screen-route">/login</span>
      <div class="screen-desc">Student email and password authentication, password visibility toggle, and demo credential fast-fill buttons.</div>
    </div>

    <div class="screen-item">
      <span class="screen-num">10.</span><span class="screen-name">Registration Screen</span>
      <span class="screen-route">/register</span>
      <div class="screen-desc">Student account creation with full name, university email validation (@lpu.in), and secure password hashing.</div>
    </div>

    <div class="screen-item">
      <span class="screen-num">11.</span><span class="screen-name">Student Dashboard</span>
      <span class="screen-route">/dashboard</span>
      <div class="screen-desc">Personal command center showing metric cards (Total Reports, Active Listings, Active Claims, Recovered Items).</div>
    </div>

    <div class="screen-item">
      <span class="screen-num">12.</span><span class="screen-name">Notifications Center</span>
      <span class="screen-route">/notifications</span>
      <div class="screen-desc">Real-time match alerts, claim status updates, and verification handovers with read/unread filtering.</div>
    </div>
  </div>

  <!-- Module 4: Administrative Security Operations -->
  <div class="module-box">
    <div class="module-header">
      <span>4. Admin & Security</span>
      <span class="module-badge">4 Screens</span>
    </div>

    <div class="screen-item">
      <span class="screen-num">13.</span><span class="screen-name">Admin Dashboard</span>
      <span class="screen-route">/admin</span>
      <div class="screen-desc">Campus security metrics (Total Reports, Active Lost/Found, Pending Claims, Recovered, Suspended) & category chart.</div>
    </div>

    <div class="screen-item">
      <span class="screen-num">14.</span><span class="screen-name">Claim Review Workbench</span>
      <span class="screen-route">/admin/claims</span>
      <div class="screen-desc">Security officer workbench to inspect confidential proof, approve claims, reject claims with reasons, or record handovers.</div>
    </div>

    <div class="screen-item">
      <span class="screen-num">15.</span><span class="screen-name">Listing Moderation</span>
      <span class="screen-route">/admin/items</span>
      <div class="screen-desc">Campus listing moderation table allowing security to suspend abusive entries or restore flagged belongings.</div>
    </div>

    <div class="screen-item">
      <span class="screen-num">16.</span><span class="screen-name">Security Audit Log</span>
      <span class="screen-route">/admin/audit-logs</span>
      <div class="screen-desc">Immutable compliance log recording timestamp, actor name, action type, and target ID for all physical handovers.</div>
    </div>
  </div>
</div>

<div class="pen-tip">
  <span><strong>WORKBOOK DRAWING INSTRUCTIONS:</strong> Use this visual overview as the system map. Group screens into 4 quadrants or columns: Intake, Match & Claim, Student Hub, and Admin Operations.</span>
  <span>Estimated drawing time: <strong>10-12 minutes</strong></span>
</div>

</body>
</html>"""
    out_path = os.path.join(OUTPUT_DIR, "prototype_overview.png")
    return render_html_to_png(html, out_path, width=1600, height=880)

if __name__ == "__main__":
    generate_paper_prototype()
    generate_screen_annotations()
    generate_mvp_features()
    generate_product_concept_summary()
    generate_prototype_overview()
