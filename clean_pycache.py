import os
import shutil

deleted = 0

for root, dirs, files in os.walk(".", topdown=False):
    for name in dirs:
        if name == "__pycache__":
            full_path = os.path.join(root, name)
            try:
                shutil.rmtree(full_path)
                print(f"✅ Deleted: {full_path}")
                deleted += 1
            except Exception as e:
                print(f"❌ Error deleting {full_path}: {e}")

if deleted == 0:
    print("🎉 No __pycache__ folders found!")
else:
    print(f"✅ Deleted {deleted} __pycache__ folders.")
