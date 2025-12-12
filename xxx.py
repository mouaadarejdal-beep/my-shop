import os

# --- CONFIGURATION ---
BASE_DIR = os.getcwd()
LAYOUT_DIR = os.path.join(BASE_DIR, "layouts")
DEFAULT_DIR = os.path.join(LAYOUT_DIR, "_default")
STATIC_CSS_DIR = os.path.join(BASE_DIR, "static", "css")

# EL MERCADO IDENTITY
PRIMARY_COLOR = "#d04f27" # The exact Orange/Red
SECONDARY_COLOR = "#222222" # Dark Gray
SNIPCART_KEY = "OWUxZTM0MzItNjA5MC00YmYxLWE1YmItZmRiMmFmZTRmMzY1NjM3NDc2Njk1Nzc4OTIwNDY0"

def create_css():
    print("--- 1. Installing El Mercado Design ---")
    os.makedirs(STATIC_CSS_DIR, exist_ok=True)
    
    css = f"""
    @import url('https://fonts.googleapis.com/css2?family=Exo:wght@400;600;700&family=Inter:wght@400;600&display=swap');
    
    :root {{ --primary: {PRIMARY_COLOR}; --dark: {SECONDARY_COLOR}; --bg: #ffffff; }}
    
    body {{ font-family: 'Inter', sans-serif; color: #444; background: var(--bg); }}
    a {{ text-decoration: none; color: inherit; transition: 0.2s; }}
    a:hover {{ color: var(--primary); }}
    
    /* TOP BAR */
    .top-bar {{ background: var(--dark); color: white; font-size: 12px; padding: 10px 0; font-family: 'Exo', sans-serif; }}
    
    /* HEADER */
    .site-header {{ padding: 30px 0; border-bottom: 1px solid #eee; }}
    .logo {{ font-family: 'Exo', sans-serif; font-weight: 800; font-size: 32px; color: #000; text-transform: uppercase; }}
    .logo span {{ color: var(--primary); }}
    
    /* SEARCH */
    .search-input {{ border: 2px solid #eee; border-radius: 50px; padding: 10px 20px; width: 100%; }}
    .search-input:focus {{ border-color: var(--primary); outline: none; }}
    
    /* NAVIGATION */
    .main-nav {{ border-bottom: 1px solid #eee; }}
    .nav-link {{ font-family: 'Exo', sans-serif; font-weight: 700; font-size: 14px; color: #333 !important; text-transform: uppercase; padding: 20px 15px !important; }}
    .nav-link:hover {{ color: var(--primary) !important; }}
    
    /* SIDEBAR (The El Mercado Look) */
    .sidebar-title {{ font-family: 'Exo', sans-serif; font-weight: 700; font-size: 16px; margin-bottom: 20px; text-transform: uppercase; border-bottom: 2px solid var(--primary); padding-bottom: 10px; display: inline-block; }}
    .cat-list li {{ margin-bottom: 10px; border-bottom: 1px dashed #eee; padding-bottom: 5px; }}
    .cat-list a {{ font-size: 14px; color: #666; font-weight: 500; }}
    .cat-list a:hover {{ color: var(--primary); padding-left: 5px; }}
    
    /* PRODUCT CARD */
    .product-card {{ border: 1px solid #f0f0f0; transition: 0.3s; background: white; text-align: center; height: 100%; position: relative; }}
    .product-card:hover {{ border-color: var(--primary); box-shadow: 0 5px 20px rgba(0,0,0,0.05); }}
    
    .card-img {{ width: 100%; height: 220px; object-fit: contain; padding: 20px; transition: 0.3s; }}
    .product-card:hover .card-img {{ transform: scale(1.05); }}
    
    .card-info {{ padding: 15px; }}
    .cat-name {{ font-size: 11px; text-transform: uppercase; color: #999; letter-spacing: 1px; margin-bottom: 5px; display: block; }}
    .prod-title {{ font-family: 'Exo', sans-serif; font-weight: 700; font-size: 14px; color: #333; margin-bottom: 10px; height: 40px; overflow: hidden; }}
    
    .price {{ color: var(--primary); font-weight: 800; font-size: 18px; margin-bottom: 15px; display: block; }}
    
    .btn-add {{ 
        background: var(--primary); color: white; border: none; 
        width: 100%; padding: 10px; font-weight: 700; font-size: 12px; 
        text-transform: uppercase; letter-spacing: 1px; cursor: pointer;
    }}
    .btn-add:hover {{ background: #b03e1e; }}
    
    /* FOOTER */
    footer {{ background: #222; color: #fff; padding: 60px 0; margin-top: 60px; }}
    footer h5 {{ font-family: 'Exo', sans-serif; font-weight: 700; margin-bottom: 20px; color: #fff; }}
    footer a {{ color: #999; }}
    footer a:hover {{ color: white; }}
    """
    with open(os.path.join(STATIC_CSS_DIR, "style.css"), "w", encoding="utf-8") as f:
        f.write(css)

def create_layouts():
    print("--- 2. Building Structure (Sidebar + Grid) ---")
    os.makedirs(DEFAULT_DIR, exist_ok=True)
    
    common_head = f"""
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="stylesheet" href="/css/style.css">
    <link rel="stylesheet" href="https://cdn.snipcart.com/themes/v3.7.2/default/snipcart.css" />
    """
    
    scripts = f"""
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script async src="https://cdn.snipcart.com/themes/v3.7.2/default/snipcart.js"></script>
    <div hidden id="snipcart" data-api-key="{SNIPCART_KEY}" data-config-modal-style="side"></div>
    """

    # --- 1. HOMEPAGE (Sidebar Left + Grid Right) ---
    index_html = f"""
<!doctype html>
<html lang="fr">
<head><title>MECADO</title>{common_head}</head>
<body>

    <div class="top-bar">
        <div class="container d-flex justify-content-between">
            <span><i class="fas fa-truck"></i> LIVRAISON PARTOUT AU MAROC</span>
            <span><i class="fab fa-whatsapp"></i> +212 600 000 000</span>
        </div>
    </div>

    <header class="site-header">
        <div class="container">
            <div class="row align-items-center">
                <div class="col-md-3">
                    <a href="/" class="logo">MECADO<span>.</span></a>
                </div>
                <div class="col-md-6">
                    <input type="text" class="search-input" placeholder="Rechercher...">
                </div>
                <div class="col-md-3 text-end">
                    <button class="btn btn-link text-dark fw-bold text-decoration-none snipcart-checkout">
                        <i class="fas fa-shopping-basket fa-lg"></i> PANIER <span class="badge bg-danger rounded-pill snipcart-items-count">0</span>
                    </button>
                </div>
            </div>
        </div>
    </header>

    <div class="main-nav d-none d-lg-block sticky-top bg-white">
        <div class="container">
            <ul class="nav">
                <li class="nav-item"><a class="nav-link" href="/">ACCUEIL</a></li>
                <li class="nav-item"><a class="nav-link" href="#">SUCRÉES</a></li>
                <li class="nav-item"><a class="nav-link" href="#">SALÉES</a></li>
                <li class="nav-item"><a class="nav-link" href="#">BOISSONS</a></li>
                <li class="nav-item"><a class="nav-link" href="#">COURSES</a></li>
                <li class="nav-item"><a class="nav-link text-danger" href="#">PROMOTIONS</a></li>
            </ul>
        </div>
    </div>

    <div class="container mt-5">
        <div class="row">
            
            <div class="col-lg-3 d-none d-lg-block">
                <div class="mb-5">
                    <h5 class="sidebar-title">CATÉGORIES</h5>
                    <ul class="list-unstyled cat-list">
                        <li><a href="#">Chocolats & Bonbons</a></li>
                        <li><a href="#">Biscuits & Gâteaux</a></li>
                        <li><a href="#">Chips & Snacks</a></li>
                        <li><a href="#">Boissons & Jus</a></li>
                        <li><a href="#">Épicerie Fine</a></li>
                        <li><a href="#">Petit Déjeuner</a></li>
                    </ul>
                </div>
                <div class="mb-5">
                    <h5 class="sidebar-title">FILTRER PAR PRIX</h5>
                    <input type="range" class="form-range" min="0" max="500">
                </div>
                <div>
                    <img src="https://placehold.co/300x400/d04f27/fff?text=PROMO" class="img-fluid rounded">
                </div>
            </div>

            <div class="col-lg-9">
                <div class="mb-4 rounded p-4 text-white d-flex align-items-center" style="background: linear-gradient(45deg, #222, {PRIMARY_COLOR}); height: 200px;">
                    <div>
                        <h2 class="fw-bold">NOS PRODUITS</h2>
                        <p class="mb-0">Découvrez notre sélection exclusive.</p>
                    </div>
                </div>

                <div class="d-flex justify-content-between align-items-center mb-4 pb-2 border-bottom">
                    <span class="text-muted small">Affichage de tous les produits</span>
                    <select class="form-select form-select-sm" style="width: auto;">
                        <option>Tri par défaut</option>
                        <option>Prix croissant</option>
                        <option>Prix décroissant</option>
                    </select>
                </div>

                <div class="row g-4">
                    {{{{ range .Site.RegularPages }}}}
                    <div class="col-6 col-md-4">
                        <div class="product-card h-100">
                            <a href="{{{{ .Permalink }}}}" class="d-block">
                                <img src="{{{{ .Params.image }}}}" class="card-img" alt="{{{{ .Title }}}}" loading="lazy">
                            </a>
                            <div class="card-info">
                                <span class="cat-name">{{{{ index .Params.categories 0 }}}}</span>
                                <h6 class="prod-title"><a href="{{{{ .Permalink }}}}" class="text-reset">{{{{ .Title }}}}</a></h6>
                                <span class="price">{{{{ .Params.price }}}} DH</span>
                                <button class="btn-add snipcart-add-item"
                                    data-item-id="{{{{ .Params.sku }}}}"
                                    data-item-price="{{{{ .Params.price }}}}"
                                    data-item-url="{{{{ .Permalink }}}}"
                                    data-item-name="{{{{ .Title }}}}"
                                    data-item-image="{{{{ .Params.image }}}}"
                                    data-item-custom1-name="Téléphone"
                                    data-item-custom1-required="true">
                                    AJOUTER AU PANIER
                                </button>
                            </div>
                        </div>
                    </div>
                    {{{{ end }}}}
                </div>
            </div>
        </div>
    </div>

    <footer>
        <div class="container">
            <div class="row">
                <div class="col-md-4">
                    <h5>MECADO.</h5>
                    <p class="text-muted small">Votre boutique préférée pour les produits importés. Qualité garantie.</p>
                </div>
                <div class="col-md-4">
                    <h5>LIENS</h5>
                    <ul class="list-unstyled small">
                        <li><a href="#">Contact</a></li>
                        <li><a href="#">Livraison</a></li>
                        <li><a href="#">Mentions Légales</a></li>
                    </ul>
                </div>
                <div class="col-md-4">
                    <h5>CONTACT</h5>
                    <p class="text-muted small">Casablanca, Maroc<br>contact@mecado.ma</p>
                </div>
            </div>
            <div class="text-center mt-4 pt-4 border-top border-secondary text-muted small">
                © 2025 MECADO - Tous droits réservés.
            </div>
        </div>
    </footer>

    {scripts}
</body>
</html>
    """

    # --- 2. PRODUCT DETAIL (The Window) ---
    single_html = f"""
<!doctype html>
<html lang="fr">
<head><title>{{{{ .Title }}}}</title>{common_head}</head>
<body>
    
    <div class="top-bar"><div class="container text-center">Livraison Gratuite dès 300 DH</div></div>
    <nav class="bg-white border-bottom py-3 sticky-top">
        <div class="container d-flex justify-content-between align-items-center">
            <a href="/" class="fw-bold text-dark"><i class="fas fa-chevron-left text-danger"></i> RETOUR BOUTIQUE</a>
            <button class="btn btn-outline-dark snipcart-checkout">
                <i class="fas fa-shopping-basket"></i> <span class="snipcart-items-count">0</span>
            </button>
        </div>
    </nav>

    <div class="container py-5">
        <div class="row gx-5">
            <div class="col-md-6 mb-4">
                <div class="border p-5 bg-white text-center">
                    <img src="{{{{ .Params.image }}}}" class="img-fluid" style="max-height: 500px;">
                </div>
            </div>

            <div class="col-md-6">
                <span class="text-muted text-uppercase fw-bold small">{{{{ index .Params.categories 0 }}}}</span>
                <h1 class="fw-bold mt-2 mb-3" style="font-family:'Exo'; font-size: 2.5rem;">{{{{ .Title }}}}</h1>
                
                <div class="h2 text-danger fw-bold mb-4">{{{{ .Params.price }}}} MAD</div>
                
                <p class="text-secondary lead mb-4" style="font-size:16px;">
                    {{{{ .Content }}}}
                    <br><br>
                    Produit en stock. Commandez maintenant pour une expédition rapide.
                </p>

                <hr class="my-4">

                <div class="d-flex gap-3">
                    <input type="number" class="form-control text-center fw-bold" value="1" min="1" style="width: 70px;">
                    <button class="btn btn-danger w-100 py-3 fw-bold text-uppercase snipcart-add-item"
                        data-item-id="{{{{ .Params.sku }}}}"
                        data-item-price="{{{{ .Params.price }}}}"
                        data-item-url="{{{{ .Permalink }}}}"
                        data-item-name="{{{{ .Title }}}}"
                        data-item-image="{{{{ .Params.image }}}}"
                        data-item-custom1-name="Téléphone"
                        data-item-custom1-required="true">
                        AJOUTER AU PANIER
                    </button>
                </div>

                <div class="mt-4 pt-3 border-top">
                    <div class="d-flex align-items-center mb-2 text-muted small">
                        <i class="fas fa-check-circle text-success me-2"></i> Stock disponible
                    </div>
                    <div class="d-flex align-items-center text-muted small">
                        <i class="fas fa-truck text-dark me-2"></i> Livraison 24h-48h
                    </div>
                </div>
            </div>
        </div>
    </div>

    {scripts}
</body>
</html>
    """

    # Write files
    with open(os.path.join(LAYOUT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_html)
    with open(os.path.join(DEFAULT_DIR, "single.html"), "w", encoding="utf-8") as f:
        f.write(single_html)

if __name__ == "__main__":
    create_css()
    create_layouts()
    print("✅ SIMULATION COMPLETE.")
    print("1. Run 'hugo' to rebuild.")
    print("2. Commit and Push to GitHub.")