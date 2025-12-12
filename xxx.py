import os
import shutil
import random
import json

# ==========================================
#   MECADO HERO BUILDER - V1.0
# ==========================================

# --- CONFIGURATION ---
BASE_DIR = os.getcwd()
SOURCE_IMG_DIR = os.path.join(BASE_DIR, "source_images")
DEST_IMG_DIR = os.path.join(BASE_DIR, "static", "images", "products")
CONTENT_DIR = os.path.join(BASE_DIR, "content", "products")
LAYOUT_DIR = os.path.join(BASE_DIR, "layouts")
DEFAULT_DIR = os.path.join(LAYOUT_DIR, "_default")
STATIC_CSS_DIR = os.path.join(BASE_DIR, "static", "css")
STATIC_JS_DIR = os.path.join(BASE_DIR, "static", "js")

# STORE CONFIG
STORE_NAME = "MECADO"
PHONE_NUMBER = "212600000000" # For WhatsApp Integration
PRIMARY_COLOR = "#d04f27" # El Mercado Orange
SNIPCART_KEY = "OWUxZTM0MzItNjA5MC00YmYxLWE1YmItZmRiMmFmZTRmMzY1NjM3NDc2Njk1Nzc4OTIwNDY0"

# --- HELPER FUNCTIONS ---

def setup_dirs():
    print("--- 1. INITIALIZING PROJECT STRUCTURE ---")
    dirs = [CONTENT_DIR, DEST_IMG_DIR, DEFAULT_DIR, STATIC_CSS_DIR, STATIC_JS_DIR]
    for d in dirs:
        if os.path.exists(d): shutil.rmtree(d)
        os.makedirs(d, exist_ok=True)

def generate_hugo_config():
    print("--- 2. CONFIGURING SEO & SETTINGS ---")
    config = f"""
baseURL = '/'
languageCode = 'fr-fr'
title = '{STORE_NAME}'
theme = []
enableRobotsTXT = true

[params]
  description = "MECADO - Votre épicerie fine en ligne au Maroc."
  currency = "MAD"
  phone = "{PHONE_NUMBER}"
  free_shipping_threshold = 300

[outputs]
  home = ["HTML", "JSON"] # For Search functionality
"""
    with open(os.path.join(BASE_DIR, "hugo.toml"), "w", encoding="utf-8") as f:
        f.write(config)

def process_products():
    print("--- 3. GENERATING SMART PRODUCT DATA ---")
    
    if not os.path.exists(SOURCE_IMG_DIR):
        os.makedirs(SOURCE_IMG_DIR)
        print(f"❌ ERROR: '{SOURCE_IMG_DIR}' is missing. Please add photos!")
        return

    files = [f for f in os.listdir(SOURCE_IMG_DIR) if f.lower().endswith(('.jpg', '.png', '.webp', '.jpeg'))]
    
    categories_map = {
        "Boissons": ['jus', 'coca', 'soda', 'eau', 'cafe', 'the', 'drink'],
        "Sucrées": ['choco', 'bonbon', 'biscuit', 'cookie', 'nutella', 'milka'],
        "Salées": ['chips', 'sale', 'apero', 'cracker', 'pringles'],
        "Courses": ['pate', 'riz', 'huile', 'sauce', 'conserve'],
        "Nouveautés": []
    }

    for i, filename in enumerate(files):
        # 1. Image Logic
        shutil.copy2(os.path.join(SOURCE_IMG_DIR, filename), os.path.join(DEST_IMG_DIR, filename))
        
        # 2. Metadata Logic
        title = filename.rsplit('.', 1)[0].replace('_', ' ').replace('-', ' ').title()
        
        # Smart Categorization
        category = "Nouveautés"
        name_lower = filename.lower()
        for cat, keywords in categories_map.items():
            if any(k in name_lower for k in keywords):
                category = cat
                break
        
        price = random.randint(30, 200)
        old_price = int(price * 1.25)
        stock = random.randint(0, 20)
        sku = f"MEC-{1000+i}"
        
        # 3. Advanced Frontmatter (SEO + Data)
        md = f"""---
title: "{title}"
date: 2023-01-01
draft: false
price: "{price}.00"
old_price: "{old_price}.00"
categories: ["{category}"]
image: "/images/products/{filename}"
sku: "{sku}"
stock: {stock}
ingredients: "Sucre, Farine de blé, Huile de palme, Cacao magre, Amidon de blé."
allergens: "Peut contenir: Lait, Soja, Fruits à coque."
weight: "250g"
tags: ["Importé", "Premium", "{category}"]
---
{title} est un produit phare de notre catalogue **{category}**.
Commandez dès maintenant et profitez d'une livraison rapide partout au Maroc.
"""
        with open(os.path.join(CONTENT_DIR, f"product-{i}.md"), "w", encoding="utf-8") as f:
            f.write(md)
            
    print(f"✓ Processed {len(files)} products with rich data.")

def create_advanced_css():
    print("--- 4. WRITING CSS (GLASSMORPHISM + UI KIT) ---")
    css = f"""
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap');
    
    :root {{ 
        --primary: {PRIMARY_COLOR}; --dark: #1e293b; --light: #f1f5f9; --white: #ffffff;
        --success: #10b981; --warning: #f59e0b;
    }}
    
    body {{ font-family: 'Plus Jakarta Sans', sans-serif; background: #f8fafc; color: #334155; }}
    a {{ text-decoration: none; color: inherit; transition: 0.2s; }}
    
    /* UTILS */
    .fw-900 {{ font-weight: 900; }}
    .text-primary {{ color: var(--primary) !important; }}
    .bg-primary {{ background-color: var(--primary) !important; }}
    .shadow-hover:hover {{ transform: translateY(-5px); box-shadow: 0 20px 40px -5px rgba(0,0,0,0.1); }}
    
    /* NAV */
    .top-bar {{ background: var(--dark); color: white; font-size: 12px; padding: 8px 0; }}
    .navbar {{ background: rgba(255,255,255,0.9); backdrop-filter: blur(12px); border-bottom: 1px solid #e2e8f0; padding: 15px 0; }}
    
    /* PRODUCT CARD (Redesigned) */
    .product-card {{ background: white; border-radius: 16px; overflow: hidden; border: 1px solid #e2e8f0; height: 100%; display: flex; flex-direction: column; }}
    .card-img-container {{ position: relative; padding-top: 100%; overflow: hidden; }}
    .card-img-container img {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; object-fit: contain; padding: 25px; transition: 0.4s; }}
    .product-card:hover img {{ transform: scale(1.1); }}
    
    .badge-discount {{ position: absolute; top: 12px; left: 12px; background: #ef4444; color: white; font-weight: 800; font-size: 11px; padding: 4px 8px; border-radius: 6px; }}
    
    .card-content {{ padding: 20px; flex-grow: 1; display: flex; flex-direction: column; }}
    .card-title {{ font-weight: 700; color: var(--dark); margin-bottom: 5px; line-height: 1.4; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }}
    .card-price {{ font-size: 18px; font-weight: 800; color: var(--primary); }}
    .card-price del {{ color: #94a3b8; font-size: 14px; font-weight: 500; margin-right: 8px; }}
    
    .btn-add {{ width: 100%; background: var(--dark); color: white; font-weight: 700; padding: 12px; border-radius: 10px; border: none; margin-top: auto; display: flex; justify-content: center; align-items: center; gap: 8px; }}
    .btn-add:hover {{ background: var(--primary); }}
    
    /* FILTERS & SEARCH */
    .filter-bar {{ background: white; padding: 20px 0; margin-bottom: 30px; border-bottom: 1px solid #e2e8f0; }}
    .search-input {{ background: var(--light); border: 1px solid #cbd5e1; border-radius: 50px; padding: 12px 25px; width: 100%; }}
    .filter-chip {{ background: white; border: 1px solid #cbd5e1; padding: 8px 20px; border-radius: 50px; font-size: 13px; font-weight: 600; cursor: pointer; white-space: nowrap; }}
    .filter-chip.active {{ background: var(--dark); color: white; border-color: var(--dark); }}
    
    /* PRODUCT PAGE (P0 Requirement) */
    .pdp-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 60px; margin-top: 40px; }}
    .pdp-gallery {{ background: white; border-radius: 20px; border: 1px solid #e2e8f0; padding: 40px; text-align: center; }}
    .pdp-gallery img {{ max-height: 500px; width: 100%; object-fit: contain; }}
    
    .pdp-info h1 {{ font-size: 36px; font-weight: 800; color: var(--dark); line-height: 1.2; margin-bottom: 20px; }}
    .pdp-meta {{ display: flex; gap: 15px; margin-bottom: 30px; font-size: 14px; color: #64748b; }}
    .trust-box {{ background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; padding: 20px; display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 40px; }}
    
    /* PROGRESS BAR */
    .shipping-progress {{ background: var(--light); height: 8px; border-radius: 4px; overflow: hidden; margin: 10px 0; }}
    .progress-fill {{ background: var(--success); height: 100%; width: 0%; transition: 1s; }}
    
    @media(max-width: 768px) {{ .pdp-grid {{ grid-template-columns: 1fr; }} }}
    """
    with open(os.path.join(STATIC_CSS_DIR, "main.css"), "w", encoding="utf-8") as f:
        f.write(css)

def create_javascript():
    print("--- 5. WRITING JS (SEARCH + CART LOGIC) ---")
    js = f"""
    document.addEventListener('DOMContentLoaded', () => {{
        
        // 1. SEARCH & FILTER LOGIC
        const searchInput = document.getElementById('searchInput');
        const filterBtns = document.querySelectorAll('.filter-chip');
        const products = document.querySelectorAll('.product-item');
        
        if(searchInput) {{
            searchInput.addEventListener('input', (e) => {{
                const term = e.target.value.toLowerCase();
                products.forEach(p => {{
                    const title = p.dataset.title.toLowerCase();
                    p.style.display = title.includes(term) ? 'block' : 'none';
                }});
            }});
        }}
        
        filterBtns.forEach(btn => {{
            btn.addEventListener('click', () => {{
                // Active State
                filterBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                
                const cat = btn.dataset.cat;
                products.forEach(p => {{
                    if(cat === 'all' || p.dataset.cat === cat) {{
                        p.style.display = 'block';
                    }} else {{
                        p.style.display = 'none';
                    }}
                }});
            }});
        }});

        // 2. SHIPPING PROGRESS LOGIC (Simulated)
        // Snipcart events can hook here for real data
        const bar = document.getElementById('shippingBar');
        if(bar) {{
            setTimeout(() => {{ bar.style.width = '35%'; }}, 1000);
        }}
    }});
    """
    with open(os.path.join(STATIC_JS_DIR, "app.js"), "w", encoding="utf-8") as f:
        f.write(js)

def create_layouts():
    print("--- 6. BUILDING TEMPLATES ---")
    
    # SNIPCART & META BLOCK
    head_block = f"""
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="stylesheet" href="/css/main.css">
    <meta property="og:title" content="{{{{ .Title }}}}">
    <meta property="og:description" content="{STORE_NAME} - Boutique en ligne">
    <link rel="stylesheet" href="https://cdn.snipcart.com/themes/v3.7.2/default/snipcart.css" />
    """
    
    footer_block = f"""
    <script src="/js/app.js"></script>
    <script async src="https://cdn.snipcart.com/themes/v3.7.2/default/snipcart.js"></script>
    <div hidden id="snipcart" data-api-key="{SNIPCART_KEY}" data-config-modal-style="side"></div>
    """

    # --- HOMEPAGE (Grid + Filter + Search) ---
    index_html = f"""<!doctype html>
<html lang="fr">
<head>
    <title>{STORE_NAME} | Accueil</title>
    {head_block}
</head>
<body>
    <div class="top-bar"><div class="container text-center"><i class="fas fa-truck me-2"></i> Livraison Gratuite dès 300 DH</div></div>
    
    <nav class="navbar sticky-top">
        <div class="container">
            <a href="/" class="fw-900 fs-3 text-primary">{STORE_NAME}.</a>
            <button class="btn-add" style="width: auto; padding: 8px 20px;" class="snipcart-checkout">
                <i class="fas fa-shopping-bag"></i> <span class="snipcart-items-count">0</span>
            </button>
        </div>
    </nav>

    <div class="filter-bar sticky-top" style="top: 70px; z-index: 90;">
        <div class="container">
            <div class="row align-items-center g-3">
                <div class="col-md-4">
                    <input type="text" id="searchInput" class="search-input" placeholder="🔍 Rechercher un produit...">
                </div>
                <div class="col-md-8">
                    <div class="d-flex gap-2 overflow-auto pb-1">
                        <span class="filter-chip active" data-cat="all">Tout</span>
                        {{{{ range $name, $taxonomy := .Site.Taxonomies.categories }}}}
                        <span class="filter-chip" data-cat="{{{{ $name }}}}">{{{{ humanize $name }}}}</span>
                        {{{{ end }}}}
                    </div>
                </div>
            </div>
        </div>
    </div>

    {{{{ define "main" }}}}
    <div class="container mb-5">
        <div class="row g-4">
            {{{{ range .Site.RegularPages }}}}
            <div class="col-6 col-md-4 col-lg-3 product-item" data-cat="{{{{ index .Params.categories 0 }}}}" data-title="{{{{ .Title }}}}">
                <div class="product-card shadow-hover">
                    <div class="card-img-container">
                        <span class="badge-discount">-20%</span>
                        <a href="{{{{ .Permalink }}}}"><img src="{{{{ .Params.image }}}}" loading="lazy" alt="{{{{ .Title }}}}"></a>
                    </div>
                    <div class="card-content">
                        <div class="text-uppercase text-muted fs-6 fw-bold mb-1" style="font-size: 10px;">{{{{ index .Params.categories 0 }}}}</div>
                        <h3 class="card-title fs-6">{{{{ .Title }}}}</h3>
                        <div class="card-price mb-3">
                            <del>{{{{ .Params.old_price }}}} DH</del> {{{{ .Params.price }}}} DH
                        </div>
                        <button class="btn-add snipcart-add-item"
                            data-item-id="{{{{ .Params.sku }}}}"
                            data-item-price="{{{{ .Params.price }}}}"
                            data-item-url="{{{{ .Permalink }}}}"
                            data-item-name="{{{{ .Title }}}}"
                            data-item-image="{{{{ .Params.image }}}}"
                            data-item-description="Vendu par {STORE_NAME}">
                            Ajouter
                        </button>
                    </div>
                </div>
            </div>
            {{{{ end }}}}
        </div>
    </div>
    {{{{ end }}}}

    <footer class="bg-dark text-white py-5 mt-5">
        <div class="container">
            <div class="row g-4">
                <div class="col-md-4">
                    <h4 class="fw-900 mb-3">{STORE_NAME}.</h4>
                    <p class="text-white-50">Votre destination qualité pour les produits importés.</p>
                </div>
                <div class="col-md-4">
                    <h5 class="mb-3">Liens Rapides</h5>
                    <ul class="list-unstyled text-white-50">
                        <li class="mb-2"><a href="#">Politique de Retour</a></li>
                        <li class="mb-2"><a href="#">Livraison</a></li>
                        <li class="mb-2"><a href="#">CGV</a></li>
                    </ul>
                </div>
                <div class="col-md-4">
                    <h5 class="mb-3">Paiement</h5>
                    <div class="fs-2 text-white-50 gap-3 d-flex">
                        <i class="fab fa-cc-visa"></i>
                        <i class="fab fa-cc-mastercard"></i>
                        <i class="fas fa-money-bill"></i>
                    </div>
                </div>
            </div>
        </div>
    </footer>

    {footer_block}
</body>
</html>"""

    # --- PRODUCT PAGE (P0 - Detail Page) ---
    single_html = f"""<!doctype html>
<html lang="fr">
<head><title>{{{{ .Title }}}}</title>{head_block}</head>
<body>
    
    <nav class="navbar sticky-top">
        <div class="container">
            <a href="/" class="fw-bold text-dark"><i class="fas fa-arrow-left"></i> RETOUR</a>
            <button class="btn-add" style="width: auto; padding: 8px 20px;" class="snipcart-checkout">
                Panier <span class="snipcart-items-count">0</span>
            </button>
        </div>
    </nav>

    <div class="container">
        <div class="pdp-grid">
            <div class="pdp-gallery">
                <img src="{{{{ .Params.image }}}}" alt="{{{{ .Title }}}}">
            </div>

            <div class="pdp-info">
                <span class="badge-discount position-static mb-3 d-inline-block">{{{{ index .Params.categories 0 }}}}</span>
                <h1>{{{{ .Title }}}}</h1>
                
                <div class="pdp-meta">
                    <span><i class="fas fa-star text-warning"></i> 4.9/5</span>
                    <span><i class="fas fa-check-circle text-success"></i> En Stock ({{{{ .Params.stock }}}})</span>
                    <span>Ref: {{{{ .Params.sku }}}}</span>
                </div>

                <div class="card-price fs-2 mb-4">
                    <del class="fs-4">{{{{ .Params.old_price }}}} DH</del> {{{{ .Params.price }}}} MAD
                </div>

                <div class="d-grid gap-3">
                    <button class="btn-add py-3 fs-5 snipcart-add-item"
                        data-item-id="{{{{ .Params.sku }}}}"
                        data-item-price="{{{{ .Params.price }}}}"
                        data-item-url="{{{{ .Permalink }}}}"
                        data-item-name="{{{{ .Title }}}}"
                        data-item-image="{{{{ .Params.image }}}}"
                        data-item-description="Produit {STORE_NAME}">
                        AJOUTER AU PANIER
                    </button>
                    
                    <a href="https://wa.me/{PHONE_NUMBER}?text=Bonjour, je veux commander: {{{{ .Title }}}}" 
                       class="btn-add bg-success" style="background: #25D366 !important;">
                       <i class="fab fa-whatsapp"></i> COMMANDER SUR WHATSAPP
                    </a>
                </div>

                <div class="trust-box">
                    <div>
                        <i class="fas fa-truck text-primary mb-2 fs-4"></i>
                        <div class="fw-bold">Livraison 24h</div>
                        <div class="small text-muted">Partout au Maroc</div>
                    </div>
                    <div>
                        <i class="fas fa-shield-alt text-primary mb-2 fs-4"></i>
                        <div class="fw-bold">Garantie</div>
                        <div class="small text-muted">Satisfait ou remboursé</div>
                    </div>
                </div>

                <div class="mt-5">
                    <h5 class="fw-bold border-bottom pb-2">Ingrédients & Allergènes</h5>
                    <p class="text-muted mt-3">{{{{ .Params.ingredients }}}}</p>
                    <p class="text-danger small fw-bold">⚠️ {{{{ .Params.allergens }}}}</p>
                </div>
            </div>
        </div>
    </div>

    {footer_block}
</body>
</html>"""

    with open(os.path.join(LAYOUT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_html)
    with open(os.path.join(DEFAULT_DIR, "single.html"), "w", encoding="utf-8") as f:
        f.write(single_html)

# --- EXECUTION ---
if __name__ == "__main__":
    setup_dirs()
    generate_hugo_config()
    process_products()
    create_advanced_css()
    create_javascript()
    create_layouts()
    print("\n✅ HERO BUILD COMPLETE.")
    print("---------------------------------------")
    print("1. Run 'hugo' to build the new system.")
    print("2. Upload 'public' to Netlify.")
    print("---------------------------------------")