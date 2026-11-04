import os
import shutil
import filecmp

src_root = r'C:\Users\bhuva\OneDrive\Desktop\ReturnLoop\frontend\src'
dst_root = r'C:\Users\bhuva\OneDrive\Desktop\Returlooptesting\frontend\src'

diffs = []
for root, dirs, files in os.walk(src_root):
    rel = os.path.relpath(root, src_root)
    target_dir = os.path.join(dst_root, rel)
    os.makedirs(target_dir, exist_ok=True)
    for f in files:
        src_file = os.path.join(root, f)
        dst_file = os.path.join(target_dir, f)
        if not os.path.exists(dst_file) or not filecmp.cmp(src_file, dst_file, shallow=False):
            shutil.copy2(src_file, dst_file)
            diffs.append(os.path.join(rel, f))

print(f"Successfully synced {len(diffs)} files to Returlooptesting:")
for d in diffs:
    print(f"  + {d}")
