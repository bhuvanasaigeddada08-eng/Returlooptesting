from playwright.sync_api import sync_playwright
import os

pdf_path = r"C:\Users\bhuva\.gemini\antigravity\brain\f2a4f60e-01fc-4c49-8ef9-15af56ade03b\.user_uploaded\media_1794302508023_f4eb45cc.pdf"
out_img = r"C:\Users\bhuva\OneDrive\Desktop\ReturnLoop\scripts\consent_form_template.png"

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1200, "height": 1700})
    page.goto(f"file:///{pdf_path.replace(os.sep, '/')}")
    page.wait_for_timeout(2000)
    page.screenshot(path=out_img)
    browser.close()
    print("Screenshot saved to", out_img)
