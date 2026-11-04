import os
import shutil
import zipfile

project_dirs = [
    r"c:\Users\bhuva\OneDrive\Desktop\ReturnLoop",
    r"c:\Users\bhuva\OneDrive\Desktop\Returlooptesting"
]

img_laptop_lost = r"C:\Users\bhuva\.gemini\antigravity-ide\brain\f2a4f60e-01fc-4c49-8ef9-15af56ade03b\hp_laptop_lost_dorm_1793181106498.jpg"
img_laptop_found = r"C:\Users\bhuva\.gemini\antigravity-ide\brain\f2a4f60e-01fc-4c49-8ef9-15af56ade03b\hp_laptop_angle_view_1793180912640.jpg"
img_bottle_lost = r"C:\Users\bhuva\.gemini\antigravity-ide\brain\f2a4f60e-01fc-4c49-8ef9-15af56ade03b\milton_bottle_lost_1793181142291.jpg"
img_bottle_found = r"C:\Users\bhuva\.gemini\antigravity-ide\brain\f2a4f60e-01fc-4c49-8ef9-15af56ade03b\bottle_found_unipolis_1793181181576.jpg"
img_wallet = r"c:\Users\bhuva\OneDrive\Desktop\ReturnLoop\backend\uploads\item_wallet_mall.jpg"
img_keys = r"C:\Users\bhuva\.gemini\antigravity-ide\brain\f2a4f60e-01fc-4c49-8ef9-15af56ade03b\campus_keys_walkway_1793180572398.jpg"
img_calc = r"c:\Users\bhuva\OneDrive\Desktop\ReturnLoop\backend\uploads\item_calculator_class.jpg"

final_assets = {
    "01_lost_hp_laptop_open_desk.jpg": img_laptop_lost,
    "02_found_hp_laptop_closed_library.jpg": img_laptop_found,
    "03_lost_milton_thermosteel_bottle.jpg": img_bottle_lost,
    "04_found_black_bottle_unipolis_seats.jpg": img_bottle_found,
    "05_brown_leather_wallet_foodcourt.jpg": img_wallet,
    "06_bike_keys_red_lanyard_walkway.jpg": img_keys,
    "07_casio_scientific_calculator_exam.jpg": img_calc,
}

readme_lines = [
    "=" * 80,
    "RETURNLOOP LPU — ALL OFFICIAL PROJECT ITEM ASSETS (PHOTOREALISTIC AI ASSETS)",
    "=" * 80,
    "",
    "This folder contains all 7 high-resolution, photorealistic item photographs",
    "specifically generated for the ReturnLoop LPU demonstration, test cases, and",
    "college presentation.",
    "",
    "Each item pair (lost vs. found) has distinct, contextual photos matching its",
    "campus location and report background story.",
    "",
    "-" * 80,
    "ASSET CATALOG:",
    "-" * 80,
    "1. 01_lost_hp_laptop_open_desk.jpg",
    "   - Category: Electronics",
    "   - Report: Lost Item #1 [RL-LOST-2026-CC0709]",
    "   - Item: HP Pavilion 15-inch Laptop",
    "   - Scene: Personal photo taken in dorm room; laptop is OPEN on study desk",
    "     showing scenic snow mountain wallpaper, React and Tux Linux stickers,",
    "     earphones, and desk lamp.",
    "",
    "2. 02_found_hp_laptop_closed_library.jpg",
    "   - Category: Electronics",
    "   - Report: Found Item #2 [RL-FND-2026-EF084C]",
    "   - Item: HP Blue Laptop with Tech Stickers",
    "   - Scene: Taken in Central Library 2nd floor reading hall; laptop is CLOSED",
    "     flat at a 3/4 angle on desk 42 with tech stickers, coiled USB-C charger,",
    "     'Stay Curious' blue mug, and Data Structures textbook.",
    "",
    "3. 03_lost_milton_thermosteel_bottle.jpg",
    "   - Category: Bottles & Tumblers",
    "   - Report: Lost Item #3 [RL-LOST-2026-30CCC7]",
    "   - Item: Milton Thermosteel Flask 1000ml (Matte Black)",
    "   - Scene: Taken at student hostel/home study table; flask shows embossed",
    "     'MILTON THERMOSTEEL' text, bright yellow carabiner on cap loop,",
    "     and bottom rim dent next to college backpack and textbooks.",
    "",
    "4. 04_found_black_bottle_unipolis_seats.jpg",
    "   - Category: Bottles & Tumblers",
    "   - Report: Found Item #4 [RL-FND-2026-B9DC57]",
    "   - Item: Black Insulated Water Bottle",
    "   - Scene: Taken inside Baldev Raj Mittal Unipolis; matte black insulated bottle",
    "     left behind on blue theater auditorium seating (Row 8) during rehearsal.",
    "",
    "5. 05_brown_leather_wallet_foodcourt.jpg",
    "   - Category: Bags & Wallets",
    "   - Report: Lost Item #5 [RL-LOST-2026-0E9E55]",
    "   - Item: Brown Leather Bifold Wallet (Wildhorn)",
    "   - Scene: Taken on tiled floor underneath wooden dining chairs at UniMall food court.",
    "",
    "6. 06_bike_keys_red_lanyard_walkway.jpg",
    "   - Category: Keys",
    "   - Report: Found Item #6 [RL-FND-2026-1ADE98]",
    "   - Item: Set of 3 Bike Keys with Red Lanyard & Motorcycle Charm",
    "   - Scene: Taken on red brick academic walkway between campus lawns and buildings.",
    "",
    "7. 07_casio_scientific_calculator_exam.jpg",
    "   - Category: Electronics",
    "   - Report: Lost Item #7 [RL-LOST-2026-930411]",
    "   - Item: Casio FX-991EX ClassWiz Scientific Calculator",
    "   - Scene: Taken in Block 36 examination room on wooden desk with handwritten",
    "     engineering mathematics exam paper and mechanical pencil.",
    "",
    "-" * 80,
    "FILE PATHS ON YOUR MACHINE:",
    "-" * 80,
    "Folder:",
    r"  c:\Users\bhuva\OneDrive\Desktop\Returlooptesting\downloadable_project_images\\",
    r"  c:\Users\bhuva\OneDrive\Desktop\ReturnLoop\downloadable_project_images\\",
    "",
    "Direct Zip Download:",
    r"  c:\Users\bhuva\OneDrive\Desktop\Returlooptesting\downloadable_project_images.zip",
    r"  c:\Users\bhuva\OneDrive\Desktop\ReturnLoop\downloadable_project_images.zip",
    "  Browser link: http://127.0.0.1:5173/downloadable_project_images.zip",
    "=" * 80,
]

for pdir in project_dirs:
    if not os.path.exists(pdir):
        continue
        
    download_dir = os.path.join(pdir, "downloadable_project_images")
    pub_dir = os.path.join(pdir, "frontend", "public")
    pub_img_dir = os.path.join(pub_dir, "project_images")
    
    # Clean and recreate
    if os.path.exists(download_dir):
        shutil.rmtree(download_dir)
    os.makedirs(download_dir, exist_ok=True)
    os.makedirs(pub_img_dir, exist_ok=True)
    
    # Copy all 7 clean assets
    for target_name, src_file in final_assets.items():
        if os.path.exists(src_file):
            shutil.copy2(src_file, os.path.join(download_dir, target_name))
            shutil.copy2(src_file, os.path.join(pub_img_dir, target_name))
            
    # Write README
    readme_path = os.path.join(download_dir, "README.txt")
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write("\n".join(readme_lines))
        
    # Rebuild clean zip
    zip_path = os.path.join(pdir, "downloadable_project_images.zip")
    pub_zip = os.path.join(pub_dir, "downloadable_project_images.zip")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(download_dir):
            for file in files:
                fpath = os.path.join(root, file)
                zf.write(fpath, os.path.relpath(fpath, download_dir))
    if os.path.exists(pub_dir):
        shutil.copy2(zip_path, pub_zip)
        
    print("Cleanly created 7 assets & zip in:", pdir)

print("SUCCESSFULLY PACKAGED ALL 7 ASSETS!")
