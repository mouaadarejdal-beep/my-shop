
    document.addEventListener('DOMContentLoaded', () => {
        
        // 1. SEARCH & FILTER LOGIC
        const searchInput = document.getElementById('searchInput');
        const filterBtns = document.querySelectorAll('.filter-chip');
        const products = document.querySelectorAll('.product-item');
        
        if(searchInput) {
            searchInput.addEventListener('input', (e) => {
                const term = e.target.value.toLowerCase();
                products.forEach(p => {
                    const title = p.dataset.title.toLowerCase();
                    p.style.display = title.includes(term) ? 'block' : 'none';
                });
            });
        }
        
        filterBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                // Active State
                filterBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                
                const cat = btn.dataset.cat;
                products.forEach(p => {
                    if(cat === 'all' || p.dataset.cat === cat) {
                        p.style.display = 'block';
                    } else {
                        p.style.display = 'none';
                    }
                });
            });
        });

        // 2. SHIPPING PROGRESS LOGIC (Simulated)
        // Snipcart events can hook here for real data
        const bar = document.getElementById('shippingBar');
        if(bar) {
            setTimeout(() => { bar.style.width = '35%'; }, 1000);
        }
    });
    