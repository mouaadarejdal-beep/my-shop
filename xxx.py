import os
import shutil
import random
import datetime

# --- 0. MASTER CONFIGURATION (The "Brain") ---
STORE_NAME = "MECADO"
BASE_URL = "/"  # Relative URL for Netlify safety
PRIMARY_COLOR = "#d04f27" # El Mercado Orange
SECONDARY_COLOR = "#222"
SNIPCART_KEY = "OWUxZTM0MzItNjA5MC00YmYxLWE1YmItZmRiMmFmZTRmMzY1NjM3NDc2Njk1Nzc4OTIwNDY0"
WHATSAPP_NUMBER = "212600000000" # Replace with yours

# Paths
BASE_DIR = os.getcwd()
SOURCE_IMG_DIR = os.path.join(BASE_DIR, "source_images")
CONTENT_DIR = os.path.join(BASE_DIR, "content", "products")
LAYOUT_DIR = os.path.join(BASE_DIR, "layouts")
DEFAULT_DIR = os.path.join(LAYOUT_DIR, "_default")
STATIC_CSS_DIR = os.path.join(BASE_DIR, "static", "css")
STATIC_JS_DIR = os.path.join(BASE_DIR, "static", "js")

# --- 1. SEO & ANALYTICS SETUP (P2) ---
def setup_config():
    print("--- 1. Configuring SEO & Analytics (P2) ---")
    config_path = os.path.join(BASE_DIR, "hugo.toml")
    with open(config_path, "w", encoding="utf-8") as f:
        f.write(f"""
baseURL = '{BASE_URL}'
languageCode = 'fr-fr'
title = '{STORE_NAME}'
theme = []
relativeURLs = true

[params]
  description = "Le meilleur de l'épicerie fine et des produits importés au Maroc."
  author = "{STORE_NAME}"
  # SEO Images
  og_image = "/images/og-default.jpg"
  
  # Analytics placeholders (P2)
  google_analytics_id = "G-XXXXXXXXXX" 
  pixel_id = "123456789"
""")

# --- 2. PRODUCT DATABASE GENERATION (P0) ---
def generate_products():
    print("--- 2. Building Product Database (P0) ---")
    
    if os.path.exists(CONTENT_DIR): shutil.rmtree(CONTENT_DIR)
    os.makedirs(CONTENT_DIR, exist_ok=True)
    
    # Destination for images
    dest_img_path = os.path.join(BASE_DIR, "static", "images", "products")
    if os.path.exists(dest_img_path): shutil.rmtree(dest_img_path)
    os.makedirs(dest_img_path, exist_ok=True)

    files = [f for f in os.listdir(SOURCE_IMG_DIR) if f.lower().endswith(('.jpg', '.png', '.jpeg', '.webp'))]
    
    if not files:
        print("❌ ERROR: No images in 'source_images'. Please add them!")
        return

    categories = ["Sucrées", "Salées", "Boissons", "Courses", "Nouveautés"]
    
    for i, filename in enumerate(files):
        shutil.copy2(os.path.join(SOURCE_IMG_DIR, filename), os.path.join(dest_img_path, filename))
        
        title = filename.rsplit('.', 1)[0].replace('_', ' ').replace('-', ' ').title()
        price = random.randint(30, 200)
        old_price = int(price * 1.2)
        cat = random.choice(categories)
        sku = f"MEC-{1000+i}"
        
        # Extended P0 Data: Ingredients, Allergens
        md = f"""---
title: "{title}"
date: 2023-01-01
draft: false
price: "{price}.00"
old_price: "{old_price}.00"
categories: ["{cat}"]
image: "/images/products/{filename}"
sku: "{sku}"
rating: 5
stock: {random.randint(5,50)}
ingredients: "Sucre, Farine de blé, Huile de palme, Cacao."
allergens: "Gluten, Soja, Lait."
---
Profitez de **{title}**, un produit authentique importé.
Idéal pour vos pauses gourmandes ou vos besoins quotidiens.
"""
        with open(os.path.join(CONTENT_DIR, f"product-{i}.md"), "w", encoding="utf-8") as f:
            f.write(md)
            
    print(f"✓ Generated {len(files)} rich product pages.")

# --- 3. STYLES & UI SYSTEM (P1) ---
def create_styles():
    print("--- 3. Creating Trust UI & Design System (P1) ---")
    os.makedirs(STATIC_CSS_DIR, exist_ok=True)
    
    css = f"""
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&family=Exo:wght@600;800&display=swap');
    
    :root {{ --primary: {PRIMARY_COLOR}; --dark: {SECONDARY_COLOR}; --light: #f8f9fa; }}
    
    body {{ font-family: 'Inter', sans-serif; background: #fff; color: #333; }}
    h1, h2, h3, h4, .btn, .nav-link {{ font-family: 'Exo', sans-serif; text-transform: uppercase; }}
    
    /* TRUST BAR */
    .top-bar {{ background: var(--dark); color: white; font-size: 11px; padding: 8px 0; font-weight: 600; letter-spacing: 0.5px; }}
    
    /* HEADER */
    .site-header {{ padding: 20px 0; border-bottom: 1px solid #eee; background: white; }}
    .logo {{ font-size: 28px; font-weight: 800; color: #000; text-decoration: none; }}
    .logo span {{ color: var(--primary); }}
    
    /* NAVIGATION */
    .main-nav {{ border-bottom: 2px solid #f0f0f0; background: white; }}
    .nav-link {{ color: #444 !important; font-weight: 700; font-size: 13px; padding: 15px !important; }}
    .nav-link:hover, .nav-link.active {{ color: var(--primary) !important; }}
    
    /* PRODUCT CARD (P1 Redesign) */
    .product-card {{ 
        border: 1px solid #eee; transition: 0.3s; background: white; height: 100%; position: relative; 
        border-radius: 8px; overflow: hidden;
    }}
    .product-card:hover {{ border-color: var(--primary); box-shadow: 0 10px 20px rgba(0,0,0,0.05); transform: translateY(-3px); }}
    
    .badge-save {{ position: absolute; top: 10px; left: 10px; background: var(--primary); color: white; font-size: 10px; padding: 4px 8px; font-weight: bold; border-radius: 4px; }}
    
    .card-img-wrap {{ position: relative; padding-top: 100%; display: block; overflow: hidden; }}
    .card-img-wrap img {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; object-fit: contain; padding: 20px; transition: 0.5s; }}
    .product-card:hover img {{ transform: scale(1.05); }}
    
    .btn-add {{ width: 100%; background: white; border: 1px solid #333; color: #333; font-weight: 700; padding: 10px; margin-top: 10px; font-size: 12px; transition: 0.2s; }}
    .btn-add:hover {{ background: var(--primary); border-color: var(--primary); color: white; }}
    
    /* CART DRAWER (P0) */
    .snipcart-modal__container {{ z-index: 9999; }}
    """
    with open(os.path.join(STATIC_CSS_DIR, "style.css"), "w", encoding="utf-8") as f:
        f.write(css)

# --- 4. LAYOUTS & LOGIC (The Core) ---
def create_layouts():
    print("--- 4. Building Templates & Logic (P0, P1) ---")
    os.makedirs(DEFAULT_DIR, exist_ok=True)
    os.makedirs(LAYOUT_DIR, exist_ok=True)
    
    # GLOBAL HEAD (SEO + Analytics + Scripts)
    head_html = f"""
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>{{{{ if .IsHome }}}}{STORE_NAME} | Boutique{{{{ else }}}}{{{{ .Title }}}}- {STORE_NAME}{{{{ end }}}}</title>
        <meta name="description" content="{{{{ .Params.description | default .Site.Params.description }}}}">
        
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <link rel="stylesheet" href="/css/style.css">
        <link rel="stylesheet" href="https://cdn.snipcart.com/themes/v3.7.2/default/snipcart.css" />
        
        </head>
    """

    # GLOBAL SCRIPTS (Snipcart + Logic)
    scripts_html = f"""
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script async src="https://cdn.snipcart.com/themes/v3.7.2/default/snipcart.js"></script>
    <div hidden id="snipcart" data-api-key="{SNIPCART_KEY}" data-config-modal-style="side" data-currency="mad"></div>
    
    <script>
        function searchProducts() {{
            let input = document.getElementById('searchInput').value.toLowerCase();
            let items = document.querySelectorAll('.product-item');
            
            items.forEach(item => {{
                let title = item.querySelector('.card-title').innerText.toLowerCase();
                if (title.includes(input)) {{
                    item.style.display = "block";
                }} else {{
                    item.style.display = "none";
                }}
            }});
        }}
    </script>
    """

    # --- HOMEPAGE (P1: Filters, Search, Trust) ---
    index_html = f"""
<!doctype html>
<html lang="fr">
{head_html}
<body>

    <div class="top-bar">
        <div class="container d-flex justify-content-between">
            <span><i class="fas fa-shipping-fast text-warning"></i> Livraison Gratuite dès 300 DH</span>
            <span><i class="fab fa-whatsapp text-success"></i> +212 600 000 000</span>
        </div>
    </div>

    <header class="site-header sticky-top">
        <div class="container">
            <div class="row align-items-center">
                <div class="col-4 col-md-3">
                    <a href="/" class="logo">{STORE_NAME}<span>.</span></a>
                </div>
                <div class="col-md-6 d-none d-md-block">
                    <div class="input-group">
                        <input type="text" id="searchInput" class="form-control rounded-0" placeholder="Rechercher un produit..." onkeyup="searchProducts()">
                        <button class="btn btn-dark rounded-0"><i class="fas fa-search"></i></button>
                    </div>
                </div>
                <div class="col-8 col-md-3 text-end">
                    <button class="btn btn-outline-dark rounded-0 fw-bold snipcart-checkout">
                        <i class="fas fa-shopping-basket"></i> PANIER <span class="badge bg-danger rounded-pill snipcart-items-count">0</span>
                    </button>
                </div>
            </div>
        </div>
    </header>

    <div class="main-nav d-none d-lg-block">
        <div class="container">
            <ul class="nav justify-content-center">
                <li class="nav-item"><a class="nav-link active" href="#" onclick="filter('all')">TOUT</a></li>
                <li class="nav-item"><a class="nav-link" href="#" onclick="filter('Sucrées')">SUCRÉES</a></li>
                <li class="nav-item"><a class="nav-link" href="#" onclick="filter('Salées')">SALÉES</a></li>
                <li class="nav-item"><a class="nav-link" href="#" onclick="filter('Boissons')">BOISSONS</a></li>
                <li class="nav-item"><a class="nav-link text-danger" href="#" onclick="filter('Nouveautés')">PROMOS</a></li>
            </ul>
        </div>
    </div>

    {{{{ define "main" }}}}
    <div class="container mt-4 mb-5">
        <div class="p-5 text-white rounded-0" style="background: linear-gradient(45deg, #111, {PRIMARY_COLOR});">
            <h1 class="display-4 fw-bold">ARRIVAGE EXCLUSIF</h1>
            <p class="lead">Les produits que vous ne trouverez nulle part ailleurs.</p>
            <a href="#shop" class="btn btn-light rounded-0 fw-bold px-4 mt-2">COMMANDER</a>
        </div>
    </div>

    <div class="container mb-5" id="shop">
        <h3 class="fw-bold mb-4 border-bottom pb-2">NOS PRODUITS</h3>
        <div class="row g-3">
            {{{{ range .Site.RegularPages }}}}
            <div class="col-6 col-md-3 product-item" data-cat="{{{{ index .Params.categories 0 }}}}">
                <div class="product-card">
                    <span class="badge-save">-20%</span>
                    <a href="{{{{ .Permalink }}}}" class="card-img-wrap">
                        <img src="{{{{ .Params.image }}}}" loading="lazy" alt="{{{{ .Title }}}}">
                    </a>
                    <div class="p-3 text-center d-flex flex-column flex-grow-1">
                        <small class="text-muted text-uppercase" style="font-size:10px">{{{{ index .Params.categories 0 }}}}</small>
                        <h6 class="card-title my-2 fw-bold text-dark">{{{{ .Title }}}}</h6>
                        
                        <div class="mb-2">
                            <span class="text-decoration-line-through text-muted small">{{{{ .Params.old_price }}}} DH</span>
                            <span class="text-danger fw-bold fs-5">{{{{ .Params.price }}}} DH</span>
                        </div>

                        <div class="mt-auto">
                            <a href="{{{{ .Permalink }}}}" class="btn btn-sm btn-light w-100 mb-1 rounded-0 border">Voir Détails</a>
                            <button class="btn-add rounded-0 snipcart-add-item"
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
            </div>
            {{{{ end }}}}
        </div>
    </div>
    {{{{ end }}}}

    <footer class="bg-dark text-white pt-5 pb-3">
        <div class="container">
            <div class="row g-4">
                <div class="col-md-4">
                    <h5>{STORE_NAME}.</h5>
                    <p class="small text-white-50">Votre épicerie de confiance. Produits importés, stock frais, livraison rapide.</p>
                </div>
                <div class="col-md-4">
                    <h5>LIENS UTILES</h5>
                    <ul class="list-unstyled small text-white-50">
                        <li><a href="#" class="text-white">Contact</a></li>
                        <li><a href="#" class="text-white">Livraison & Retours</a></li>
                        <li><a href="#" class="text-white">Conditions Générales</a></li>
                    </ul>
                </div>
                <div class="col-md-4">
                    <h5>PAIEMENT</h5>
                    <div class="fs-2 text-white-50">
                        <i class="fab fa-cc-visa"></i> <i class="fab fa-cc-mastercard"></i> <i class="fas fa-money-bill"></i>
                    </div>
                </div>
            </div>
            <div class="text-center border-top border-secondary mt-4 pt-3 small">© 2025 {STORE_NAME}.</div>
        </div>
    </footer>

    <script>
        function filter(cat) {{
            document.querySelectorAll('.product-item').forEach(item => {{
                item.style.display = (cat === 'all' || item.dataset.cat === cat) ? 'block' : 'none';
            }});
        }}
    </script>

    {scripts_html}
</body>
</html>
    """

    # --- PRODUCT PAGE (P0: Detail View) ---
    single_html = f"""
<!doctype html>
<html lang="fr">
{head_html}
<body style="background: #fff;">

    <nav class="navbar border-bottom sticky-top bg-white">
        <div class="container">
            <a href="/" class="fw-bold text-dark text-decoration-none"><i class="fas fa-arrow-left"></i> RETOUR</a>
            <button class="btn btn-dark rounded-0 snipcart-checkout">
                <i class="fas fa-shopping-basket"></i> <span class="snipcart-items-count">0</span>
            </button>
        </div>
    </nav>

    <div class="container py-5">
        <div class="row gx-5">
            <div class="col-md-6 mb-4">
                <div class="border p-5 text-center bg-white">
                    <img src="{{{{ .Params.image }}}}" class="img-fluid" style="max-height: 500px;">
                </div>
            </div>

            <div class="col-md-6">
                <span class="badge bg-secondary mb-2">{{{{ index .Params.categories 0 }}}}</span>
                <h1 class="fw-bold mb-3">{{{{ .Title }}}}</h1>
                
                <div class="mb-3 text-warning">
                    <i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i>
                    <span class="text-muted small text-dark ms-2">(Avis Clients)</span>
                </div>

                <div class="h2 text-danger fw-bold mb-4">{{{{ .Params.price }}}} MAD</div>
                
                <p class="text-muted mb-4">{{{{ .Content }}}}</p>

                <ul class="nav nav-tabs mb-3" id="myTab">
                    <li class="nav-item"><button class="nav-link active" data-bs-toggle="tab" data-bs-target="#desc">Description</button></li>
                    <li class="nav-item"><button class="nav-link" data-bs-toggle="tab" data-bs-target="#ingr">Ingrédients</button></li>
                </ul>
                <div class="tab-content mb-4 p-3 border border-top-0">
                    <div class="tab-pane fade show active" id="desc">
                        Produit authentique. Importé directement pour garantir la meilleure qualité.
                    </div>
                    <div class="tab-pane fade" id="ingr">
                        {{{{ .Params.ingredients }}}} <br><strong>Allergènes:</strong> {{{{ .Params.allergens }}}}
                    </div>
                </div>

                <div class="d-grid gap-2">
                    <button class="btn btn-danger btn-lg rounded-0 fw-bold snipcart-add-item"
                        data-item-id="{{{{ .Params.sku }}}}"
                        data-item-price="{{{{ .Params.price }}}}"
                        data-item-url="{{{{ .Permalink }}}}"
                        data-item-name="{{{{ .Title }}}}"
                        data-item-image="{{{{ .Params.image }}}}"
                        data-item-description="Produit {STORE_NAME}">
                        AJOUTER AU PANIER
                    </button>
                    
                    <a href="https://wa.me/{WHATSAPP_NUMBER}?text=Bonjour, je veux commander: {{{{ .Title }}}}" target="_blank" class="btn btn-success rounded-0 fw-bold">
                        <i class="fab fa-whatsapp"></i> COMMANDER SUR WHATSAPP
                    </a>
                </div>

                <div class="mt-4 small text-muted">
                    <div class="d-flex align-items-center mb-2"><i class="fas fa-truck me-2"></i> Livraison 24h/48h</div>
                    <div class="d-flex align-items-center"><i class="fas fa-lock me-2"></i> Paiement à la livraison</div>
                </div>
            </div>
        </div>
    </div>

    {scripts_html}
</body>
</html>
    """

    with open(os.path.join(LAYOUT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_html)
    with open(os.path.join(DEFAULT_DIR, "single.html"), "w", encoding="utf-8") as f:
        f.write(single_html)

if __name__ == "__main__":
    setup_config()
    generate_products()
    create_styles()
    create_layouts()
    print("\n✅ HERO BUILD COMPLETE.")
    print("1. Run 'hugo'")
    print("2. Commit & Push to GitHub.")