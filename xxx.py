import os
import shutil
import random

# --- CONFIGURATION ---
BASE_DIR = os.getcwd()
SOURCE_IMG_DIR = os.path.join(BASE_DIR, "source_images")
DEST_IMG_DIR = os.path.join(BASE_DIR, "static", "images", "products")
CONTENT_DIR = os.path.join(BASE_DIR, "content", "products")
LAYOUT_DIR = os.path.join(BASE_DIR, "layouts")
DEFAULT_DIR = os.path.join(LAYOUT_DIR, "_default")

STORE_NAME = "MECADO"
PRIMARY_COLOR = "#d04f27" # El Mercado Orange/Red

# --- SMART CATEGORIES ---
def get_details(filename):
    name = filename.lower()
    cat = "Nouveautés"
    if any(x in name for x in ['jus', 'coca', 'soda', 'eau', 'cafe', 'coffee', 'the', 'tea', 'drink', 'boisson']): cat = "Boissons"
    elif any(x in name for x in ['choco', 'bonbon', 'biscuit', 'cookie', 'sucre', 'gateau', 'nutella', 'milka', 'kinder']): cat = "Sucrées"
    elif any(x in name for x in ['chips', 'sale', 'apero', 'cracker', 'pringles', 'doritos']): cat = "Salées"
    elif any(x in name for x in ['pate', 'pasta', 'riz', 'rice', 'huile', 'oil', 'sauce', 'conserve']): cat = "Courses"
    
    # Generate realistic price
    price = random.randint(25, 150)
    # Generate fake "Old Price" for promotion effect
    old_price = int(price * 1.2) 
    
    return cat, price, old_price

def restore_content():
    print("--- 1. Restoring Images & Products ---")
    
    # Clean destinations
    if os.path.exists(CONTENT_DIR): shutil.rmtree(CONTENT_DIR)
    os.makedirs(CONTENT_DIR, exist_ok=True)
    if os.path.exists(DEST_IMG_DIR): shutil.rmtree(DEST_IMG_DIR)
    os.makedirs(DEST_IMG_DIR, exist_ok=True)
    os.makedirs(DEFAULT_DIR, exist_ok=True)

    # Check Source
    if not os.path.exists(SOURCE_IMG_DIR):
        print(f"❌ ERROR: '{SOURCE_IMG_DIR}' not found.")
        return

    files = [f for f in os.listdir(SOURCE_IMG_DIR) if f.lower().endswith(('.jpg', '.png', '.jpeg', '.webp'))]
    
    if not files:
        print("❌ ERROR: No images found. Please add photos to 'source_images'.")
        return

    print(f"✓ Found {len(files)} images. Processing...")

    for i, filename in enumerate(files):
        # Copy Image
        shutil.copy2(os.path.join(SOURCE_IMG_DIR, filename), os.path.join(DEST_IMG_DIR, filename))
        
        # Get Data
        title = filename.rsplit('.', 1)[0].replace('_', ' ').replace('-', ' ').title()
        cat, price, old_price = get_details(filename)
        sku = f"MEC-{i+1000}"
        
        # Create Product Page
        md = f"""---
title: "{title}"
date: 2022-01-01
draft: false
price: "{price}.00"
old_price: "{old_price}.00"
categories: ["{cat}"]
image: "/images/products/{filename}"
sku: "{sku}"
---
Profitez de **{title}** au meilleur prix.
Produit importé authentique, stocké dans nos entrepôts.
Livraison rapide garantie.
"""
        with open(os.path.join(CONTENT_DIR, f"product-{i}.md"), "w", encoding="utf-8") as f:
            f.write(md)
            
    print(f"✅ Restored {len(files)} products.")

def upgrade_design():
    print("--- 2. Upgrading Design Logic ---")
    
    # HEADERS
    head = f"""
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="stylesheet" href="https://cdn.snipcart.com/themes/v3.7.2/default/snipcart.css" />
    <style>
        :root {{ --primary: {PRIMARY_COLOR}; --dark: #222; }}
        body {{ font-family: 'Segoe UI', sans-serif; background: #fff; }}
        a {{ text-decoration: none; }}
        
        /* HEADER */
        .top-bar {{ background: var(--dark); color: white; font-size: 12px; padding: 5px 0; font-weight: bold; }}
        .navbar-brand {{ font-weight: 900; font-size: 28px; color: #000; letter-spacing: -1px; }}
        .navbar-brand span {{ color: var(--primary); }}
        
        /* NAV TABS */
        .nav-pills .nav-link {{ color: #555; font-weight: 700; text-transform: uppercase; font-size: 13px; padding: 10px 20px; border-radius: 30px; margin: 0 5px; }}
        .nav-pills .nav-link.active, .nav-pills .nav-link:hover {{ background-color: var(--primary); color: white; }}
        
        /* PRODUCT CARD */
        .product-card {{ border: 1px solid #eee; transition: 0.3s; height: 100%; position: relative; background: white; }}
        .product-card:hover {{ box-shadow: 0 10px 25px rgba(0,0,0,0.1); border-color: var(--primary); }}
        .badge-save {{ position: absolute; top: 10px; left: 10px; background: var(--primary); color: white; font-size: 11px; font-weight: bold; padding: 4px 8px; border-radius: 4px; }}
        
        .img-wrap {{ position: relative; padding-top: 100%; overflow: hidden; }}
        .img-wrap img {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; object-fit: contain; padding: 20px; transition: transform 0.5s; }}
        .product-card:hover img {{ transform: scale(1.1); }}
        
        .card-body {{ padding: 15px; text-align: center; }}
        .price-new {{ color: var(--primary); font-weight: 800; font-size: 18px; }}
        .price-old {{ text-decoration: line-through; color: #999; font-size: 14px; margin-right: 5px; }}
        
        .btn-add {{ width: 100%; background: white; border: 2px solid var(--dark); color: var(--dark); font-weight: 700; font-size: 12px; padding: 10px; transition: 0.3s; text-transform: uppercase; }}
        .btn-add:hover {{ background: var(--primary); border-color: var(--primary); color: white; }}
        
        /* FOOTER */
        footer {{ background: #111; color: #777; padding: 50px 0; margin-top: 50px; font-size: 13px; }}
        footer h5 {{ color: white; font-weight: 700; margin-bottom: 20px; }}
        footer ul li {{ margin-bottom: 8px; }}
    </style>
    """
    
    scripts = """
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script async src="https://cdn.snipcart.com/themes/v3.7.2/default/snipcart.js"></script>
    <div hidden id="snipcart" data-api-key="OWUxZTM0MzItNjA5MC00YmYxLWE1YmItZmRiMmFmZTRmMzY1NjM3NDc2Njk1Nzc4OTIwNDY0" data-config-modal-style="side"></div>
    """

    # --- HOMEPAGE ---
    index_html = f"""
<!doctype html>
<html lang="fr">
<head><title>{STORE_NAME}</title>{head}</head>
<body>
    <div class="top-bar"><div class="container text-center"><i class="fas fa-truck"></i> LIVRAISON GRATUITE DÈS 300 DH</div></div>
    
    <nav class="navbar navbar-expand-lg bg-white border-bottom sticky-top">
        <div class="container">
            <a class="navbar-brand" href="/">{STORE_NAME}<span>.</span></a>
            <div class="d-flex align-items-center gap-3">
                <div class="input-group d-none d-md-flex" style="width: 300px;">
                    <input type="text" class="form-control" placeholder="Rechercher...">
                    <button class="btn btn-dark"><i class="fas fa-search"></i></button>
                </div>
                <button class="btn btn-outline-dark fw-bold rounded-pill snipcart-checkout">
                    <i class="fas fa-shopping-basket"></i> <span class="snipcart-items-count">0</span>
                </button>
            </div>
        </div>
    </nav>

    {{{{ define "main" }}}}
    
    <div class="container mt-4">
        <div class="p-5 text-white rounded-3 d-flex align-items-center" style="background: linear-gradient(45deg, #111, {PRIMARY_COLOR}); min-height: 300px;">
            <div class="ps-md-5">
                <span class="badge bg-warning text-dark mb-2">NOUVEAU</span>
                <h1 class="display-4 fw-bold">ARRIVAGE EXCLUSIF</h1>
                <p class="lead">Les meilleurs produits importés sont là.</p>
                <a href="#shop" class="btn btn-light fw-bold rounded-pill px-4">ACHETER</a>
            </div>
        </div>
    </div>

    <div class="container mt-5" id="shop">
        <ul class="nav nav-pills justify-content-center mb-4" id="filters">
            <li class="nav-item"><a class="nav-link active" onclick="filter('all')">Tout</a></li>
            <li class="nav-item"><a class="nav-link" onclick="filter('Sucrées')">Sucrées</a></li>
            <li class="nav-item"><a class="nav-link" onclick="filter('Salées')">Salées</a></li>
            <li class="nav-item"><a class="nav-link" onclick="filter('Boissons')">Boissons</a></li>
            <li class="nav-item"><a class="nav-link" onclick="filter('Courses')">Courses</a></li>
            <li class="nav-item"><a class="nav-link text-danger" onclick="filter('Nouveautés')">Nouveautés</a></li>
        </ul>

        <div class="row g-4">
            {{{{ range .Site.RegularPages }}}}
            <div class="col-6 col-md-4 col-lg-3 product-item" data-cat="{{{{ index .Params.categories 0 }}}}">
                <div class="product-card">
                    <span class="badge-save">PROMO</span>
                    <a href="{{{{ .Permalink }}}}" class="img-wrap">
                        <img src="{{{{ .Params.image }}}}" loading="lazy" alt="{{{{ .Title }}}}">
                    </a>
                    <div class="card-body d-flex flex-column">
                        <small class="text-uppercase text-muted fw-bold mb-1" style="font-size:10px;">{{{{ index .Params.categories 0 }}}}</small>
                        <h6 class="fw-bold mb-2 text-dark text-truncate">{{{{ .Title }}}}</h6>
                        <div class="mb-3">
                            <span class="price-old">{{{{ .Params.old_price }}}}</span>
                            <span class="price-new">{{{{ .Params.price }}}} MAD</span>
                        </div>
                        <button class="btn-add mt-auto snipcart-add-item"
                            data-item-id="{{{{ .Params.sku }}}}"
                            data-item-price="{{{{ .Params.price }}}}"
                            data-item-url="{{{{ .Permalink }}}}"
                            data-item-name="{{{{ .Title }}}}"
                            data-item-image="{{{{ .Params.image }}}}"
                            data-item-description="Produit {STORE_NAME}">
                            AJOUTER
                        </button>
                    </div>
                </div>
            </div>
            {{{{ end }}}}
        </div>
    </div>
    {{{{ end }}}}

    <script>
        function filter(cat) {{
            document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
            event.target.classList.add('active');
            document.querySelectorAll('.product-item').forEach(item => {{
                item.style.display = (cat === 'all' || item.dataset.cat === cat) ? 'block' : 'none';
            }});
        }}
    </script>

    <footer class="mt-5">
        <div class="container">
            <div class="row">
                <div class="col-md-4">
                    <h5 class="text-white">{STORE_NAME}.</h5>
                    <p>Votre satisfaction est notre priorité.</p>
                </div>
                <div class="col-md-4">
                    <h5>CONTACT</h5>
                    <ul class="list-unstyled">
                        <li>Casablanca, Maroc</li>
                        <li>+212 600 000 000</li>
                        <li>contact@mecado.ma</li>
                    </ul>
                </div>
                <div class="col-md-4">
                    <h5>PAIEMENT</h5>
                    <div class="fs-2">
                        <i class="fab fa-cc-visa"></i> <i class="fab fa-cc-mastercard"></i> <i class="fas fa-money-bill"></i>
                    </div>
                </div>
            </div>
            <div class="text-center mt-4 pt-4 border-top border-secondary">© 2025 {STORE_NAME}</div>
        </div>
    </footer>
    {scripts}
</body>
</html>
    """

    # --- PRODUCT PAGE ---
    single_html = f"""
<!doctype html>
<html lang="fr">
<head><title>{{{{ .Title }}}}</title>{head}</head>
<body>
    <nav class="navbar bg-white border-bottom sticky-top">
        <div class="container">
            <a href="/" class="fw-bold text-dark"><i class="fas fa-arrow-left"></i> RETOUR</a>
            <button class="btn btn-dark rounded-pill fw-bold snipcart-checkout">
                Panier <span class="snipcart-items-count">0</span>
            </button>
        </div>
    </nav>

    <div class="container py-5">
        <div class="row align-items-center">
            <div class="col-md-6 mb-4 text-center">
                <div class="border rounded p-5 bg-white">
                    <img src="{{{{ .Params.image }}}}" class="img-fluid" style="max-height: 500px;">
                </div>
            </div>
            <div class="col-md-6">
                <span class="badge bg-dark mb-2">{{{{ index .Params.categories 0 }}}}</span>
                <h1 class="display-5 fw-bold mb-3">{{{{ .Title }}}}</h1>
                <div class="mb-3 text-warning"><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i></div>
                
                <div class="d-flex align-items-center mb-4">
                    <span class="text-decoration-line-through text-muted fs-4 me-3">{{{{ .Params.old_price }}}} MAD</span>
                    <span class="display-6 fw-bold" style="color: {PRIMARY_COLOR};">{{{{ .Params.price }}}} MAD</span>
                </div>

                <p class="lead text-muted mb-4">{{{{ .Content }}}}</p>
                
                <div class="d-grid gap-2">
                    <button class="btn btn-lg fw-bold text-white snipcart-add-item" style="background: {PRIMARY_COLOR}; padding: 15px;"
                        data-item-id="{{{{ .Params.sku }}}}"
                        data-item-price="{{{{ .Params.price }}}}"
                        data-item-url="{{{{ .Permalink }}}}"
                        data-item-name="{{{{ .Title }}}}"
                        data-item-image="{{{{ .Params.image }}}}"
                        data-item-description="Produit {STORE_NAME}">
                        AJOUTER AU PANIER
                    </button>
                </div>
                
                <div class="row mt-4 text-center small text-muted">
                    <div class="col"><i class="fas fa-truck fa-2x mb-1"></i><br>24/48H</div>
                    <div class="col"><i class="fas fa-shield-alt fa-2x mb-1"></i><br>Garantie</div>
                    <div class="col"><i class="fas fa-phone fa-2x mb-1"></i><br>Support</div>
                </div>
            </div>
        </div>
    </div>
    {scripts}
</body>
</html>
    """

    with open(os.path.join(LAYOUT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_html)
    with open(os.path.join(DEFAULT_DIR, "single.html"), "w", encoding="utf-8") as f:
        f.write(single_html)

if __name__ == "__main__":
    restore_content()
    upgrade_design()
    print("✅ RESTORATION & UPGRADE COMPLETE.")
    print("1. Run 'hugo' to rebuild.")
    print("2. Commit and Push to GitHub.")