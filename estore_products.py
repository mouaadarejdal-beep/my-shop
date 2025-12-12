import os
import shutil
import random

# --- CONFIGURATION ---
BASE_DIR = os.getcwd()
SOURCE_IMG_DIR = os.path.join(BASE_DIR, "source_images")
DEST_IMG_DIR = os.path.join(BASE_DIR, "static", "images", "products")
CONTENT_DIR = os.path.join(BASE_DIR, "content", "products")

# --- CATEGORY LOGIC (To sort your 20 products) ---
def get_category(filename):
    name = filename.lower()
    if any(x in name for x in ['jus', 'coca', 'soda', 'eau', 'cafe', 'coffee', 'the', 'tea', 'drink', 'boisson', 'nescafe', 'starbucks']): return "Boissons"
    if any(x in name for x in ['choco', 'bonbon', 'biscuit', 'cookie', 'sucre', 'gateau', 'nutella', 'milka', 'kinder', 'oreo', 'twix']): return "Sucrées"
    if any(x in name for x in ['chips', 'sale', 'apero', 'cracker', 'pringles', 'doritos', 'nuts']): return "Salées"
    if any(x in name for x in ['pate', 'pasta', 'riz', 'rice', 'huile', 'oil', 'sauce', 'conserve', 'thon']): return "Courses"
    return "Nouveautés"

def restore_products():
    print("--- RESTORING PRODUCTS FROM SOURCE IMAGES ---")
    
    # 1. Check Source
    if not os.path.exists(SOURCE_IMG_DIR):
        print(f"❌ ERROR: Could not find '{SOURCE_IMG_DIR}'. Did you delete the source folder?")
        return

    files = [f for f in os.listdir(SOURCE_IMG_DIR) if f.lower().endswith(('.jpg', '.png', '.jpeg', '.webp'))]
    
    if not files:
        print("❌ ERROR: 'source_images' folder is empty. Please put your photos back in there.")
        return

    # 2. Reset Content Folders
    if os.path.exists(CONTENT_DIR): shutil.rmtree(CONTENT_DIR)
    os.makedirs(CONTENT_DIR, exist_ok=True)
    
    if os.path.exists(DEST_IMG_DIR): shutil.rmtree(DEST_IMG_DIR)
    os.makedirs(DEST_IMG_DIR, exist_ok=True)

    # 3. Generate Products
    print(f"Processing {len(files)} images...")
    
    for i, filename in enumerate(files):
        # Clean Title
        title = filename.rsplit('.', 1)[0].replace('_', ' ').replace('-', ' ').title()
        
        # Copy Image
        shutil.copy2(os.path.join(SOURCE_IMG_DIR, filename), os.path.join(DEST_IMG_DIR, filename))
        
        # Generate Data
        price = random.randint(30, 250)
        category = get_category(filename)
        sku = f"MEC-{random.randint(10000, 99999)}"
        
        # Write Markdown
        md = f"""---
title: "{title}"
date: 2022-01-01
draft: false
price: "{price}.00"
categories: ["{category}"]
image: "/images/products/{filename}"
sku: "{sku}"
---
Découvrez **{title}**, un produit de qualité sélectionné pour vous.
Disponible immédiatement en stock.
"""
        with open(os.path.join(CONTENT_DIR, f"product-{i}.md"), "w", encoding="utf-8") as f:
            f.write(md)
            
    print(f"✅ SUCCESS: {len(files)} products restored.")
    print("Run 'hugo' and upload to Netlify to see them in the new design.")

if __name__ == "__main__":
    restore_products()