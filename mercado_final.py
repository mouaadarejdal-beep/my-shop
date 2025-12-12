import os

# --- CONFIGURATION ---
# We use relative URL "/" so it works on ANY Netlify domain automatically
BASE_URL = "/" 
STORE_NAME = "MECADO"
PRIMARY_COLOR = "#d04f27" # The exact Orange/Red from El Mercado
SECONDARY_COLOR = "#222222" # Dark Black
SNIPCART_KEY = "OWUxZTM0MzItNjA5MC00YmYxLWE1YmItZmRiMmFmZTRmMzY1NjM3NDc2Njk1Nzc4OTIwNDY0"

# Paths
BASE_DIR = os.getcwd()
LAYOUT_DIR = os.path.join(BASE_DIR, "layouts")
DEFAULT_DIR = os.path.join(LAYOUT_DIR, "_default")
STATIC_CSS_DIR = os.path.join(BASE_DIR, "static", "css")

def fix_config():
    print("--- 1. Fixing the 'Localhost' Bug ---")
    config_path = os.path.join(BASE_DIR, "hugo.toml")
    with open(config_path, "w", encoding="utf-8") as f:
        f.write(f"""
baseURL = '{BASE_URL}'
languageCode = 'fr-fr'
title = '{STORE_NAME}'
theme = []
relativeURLs = true
""")

def create_pro_css():
    print("--- 2. Installing 'El Mercado' Design Theme ---")
    os.makedirs(STATIC_CSS_DIR, exist_ok=True)
    
    css = f"""
    @import url('https://fonts.googleapis.com/css2?family=Exo:wght@400;600;700;800&family=Open+Sans:wght@400;600&display=swap');
    
    :root {{ --primary: {PRIMARY_COLOR}; --dark: {SECONDARY_COLOR}; --light: #f4f4f4; }}
    
    body {{ font-family: 'Open Sans', sans-serif; background: #fff; color: #333; }}
    h1, h2, h3, h4, h5, .nav-link, .btn {{ font-family: 'Exo', sans-serif; text-transform: uppercase; }}
    
    /* TOP BAR */
    .top-bar {{ background: var(--dark); color: white; font-size: 11px; padding: 8px 0; font-weight: 600; letter-spacing: 0.5px; }}
    
    /* HEADER */
    .site-header {{ padding: 25px 0; border-bottom: 1px solid #eee; }}
    .logo {{ font-size: 34px; font-weight: 800; color: #000; letter-spacing: -1px; text-decoration: none; }}
    .logo span {{ color: var(--primary); }}
    
    .search-box input {{ border-radius: 0; border: 1px solid #ddd; padding: 10px; font-size: 13px; }}
    .search-box button {{ background: var(--primary); color: white; border: none; padding: 0 15px; }}
    
    /* NAVIGATION */
    .main-nav {{ border-bottom: 2px solid #f0f0f0; background: white; }}
    .nav-link {{ color: #222 !important; font-weight: 700; font-size: 13px; padding: 15px 12px !important; transition: 0.2s; }}
    .nav-link:hover {{ color: var(--primary) !important; background: #f9f9f9; }}
    .nav-link.active {{ color: var(--primary) !important; border-bottom: 3px solid var(--primary); }}
    
    /* PRODUCT CARD */
    .product-card {{ 
        border: 1px solid #f0f0f0; transition: all 0.3s; background: white; position: relative; height: 100%;
    }}
    .product-card:hover {{ border-color: var(--primary); box-shadow: 0 10px 30px rgba(0,0,0,0.08); z-index: 2; }}
    
    .card-img-wrap {{ position: relative; padding-top: 100%; overflow: hidden; display: block; }}
    .card-img-wrap img {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; object-fit: contain; padding: 20px; transition: 0.4s; }}
    .product-card:hover img {{ transform: scale(1.05); }}
    
    .badge-promo {{ position: absolute; top: 10px; left: 10px; background: var(--primary); color: white; font-size: 10px; font-weight: bold; padding: 3px 8px; border-radius: 2px; }}
    
    .card-body {{ padding: 15px; text-align: center; }}
    .card-cat {{ color: #999; font-size: 10px; font-weight: 700; margin-bottom: 5px; display: block; }}
    .card-title {{ font-size: 13px; font-weight: 700; color: #000; margin-bottom: 10px; height: 36px; overflow: hidden; }}
    
    .price {{ color: var(--primary); font-weight: 800; font-size: 16px; }}
    
    .btn-add {{ 
        display: block; width: 100%; 
        background: white; border: 1px solid #ddd; 
        color: #333; font-weight: 700; font-size: 12px; 
        padding: 8px; margin-top: 10px; 
        transition: 0.2s; 
    }}
    .product-card:hover .btn-add {{ background: var(--primary); border-color: var(--primary); color: white; }}
    
    /* FOOTER */
    footer {{ background: #111; color: #888; font-size: 13px; padding: 60px 0; margin-top: 50px; }}
    footer h5 {{ color: white; font-size: 14px; margin-bottom: 20px; }}
    footer ul li {{ margin-bottom: 8px; }}
    footer a {{ color: #888; text-decoration: none; }}
    footer a:hover {{ color: white; }}
    """
    with open(os.path.join(STATIC_CSS_DIR, "style.css"), "w", encoding="utf-8") as f:
        f.write(css)

def create_layouts():
    print("--- 3. Injecting Logic & Structure ---")
    
    common_head = f"""
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="stylesheet" href="/css/style.css">
    <link rel="stylesheet" href="https://cdn.snipcart.com/themes/v3.7.2/default/snipcart.css" />
    """
    
    common_scripts = f"""
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script async src="https://cdn.snipcart.com/themes/v3.7.2/default/snipcart.js"></script>
    <div hidden id="snipcart" data-api-key="{SNIPCART_KEY}" data-config-modal-style="side"></div>
    """

    # --- 1. HOMEPAGE ---
    index_html = f"""
<!doctype html>
<html lang="fr">
<head>
    <title>{STORE_NAME} | Produits Importés</title>
    {common_head}
</head>
<body>

    <div class="top-bar">
        <div class="container d-flex justify-content-between align-items-center">
            <span><i class="fas fa-truck me-2"></i>LIVRAISON PARTOUT AU MAROC</span>
            <span class="d-none d-md-block"><i class="fab fa-whatsapp me-2"></i>SERVICE CLIENT: +212 600 000 000</span>
            <span><i class="fas fa-user me-2"></i>MON COMPTE</span>
        </div>
    </div>

    <header class="site-header">
        <div class="container">
            <div class="row align-items-center">
                <div class="col-6 col-md-3">
                    <a href="/" class="logo">{STORE_NAME}<span>.</span></a>
                </div>
                <div class="col-md-6 d-none d-md-block">
                    <div class="input-group search-box">
                        <input type="text" class="form-control" placeholder="Je cherche...">
                        <button class="btn"><i class="fas fa-search"></i></button>
                    </div>
                </div>
                <div class="col-6 col-md-3 text-end">
                    <button class="btn btn-light border fw-bold snipcart-checkout">
                        <i class="fas fa-shopping-basket text-danger"></i> PANIER 
                        <span class="badge bg-dark rounded-pill ms-1 snipcart-items-count">0</span>
                    </button>
                </div>
            </div>
        </div>
    </header>

    <div class="main-nav sticky-top">
        <div class="container">
            <ul class="nav nav-pills justify-content-center" id="cat-filters">
                <li class="nav-item"><a class="nav-link active" onclick="filter('all')">TOUT</a></li>
                <li class="nav-item"><a class="nav-link" onclick="filter('Sucrées')">SUCRÉES</a></li>
                <li class="nav-item"><a class="nav-link" onclick="filter('Salées')">SALÉES</a></li>
                <li class="nav-item"><a class="nav-link" onclick="filter('Boissons')">BOISSONS</a></li>
                <li class="nav-item"><a class="nav-link" onclick="filter('Courses')">COURSES</a></li>
                <li class="nav-item"><a class="nav-link text-danger" onclick="filter('Nouveautés')">PROMOS</a></li>
            </ul>
        </div>
    </div>

    {{{{ define "main" }}}}
    
    <div class="container my-5">
        
        <div class="row mb-5">
            <div class="col-md-8">
                <div class="p-5 text-white rounded-3 h-100 d-flex align-items-center" style="background: linear-gradient(45deg, #222, {PRIMARY_COLOR});">
                    <div>
                        <span class="badge bg-warning text-dark mb-2">ARRIVAGE</span>
                        <h1 class="display-5 fw-bold">NOUVEAUX PRODUITS</h1>
                        <p class="lead">Découvrez notre sélection exclusive importée.</p>
                        <a href="#products" class="btn btn-light fw-bold rounded-0">DÉCOUVRIR</a>
                    </div>
                </div>
            </div>
            <div class="col-md-4 d-none d-md-block">
                <div class="bg-light p-4 rounded-3 h-100 border text-center d-flex flex-column justify-content-center">
                    <i class="fas fa-shipping-fast fa-3x text-danger mb-3"></i>
                    <h4>Livraison 24H</h4>
                    <p class="small text-muted">Partout au Maroc</p>
                    <hr>
                    <i class="fas fa-lock fa-3x text-danger mb-3"></i>
                    <h4>Paiement Sûr</h4>
                    <p class="small text-muted">À la livraison</p>
                </div>
            </div>
        </div>

        <div class="d-flex justify-content-between align-items-center mb-4">
            <h3 class="fw-bold m-0"><span style="border-bottom: 3px solid {PRIMARY_COLOR};">NOS PRODUITS</span></h3>
        </div>

        <div class="row g-3" id="products">
            {{{{ range .Site.RegularPages }}}}
            <div class="col-6 col-md-3 product-item" data-cat="{{{{ index .Params.categories 0 }}}}">
                <div class="product-card">
                    <span class="badge-promo">NOUVEAU</span>
                    <a href="{{{{ .Permalink }}}}" class="card-img-wrap">
                        <img src="{{{{ .Params.image }}}}" loading="lazy" alt="{{{{ .Title }}}}">
                    </a>
                    <div class="card-body">
                        <span class="card-cat">{{{{ index .Params.categories 0 }}}}</span>
                        <h6 class="card-title">{{{{ .Title }}}}</h6>
                        <div class="price">{{{{ .Params.price }}}} MAD</div>
                        
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
            {{{{ end }}}}
        </div>
    </div>
    {{{{ end }}}}

    <script>
        function filter(cat) {{
            const items = document.querySelectorAll('.product-item');
            const links = document.querySelectorAll('.nav-link');
            
            // Remove active class
            links.forEach(l => l.classList.remove('active'));
            event.target.classList.add('active');

            items.forEach(item => {{
                if(cat === 'all' || item.dataset.cat === cat) {{
                    item.style.display = 'block';
                }} else {{
                    item.style.display = 'none';
                }}
            }});
        }}
    </script>

    <footer class="pt-5">
        <div class="container">
            <div class="row g-4">
                <div class="col-lg-4">
                    <h5 class="text-white mb-3">{STORE_NAME}.</h5>
                    <p>Le spécialiste de l'épicerie fine et des produits importés au Maroc. Une sélection unique, des prix justes.</p>
                </div>
                <div class="col-6 col-lg-2">
                    <h5>Navigation</h5>
                    <ul class="list-unstyled">
                        <li><a href="#">Accueil</a></li>
                        <li><a href="#">Boutique</a></li>
                        <li><a href="#">Promotions</a></li>
                    </ul>
                </div>
                <div class="col-6 col-lg-2">
                    <h5>Support</h5>
                    <ul class="list-unstyled">
                        <li><a href="#">Contact</a></li>
                        <li><a href="#">FAQ</a></li>
                        <li><a href="#">Livraison</a></li>
                    </ul>
                </div>
                <div class="col-lg-4">
                    <h5>Newsletter</h5>
                    <div class="input-group mb-3">
                        <input type="text" class="form-control rounded-0" placeholder="Votre email...">
                        <button class="btn btn-danger rounded-0">OK</button>
                    </div>
                </div>
            </div>
            <div class="border-top border-secondary mt-5 pt-3 text-center small">
                © 2025 {STORE_NAME}. Tous droits réservés.
            </div>
        </div>
    </footer>

    {common_scripts}
</body>
</html>
    """
    
    # --- PRODUCT PAGE (Single.html) ---
    single_html = f"""
<!doctype html>
<html lang="fr">
<head>
    <title>{{{{ .Title }}}}</title>
    {common_head}
</head>
<body style="background:#fff;">

    <div class="top-bar">
        <div class="container text-center">Livraison Gratuite dès 300 DH !</div>
    </div>
    <nav class="site-header py-3 sticky-top bg-white border-bottom">
        <div class="container d-flex justify-content-between align-items-center">
            <a href="/" class="text-decoration-none fw-bold text-dark"><i class="fas fa-arrow-left"></i> RETOUR</a>
            <a href="/" class="logo" style="font-size:20px;">{STORE_NAME}<span>.</span></a>
            <button class="btn btn-light border snipcart-checkout">
                <i class="fas fa-shopping-basket"></i> <span class="snipcart-items-count">0</span>
            </button>
        </div>
    </nav>

    <div class="container py-5">
        <div class="row gx-5">
            <div class="col-md-6 mb-4">
                <div class="border p-5 text-center">
                    <img src="{{{{ .Params.image }}}}" class="img-fluid" style="max-height: 500px;">
                </div>
            </div>
            <div class="col-md-6">
                <div class="text-uppercase text-muted fw-bold small mb-2">{{{{ index .Params.categories 0 }}}}</div>
                <h1 class="fw-bold mb-3" style="font-family:'Exo';">{{{{ .Title }}}}</h1>
                <div class="h2 text-danger fw-bold mb-4">{{{{ .Params.price }}}} MAD</div>
                
                <p class="lead text-muted mb-4" style="font-size:15px;">
                    {{{{ .Content }}}}
                    <br><br>
                    Produit en stock. Expédié sous 24h via Amana ou nos livreurs.
                </p>

                <div class="d-flex gap-2 mb-4">
                    <input type="number" value="1" min="1" class="form-control text-center" style="width: 60px;">
                    <button class="btn btn-danger w-100 fw-bold rounded-0 snipcart-add-item"
                        data-item-id="{{{{ .Params.sku }}}}"
                        data-item-price="{{{{ .Params.price }}}}"
                        data-item-url="{{{{ .Permalink }}}}"
                        data-item-name="{{{{ .Title }}}}"
                        data-item-image="{{{{ .Params.image }}}}"
                        data-item-description="Produit {STORE_NAME}">
                        AJOUTER AU PANIER
                    </button>
                </div>

                <div class="bg-light p-3 border rounded small">
                    <div class="d-flex align-items-center mb-2"><i class="fas fa-check text-success me-2"></i> Produit Authentique</div>
                    <div class="d-flex align-items-center"><i class="fas fa-truck text-primary me-2"></i> Livraison Rapide</div>
                </div>
            </div>
        </div>
    </div>

    {common_scripts}
</body>
</html>
    """

    with open(os.path.join(LAYOUT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_html)
    with open(os.path.join(DEFAULT_DIR, "single.html"), "w", encoding="utf-8") as f:
        f.write(single_html)

if __name__ == "__main__":
    fix_config()
    create_pro_css()
    create_layouts()
    print("✅ FINAL UPDATE COMPLETE.")
    print("1. Run 'hugo' (This builds the site properly).")
    print("2. Upload the 'public' folder to Netlify.")