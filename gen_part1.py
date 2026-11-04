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
# 1. STORYBOARD (Deliverable 4: Six-Panel User Storyboard)
# ==============================================================================
def generate_storyboard():
    html = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background: #ffffff; color: #0f172a; padding: 30px; }
.header { border-bottom: 3px solid #0f172a; padding-bottom: 12px; margin-bottom: 24px; display: flex; justify-content: space-between; align-items: flex-end; }
.title { font-size: 26px; font-weight: 900; letter-spacing: -0.5px; }
.subtitle { font-size: 13px; color: #475569; font-weight: 500; margin-top: 4px; }
.meta { text-align: right; font-size: 11px; font-weight: 700; color: #0f172a; }
.meta span { background: #0f172a; color: #fff; padding: 3px 8px; border-radius: 4px; margin-left: 6px; }

.grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }
.panel { border: 2.5px solid #0f172a; border-radius: 12px; background: #ffffff; overflow: hidden; display: flex; flex-direction: column; }
.panel-header { background: #f1f5f9; border-bottom: 2px solid #0f172a; padding: 8px 12px; display: flex; justify-content: space-between; align-items: center; }
.panel-num { font-size: 12px; font-weight: 900; background: #0f172a; color: #fff; width: 22px; height: 22px; border-radius: 50%; display: flex; align-items: center; justify-content: center; }
.panel-title { font-size: 13px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.5px; }
.emotion-tag { font-size: 11px; font-weight: 700; border: 1.5px solid #0f172a; padding: 2px 8px; border-radius: 12px; background: #ffffff; }

.drawing-area { height: 220px; background: #ffffff; border-bottom: 2px solid #0f172a; position: relative; display: flex; align-items: center; justify-content: center; padding: 12px; }
.caption-area { padding: 12px 14px; background: #fafafa; flex: 1; display: flex; flex-direction: column; justify-content: space-between; }
.caption-text { font-size: 12px; line-height: 1.45; color: #1e293b; font-weight: 500; }
.dialogue-box { margin-top: 8px; background: #ffffff; border: 1.5px dashed #0f172a; padding: 6px 10px; border-radius: 6px; font-size: 11px; font-style: italic; color: #334155; }
.pen-tip { margin-top: 20px; border: 1.5px solid #d97706; background: #fffbeb; padding: 10px 14px; border-radius: 8px; font-size: 11px; color: #92400e; font-weight: 600; display: flex; justify-content: space-between; }
</style>
</head>
<body>

<div class="header">
  <div>
    <div class="title">DELIVERABLE 4: SIX-PANEL USER STORYBOARD</div>
    <div class="subtitle">Project: ReturnLoop LPU • Course: INT335 Design Thinking Action Workbook • Persona: Aarav Sharma (B.Tech CSE, LPU)</div>
  </div>
  <div class="meta">
    STAGE: <strong>PROTOTYPING & NARRATIVE</strong>
    <span>ACTIVITY 4.2</span>
  </div>
</div>

<div class="grid">
  <!-- Panel 1 -->
  <div class="panel">
    <div class="panel-header">
      <div style="display:flex; align-items:center; gap:8px;">
        <div class="panel-num">1</div>
        <div class="panel-title">Setup</div>
      </div>
      <div class="emotion-tag">😐 Focused / Relaxed</div>
    </div>
    <div class="drawing-area">
      <svg width="280" height="200" viewBox="0 0 280 200">
        <!-- Room lines (Central Library) -->
        <line x1="10" y1="160" x2="270" y2="160" stroke="#0f172a" stroke-width="2.5" />
        <line x1="210" y1="40" x2="210" y2="160" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="3,3" />
        <text x="215" y="60" font-size="9" fill="#64748b" font-weight="700">CENTRAL LIBRARY - 3RD FL</text>
        <!-- Desk -->
        <rect x="40" y="110" width="180" height="50" fill="#f8fafc" stroke="#0f172a" stroke-width="2" rx="4" />
        <line x1="50" y1="160" x2="50" y2="190" stroke="#0f172a" stroke-width="2" />
        <line x1="210" y1="160" x2="210" y2="190" stroke="#0f172a" stroke-width="2" />
        <!-- Student Stick/Simple Figure -->
        <circle cx="100" cy="70" r="16" fill="#ffffff" stroke="#0f172a" stroke-width="2.5" />
        <path d="M100 86 L100 125 M85 100 L115 100 M100 125 L85 155 M100 125 L115 155" stroke="#0f172a" stroke-width="2.5" stroke-linecap="round" />
        <!-- Laptop on desk -->
        <path d="M130 108 L170 108 L160 85 L140 85 Z" fill="#ffffff" stroke="#0f172a" stroke-width="2" />
        <rect x="125" y="108" width="50" height="6" fill="#0f172a" rx="2" />
        <text x="135" y="100" font-size="8" font-weight="bold" fill="#0f172a">HP 15</text>
        <!-- Books -->
        <rect x="60" y="98" width="22" height="12" fill="#e2e8f0" stroke="#0f172a" stroke-width="1.5" />
      </svg>
    </div>
    <div class="caption-area">
      <p class="caption-text"><strong>Aarav</strong> studies at LPU Central Library with his blue HP laptop and notebook before his 2:00 PM computer networks practical.</p>
      <div class="dialogue-box">"Almost done with my practical assignment..."</div>
    </div>
  </div>

  <!-- Panel 2 -->
  <div class="panel">
    <div class="panel-header">
      <div style="display:flex; align-items:center; gap:8px;">
        <div class="panel-num">2</div>
        <div class="panel-title">Problem</div>
      </div>
      <div class="emotion-tag">😰 Panicked / Frustrated</div>
    </div>
    <div class="drawing-area">
      <svg width="280" height="200" viewBox="0 0 280 200">
        <!-- Academic Block 34 hallway -->
        <line x1="20" y1="170" x2="260" y2="170" stroke="#0f172a" stroke-width="2.5" />
        <!-- Aarav Panicking -->
        <circle cx="80" cy="80" r="18" fill="#ffffff" stroke="#0f172a" stroke-width="2.5" />
        <!-- Sweat drops -->
        <path d="M60 70 Q55 75 60 80 Q65 75 60 70 Z" fill="#0f172a" />
        <path d="M102 70 Q107 75 102 80 Q97 75 102 70 Z" fill="#0f172a" />
        <!-- Shock face -->
        <circle cx="74" cy="78" r="2" fill="#0f172a" /><circle cx="86" cy="78" r="2" fill="#0f172a" />
        <ellipse cx="80" cy="88" rx="4" ry="6" fill="#0f172a" />
        <path d="M80 98 L80 140 M65 110 L95 110 M80 140 L65 170 M80 140 L95 170" stroke="#0f172a" stroke-width="2.5" stroke-linecap="round" />
        <!-- Hand on head gesture -->
        <path d="M65 110 L60 85 L70 75" stroke="#0f172a" stroke-width="2.5" fill="none" />
        <!-- Empty Backpack -->
        <rect x="115" y="115" width="30" height="40" rx="6" fill="#f1f5f9" stroke="#0f172a" stroke-width="2" />
        <text x="120" y="138" font-size="9" font-weight="900" fill="#dc2626">EMPTY!</text>
        <!-- WhatsApp chaotic chat box bubble -->
        <rect x="155" y="30" width="115" height="75" rx="8" fill="#ffffff" stroke="#0f172a" stroke-width="2" />
        <text x="162" y="46" font-size="8" font-weight="bold" fill="#0f172a">WhatsApp Group (750 msgs):</text>
        <line x1="162" y1="52" x2="260" y2="52" stroke="#cbd5e1" stroke-width="1" />
        <text x="162" y="65" font-size="8" fill="#64748b">"Anyone seen my laptop?"</text>
        <text x="162" y="77" font-size="8" fill="#dc2626">"Spam, fake claims, no reply"</text>
        <text x="162" y="92" font-size="7.5" fill="#0f172a" font-weight="bold">⚠️ Phone leaked publicly!</text>
      </svg>
    </div>
    <div class="caption-area">
      <p class="caption-text">Reaching Block 34 lab, he discovers his laptop bag is empty. He posts in chaotic WhatsApp groups where his phone number is leaked with zero results.</p>
      <div class="dialogue-box">"My project code is on that laptop! Where do I search?!"</div>
    </div>
  </div>

  <!-- Panel 3 -->
  <div class="panel">
    <div class="panel-header">
      <div style="display:flex; align-items:center; gap:8px;">
        <div class="panel-num">3</div>
        <div class="panel-title">Discovery</div>
      </div>
      <div class="emotion-tag">💡 Hopeful / Curious</div>
    </div>
    <div class="drawing-area">
      <svg width="280" height="200" viewBox="0 0 280 200">
        <!-- Friend showing phone -->
        <circle cx="70" cy="75" r="16" fill="#ffffff" stroke="#0f172a" stroke-width="2.5" />
        <path d="M70 91 L70 140 M55 110 L95 105 M70 140 L55 170 M70 140 L85 170" stroke="#0f172a" stroke-width="2.5" />
        <!-- Aarav listening -->
        <circle cx="210" cy="75" r="16" fill="#ffffff" stroke="#0f172a" stroke-width="2.5" />
        <path d="M210 91 L210 140 M190 110 L230 110 M210 140 L195 170 M210 140 L225 170" stroke="#0f172a" stroke-width="2.5" />
        <!-- Big Phone between them showing ReturnLoop -->
        <rect x="110" y="35" width="70" height="120" rx="10" fill="#ffffff" stroke="#0f172a" stroke-width="2.5" />
        <!-- Screen details -->
        <rect x="116" y="45" width="58" height="18" fill="#0f172a" rx="2" />
        <text x="120" y="58" font-size="8" font-weight="bold" fill="#ffffff">ReturnLoop</text>
        <rect x="118" y="70" width="54" height="14" fill="#fee2e2" stroke="#0f172a" stroke-width="1" rx="3" />
        <text x="122" y="80" font-size="7" font-weight="bold" fill="#991b1b">Report Lost</text>
        <rect x="118" y="90" width="54" height="14" fill="#ccfbf1" stroke="#0f172a" stroke-width="1" rx="3" />
        <text x="120" y="100" font-size="7" font-weight="bold" fill="#115e59">Report Found</text>
        <rect x="118" y="112" width="54" height="30" fill="#f8fafc" stroke="#94a3b8" stroke-width="1" rx="2" />
        <text x="122" y="125" font-size="6.5" font-weight="bold" fill="#0f172a">Campus Hub</text>
        <text x="122" y="134" font-size="6" fill="#475569">Block 34 Helpdesk</text>
      </svg>
    </div>
    <div class="caption-area">
      <p class="caption-text">Classmate Priya tells him about <strong>ReturnLoop LPU</strong>, the dedicated zero-cost campus lost-and-found registry connected to security.</p>
      <div class="dialogue-box">"Don't worry, post it on ReturnLoop LPU! Security logs items there."</div>
    </div>
  </div>

  <!-- Panel 4 -->
  <div class="panel">
    <div class="panel-header">
      <div style="display:flex; align-items:center; gap:8px;">
        <div class="panel-num">4</div>
        <div class="panel-title">Action</div>
      </div>
      <div class="emotion-tag">✍️ Proactive / Secure</div>
    </div>
    <div class="drawing-area">
      <svg width="280" height="200" viewBox="0 0 280 200">
        <!-- Split view: Aarav filling report on phone VS Security logging item -->
        <!-- Left: Aarav's mobile screen -->
        <rect x="25" y="20" width="105" height="165" rx="8" fill="#ffffff" stroke="#0f172a" stroke-width="2" />
        <rect x="25" y="20" width="105" height="20" fill="#0f172a" />
        <text x="32" y="34" font-size="8" font-weight="bold" fill="#ffffff">Report Lost Item</text>
        <text x="32" y="52" font-size="7" font-weight="bold">Item: HP 15 Blue</text>
        <rect x="30" y="56" width="95" height="12" fill="#f1f5f9" stroke="#94a3b8" stroke-width="1" />
        <text x="32" y="78" font-size="7" font-weight="bold">Loc: Central Library</text>
        <rect x="30" y="82" width="95" height="12" fill="#f1f5f9" stroke="#94a3b8" stroke-width="1" />
        <!-- Private Proof Box -->
        <rect x="30" y="102" width="95" height="35" fill="#fef3c7" stroke="#d97706" stroke-width="1" rx="3" />
        <text x="34" y="113" font-size="6.5" font-weight="bold" fill="#92400e">🔒 Private Marks (Hidden):</text>
        <text x="34" y="123" font-size="6" fill="#92400e">"Python sticker, crack on lid,"</text>
        <text x="34" y="131" font-size="6" fill="#92400e">"Wallpaper: Red Ferrari"</text>
        <rect x="30" y="145" width="95" height="16" fill="#0f172a" rx="4" />
        <text x="45" y="156" font-size="7" font-weight="bold" fill="#ffffff">Submit Lost Report</text>

        <!-- Divider -->
        <line x1="140" y1="20" x2="140" y2="185" stroke="#94a3b8" stroke-dasharray="4,4" stroke-width="1.5" />

        <!-- Right: Security Staff logging found item -->
        <rect x="155" y="20" width="105" height="165" rx="8" fill="#ffffff" stroke="#0f172a" stroke-width="2" />
        <rect x="155" y="20" width="105" height="20" fill="#047857" />
        <text x="162" y="34" font-size="8" font-weight="bold" fill="#ffffff">Security Report Found</text>
        <text x="162" y="54" font-size="7" font-weight="bold">Custodian: Guard Om</text>
        <text x="162" y="68" font-size="7" font-weight="bold">Found at: Library Desk</text>
        <text x="162" y="82" font-size="7" font-weight="bold">Item: Blue Laptop</text>
        <rect x="160" y="95" width="95" height="42" fill="#f1f5f9" stroke="#94a3b8" stroke-width="1" rx="3" />
        <text x="164" y="108" font-size="7" font-weight="bold" fill="#0f172a">Safe Custody:</text>
        <text x="164" y="120" font-size="6.5" fill="#475569">Block 34 Security Office</text>
        <text x="164" y="130" font-size="6.5" fill="#475569">Ground Floor Vault</text>
        <text x="175" y="160" font-size="8" font-weight="bold" fill="#047857">RL-FND-2026-9021</text>
      </svg>
    </div>
    <div class="caption-area">
      <p class="caption-text">Aarav logs his lost report with hidden proof (custom sticker & wallpaper description). Concurrently, Central Security logs a laptop found by library staff.</p>
      <div class="dialogue-box">"My private details remain strictly hidden from the public feed."</div>
    </div>
  </div>

  <!-- Panel 5 -->
  <div class="panel">
    <div class="panel-header">
      <div style="display:flex; align-items:center; gap:8px;">
        <div class="panel-num">5</div>
        <div class="panel-title">Experience</div>
      </div>
      <div class="emotion-tag">✨ Relieved / Excited</div>
    </div>
    <div class="drawing-area">
      <svg width="280" height="200" viewBox="0 0 280 200">
        <!-- Notification Pop & Algorithmic Matching -->
        <rect x="25" y="25" width="230" height="60" rx="8" fill="#ffffff" stroke="#0f172a" stroke-width="2" />
        <circle cx="45" cy="55" r="14" fill="#0f172a" />
        <text x="41" y="60" font-size="12" fill="#fff" font-weight="bold">⚡</text>
        <text x="68" y="45" font-size="9" font-weight="900" fill="#0f172a">HIGH PROBABILITY MATCH DETECTED!</text>
        <text x="68" y="58" font-size="8" fill="#475569">5-Trait Engine: Category, Location, Color & Time match</text>
        <rect x="68" y="63" width="75" height="15" fill="#dbeafe" rx="3" stroke="#2563eb" stroke-width="1" />
        <text x="73" y="74" font-size="8" font-weight="bold" fill="#1e40af">92% Match Score</text>

        <!-- Claim filing card -->
        <rect x="25" y="95" width="230" height="90" rx="8" fill="#f8fafc" stroke="#0f172a" stroke-width="2" />
        <text x="35" y="112" font-size="9" font-weight="bold">Step: Submit Confidential Ownership Claim</text>
        <rect x="35" y="120" width="210" height="35" fill="#ffffff" stroke="#94a3b8" stroke-width="1" rx="4" />
        <text x="40" y="133" font-size="7.5" fill="#334155">"My laptop serial ends in 4492 and has Python sticker on lid."</text>
        <rect x="35" y="160" width="120" height="18" fill="#0f172a" rx="4" />
        <text x="45" y="172" font-size="8" font-weight="bold" fill="#ffffff">File Verification Claim</text>
        <text x="165" y="172" font-size="7.5" font-weight="bold" fill="#047857">Status: Under Review</text>
      </svg>
    </div>
    <div class="caption-area">
      <p class="caption-text">ReturnLoop's 5-trait similarity engine pairs the reports with a <strong>92% match score</strong>. Aarav receives an instant notification and files a private ownership claim.</p>
      <div class="dialogue-box">"Notification received! A blue HP laptop was found at Library 3rd Floor!"</div>
    </div>
  </div>

  <!-- Panel 6 -->
  <div class="panel">
    <div class="panel-header">
      <div style="display:flex; align-items:center; gap:8px;">
        <div class="panel-num">6</div>
        <div class="panel-title">Resolution</div>
      </div>
      <div class="emotion-tag">🎉 Delighted & Empowered</div>
    </div>
    <div class="drawing-area">
      <svg width="280" height="200" viewBox="0 0 280 200">
        <!-- Block 34 Security Desk Handover -->
        <rect x="40" y="110" width="200" height="50" fill="#f8fafc" stroke="#0f172a" stroke-width="2.5" rx="4" />
        <text x="80" y="135" font-size="10" font-weight="900" fill="#0f172a">BLOCK 34 SECURITY DESK</text>
        <text x="105" y="148" font-size="7.5" fill="#64748b">Central Handover Station</text>
        <!-- Security Officer -->
        <circle cx="85" cy="65" r="15" fill="#ffffff" stroke="#0f172a" stroke-width="2.5" />
        <!-- Security Cap -->
        <rect x="73" y="52" width="24" height="6" fill="#0f172a" rx="1" />
        <path d="M85 80 L85 120 M70 100 L100 100" stroke="#0f172a" stroke-width="2.5" />
        <!-- Handing laptop over desk -->
        <rect x="125" y="98" width="30" height="12" fill="#ffffff" stroke="#0f172a" stroke-width="2" rx="2" />
        <!-- Aarav smiling -->
        <circle cx="195" cy="65" r="15" fill="#ffffff" stroke="#0f172a" stroke-width="2.5" />
        <path d="M190 70 Q195 76 200 70" stroke="#0f172a" stroke-width="2" fill="none" />
        <path d="M195 80 L195 120 M180 100 L210 100" stroke="#0f172a" stroke-width="2.5" />
        <!-- Verified ID badge -->
        <rect x="180" y="112" width="16" height="22" rx="2" fill="#dbeafe" stroke="#0f172a" stroke-width="1.5" />
        <text x="182" y="125" font-size="6" font-weight="bold">ID</text>
        <!-- Verified Stamp -->
        <rect x="80" y="165" width="120" height="24" fill="#dcfce7" stroke="#16a34a" stroke-width="2" rx="6" />
        <text x="92" y="181" font-size="9" font-weight="900" fill="#15803d">✓ HANDOVER VERIFIED & AUDITED</text>
      </svg>
    </div>
    <div class="caption-area">
      <p class="caption-text">At Block 34 Helpdesk, Security Officer verifies Aarav's university registration ID and matching serial. The physical handover is recorded in the permanent audit trail.</p>
      <div class="dialogue-box">"Laptop safely recovered! ₹0 spent, zero privacy leaks."</div>
    </div>
  </div>
</div>

<div class="pen-tip">
  <span><strong>WORKBOOK DRAWING INSTRUCTIONS:</strong> Draw 6 equal boxes with a ruler. Use stick figures with simple geometric shapes (circle head, rectangular desk, phone outline). Include speech bubbles and emotion indicators.</span>
  <span>Estimated drawing time: <strong>12-15 minutes</strong></span>
</div>

</body>
</html>"""
    out_path = os.path.join(OUTPUT_DIR, "storyboard.png")
    return render_html_to_png(html, out_path, width=1500, height=960)

# ==============================================================================
# 2. USER FLOW DIAGRAM (Deliverable 5: User Flow Diagram)
# ==============================================================================
def generate_user_flow():
    html = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background: #ffffff; color: #0f172a; padding: 30px; }
.header { border-bottom: 3px solid #0f172a; padding-bottom: 12px; margin-bottom: 24px; display: flex; justify-content: space-between; align-items: flex-end; }
.title { font-size: 26px; font-weight: 900; letter-spacing: -0.5px; }
.subtitle { font-size: 13px; color: #475569; font-weight: 500; margin-top: 4px; }
.meta { text-align: right; font-size: 11px; font-weight: 700; color: #0f172a; }
.meta span { background: #0f172a; color: #fff; padding: 3px 8px; border-radius: 4px; margin-left: 6px; }

.canvas-card { border: 2.5px solid #0f172a; border-radius: 12px; background: #ffffff; padding: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }
.legend { display: flex; gap: 20px; border-bottom: 1.5px solid #e2e8f0; padding-bottom: 14px; margin-bottom: 16px; font-size: 11px; font-weight: 700; }
.legend-item { display: flex; align-items: center; gap: 8px; }
.shape-oval { width: 36px; height: 18px; border: 2px solid #0f172a; border-radius: 12px; background: #f1f5f9; }
.shape-rect { width: 36px; height: 20px; border: 2px solid #0f172a; border-radius: 4px; background: #ffffff; }
.shape-diamond { width: 20px; height: 20px; border: 2px solid #0f172a; transform: rotate(45deg); background: #fef3c7; }
.shape-arrow { width: 30px; height: 2px; background: #0f172a; position: relative; }
.shape-arrow::after { content: ''; position: absolute; right: 0; top: -3px; border-top: 4px solid transparent; border-bottom: 4px solid transparent; border-left: 6px solid #0f172a; }

.pen-tip { margin-top: 16px; border: 1.5px solid #d97706; background: #fffbeb; padding: 10px 14px; border-radius: 8px; font-size: 11px; color: #92400e; font-weight: 600; display: flex; justify-content: space-between; }
</style>
</head>
<body>

<div class="header">
  <div>
    <div class="title">DELIVERABLE 5: COMPLETE USER FLOW DIAGRAM</div>
    <div class="subtitle">ReturnLoop LPU • End-to-End Navigation, Decision Points, Trait Matching, Claims & Verification Flow</div>
  </div>
  <div class="meta">
    STAGE: <strong>SYSTEM ARCHITECTURE</strong>
    <span>ACTIVITY 5.1</span>
  </div>
</div>

<div class="canvas-card">
  <div class="legend">
    <div class="legend-item"><div class="shape-oval"></div> Start / End Point</div>
    <div class="legend-item"><div class="shape-rect"></div> Page / Screen (Action)</div>
    <div class="legend-item" style="margin-left: 8px;"><div class="shape-diamond"></div> Decision Branch (Yes / No)</div>
    <div class="legend-item"><div class="shape-arrow"></div> User Progression Path</div>
    <div class="legend-item" style="margin-left:auto; color:#dc2626;">⚠️ Error / Alternative Recovery Route</div>
  </div>

  <svg width="1400" height="740" viewBox="0 0 1400 740" style="font-family: inherit;">
    <!-- Definitions for arrows -->
    <defs>
      <marker id="arr" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
        <path d="M0,0 L0,6 L8,3 z" fill="#0f172a" />
      </marker>
      <marker id="arr-red" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
        <path d="M0,0 L0,6 L8,3 z" fill="#dc2626" />
      </marker>
      <marker id="arr-green" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
        <path d="M0,0 L0,6 L8,3 z" fill="#16a34a" />
      </marker>
    </defs>

    <!-- START -->
    <ellipse cx="90" cy="80" rx="50" ry="24" fill="#0f172a" />
    <text x="90" y="85" font-size="12" font-weight="bold" fill="#ffffff" text-anchor="middle">START</text>

    <!-- Arrow to Landing Page -->
    <line x1="140" y1="80" x2="200" y2="80" stroke="#0f172a" stroke-width="2" marker-end="url(#arr)" />

    <!-- 1. Landing Page -->
    <rect x="200" y="55" width="170" height="50" rx="6" fill="#ffffff" stroke="#0f172a" stroke-width="2" />
    <text x="285" y="77" font-size="11" font-weight="900" text-anchor="middle">Landing Page ( / )</text>
    <text x="285" y="93" font-size="9" fill="#475569" text-anchor="middle">Hero, Search & Categories</text>

    <!-- Arrow to Decision: What is user intent? -->
    <line x1="370" y1="80" x2="440" y2="80" stroke="#0f172a" stroke-width="2" marker-end="url(#arr)" />

    <!-- Decision 1: Intent -->
    <polygon points="500,40 560,80 500,120 440,80" fill="#fef3c7" stroke="#0f172a" stroke-width="2" />
    <text x="500" y="78" font-size="9.5" font-weight="900" text-anchor="middle">User</text>
    <text x="500" y="90" font-size="9.5" font-weight="900" text-anchor="middle">Action?</text>

    <!-- Branch A: Report Lost (Up) -->
    <line x1="500" y1="40" x2="500" y2="15" stroke="#0f172a" stroke-width="2" />
    <line x1="500" y1="15" x2="630" y2="15" stroke="#0f172a" stroke-width="2" marker-end="url(#arr)" />
    <text x="540" y="28" font-size="9" font-weight="bold" fill="#b91c1c">"Lost Item"</text>

    <!-- Branch B: Browse / Explore (Middle) -->
    <line x1="560" y1="80" x2="630" y2="80" stroke="#0f172a" stroke-width="2" marker-end="url(#arr)" />
    <text x="590" y="74" font-size="9" font-weight="bold">"Browse"</text>

    <!-- Branch C: Report Found (Down) -->
    <line x1="500" y1="120" x2="500" y2="150" stroke="#0f172a" stroke-width="2" />
    <line x1="500" y1="150" x2="630" y2="150" stroke="#0f172a" stroke-width="2" marker-end="url(#arr)" />
    <text x="540" y="142" font-size="9" font-weight="bold" fill="#047857">"Found Item"</text>

    <!-- Screen: Report Lost Page -->
    <rect x="630" y="-8" width="180" height="46" rx="6" fill="#fff1f2" stroke="#e11d48" stroke-width="2" />
    <text x="720" y="12" font-size="10.5" font-weight="bold" fill="#9f1239" text-anchor="middle">Report Lost Form</text>
    <text x="720" y="27" font-size="8.5" fill="#475569" text-anchor="middle">Title, Category, Color, Private Proof</text>

    <!-- Screen: Explore Page -->
    <rect x="630" y="58" width="180" height="46" rx="6" fill="#ffffff" stroke="#0f172a" stroke-width="2" />
    <text x="720" y="78" font-size="10.5" font-weight="bold" text-anchor="middle">Explore Listings</text>
    <text x="720" y="93" font-size="8.5" fill="#475569" text-anchor="middle">Search filter & Quick Pills</text>

    <!-- Screen: Report Found Page -->
    <rect x="630" y="128" width="180" height="46" rx="6" fill="#f0fdf4" stroke="#16a34a" stroke-width="2" />
    <text x="720" y="148" font-size="10.5" font-weight="bold" fill="#14532d" text-anchor="middle">Report Found Form</text>
    <text x="720" y="163" font-size="8.5" fill="#475569" text-anchor="middle">Loc, Custody / Helpdesk Info</text>

    <!-- Converge to Backend Database & 5-Trait Matching Engine -->
    <line x1="810" y1="15" x2="870" y2="15" stroke="#0f172a" stroke-width="2" />
    <line x1="870" y1="15" x2="870" y2="80" stroke="#0f172a" stroke-width="2" />
    <line x1="810" y1="80" x2="880" y2="80" stroke="#0f172a" stroke-width="2" />
    <line x1="810" y1="150" x2="870" y2="150" stroke="#0f172a" stroke-width="2" />
    <line x1="870" y1="150" x2="870" y2="80" stroke="#0f172a" stroke-width="2" />
    <line x1="870" y1="80" x2="900" y2="80" stroke="#0f172a" stroke-width="2" marker-end="url(#arr)" />

    <!-- Trait Matching Engine -->
    <rect x="900" y="52" width="190" height="56" rx="8" fill="#f1f5f9" stroke="#0f172a" stroke-width="2" stroke-dasharray="4,2" />
    <text x="995" y="72" font-size="10" font-weight="900" text-anchor="middle">5-Trait Similarity Engine</text>
    <text x="995" y="87" font-size="8.5" fill="#475569" text-anchor="middle">Category, Keywords, Color, Loc, Date</text>
    <text x="995" y="100" font-size="8" font-weight="bold" fill="#2563eb" text-anchor="middle">Computes Match Score (0 - 100%)</text>

    <!-- Arrow from Matching Engine to Decision: Match Found? -->
    <line x1="1090" y1="80" x2="1140" y2="80" stroke="#0f172a" stroke-width="2" marker-end="url(#arr)" />

    <!-- Decision: Potential Match? -->
    <polygon points="1200,45 1255,80 1200,115 1145,80" fill="#fef3c7" stroke="#0f172a" stroke-width="2" />
    <text x="1200" y="78" font-size="9" font-weight="900" text-anchor="middle">Match</text>
    <text x="1200" y="90" font-size="9" font-weight="900" text-anchor="middle">&gt; 50%?</text>

    <!-- Match YES -> Alert User -->
    <line x1="1255" y1="80" x2="1320" y2="80" stroke="#16a34a" stroke-width="2" marker-end="url(#arr-green)" />
    <text x="1285" y="73" font-size="9" font-weight="bold" fill="#16a34a">YES</text>

    <rect x="1320" y="58" width="70" height="44" rx="6" fill="#dcfce7" stroke="#16a34a" stroke-width="2" />
    <text x="1355" y="76" font-size="8.5" font-weight="bold" fill="#14532d" text-anchor="middle">In-App</text>
    <text x="1355" y="90" font-size="8.5" font-weight="bold" fill="#14532d" text-anchor="middle">Alert (Bell)</text>

    <!-- Match NO -> Passive Waiting -->
    <line x1="1200" y1="115" x2="1200" y2="160" stroke="#dc2626" stroke-width="2" marker-end="url(#arr-red)" />
    <text x="1208" y="140" font-size="9" font-weight="bold" fill="#dc2626">NO</text>
    <rect x="1135" y="160" width="130" height="35" rx="4" fill="#f8fafc" stroke="#94a3b8" stroke-width="1.5" />
    <text x="1200" y="176" font-size="8.5" font-weight="bold" text-anchor="middle">Listing Active in Feed</text>
    <text x="1200" y="188" font-size="7.5" fill="#64748b" text-anchor="middle">Auto-notifies on future report</text>

    <!-- LEVEL 2: ITEM DETAILS & CLAIM SUBMISSION -->
    <!-- Connect from Explore / Match Alert down to Item Details Page -->
    <line x1="720" y1="104" x2="720" y2="240" stroke="#0f172a" stroke-width="2" marker-end="url(#arr)" />
    <line x1="1355" y1="102" x2="1355" y2="220" stroke="#0f172a" stroke-width="2" />
    <line x1="1355" y1="220" x2="820" y2="220" stroke="#0f172a" stroke-width="2" />
    <line x1="820" y1="220" x2="820" y2="240" stroke="#0f172a" stroke-width="2" marker-end="url(#arr)" />

    <!-- Screen: Item Details Page -->
    <rect x="620" y="240" width="230" height="54" rx="6" fill="#ffffff" stroke="#0f172a" stroke-width="2" />
    <text x="735" y="260" font-size="11" font-weight="900" text-anchor="middle">Item Details Page ( /items/:id )</text>
    <text x="735" y="275" font-size="8.5" fill="#475569" text-anchor="middle">Full details, photo, trait match candidates</text>
    <text x="735" y="287" font-size="8" font-weight="bold" fill="#047857" text-anchor="middle">Button: "Claim This Belonging"</text>

    <!-- Arrow to Authenticated? -->
    <line x1="620" y1="267" x2="550" y2="267" stroke="#0f172a" stroke-width="2" marker-end="url(#arr)" />

    <!-- Decision: Logged in? -->
    <polygon points="480,240 540,267 480,294 420,267" fill="#fef3c7" stroke="#0f172a" stroke-width="2" />
    <text x="480" y="265" font-size="9" font-weight="900" text-anchor="middle">Logged</text>
    <text x="480" y="277" font-size="9" font-weight="900" text-anchor="middle">In?</text>

    <!-- Not logged in -> Login / Register -->
    <line x1="480" y1="240" x2="480" y2="200" stroke="#dc2626" stroke-width="2" marker-end="url(#arr-red)" />
    <text x="488" y="222" font-size="9" font-weight="bold" fill="#dc2626">NO</text>
    <rect x="410" y="165" width="140" height="35" rx="4" fill="#ffffff" stroke="#0f172a" stroke-width="1.5" />
    <text x="480" y="180" font-size="9" font-weight="bold" text-anchor="middle">Sign In / Register</text>
    <text x="480" y="193" font-size="7.5" fill="#475569" text-anchor="middle">Validate @lpu.in email</text>
    <line x1="410" y1="182" x2="360" y2="182" stroke="#0f172a" stroke-width="1.5" />
    <line x1="360" y1="182" x2="360" y2="267" stroke="#0f172a" stroke-width="1.5" />
    <line x1="360" y1="267" x2="420" y2="267" stroke="#0f172a" stroke-width="1.5" marker-end="url(#arr)" />

    <!-- Logged in YES -> Claim Submission Form -->
    <line x1="420" y1="267" x2="310" y2="267" stroke="#16a34a" stroke-width="2" marker-end="url(#arr-green)" />
    <text x="365" y="260" font-size="9" font-weight="bold" fill="#16a34a">YES</text>

    <!-- Screen: Submit Claim Page -->
    <rect x="100" y="240" width="210" height="54" rx="6" fill="#f0fdfa" stroke="#0d9488" stroke-width="2" />
    <text x="205" y="260" font-size="11" font-weight="900" fill="#0f766e" text-anchor="middle">Submit Claim Page</text>
    <text x="205" y="275" font-size="8.5" fill="#475569" text-anchor="middle">Hidden Proof: marks, serial, wallpaper</text>
    <text x="205" y="287" font-size="8" font-weight="bold" fill="#0f172a" text-anchor="middle">Status: PENDING REVIEW</text>

    <!-- LEVEL 3: ADMINISTRATIVE VERIFICATION & HANDOVER -->
    <line x1="205" y1="294" x2="205" y2="370" stroke="#0f172a" stroke-width="2" marker-end="url(#arr)" />

    <!-- Security Admin Workbench -->
    <rect x="90" y="370" width="230" height="60" rx="8" fill="#f8fafc" stroke="#0f172a" stroke-width="2" />
    <text x="205" y="392" font-size="11" font-weight="900" text-anchor="middle">Admin Claim Review ( /admin/claims )</text>
    <text x="205" y="407" font-size="8.5" fill="#475569" text-anchor="middle">Security Officer audits private proof against item</text>
    <text x="205" y="420" font-size="8" font-weight="bold" fill="#2563eb" text-anchor="middle">Enforces role-based backend authorization</text>

    <!-- Arrow to Decision: Proof Valid? -->
    <line x1="320" y1="400" x2="410" y2="400" stroke="#0f172a" stroke-width="2" marker-end="url(#arr)" />

    <!-- Decision: Proof matches? -->
    <polygon points="490,365 570,400 490,435 410,400" fill="#fef3c7" stroke="#0f172a" stroke-width="2" />
    <text x="490" y="397" font-size="9" font-weight="900" text-anchor="middle">Proof</text>
    <text x="490" y="410" font-size="9" font-weight="900" text-anchor="middle">Valid?</text>

    <!-- Proof FALSE -> Reject Claim -->
    <line x1="490" y1="435" x2="490" y2="500" stroke="#dc2626" stroke-width="2" marker-end="url(#arr-red)" />
    <text x="498" y="465" font-size="9" font-weight="bold" fill="#dc2626">NO (Mismatched)</text>
    <rect x="420" y="500" width="140" height="40" rx="4" fill="#fee2e2" stroke="#dc2626" stroke-width="1.5" />
    <text x="490" y="518" font-size="9" font-weight="bold" fill="#991b1b" text-anchor="middle">Claim Rejected</text>
    <text x="490" y="532" font-size="8" fill="#475569" text-anchor="middle">Mandatory reason logged</text>

    <!-- Proof INSUFFICIENT -> Request Info -->
    <line x1="490" y1="365" x2="490" y2="320" stroke="#d97706" stroke-width="2" marker-end="url(#arr)" />
    <text x="498" y="348" font-size="8.5" font-weight="bold" fill="#d97706">Unclear</text>
    <rect x="420" y="285" width="140" height="35" rx="4" fill="#fffbeb" stroke="#d97706" stroke-width="1.5" />
    <text x="490" y="300" font-size="8.5" font-weight="bold" fill="#92400e" text-anchor="middle">Request Additional Proof</text>
    <text x="490" y="312" font-size="7.5" fill="#475569" text-anchor="middle">Student notified to update</text>
    <!-- Loop back arrow -->
    <line x1="420" y1="300" x2="310" y2="300" stroke="#d97706" stroke-width="1.5" stroke-dasharray="3,3" marker-end="url(#arr)" />

    <!-- Proof VALID -> Approve for Handover -->
    <line x1="570" y1="400" x2="660" y2="400" stroke="#16a34a" stroke-width="2" marker-end="url(#arr-green)" />
    <text x="600" y="392" font-size="9" font-weight="bold" fill="#16a34a">YES (Verified)</text>

    <rect x="660" y="375" width="190" height="50" rx="6" fill="#ecfdf5" stroke="#16a34a" stroke-width="2" />
    <text x="755" y="396" font-size="10.5" font-weight="900" fill="#166534" text-anchor="middle">Claim Status: APPROVED</text>
    <text x="755" y="412" font-size="8.5" fill="#15803d" text-anchor="middle">Student instructed to visit Block 34</text>

    <!-- Arrow to In-Person Physical Handover -->
    <line x1="850" y1="400" x2="940" y2="400" stroke="#0f172a" stroke-width="2" marker-end="url(#arr)" />

    <!-- Station: In-Person Physical Handover -->
    <rect x="940" y="370" width="200" height="60" rx="8" fill="#ffffff" stroke="#0f172a" stroke-width="2.5" />
    <text x="1040" y="392" font-size="11" font-weight="900" text-anchor="middle">Physical Handover at Helpdesk</text>
    <text x="1040" y="407" font-size="8.5" fill="#475569" text-anchor="middle">Security verifies physical Student ID card</text>
    <text x="1040" y="420" font-size="8" font-weight="bold" fill="#047857" text-anchor="middle">Admin inputs notes & clicks "Complete"</text>

    <!-- Arrow to Audit Log & Status Update -->
    <line x1="1140" y1="400" x2="1210" y2="400" stroke="#0f172a" stroke-width="2" marker-end="url(#arr)" />

    <!-- Database / Audit System Action -->
    <rect x="1210" y="372" width="170" height="56" rx="6" fill="#f1f5f9" stroke="#0f172a" stroke-width="1.5" />
    <text x="1295" y="392" font-size="9.5" font-weight="bold" text-anchor="middle">System Updates:</text>
    <text x="1295" y="406" font-size="8" fill="#475569" text-anchor="middle">• Item marked "recovered"</text>
    <text x="1295" y="418" font-size="8" fill="#475569" text-anchor="middle">• Immutable Audit Log recorded</text>

    <!-- Down to End Point -->
    <line x1="1295" y1="428" x2="1295" y2="520" stroke="#0f172a" stroke-width="2" marker-end="url(#arr)" />

    <!-- END -->
    <ellipse cx="1295" cy="545" rx="70" ry="25" fill="#0f172a" />
    <text x="1295" y="550" font-size="11" font-weight="900" fill="#ffffff" text-anchor="middle">SUCCESSFUL</text>
    <text x="1295" y="561" font-size="9" fill="#38bdf8" text-anchor="middle">RECOVERY</text>

    <!-- Bottom summary notes box -->
    <rect x="90" y="600" width="1290" height="95" rx="8" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5" />
    <text x="110" y="622" font-size="11" font-weight="900" fill="#0f172a">KEY DESIGN THINKING ATTRIBUTES OF THIS USER FLOW:</text>
    <text x="110" y="642" font-size="9.5" fill="#334155">1. <strong>Privacy Shielding:</strong> Public users NEVER see reporter phone numbers, emails, or identifying serial numbers in the search or details screen.</text>
    <text x="110" y="658" font-size="9.5" fill="#334155">2. <strong>Algorithmic Trait Pairing:</strong> 5-point fuzzy scoring eliminates reliance on exact word-for-word spelling (handles variations like "HP laptop" vs "Hewlett Packard").</text>
    <text x="110" y="674" font-size="9.5" fill="#334155">3. <strong>Admin-Gated Chain of Custody:</strong> Prevents rogue handovers or impersonations. Handovers must be authorized and recorded in SQLite audit logs.</text>
  </svg>
</div>

<div class="pen-tip">
  <span><strong>WORKBOOK DRAWING INSTRUCTIONS:</strong> Use a ruler for vertical and horizontal alignment. Draw ovals for Start/End, diamonds for decisions with clear YES/NO labels, and boxes for screens. Color-code arrows or highlight critical paths with a highlighter.</span>
  <span>Estimated drawing time: <strong>15-18 minutes</strong></span>
</div>

</body>
</html>"""
    out_path = os.path.join(OUTPUT_DIR, "user_flow.png")
    return render_html_to_png(html, out_path, width=1500, height=980)

print("Modules 1 & 2 defined.")

if __name__ == "__main__":
    generate_storyboard()
    generate_user_flow()

