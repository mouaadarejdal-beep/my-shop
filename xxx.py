import os

# --- CONFIGURATION ---
STORE_NAME = "MECADO"
PRIMARY_COLOR = "#d04f27" # El Mercado Orange
SECONDARY_COLOR = "#222"
# Using your public Snipcart Key
SNIPCART_KEY = "OWUxZTM0MzItNjA5MC00YmYxLWE1YmItZmRiMmFmZTRmMzY1NjM3NDc2Njk1Nzc4OTIwNDY0"
WHATSAPP_NUMBER = "212600000000"

BASE_DIR = os.getcwd()
LAYOUT_DIR = os.path.join(BASE_DIR, "layouts")
DEFAULT_DIR = os.path.join(LAYOUT_DIR, "_default")
STATIC_CSS_DIR = os.path.join(BASE_DIR, "static", "css")

def upgrade_styles():
    print("--- 1. Upgrading Design System (P1) ---")
    os.makedirs(STATIC_CSS_DIR, exist_ok=True)
    
    css = f"""
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&family=Oswald:wght@500;700&display=swap');
    
    :root {{ --primary: {PRIMARY_COLOR}; --dark: {SECONDARY_COLOR}; --light: #f4f4f4; }}
    
    body {{ font-family: 'Inter', sans-serif; color: #333; background-color: #fff; }}
    h1, h2, h3, h4, .btn-primary, .nav-link {{ font-family: 'Oswald', sans-serif; text-transform: uppercase; letter-spacing: 0.5px; }}
    
    /* TOP BAR & SHIPPING PROGRESS */
    .top-bar {{ background: #000; color: white; padding: 8px 0; font-size: 12px; }}
    .shipping-progress {{ height: 4px; background: #444; width: 100%; position: relative; }}
    .shipping-bar {{ height: 100%; background: #00c851; width: 0%; transition: 1s; }}
    
    /* HEADER */
    .navbar {{ padding: 20px 0; border-bottom: 1px solid #eee; background: white; }}
    .brand-logo {{ font-size: 28px; font-weight: 700; color: #000; text-decoration: none; }}
    .brand-logo span {{ color: var(--primary); }}
    
    /* PRODUCT GRID */
    .product-card {{ 
        border: 1px solid #eee; border-radius: 8px; overflow: hidden; 
        transition: 0.3s; position: relative; height: 100%; 
        background: white;
    }}
    .product-card:hover {{ border-color: var(--primary); box-shadow: 0 10px 30px rgba(0,0,0,0.05); transform: translateY(-3px); }}
    
    .badge-promo {{ 
        position: absolute; top: 10px; left: 10px; z-index: 10;
        background: var(--primary); color: white; 
        font-size: 11px; font-weight: bold; padding: 4px 8px; border-radius: 4px;
    }}
    
    .img-wrap {{ position: relative; padding-top: 100%; display: block; overflow: hidden; }}
    .img-wrap img {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; object-fit: contain; padding: 20px; transition: 0.5s; }}
    .product-card:hover img {{ transform: scale(1.08); }}
    
    .btn-add {{ 
        width: 100%; background: white; color: var(--dark); border: 2px solid var(--dark);
        padding: 10px; font-weight: 700; font-size: 13px; margin-top: 10px; transition: 0.2s;
    }}
    .btn-add:hover {{ background: var(--primary); border-color: var(--primary); color: white; }}
    
    /* TABS */
    .nav-tabs .nav-link {{ color: #666; font-weight: 600; border: none; border-bottom: 3px solid transparent; }}
    .nav-tabs .nav-link.active {{ color: var(--primary); border-bottom-color: var(--primary); }}
    
    /* FOOTER */
    footer {{ background: #111; color: #aaa; padding: 60px 0; margin-top: 80px; font-size: 13px; }}
    footer h5 {{ color: white; margin-bottom: 20px; }}
    footer a {{ color: #aaa; text-decoration: none; }}
    footer a:hover {{ color: white; }}
    """
    with open(os.path.join(STATIC_CSS_DIR, "style.css"), "w", encoding="utf-8") as f:
        f.write(css)

def upgrade_layouts():
    print("--- 2. Upgrading Layouts (P0, P1, P2) ---")
    os.makedirs(DEFAULT_DIR, exist_ok=True)
    
    # Common Head (SEO + Analytics)
    head = f"""
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>{STORE_NAME} | Boutique en Ligne</title>
        
        <meta name="description" content="Découvrez les meilleurs produits importés au Maroc. Livraison rapide et paiement à la livraison.">
        <meta property="og:title" content="{STORE_NAME}">
        <meta property="og:description" content="Épicerie fine, chocolats, snacks et boissons importées.">
        <meta property="og:image" content="/images/og-cover.jpg">
        
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <link rel="stylesheet" href="/css/style.css">
        <link rel="stylesheet" href="https://cdn.snipcart.com/themes/v3.7.2/default/snipcart.css" />
        
        </head>
    """
    
    # Common Scripts (Snipcart Logic)
    scripts = f"""
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script async src="https://cdn.snipcart.com/themes/v3.7.2/default/snipcart.js"></script>
    <div hidden id="snipcart" 
         data-api-key="{SNIPCART_KEY}" 
         data-config-modal-style="side" 
         data-currency="mad">
    </div>
    
    <script>
        function filter(cat) {{
            document.querySelectorAll('.product-col').forEach(el => {{
                el.style.display = (cat === 'all' || el.dataset.cat === cat) ? 'block' : 'none';
            }});
            document.querySelectorAll('.cat-link').forEach(l => l.classList.remove('active', 'text-danger'));
            event.target.classList.add('active', 'text-danger');
        }}
        
        function search() {{
            let q = document.getElementById('search').value.toLowerCase();
            document.querySelectorAll('.product-col').forEach(el => {{
                let title = el.querySelector('h6').innerText.toLowerCase();
                el.style.display = title.includes(q) ? 'block' : 'none';
            }});
        }}
    </script>
    """

    # --- HOMEPAGE ---
    index_html = f"""
<!doctype html>
<html lang="fr">
{head}
<body>
    <div class="top-bar">
        <div class="container d-flex justify-content-between align-items-center">
            <span><i class="fas fa-truck text-success"></i> LIVRAISON GRATUITE DÈS 300 DH</span>
            <span><i class="fas fa-phone-alt"></i> SERVICE CLIENT 7J/7</span>
        </div>
    </div>

    <nav class="navbar sticky-top">
        <div class="container">
            <a class="brand-logo" href="/">{STORE_NAME}<span>.</span></a>
            
            <div class="d-none d-md-flex flex-grow-1 mx-5">
                <input type="text" id="search" class="form-control rounded-0 border-end-0" placeholder="Rechercher (ex: Milka, Pringles...)" onkeyup="search()">
                <button class="btn btn-dark rounded-0"><i class="fas fa-search"></i></button>
            </div>
            
            <button class="btn btn-outline-dark fw-bold rounded-0 snipcart-checkout">
                <i class="fas fa-shopping-bag"></i> <span class="snipcart-items-count">0</span>
            </button>
        </div>
    </nav>

    <div class="border-bottom bg-white py-2 sticky-top" style="top: 80px; z-index: 900;">
        <div class="container text-center">
            <a class="cat-link mx-3 text-dark fw-bold text-decoration-none active text-danger" onclick="filter('all')">TOUT</a>
            <a class="cat-link mx-3 text-dark fw-bold text-decoration-none" onclick="filter('Sucrées')">SUCRÉES</a>
            <a class="cat-link mx-3 text-dark fw-bold text-decoration-none" onclick="filter('Salées')">SALÉES</a>
            <a class="cat-link mx-3 text-dark fw-bold text-decoration-none" onclick="filter('Boissons')">BOISSONS</a>
            <a class="cat-link mx-3 text-dark fw-bold text-decoration-none" onclick="filter('Courses')">COURSES</a>
        </div>
    </div>

    {{{{ define "main" }}}}
    
    <div class="container mt-4 mb-5">
        <div class="p-5 text-white d-flex align-items-center rounded-3" 
             style="background: linear-gradient(135deg, #111, {PRIMARY_COLOR}); min-height: 300px;">
            <div>
                <span class="badge bg-warning text-dark mb-2">NOUVEAU</span>
                <h1 class="display-4 fw-bold">ARRIVAGES EXCLUSIFS</h1>
                <p class="lead">Le meilleur des marques importées au Maroc.</p>
                <a href="#shop" class="btn btn-light rounded-0 fw-bold px-4">ACHETER MAINTENANT</a>
            </div>
        </div>
    </div>

    <div class="container mb-5" id="shop">
        <h3 class="mb-4 fw-bold">NOS PRODUITS</h3>
        <div class="row g-3">
            {{{{ range .Site.RegularPages }}}}
            <div class="col-6 col-md-3 product-col" data-cat="{{{{ index .Params.categories 0 }}}}">
                <div class="product-card">
                    <span class="badge-promo">-20%</span>
                    <a href="{{{{ .Permalink }}}}" class="img-wrap">
                        <img src="{{{{ .Params.image }}}}" loading="lazy" alt="{{{{ .Title }}}}">
                    </a>
                    <div class="p-3 text-center">
                        <small class="text-muted text-uppercase" style="font-size:10px">{{{{ index .Params.categories 0 }}}}</small>
                        <h6 class="my-2 fw-bold text-dark text-truncate">{{{{ .Title }}}}</h6>
                        <div class="mb-2">
                            <span class="text-decoration-line-through text-muted small">{{{{ .Params.old_price }}}} DH</span>
                            <span class="text-danger fw-bold fs-5">{{{{ .Params.price }}}} DH</span>
                        </div>
                        
                        <button class="btn-add snipcart-add-item"
                            data-item-id="{{{{ .Params.sku }}}}"
                            data-item-price="{{{{ .Params.price }}}}"
                            data-item-url="{{{{ .Permalink }}}}"
                            data-item-name="{{{{ .Title }}}}"
                            data-item-image="{{{{ .Params.image }}}}"
                            data-item-custom1-name="Téléphone"
                            data-item-custom1-required="true">
                            AJOUTER
                        </button>
                    </div>
                </div>
            </div>
            {{{{ end }}}}
        </div>
    </div>
    {{{{ end }}}}

    <footer class="bg-dark text-light">
        <div class="container">
            <div class="row g-4">
                <div class="col-lg-4">
                    <h5 class="text-white">{STORE_NAME}</h5>
                    <p class="text-muted">Votre référence pour les produits d'épicerie fine importés. Qualité garantie.</p>
                </div>
                <div class="col-lg-2">
                    <h5 class="text-white">LIENS</h5>
                    <ul class="list-unstyled">
                        <li><a href="#">Accueil</a></li>
                        <li><a href="#">Boutique</a></li>
                        <li><a href="#">Contact</a></li>
                    </ul>
                </div>
                <div class="col-lg-3">
                    <h5 class="text-white">LÉGAL</h5>
                    <ul class="list-unstyled">
                        <li><a href="#">CGV</a></li>
                        <li><a href="#">Politique de Retour</a></li>
                        <li><a href="#">Livraison</a></li>
                    </ul>
                </div>
                <div class="col-lg-3">
                    <h5 class="text-white">PAIEMENT</h5>
                    <div class="fs-2 text-muted">
                        <i class="fab fa-cc-visa"></i> <i class="fab fa-cc-mastercard"></i> <i class="fas fa-money-bill-wave"></i>
                    </div>
                </div>
            </div>
            <div class="border-top border-secondary mt-5 pt-4 text-center text-muted small">
                &copy; 2025 {STORE_NAME}. Tous droits réservés.
            </div>
        </div>
    </footer>

    {scripts}
</body>
</html>
    """

    # --- PRODUCT DETAIL PAGE (P0: Detailed View) ---
    single_html = f"""
<!doctype html>
<html lang="fr">
{head}
<body style="background: #fff;">

    <nav class="navbar border-bottom sticky-top bg-white">
        <div class="container">
            <a href="/" class="text-dark fw-bold text-decoration-none"><i class="fas fa-arrow-left me-2"></i> RETOUR</a>
            <button class="btn btn-dark rounded-0 snipcart-checkout">PANIER <span class="snipcart-items-count">0</span></button>
        </div>
    </nav>

    <div class="container py-5">
        <div class="row gx-5">
            <div class="col-md-6 mb-4">
                <div class="border p-5 text-center bg-white rounded-3">
                    <img src="{{{{ .Params.image }}}}" class="img-fluid" style="max-height: 500px;">
                </div>
            </div>

            <div class="col-md-6">
                <span class="badge bg-secondary mb-2">{{{{ index .Params.categories 0 }}}}</span>
                <h1 class="display-5 fw-bold mb-3">{{{{ .Title }}}}</h1>
                
                <div class="mb-3 text-warning">
                    <i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i>
                    <span class="text-dark small ms-2">(Avis Clients)</span>
                </div>

                <div class="h2 text-danger fw-bold mb-4">{{{{ .Params.price }}}} MAD</div>
                
                <ul class="nav nav-tabs mb-3" id="myTab">
                    <li class="nav-item"><button class="nav-link active" data-bs-toggle="tab" data-bs-target="#desc">Description</button></li>
                    <li class="nav-item"><button class="nav-link" data-bs-toggle="tab" data-bs-target="#ship">Livraison</button></li>
                </ul>
                <div class="tab-content mb-4 p-3 border border-top-0 rounded-bottom">
                    <div class="tab-pane fade show active" id="desc">
                        {{{{ .Content }}}}
                        <br><br><strong>Ingrédients:</strong> Sucre, Cacao, Lait (Exemple).
                    </div>
                    <div class="tab-pane fade" id="ship">
                        <i class="fas fa-truck text-success me-2"></i> Expédié sous 24h.
                        <br>Livraison à domicile via Amana ou Coursier.
                    </div>
                </div>

                <div class="d-grid gap-2 mb-3">
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
                    
                    <a href="https://wa.me/{WHATSAPP_NUMBER}?text=Je veux commander: {{{{ .Title }}}}" target="_blank" class="btn btn-success rounded-0 fw-bold">
                        <i class="fab fa-whatsapp me-2"></i> COMMANDER SUR WHATSAPP
                    </a>
                </div>
            </div>
        </div>
        
        <div class="mt-5 pt-5 border-top">
            <h3 class="fw-bold mb-4">VOUS AIMEREZ AUSSI</h3>
            <div class="row g-3">
                {{{{ range first 4 (where .Site.RegularPages "Type" "products") }}}}
                <div class="col-6 col-md-3">
                    <div class="product-card">
                        <a href="{{{{ .Permalink }}}}" class="img-wrap">
                            <img src="{{{{ .Params.image }}}}" loading="lazy">
                        </a>
                        <div class="p-3 text-center">
                            <h6 class="fw-bold text-truncate">{{{{ .Title }}}}</h6>
                            <div class="text-danger fw-bold">{{{{ .Params.price }}}} MAD</div>
                        </div>
                    </div>
                </div>
                {{{{ end }}}}
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
    upgrade_styles()
    upgrade_layouts()
    print("✅ UPGRADE COMPLETE. Your products are safe.")
    print("1. Run 'hugo' to rebuild.")
    print("2. Commit & Push to GitHub.")