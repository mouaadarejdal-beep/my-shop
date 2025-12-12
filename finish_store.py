import os
import shutil

# --- CONFIGURATION ---
BASE_DIR = os.getcwd()
LAYOUT_DIR = os.path.join(BASE_DIR, "layouts")
DEFAULT_DIR = os.path.join(LAYOUT_DIR, "_default")
STATIC_CSS_DIR = os.path.join(BASE_DIR, "static", "css")

# EL MERCADO STYLE CONFIG
STORE_NAME = "MECADO"
PRIMARY_COLOR = "#d04f27" # The exact Orange/Red from El Mercado
SECONDARY_COLOR = "#222222" # Dark Gray/Black

# LATEST SNIPCART VERSION (Fixes the "Preparing Cart" bug)
SNIPCART_KEY = "OWUxZTM0MzItNjA5MC00YmYxLWE1YmItZmRiMmFmZTRmMzY1NjM3NDc2Njk1Nzc4OTIwNDY0"

def create_final_css():
    print("--- 1. Creating El Mercado Styles ---")
    os.makedirs(STATIC_CSS_DIR, exist_ok=True)
    
    css = f"""
    @import url('https://fonts.googleapis.com/css2?family=Exo:wght@400;600;700&family=Inter:wght@400;600&display=swap');
    
    :root {{ 
        --primary: {PRIMARY_COLOR}; 
        --dark: {SECONDARY_COLOR};
        --light: #f9f9f9;
        --border: #e5e5e5;
    }}
    
    body {{ font-family: 'Inter', sans-serif; color: #444; background: #fff; }}
    h1, h2, h3, h4, h5, h6, .nav-link, .btn {{ font-family: 'Exo', sans-serif; text-transform: uppercase; }}
    
    /* TOP BAR (Black Strip) */
    .top-bar {{ background: var(--dark); color: white; font-size: 12px; padding: 8px 0; font-weight: 600; }}
    .top-bar i {{ color: var(--primary); margin-right: 5px; }}
    
    /* HEADER */
    .site-header {{ padding: 25px 0; border-bottom: 1px solid var(--border); }}
    .logo {{ font-size: 32px; font-weight: 800; letter-spacing: -1px; color: black; text-decoration: none; }}
    .logo span {{ color: var(--primary); }}
    
    /* NAVIGATION (The "Anglets") */
    .main-nav {{ border-bottom: 1px solid var(--border); background: white; }}
    .nav-link {{ color: #333 !important; font-weight: 700; font-size: 14px; padding: 18px 15px !important; letter-spacing: 0.5px; }}
    .nav-link:hover, .nav-link.active {{ color: var(--primary) !important; }}
    
    /* PRODUCT GRID */
    .product-card {{ 
        border: 1px solid var(--border); 
        transition: all 0.3s ease; 
        position: relative; 
        background: white;
        height: 100%;
        display: flex;
        flex-direction: column;
    }}
    .product-card:hover {{ border-color: var(--primary); transform: translateY(-5px); box-shadow: 0 10px 30px rgba(0,0,0,0.08); }}
    
    .card-img-wrap {{ position: relative; padding-top: 100%; overflow: hidden; }}
    .card-img-wrap img {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; object-fit: contain; padding: 20px; transition: 0.5s; }}
    .product-card:hover img {{ transform: scale(1.1); }}
    
    /* BADGES */
    .badge-promo {{ 
        position: absolute; top: 10px; right: 10px; 
        background: var(--primary); color: white; 
        font-size: 11px; font-weight: 700; 
        padding: 4px 8px; border-radius: 4px; z-index: 2;
    }}
    
    /* PRICES */
    .price-wrap {{ color: var(--primary); font-weight: 800; font-size: 18px; margin: 10px 0; }}
    .price-old {{ text-decoration: line-through; color: #999; font-size: 14px; font-weight: 400; margin-right: 5px; }}
    
    /* BUTTONS */
    .btn-cart {{ 
        background: white; color: var(--dark); 
        border: 2px solid var(--dark); 
        width: 100%; padding: 10px; 
        font-weight: 700; font-size: 13px; 
        transition: 0.3s; 
    }}
    .btn-cart:hover {{ background: var(--primary); border-color: var(--primary); color: white; }}
    
    /* SNIPCART OVERRIDES */
    .snipcart-modal__container {{ z-index: 9999; }}
    """
    
    with open(os.path.join(STATIC_CSS_DIR, "style.css"), "w", encoding="utf-8") as f:
        f.write(css)

def create_layouts():
    print("--- 2. Building El Mercado Structure ---")
    
    # We use the LATEST Snipcart version (v3.7.2) to fix the "Preparing" bug
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

    # --- HOMEPAGE ---
    index_html = f"""
<!doctype html>
<html lang="fr">
<head>
    <title>{STORE_NAME} | Épicerie Fine & Produits Importés</title>
    {common_head}
</head>
<body>

    <div class="top-bar">
        <div class="container d-flex justify-content-between">
            <span><i class="fas fa-truck"></i> Livraison Partout au Maroc</span>
            <span><i class="fab fa-whatsapp"></i> Service Client: +212 600 000 000</span>
            <span class="d-none d-md-block"><i class="fas fa-check-circle"></i> Satisfait ou Remboursé</span>
        </div>
    </div>

    <header class="site-header">
        <div class="container">
            <div class="row align-items-center">
                <div class="col-md-3">
                    <a href="/" class="logo">{STORE_NAME}<span>.</span></a>
                </div>
                <div class="col-md-6 my-2 my-md-0">
                    <div class="input-group">
                        <input type="text" class="form-control border-end-0" placeholder="Rechercher un produit (ex: Chocolat)...">
                        <span class="input-group-text bg-white border-start-0"><i class="fas fa-search text-muted"></i></span>
                    </div>
                </div>
                <div class="col-md-3 text-end">
                    <button class="btn btn-outline-dark rounded-0 fw-bold snipcart-checkout position-relative">
                        <i class="fas fa-shopping-basket me-2"></i> PANIER
                        <span class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger snipcart-items-count">0</span>
                    </button>
                </div>
            </div>
        </div>
    </header>

    <nav class="main-nav d-none d-lg-block sticky-top">
        <div class="container">
            <ul class="nav justify-content-center">
                <li class="nav-item"><a class="nav-link active" href="/">ACCUEIL</a></li>
                <li class="nav-item"><a class="nav-link" href="#">SUCRÉES</a></li>
                <li class="nav-item"><a class="nav-link" href="#">SALÉES</a></li>
                <li class="nav-item"><a class="nav-link" href="#">BOISSONS</a></li>
                <li class="nav-item"><a class="nav-link" href="#">ÉPICERIE FINE</a></li>
                <li class="nav-item"><a class="nav-link" href="#">BIO & SANTÉ</a></li>
                <li class="nav-item"><a class="nav-link" href="#">BOX CADEAUX</a></li>
                <li class="nav-item"><a class="nav-link text-danger" href="#">PROMOTIONS</a></li>
            </ul>
        </div>
    </nav>

    {{{{ define "main" }}}}
    
    <div class="container mt-4 mb-5">
        <div class="rounded-3 p-5 text-white" style="background: url('https://placehold.co/1200x400/222/d04f27?text=NOUVEAUX+ARRIVAGES') no-repeat center/cover; min-height: 300px; display: flex; align-items: center;">
            <div class="bg-dark bg-opacity-75 p-4 rounded ms-md-5">
                <h2 class="display-5 fw-bold mb-3">PLEIN DE NOUVEAUTÉS</h2>
                <p class="lead mb-4">Découvrez nos derniers produits importés.</p>
                <a href="#shop" class="btn btn-light rounded-0 fw-bold px-4">ACHETER MAINTENANT</a>
            </div>
        </div>
    </div>

    <div class="container mb-5" id="shop">
        <div class="d-flex justify-content-between align-items-center mb-4">
            <h3 class="fw-bold border-start border-4 border-danger ps-3 m-0">NOS PRODUITS</h3>
            <a href="#" class="text-muted text-decoration-none small fw-bold">VOIR TOUT <i class="fas fa-arrow-right"></i></a>
        </div>

        <div class="row g-3 g-md-4">
            {{{{ range .Site.RegularPages }}}}
            <div class="col-6 col-md-4 col-lg-3">
                <div class="product-card">
                    <span class="badge-promo">-20%</span>
                    
                    <a href="{{{{ .Permalink }}}}" class="card-img-wrap">
                        <img src="{{{{ .Params.image }}}}" loading="lazy" alt="{{{{ .Title }}}}">
                    </a>
                    
                    <div class="p-3 d-flex flex-column flex-grow-1">
                        <small class="text-muted text-uppercase mb-1" style="font-size: 11px;">{{{{ index .Params.categories 0 }}}}</small>
                        <h6 class="fw-bold text-dark mb-2 text-truncate">{{{{ .Title }}}}</h6>
                        
                        <div class="price-wrap">
                            <span class="price-old">250 DH</span> {{{{ .Params.price }}}} DH
                        </div>
                        
                        <div class="mt-auto">
                            <a href="{{{{ .Permalink }}}}" class="btn btn-sm btn-outline-secondary w-100 mb-2 rounded-0">VOIR DÉTAILS</a>
                            <button class="btn-cart rounded-0 snipcart-add-item"
                                data-item-id="{{{{ .Params.sku }}}}"
                                data-item-price="{{{{ .Params.price }}}}"
                                data-item-url="{{{{ .Permalink }}}}"
                                data-item-name="{{{{ .Title }}}}"
                                data-item-image="{{{{ .Params.image }}}}"
                                data-item-description="Produit {STORE_NAME}">
                                AJOUTER AU PANIER
                            </button>
                        </div>
                    </div>
                </div>
            </div>
            {{{{ end }}}}
        </div>
    </div>
    {{{{ end }}}}

    <footer class="bg-dark text-white pt-5 pb-3 mt-5">
        <div class="container">
            <div class="row g-4">
                <div class="col-lg-3 col-md-6">
                    <h5 class="text-white mb-3">À PROPOS</h5>
                    <p class="small text-white-50">{STORE_NAME} est votre référence pour les produits d'épicerie fine et importés au Maroc. Qualité et fraîcheur garanties.</p>
                    <div class="d-flex gap-3">
                        <a href="#" class="text-white"><i class="fab fa-facebook fa-lg"></i></a>
                        <a href="#" class="text-white"><i class="fab fa-instagram fa-lg"></i></a>
                        <a href="#" class="text-white"><i class="fab fa-whatsapp fa-lg"></i></a>
                    </div>
                </div>
                <div class="col-lg-3 col-md-6">
                    <h5 class="text-white mb-3">CATÉGORIES</h5>
                    <ul class="list-unstyled small text-white-50">
                        <li><a href="#" class="text-reset text-decoration-none">Sucrées</a></li>
                        <li><a href="#" class="text-reset text-decoration-none">Salées</a></li>
                        <li><a href="#" class="text-reset text-decoration-none">Boissons</a></li>
                        <li><a href="#" class="text-reset text-decoration-none">Nouveautés</a></li>
                    </ul>
                </div>
                <div class="col-lg-3 col-md-6">
                    <h5 class="text-white mb-3">INFOS LÉGALES</h5>
                    <ul class="list-unstyled small text-white-50">
                        <li><a href="#" class="text-reset text-decoration-none">Politique de retour</a></li>
                        <li><a href="#" class="text-reset text-decoration-none">Conditions d'utilisation</a></li>
                        <li><a href="#" class="text-reset text-decoration-none">Politique d'expédition</a></li>
                    </ul>
                </div>
                <div class="col-lg-3 col-md-6">
                    <h5 class="text-white mb-3">NEWSLETTER</h5>
                    <p class="small text-white-50">Inscrivez-vous pour recevoir nos promos.</p>
                    <div class="input-group mb-3">
                        <input type="text" class="form-control rounded-0" placeholder="Email...">
                        <button class="btn btn-primary rounded-0">OK</button>
                    </div>
                </div>
            </div>
            <div class="border-top border-secondary mt-5 pt-3 text-center small text-white-50">
                &copy; 2025 {STORE_NAME} - Design inspired by El Mercado.
            </div>
        </div>
    </footer>

    {common_scripts}
</body>
</html>
    """
    
    # --- PRODUCT WINDOW (Single.html) ---
    single_html = f"""
<!doctype html>
<html lang="fr">
<head>
    <title>{{{{ .Title }}}}</title>
    {common_head}
</head>
<body style="background:#fff;">

    <div class="top-bar">
        <div class="container text-center">
            <span><i class="fas fa-shipping-fast"></i> Livraison Gratuite dès 300 DH d'achat !</span>
        </div>
    </div>
    
    <nav class="navbar border-bottom sticky-top bg-white">
        <div class="container">
            <a href="/" class="text-decoration-none text-dark fw-bold"><i class="fas fa-chevron-left text-danger me-2"></i> REVENIR À LA BOUTIQUE</a>
            <button class="btn btn-dark rounded-0 snipcart-checkout">
                <i class="fas fa-shopping-bag"></i> <span class="snipcart-items-count">0</span>
            </button>
        </div>
    </nav>

    <div class="container py-5">
        <div class="row gx-5">
            <div class="col-md-6 mb-4">
                <div class="border p-5 rounded-0 text-center">
                    <img src="{{{{ .Params.image }}}}" class="img-fluid" style="max-height: 500px;">
                </div>
            </div>

            <div class="col-md-6">
                <nav aria-label="breadcrumb">
                    <ol class="breadcrumb small text-uppercase fw-bold text-muted">
                        <li class="breadcrumb-item"><a href="/" class="text-reset text-decoration-none">Accueil</a></li>
                        <li class="breadcrumb-item">{{{{ index .Params.categories 0 }}}}</li>
                        <li class="breadcrumb-item active">{{{{ .Title }}}}</li>
                    </ol>
                </nav>

                <h1 class="fw-bold mb-3" style="font-family:'Exo';">{{{{ .Title }}}}</h1>
                
                <div class="mb-3 text-warning">
                    <i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i>
                    <span class="text-muted small ms-2">(Avis vérifiés)</span>
                </div>

                <div class="price-wrap fs-2 mb-4">{{{{ .Params.price }}}} DH <span class="text-muted fw-normal fs-6 ms-2">TTC</span></div>
                
                <p class="text-secondary mb-4" style="line-height: 1.8;">
                    {{{{ .Content }}}}
                    <br><br>
                    Produit authentique disponible immédiatement dans nos stocks. Commandez avant 14h pour une expédition le jour même.
                </p>

                <div class="d-flex gap-3 mb-4">
                    <button class="btn btn-dark w-100 py-3 fw-bold rounded-0 shadow-sm snipcart-add-item"
                        data-item-id="{{{{ .Params.sku }}}}"
                        data-item-price="{{{{ .Params.price }}}}"
                        data-item-url="{{{{ .Permalink }}}}"
                        data-item-name="{{{{ .Title }}}}"
                        data-item-image="{{{{ .Params.image }}}}"
                        data-item-description="Produit {STORE_NAME}">
                        AJOUTER AU PANIER
                    </button>
                </div>

                <div class="row g-0 border rounded-0 text-center small text-uppercase fw-bold text-muted">
                    <div class="col-4 border-end p-3"><i class="fas fa-truck fa-2x mb-2 text-danger"></i><br>Livraison<br>Rapide</div>
                    <div class="col-4 border-end p-3"><i class="fas fa-lock fa-2x mb-2 text-danger"></i><br>Paiement<br>Sécurisé</div>
                    <div class="col-4 p-3"><i class="fas fa-box-open fa-2x mb-2 text-danger"></i><br>Retour<br>Facile</div>
                </div>
            </div>
        </div>
        
        <div class="mt-5 pt-5 border-top">
            <h3 class="fw-bold mb-4">VOUS AIMEREZ AUSSI</h3>
            <div class="row g-4">
                {{{{ range first 4 (where .Site.RegularPages "Type" "products") }}}}
                <div class="col-6 col-md-3">
                    <div class="product-card h-100">
                        <a href="{{{{ .Permalink }}}}" class="card-img-wrap">
                            <img src="{{{{ .Params.image }}}}" loading="lazy">
                        </a>
                        <div class="p-3 text-center">
                            <h6 class="fw-bold text-truncate">{{{{ .Title }}}}</h6>
                            <div class="text-danger fw-bold">{{{{ .Params.price }}}} DH</div>
                        </div>
                    </div>
                </div>
                {{{{ end }}}}
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
    create_final_css()
    create_layouts()
    print("✅ FINISH COMPLETE.")
    print("1. Run 'hugo'")
    print("2. Upload 'public' to Netlify.")