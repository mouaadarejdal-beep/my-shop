import os

# --- CONFIGURATION ---
# Your specific Netlify URL is required for the Cart to work properly
BASE_URL = "https://693c5fdf901959000848dbed--finalff12.netlify.app/"
STORE_NAME = "MECADO"
PRIMARY_COLOR = "#d04f27" 
SECONDARY_COLOR = "#222"
SNIPCART_KEY = "OWUxZTM0MzItNjA5MC00YmYxLWE1YmItZmRiMmFmZTRmMzY1NjM3NDc2Njk1Nzc4OTIwNDY0"

# Contact Info
FB_LINK = "https://www.facebook.com/share/1Bq4qfh8Uj/"
EMAIL = "mouaadarejdal@gmail.com"
PHONE_DISPLAY = "07 20 49 81 10"
WHATSAPP_API = "212720498110" # Formatted for API

BASE_DIR = os.getcwd()
LAYOUT_DIR = os.path.join(BASE_DIR, "layouts")
DEFAULT_DIR = os.path.join(LAYOUT_DIR, "_default")
CONFIG_FILE = os.path.join(BASE_DIR, "hugo.toml")

def update_config():
    print("--- 1. configuring Cart & URL ---")
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        f.write(f"""
baseURL = '{BASE_URL}'
languageCode = 'fr-fr'
title = '{STORE_NAME}'
theme = []
# Absolute URLs are required for Snipcart validation
relativeURLs = false
canonifyURLs = true
""")

def create_layouts():
    print("--- 2. Building Organized Layouts ---")
    
    # CSS & HEADER
    head = f"""
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>{STORE_NAME} | Boutique</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <link rel="stylesheet" href="https://cdn.snipcart.com/themes/v3.7.2/default/snipcart.css" />
        <link rel="stylesheet" href="/css/style.css">
        <style>
            /* Custom Search Highlight */
            .search-highlight {{ border: 2px solid {PRIMARY_COLOR}; }}
            /* Category Section Headers */
            .cat-header {{ border-left: 5px solid {PRIMARY_COLOR}; padding-left: 15px; margin: 40px 0 20px 0; font-weight: 800; text-transform: uppercase; }}
        </style>
    </head>
    """

    scripts = f"""
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script async src="https://cdn.snipcart.com/themes/v3.7.2/default/snipcart.js"></script>
    <div hidden id="snipcart" data-api-key="{SNIPCART_KEY}" data-config-modal-style="side"></div>
    
    <script>
        function liveSearch() {{
            let input = document.getElementById("searchBox").value.toLowerCase();
            let products = document.querySelectorAll(".product-col");
            
            products.forEach(product => {{
                let title = product.getAttribute("data-title");
                let cat = product.getAttribute("data-cat");
                
                if (title.includes(input) || cat.includes(input)) {{
                    product.style.display = "block";
                }} else {{
                    product.style.display = "none";
                }}
            }});
        }}
    </script>
    """

    # --- 1. HOMEPAGE (Organized by Category) ---
    index_html = f"""
<!doctype html>
<html lang="fr">
{head}
<body>

    <div class="top-bar">
        <div class="container d-flex justify-content-between">
            <span><i class="fas fa-truck"></i> LIVRAISON PARTOUT AU MAROC</span>
            <span><i class="fab fa-whatsapp"></i> {PHONE_DISPLAY}</span>
        </div>
    </div>

    <header class="site-header sticky-top bg-white shadow-sm">
        <div class="container">
            <div class="row align-items-center">
                <div class="col-md-3 col-6">
                    <a href="/" class="logo">{STORE_NAME}<span>.</span></a>
                </div>
                <div class="col-md-6 d-none d-md-block">
                    <div class="input-group">
                        <input type="text" id="searchBox" class="form-control rounded-0" placeholder="Rechercher (ex: Nutella, Boissons...)" onkeyup="liveSearch()">
                        <button class="btn btn-dark rounded-0"><i class="fas fa-search"></i></button>
                    </div>
                </div>
                <div class="col-md-3 col-6 text-end">
                    <button class="btn btn-outline-dark fw-bold rounded-0 snipcart-checkout">
                        <i class="fas fa-shopping-basket"></i> PANIER <span class="badge bg-danger rounded-pill snipcart-items-count">0</span>
                    </button>
                </div>
            </div>
            <div class="mt-2 d-block d-md-none">
                <input type="text" class="form-control rounded-0" placeholder="Rechercher..." onkeyup="liveSearch()">
            </div>
        </div>
    </header>

    {{{{ define "main" }}}}
    
    <div class="container my-4">
        
        <div class="p-5 mb-5 text-white rounded-3" style="background: linear-gradient(45deg, #111, {PRIMARY_COLOR});">
            <h1 class="display-5 fw-bold">BIENVENUE CHEZ MECADO</h1>
            <p class="lead">Le meilleur des produits importés.</p>
        </div>

        <h3 class="cat-header">🍬 Univers Sucré</h3>
        <div class="row g-3">
            {{{{ range where .Site.RegularPages "Params.categories" "intersect" (slice "Sucrées") }}}}
                {{{{ partial "product-card.html" . }}}}
            {{{{ end }}}}
        </div>

        <h3 class="cat-header">🥨 Univers Salé</h3>
        <div class="row g-3">
            {{{{ range where .Site.RegularPages "Params.categories" "intersect" (slice "Salées") }}}}
                {{{{ partial "product-card.html" . }}}}
            {{{{ end }}}}
        </div>

        <h3 class="cat-header">🥤 Boissons & Café</h3>
        <div class="row g-3">
            {{{{ range where .Site.RegularPages "Params.categories" "intersect" (slice "Boissons") }}}}
                {{{{ partial "product-card.html" . }}}}
            {{{{ end }}}}
        </div>

        <h3 class="cat-header">🛒 Courses & Divers</h3>
        <div class="row g-3">
            {{{{ range where .Site.RegularPages "Params.categories" "intersect" (slice "Courses" "Nouveautés") }}}}
                {{{{ partial "product-card.html" . }}}}
            {{{{ end }}}}
        </div>

    </div>
    {{{{ end }}}}

    <footer class="bg-dark text-white pt-5 pb-3 mt-5">
        <div class="container">
            <div class="row g-4">
                <div class="col-md-4">
                    <h5 class="text-white">{STORE_NAME}</h5>
                    <p class="small text-white-50">Votre satisfaction est notre priorité.</p>
                    <div class="d-flex gap-3">
                        <a href="{FB_LINK}" target="_blank" class="text-white fs-4"><i class="fab fa-facebook"></i></a>
                        <a href="https://wa.me/{WHATSAPP_API}" target="_blank" class="text-white fs-4"><i class="fab fa-whatsapp"></i></a>
                        <a href="mailto:{EMAIL}" class="text-white fs-4"><i class="fas fa-envelope"></i></a>
                    </div>
                </div>
                <div class="col-md-4">
                    <h5>CONTACT</h5>
                    <ul class="list-unstyled small text-white-50">
                        <li><i class="fas fa-phone me-2"></i> {PHONE_DISPLAY}</li>
                        <li><i class="fas fa-envelope me-2"></i> {EMAIL}</li>
                        <li><i class="fab fa-facebook me-2"></i> Mecado Shop</li>
                    </ul>
                </div>
                <div class="col-md-4">
                    <h5>PAIEMENT</h5>
                    <div class="fs-2 text-white-50">
                        <i class="fab fa-cc-visa"></i> <i class="fab fa-cc-mastercard"></i> <i class="fas fa-money-bill"></i>
                    </div>
                </div>
            </div>
            <div class="text-center mt-4 pt-3 border-top border-secondary small">
                © 2025 {STORE_NAME}. Tous droits réservés.
            </div>
        </div>
    </footer>

    {scripts}
</body>
</html>
    """

    # --- 2. PRODUCT CARD PARTIAL (Reusable) ---
    # Note: We verify the URL matches the Base URL for Snipcart to verify the price
    card_html = f"""
    <div class="col-6 col-md-3 product-col" data-title="{{{{ lower .Title }}}}" data-cat="{{{{ lower (index .Params.categories 0) }}}}">
        <div class="product-card h-100">
            <span class="badge-promo">-20%</span>
            <a href="{{{{ .Permalink }}}}" class="card-img-wrap">
                <img src="{{{{ .Params.image }}}}" loading="lazy" alt="{{{{ .Title }}}}">
            </a>
            <div class="p-3 text-center d-flex flex-column flex-grow-1">
                <small class="text-muted text-uppercase" style="font-size:10px">{{{{ index .Params.categories 0 }}}}</small>
                <h6 class="fw-bold text-dark my-2 text-truncate">{{{{ .Title }}}}</h6>
                
                <div class="mb-2">
                    <span class="text-danger fw-bold fs-5">{{{{ .Params.price }}}} DH</span>
                </div>

                <div class="mt-auto">
                    <a href="{{{{ .Permalink }}}}" class="btn btn-sm btn-light w-100 mb-2 border">VOIR</a>
                    <button class="btn-add snipcart-add-item"
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
    """

    # --- 3. SINGLE PAGE (Product Window) ---
    single_html = f"""
<!doctype html>
<html lang="fr">
{head}
<body style="background:#fff;">

    <nav class="navbar border-bottom sticky-top bg-white">
        <div class="container">
            <a href="/" class="fw-bold text-dark text-decoration-none"><i class="fas fa-arrow-left me-2"></i> RETOUR</a>
            <button class="btn btn-dark rounded-0 snipcart-checkout">
                <i class="fas fa-shopping-basket"></i> <span class="badge bg-danger rounded-pill ms-1 snipcart-items-count">0</span>
            </button>
        </div>
    </nav>

    <div class="container py-5">
        <div class="row gx-5">
            <div class="col-md-6 mb-4 text-center">
                <img src="{{{{ .Params.image }}}}" class="img-fluid border rounded p-4" style="max-height: 500px;">
            </div>

            <div class="col-md-6">
                <span class="badge bg-dark mb-2">{{{{ index .Params.categories 0 }}}}</span>
                <h1 class="fw-bold mb-3">{{{{ .Title }}}}</h1>
                <div class="h2 text-danger fw-bold mb-4">{{{{ .Params.price }}}} MAD</div>
                
                <p class="lead text-muted mb-4">{{{{ .Content }}}}</p>

                <div class="d-grid gap-2 mb-4">
                    <button class="btn btn-danger btn-lg rounded-0 fw-bold snipcart-add-item"
                        data-item-id="{{{{ .Params.sku }}}}"
                        data-item-price="{{{{ .Params.price }}}}"
                        data-item-url="{{{{ .Permalink }}}}"
                        data-item-name="{{{{ .Title }}}}"
                        data-item-image="{{{{ .Params.image }}}}"
                        data-item-custom1-name="Téléphone"
                        data-item-custom1-required="true">
                        AJOUTER AU PANIER
                    </button>
                    <a href="https://wa.me/{WHATSAPP_API}?text=Je souhaite commander : {{{{ .Title }}}}" class="btn btn-success btn-lg rounded-0 fw-bold">
                        <i class="fab fa-whatsapp"></i> COMMANDER PAR WHATSAPP
                    </a>
                </div>
            </div>
        </div>
    </div>

    <footer class="bg-dark text-white pt-5 pb-3">
        <div class="container">
            <div class="row">
                <div class="col-md-4">
                    <h5>CONTACT</h5>
                    <ul class="list-unstyled">
                        <li><i class="fab fa-whatsapp me-2"></i> {PHONE_DISPLAY}</li>
                        <li><i class="fas fa-envelope me-2"></i> {EMAIL}</li>
                        <li><a href="{FB_LINK}" class="text-white text-decoration-none"><i class="fab fa-facebook me-2"></i> Facebook</a></li>
                    </ul>
                </div>
            </div>
            <div class="text-center mt-4 border-top border-secondary pt-3 small">© 2025 {STORE_NAME}</div>
        </div>
    </footer>

    {scripts}
</body>
</html>
    """

    # WRITE FILES
    with open(os.path.join(LAYOUT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_html)
    
    # Create a partials folder for the card
    partials_dir = os.path.join(LAYOUT_DIR, "partials")
    os.makedirs(partials_dir, exist_ok=True)
    with open(os.path.join(partials_dir, "product-card.html"), "w", encoding="utf-8") as f:
        f.write(card_html)

    with open(os.path.join(DEFAULT_DIR, "single.html"), "w", encoding="utf-8") as f:
        f.write(single_html)

if __name__ == "__main__":
    update_config()
    create_layouts()
    print("✅ FIXES APPLIED: Contacts, Search, Categories, Cart.")
    print("1. Run 'hugo'")
    print("2. Commit and Push to GitHub")