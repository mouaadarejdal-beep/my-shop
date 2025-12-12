import os
import re

# --- YOUR SPECIFIC DATA ---
STORE_NAME = "MECADO"
PRIMARY_COLOR = "#d04f27"  # The El Mercado Orange
SECONDARY_COLOR = "#222222"
SNIPCART_KEY = "OWUxZTM0MzItNjA5MC00YmYxLWE1YmItZmRiMmFmZTRmMzY1NjM3NDc2Njk1Nzc4OTIwNDY0"

CONTACTS = {
    "fb": "https://www.facebook.com/share/1Bq4qfh8Uj/",
    "email": "mouaadarejdal@gmail.com",
    "phone": "07 20 49 81 10",
    "whatsapp_api": "212720498110"
}

# Paths
BASE_DIR = os.getcwd()
CONTENT_DIR = os.path.join(BASE_DIR, "content", "products")
LAYOUT_DIR = os.path.join(BASE_DIR, "layouts")
DEFAULT_DIR = os.path.join(LAYOUT_DIR, "_default")
STATIC_CSS = os.path.join(BASE_DIR, "static", "css")

# --- STEP 1: FIX PRODUCT CATEGORIES ---
def categorize_products():
    print("--- 1. Organizing Products into Categories ---")
    if not os.path.exists(CONTENT_DIR):
        print("❌ Error: Content folder missing. Are you in the right directory?")
        return

    files = [f for f in os.listdir(CONTENT_DIR) if f.endswith(".md")]
    count = 0

    for filename in files:
        filepath = os.path.join(CONTENT_DIR, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # Guess category from filename
        lower_name = filename.lower()
        new_cat = "Nouveautés" # Default
        
        if any(x in lower_name for x in ['jus', 'coca', 'soda', 'eau', 'cafe', 'coffee', 'the', 'tea', 'drink', 'boisson', 'nescafe', 'starbucks']): 
            new_cat = "Boissons"
        elif any(x in lower_name for x in ['choco', 'bonbon', 'biscuit', 'cookie', 'sucre', 'gateau', 'nutella', 'milka', 'kinder', 'oreo', 'twix']): 
            new_cat = "Sucrées"
        elif any(x in lower_name for x in ['chips', 'sale', 'apero', 'cracker', 'pringles', 'doritos', 'nuts']): 
            new_cat = "Salées"
        elif any(x in lower_name for x in ['pate', 'pasta', 'riz', 'rice', 'huile', 'oil', 'sauce', 'conserve', 'thon']): 
            new_cat = "Courses"

        # Replace the category line using Regex
        # Looks for: categories: ["Something"] -> Replaces with: categories: ["NewCat"]
        new_content = re.sub(r'categories:\s*\[".*?"\]', f'categories: ["{new_cat}"]', content)
        
        # Ensure draft is false
        new_content = new_content.replace("draft: true", "draft: false")

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)
        count += 1

    print(f"✅ Organized {count} products into correct shelves.")

# --- STEP 2: CREATE THE DESIGN (CSS) ---
def create_styles():
    print("--- 2. Creating 'El Mercado' Style ---")
    os.makedirs(STATIC_CSS, exist_ok=True)
    
    css = f"""
    @import url('https://fonts.googleapis.com/css2?family=Exo:wght@400;600;700;800&family=Inter:wght@400;600&display=swap');
    
    :root {{ --primary: {PRIMARY_COLOR}; --dark: {SECONDARY_COLOR}; --bg: #ffffff; }}
    
    body {{ font-family: 'Inter', sans-serif; color: #444; background: #fdfdfd; }}
    h1, h2, h3, h4, h5, .nav-link, .btn {{ font-family: 'Exo', sans-serif; text-transform: uppercase; }}
    
    /* HEADER */
    .top-bar {{ background: var(--dark); color: white; font-size: 12px; padding: 8px 0; font-weight: 600; }}
    .site-header {{ background: white; padding: 20px 0; border-bottom: 1px solid #eee; }}
    .logo {{ font-size: 32px; font-weight: 800; color: #000; text-decoration: none; letter-spacing: -1px; }}
    .logo span {{ color: var(--primary); }}
    
    /* NAV */
    .cat-nav {{ background: white; border-bottom: 2px solid #f0f0f0; overflow-x: auto; white-space: nowrap; }}
    .nav-link {{ color: #333 !important; font-weight: 700; font-size: 13px; padding: 15px 20px !important; }}
    .nav-link:hover, .nav-link.active {{ color: var(--primary) !important; background: #f9f9f9; }}
    
    /* CARDS */
    .product-card {{ 
        background: white; border: 1px solid #f0f0f0; border-radius: 8px; 
        transition: 0.3s; position: relative; height: 100%; overflow: hidden; 
    }}
    .product-card:hover {{ border-color: var(--primary); box-shadow: 0 10px 25px rgba(0,0,0,0.08); transform: translateY(-3px); }}
    
    .card-img-wrap {{ position: relative; padding-top: 100%; display: block; overflow: hidden; }}
    .card-img-wrap img {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; object-fit: contain; padding: 20px; transition: 0.5s; }}
    .product-card:hover img {{ transform: scale(1.08); }}
    
    .btn-add {{ 
        width: 100%; background: white; color: var(--dark); border: 2px solid var(--dark);
        padding: 8px; font-weight: 700; font-size: 12px; margin-top: 10px; transition: 0.2s;
    }}
    .btn-add:hover {{ background: var(--primary); border-color: var(--primary); color: white; }}
    
    /* FOOTER */
    footer {{ background: #1a1a1a; color: #bbb; padding: 60px 0; margin-top: 60px; font-size: 13px; }}
    footer h5 {{ color: white; margin-bottom: 20px; }}
    footer a {{ color: #bbb; text-decoration: none; }}
    footer a:hover {{ color: var(--primary); }}
    """
    with open(os.path.join(STATIC_CSS, "style.css"), "w", encoding="utf-8") as f:
        f.write(css)

# --- STEP 3: CREATE LAYOUTS ---
def create_layouts():
    print("--- 3. Building Pages ---")
    os.makedirs(DEFAULT_DIR, exist_ok=True)
    
    # Common Head
    head = f"""
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>{STORE_NAME} | Boutique</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <link rel="stylesheet" href="/css/style.css">
        <link rel="stylesheet" href="https://cdn.snipcart.com/themes/v3.7.2/default/snipcart.css" />
    </head>
    """
    
    scripts = f"""
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script async src="https://cdn.snipcart.com/themes/v3.7.2/default/snipcart.js"></script>
    <div hidden id="snipcart" data-api-key="{SNIPCART_KEY}" data-config-modal-style="side"></div>
    
    <script>
        function filter(cat) {{
            // Hide/Show products
            document.querySelectorAll('.product-col').forEach(el => {{
                el.style.display = (cat === 'all' || el.dataset.cat === cat) ? 'block' : 'none';
            }});
            // Update buttons
            document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active', 'text-danger'));
            event.target.classList.add('active');
        }}
        
        function liveSearch() {{
            let q = document.getElementById('searchInput').value.toLowerCase();
            document.querySelectorAll('.product-col').forEach(el => {{
                let title = el.dataset.title;
                el.style.display = title.includes(q) ? 'block' : 'none';
            }});
        }}
    </script>
    """

    # INDEX.HTML
    index_html = f"""
<!doctype html>
<html lang="fr">
{head}
<body>

    <div class="top-bar">
        <div class="container d-flex justify-content-between">
            <span><i class="fas fa-truck"></i> LIVRAISON PARTOUT AU MAROC</span>
            <span><i class="fab fa-whatsapp"></i> {CONTACTS['phone']}</span>
        </div>
    </div>

    <header class="site-header sticky-top">
        <div class="container">
            <div class="row align-items-center">
                <div class="col-6 col-md-3">
                    <a href="/" class="logo">{STORE_NAME}<span>.</span></a>
                </div>
                <div class="col-md-6 d-none d-md-block">
                    <div class="input-group">
                        <input type="text" id="searchInput" class="form-control rounded-0" placeholder="Rechercher (ex: Milka)..." onkeyup="liveSearch()">
                        <button class="btn btn-dark rounded-0"><i class="fas fa-search"></i></button>
                    </div>
                </div>
                <div class="col-6 col-md-3 text-end">
                    <button class="btn btn-outline-dark fw-bold rounded-0 snipcart-checkout">
                        <i class="fas fa-shopping-basket"></i> PANIER <span class="badge bg-danger rounded-pill snipcart-items-count">0</span>
                    </button>
                </div>
            </div>
            <div class="d-md-none mt-3">
                <input type="text" class="form-control rounded-0" placeholder="Rechercher..." onkeyup="liveSearch()">
            </div>
        </div>
    </header>

    <div class="cat-nav sticky-top" style="top: 85px; z-index: 900;">
        <div class="container">
            <ul class="nav">
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
        
        <div class="rounded-3 p-5 mb-5 text-white d-flex align-items-center" style="background: linear-gradient(45deg, #111, {PRIMARY_COLOR}); min-height: 250px;">
            <div>
                <span class="badge bg-warning text-dark mb-2">ARRIVAGE</span>
                <h1 class="display-4 fw-bold">NOUVEAUTÉS IMPORTÉES</h1>
                <p class="lead">Le meilleur de l'épicerie fine chez vous.</p>
            </div>
        </div>

        <div class="row g-3 g-md-4">
            {{{{ range .Site.RegularPages }}}}
            <div class="col-6 col-md-3 product-col" data-cat="{{{{ index .Params.categories 0 }}}}" data-title="{{{{ lower .Title }}}}">
                <div class="product-card h-100">
                    <a href="{{{{ .Permalink }}}}" class="card-img-wrap">
                        <img src="{{{{ .Params.image }}}}" loading="lazy">
                    </a>
                    <div class="p-3 text-center d-flex flex-column flex-grow-1">
                        <small class="text-muted text-uppercase" style="font-size:10px">{{{{ index .Params.categories 0 }}}}</small>
                        <h6 class="fw-bold text-dark my-2 text-truncate">{{{{ .Title }}}}</h6>
                        
                        <div class="mb-auto">
                            <span class="text-danger fw-bold fs-5">{{{{ .Params.price }}}} DH</span>
                        </div>

                        <div class="mt-3">
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
            </div>
            {{{{ end }}}}
        </div>
    </div>
    {{{{ end }}}}

    <footer>
        <div class="container">
            <div class="row g-4">
                <div class="col-md-4">
                    <h5 class="text-white">{STORE_NAME}</h5>
                    <p>Votre épicerie fine en ligne au Maroc. Produits authentiques et livraison rapide.</p>
                    <div class="d-flex gap-3 fs-4">
                        <a href="{CONTACTS['fb']}" target="_blank"><i class="fab fa-facebook"></i></a>
                        <a href="https://wa.me/{CONTACTS['whatsapp_api']}" target="_blank"><i class="fab fa-whatsapp"></i></a>
                    </div>
                </div>
                <div class="col-md-4">
                    <h5 class="text-white">CONTACT</h5>
                    <ul class="list-unstyled">
                        <li><i class="fas fa-phone me-2"></i> {CONTACTS['phone']}</li>
                        <li><i class="fas fa-envelope me-2"></i> {CONTACTS['email']}</li>
                    </ul>
                </div>
                <div class="col-md-4">
                    <h5 class="text-white">PAIEMENT</h5>
                    <div class="fs-2 text-muted">
                        <i class="fab fa-cc-visa"></i> <i class="fab fa-cc-mastercard"></i> <i class="fas fa-money-bill"></i>
                    </div>
                </div>
            </div>
            <div class="text-center mt-5 pt-3 border-top border-secondary">© 2025 {STORE_NAME}</div>
        </div>
    </footer>

    {scripts}
</body>
</html>
    """

    # SINGLE.HTML (Product Window)
    single_html = f"""
<!doctype html>
<html lang="fr">
{head}
<body style="background: #fff;">

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
                <div class="border p-5 rounded">
                    <img src="{{{{ .Params.image }}}}" class="img-fluid" style="max-height: 500px;">
                </div>
            </div>
            <div class="col-md-6">
                <span class="badge bg-secondary mb-2">{{{{ index .Params.categories 0 }}}}</span>
                <h1 class="fw-bold mb-3" style="font-family:'Exo';">{{{{ .Title }}}}</h1>
                <div class="h2 text-danger fw-bold mb-4">{{{{ .Params.price }}}} MAD</div>
                
                <p class="lead text-muted mb-4" style="font-size: 15px;">
                    {{{{ .Content }}}}
                    <br><br>
                    Produit disponible en stock.
                </p>

                <div class="d-grid gap-2">
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
                    <a href="https://wa.me/{CONTACTS['whatsapp_api']}?text=Je veux commander: {{{{ .Title }}}}" class="btn btn-success btn-lg rounded-0 fw-bold">
                        <i class="fab fa-whatsapp me-2"></i> COMMANDER SUR WHATSAPP
                    </a>
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
    categorize_products()
    create_styles()
    create_layouts()
    print("✅ SURGICAL FIX COMPLETE.")
    print("1. Run 'hugo'")
    print("2. Commit and Push")