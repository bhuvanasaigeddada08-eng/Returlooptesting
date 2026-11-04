import os
import shutil
import sqlite3
import zipfile

new_laptop_lost = r"C:\Users\bhuva\.gemini\antigravity-ide\brain\f2a4f60e-01fc-4c49-8ef9-15af56ade03b\hp_laptop_lost_dorm_1793181106498.jpg"
new_laptop_found = r"C:\Users\bhuva\.gemini\antigravity-ide\brain\f2a4f60e-01fc-4c49-8ef9-15af56ade03b\hp_laptop_angle_view_1793180912640.jpg"
new_bottle_lost = r"C:\Users\bhuva\.gemini\antigravity-ide\brain\f2a4f60e-01fc-4c49-8ef9-15af56ade03b\milton_bottle_lost_1793181142291.jpg"
new_bottle_found = r"C:\Users\bhuva\.gemini\antigravity-ide\brain\f2a4f60e-01fc-4c49-8ef9-15af56ade03b\bottle_found_unipolis_1793181181576.jpg"

project_dirs = [
    r"c:\Users\bhuva\OneDrive\Desktop\ReturnLoop",
    r"c:\Users\bhuva\OneDrive\Desktop\Returlooptesting"
]

for pdir in project_dirs:
    if not os.path.exists(pdir):
        continue
    
    uploads = os.path.join(pdir, "backend", "uploads")
    download_dir = os.path.join(pdir, "downloadable_project_images")
    public_img_dir = os.path.join(pdir, "frontend", "public", "project_images")
    db_path = os.path.join(pdir, "backend", "instance", "returnloop.db")
    
    os.makedirs(uploads, exist_ok=True)
    os.makedirs(download_dir, exist_ok=True)
    os.makedirs(public_img_dir, exist_ok=True)
    
    # Copy distinct files to backend/uploads
    shutil.copy2(new_laptop_lost, os.path.join(uploads, "item_laptop_lost.jpg"))
    shutil.copy2(new_laptop_found, os.path.join(uploads, "item_laptop_library.jpg"))
    shutil.copy2(new_bottle_lost, os.path.join(uploads, "item_bottle_lost.jpg"))
    shutil.copy2(new_bottle_found, os.path.join(uploads, "item_bottle_found.jpg"))
    shutil.copy2(new_bottle_found, os.path.join(uploads, "item_bottle_bench.jpg"))
    
    # Update SQLite database item_images
    if os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("UPDATE item_images SET file_path='/api/uploads/item_laptop_lost.jpg', file_name='item_laptop_lost.jpg' WHERE item_report_id=1")
        cur.execute("UPDATE item_images SET file_path='/api/uploads/item_laptop_library.jpg', file_name='item_laptop_library.jpg' WHERE item_report_id=2")
        cur.execute("UPDATE item_images SET file_path='/api/uploads/item_bottle_lost.jpg', file_name='item_bottle_lost.jpg' WHERE item_report_id=3")
        cur.execute("UPDATE item_images SET file_path='/api/uploads/item_bottle_found.jpg', file_name='item_bottle_found.jpg' WHERE item_report_id=4")
        conn.commit()
        
        # Verify update
        print("Updated DB rows for", pdir)
        for row in cur.execute("SELECT item_report_id, file_path, file_name FROM item_images WHERE item_report_id IN (1,2,3,4)"):
            print(" ", row)
        conn.close()
        
    # Copy all distinct assets to downloadable_project_images with clear filenames
    catalog = {
        "01_lost_hp_laptop_student_desk.jpg": new_laptop_lost,
        "02_found_hp_laptop_library_desk.jpg": new_laptop_found,
        "03_lost_milton_thermosteel_bottle.jpg": new_bottle_lost,
        "04_found_black_bottle_unipolis_seats.jpg": new_bottle_found,
        "05_casio_scientific_calculator.jpg": os.path.join(uploads, "item_calculator_class.jpg"),
        "06_bike_keys_red_lanyard.jpg": os.path.join(uploads, "item_keys_walkway.jpg"),
        "07_brown_leather_wallet.jpg": os.path.join(uploads, "item_wallet_mall.jpg"),
    }
    
    for fname, src in catalog.items():
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(download_dir, fname))
            shutil.copy2(src, os.path.join(public_img_dir, fname))
            
    # Create updated zip
    zip_path = os.path.join(pdir, "downloadable_project_images.zip")
    pub_zip = os.path.join(pdir, "frontend", "public", "downloadable_project_images.zip")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(download_dir):
            for file in files:
                fpath = os.path.join(root, file)
                zf.write(fpath, os.path.relpath(fpath, download_dir))
    if os.path.exists(os.path.dirname(pub_zip)):
        shutil.copy2(zip_path, pub_zip)
        
    print(f"Finished updating assets in {pdir}")

print("ALL ASSETS & DATABASES FULLY SYNCHRONIZED!")
