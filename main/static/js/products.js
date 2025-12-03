/**
 * Product Manager Class
 * Handles fetching, filtering, sorting, and displaying products via API
 */
class ProductManager {
    constructor() {
        // API Configuration
        this.apiBaseUrl = '/api/products/';
        this.currentPage = 1;
        this.currentFilters = {
            search: '',
            category: '',
            minPrice: '',
            maxPrice: '',
            size: [],
            color: [],
            ordering: '-created_at'
        };

        // DOM Elements
        this.gridElement = document.getElementById('product-grid');
        this.paginationElement = document.getElementById('pagination');
        this.countElement = document.getElementById('product-count');
        this.activeFiltersElement = document.getElementById('active-filters');
        this.categoryListElement = document.getElementById('category-list');

        // Inputs
        this.minPriceInput = document.getElementById('min-price');
        this.maxPriceInput = document.getElementById('max-price');
        this.sortSelect = document.getElementById('sort-select');

        // Buttons
        this.applyPriceBtn = document.getElementById('apply-price');
        this.clearFiltersBtn = document.getElementById('clear-filters');

        if (!this.gridElement) {
            console.error('Product grid element not found!');
            return;
        }

        this.init();
    }

    init() {
        this.loadCategories();
        this.loadProducts();
        this.setupEventListeners();
        this.checkUrlParams();
    }

    setupEventListeners() {
        // Price Filter
        if (this.applyPriceBtn) {
            this.applyPriceBtn.addEventListener('click', () => {
                this.currentFilters.minPrice = this.minPriceInput.value;
                this.currentFilters.maxPrice = this.maxPriceInput.value;
                this.currentPage = 1;
                this.loadProducts();
            });
        }

        // Sorting
        if (this.sortSelect) {
            this.sortSelect.addEventListener('change', (e) => {
                this.currentFilters.ordering = e.target.value;
                this.currentPage = 1;
                this.loadProducts();
            });
        }

        // Size Filter Checkboxes
        const sizeCheckboxes = document.querySelectorAll('input[name="size"]');
        sizeCheckboxes.forEach(checkbox => {
            checkbox.addEventListener('change', () => {
                this.updateArrayFilter('size', checkbox.value, checkbox.checked);
                this.currentPage = 1;
                this.loadProducts();
            });
        });

        // Color Filter Checkboxes
        const colorCheckboxes = document.querySelectorAll('input[name="color"]');
        colorCheckboxes.forEach(checkbox => {
            checkbox.addEventListener('change', () => {
                this.updateArrayFilter('color', checkbox.value, checkbox.checked);
                this.currentPage = 1;
                this.loadProducts();
            });
        });

        // Clear Filters
        if (this.clearFiltersBtn) {
            this.clearFiltersBtn.addEventListener('click', () => {
                this.resetFilters();
            });
        }
    }

    checkUrlParams() {
        const urlParams = new URLSearchParams(window.location.search);
        const category = urlParams.get('category');

        if (category) {
            this.currentFilters.category = category;
        }
    }

    resetFilters() {
        this.currentFilters = {
            search: '',
            category: '',
            minPrice: '',
            maxPrice: '',
            size: [],
            color: [],
            ordering: '-created_at'
        };

        // Reset UI
        if (this.minPriceInput) this.minPriceInput.value = '';
        if (this.maxPriceInput) this.maxPriceInput.value = '';
        if (this.sortSelect) this.sortSelect.value = '-created_at';

        // Uncheck all size and color checkboxes
        document.querySelectorAll('input[name="size"]').forEach(cb => cb.checked = false);
        document.querySelectorAll('input[name="color"]').forEach(cb => cb.checked = false);

        // Remove active class from categories
        document.querySelectorAll('.category-item').forEach(item => {
            item.classList.remove('active');
        });

        this.currentPage = 1;
        this.loadProducts();
    }

    updateArrayFilter(filterName, value, isChecked) {
        if (isChecked) {
            // Add value if not already present
            if (!this.currentFilters[filterName].includes(value)) {
                this.currentFilters[filterName].push(value);
            }
        } else {
            // Remove value
            this.currentFilters[filterName] = this.currentFilters[filterName].filter(v => v !== value);
        }
    }

    async loadCategories() {
        try {
            const response = await fetch('/api/categories/');
            const categories = await response.json();

            this.renderCategories(categories);
        } catch (error) {
            console.error('Error loading categories:', error);
            if (this.categoryListElement) {
                this.categoryListElement.innerHTML = '<li class="error-msg">Failed to load categories</li>';
            }
        }
    }

    renderCategories(categories) {
        if (!this.categoryListElement) return;

        // Add "All Categories" option
        let html = `
            <li class="category-item ${!this.currentFilters.category ? 'active' : ''}" data-slug="">
                <span>All Categories</span>
            </li>
        `;

        categories.forEach(cat => {
            const isActive = this.currentFilters.category === cat.slug;
            html += `
                <li class="category-item ${isActive ? 'active' : ''}" data-slug="${cat.slug}">
                    <span>${cat.name}</span>
                </li>
            `;
        });

        this.categoryListElement.innerHTML = html;

        // Add click listeners
        document.querySelectorAll('.category-item').forEach(item => {
            item.addEventListener('click', () => {
                // Update active state
                document.querySelectorAll('.category-item').forEach(i => i.classList.remove('active'));
                item.classList.add('active');

                // Update filter
                this.currentFilters.category = item.dataset.slug;
                this.currentPage = 1;
                this.loadProducts();
            });
        });
    }

    async loadProducts() {
        this.showLoading();
        this.updateActiveFilters();

        try {
            // Build query string
            const params = new URLSearchParams();
            params.append('page', this.currentPage);

            if (this.currentFilters.search) params.append('search', this.currentFilters.search);
            if (this.currentFilters.category) params.append('category__slug', this.currentFilters.category);
            if (this.currentFilters.ordering) params.append('ordering', this.currentFilters.ordering);
            if (this.currentFilters.minPrice) params.append('min_price', this.currentFilters.minPrice);
            if (this.currentFilters.maxPrice) params.append('max_price', this.currentFilters.maxPrice);

            // Add size filter (only first selected size for now)
            if (this.currentFilters.size.length > 0) {
                params.append('size', this.currentFilters.size[0]);
            }

            // Add color filter (only first selected color for now)
            if (this.currentFilters.color.length > 0) {
                params.append('color', this.currentFilters.color[0]);
            }

            const url = `${this.apiBaseUrl}?${params.toString()}`;
            const response = await fetch(url);

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();

            if (!data.results) {
                throw new Error('Invalid data format: results missing');
            }

            this.renderProducts(data.results);
            this.renderPagination(data);

            if (this.countElement) {
                this.countElement.textContent = `Showing ${data.results.length} of ${data.count} products`;
            }

        } catch (error) {
            console.error('Error loading products:', error);
            this.gridElement.innerHTML = `
                <div class="error-state">
                    <p>Failed to load products. ${error.message}</p>
                    <button class="btn btn-sm" onclick="productManager.loadProducts()">Retry</button>
                </div>
            `;
        }
    }

    showLoading() {
        this.gridElement.innerHTML = `
            <div class="loading-spinner">
                <div class="spinner"></div>
                <p>Loading products...</p>
            </div>
        `;
    }

    updateActiveFilters() {
        if (!this.activeFiltersElement) return;

        let html = '';
        if (this.currentFilters.search) {
            html += `
                <span class="filter-tag">
                    Search: ${this.currentFilters.search}
                    <i class="fas fa-times" onclick="productManager.clearFilter('search')"></i>
                </span>
            `;
        }

        if (this.currentFilters.minPrice || this.currentFilters.maxPrice) {
            const range = `${this.currentFilters.minPrice || '0'} - ${this.currentFilters.maxPrice || '∞'}`;
            html += `
                <span class="filter-tag">
                    Price: $${range}
                    <i class="fas fa-times" onclick="productManager.clearFilter('price')"></i>
                </span>
            `;
        }

        this.activeFiltersElement.innerHTML = html;
    }

    clearFilter(type) {
        if (type === 'search') {
            this.currentFilters.search = '';
        } else if (type === 'price') {
            this.currentFilters.minPrice = '';
            this.currentFilters.maxPrice = '';
            if (this.minPriceInput) this.minPriceInput.value = '';
            if (this.maxPriceInput) this.maxPriceInput.value = '';
        }
        this.currentPage = 1;
        this.loadProducts();
    }

    renderProducts(products) {
        if (products.length === 0) {
            this.gridElement.innerHTML = `
                <div class="empty-state">
                    <i class="fas fa-search"></i>
                    <h3>No products found</h3>
                    <p>Try adjusting your filters or search terms</p>
                </div>
            `;
            return;
        }

        // Client-side price filtering if needed
        let filteredProducts = products;
        if (this.currentFilters.minPrice) {
            filteredProducts = filteredProducts.filter(p => parseFloat(p.price) >= parseFloat(this.currentFilters.minPrice));
        }
        if (this.currentFilters.maxPrice) {
            filteredProducts = filteredProducts.filter(p => parseFloat(p.price) <= parseFloat(this.currentFilters.maxPrice));
        }

        if (filteredProducts.length === 0) {
            this.gridElement.innerHTML = `
                <div class="empty-state">
                    <p>No products found in this price range.</p>
                </div>
            `;
            return;
        }

        this.gridElement.innerHTML = filteredProducts.map(product => this.createProductCard(product)).join('');

        // Add event listeners for "Quick Add" buttons
        document.querySelectorAll('.quick-add-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                const productId = btn.dataset.id;
                this.addToCart(productId);
            });
        });
    }

    createProductCard(product) {
        // Calculate discount if original price exists
        let discountBadge = '';
        if (product.original_price && product.original_price > product.price) {
            const discount = Math.round(((product.original_price - product.price) / product.original_price) * 100);
            discountBadge = `<span class="product-badge">${discount}% OFF</span>`;
        } else if (product.is_new) {
            discountBadge = `<span class="product-badge">NEW</span>`;
        }

        // Create color swatches (mock data - replace with actual product colors)
        const colorSwatches = `
            <div class="color-swatches">
                <span class="color-circle" style="background: #212a2f" title="Classic Black"></span>
                <span class="color-circle" style="background: #e5e5e5" title="Mist Grey"></span>
                <span class="color-circle" style="background: #f5f5f5" title="Natural White"></span>
                <span class="color-count">+${Math.floor(Math.random() * 5) + 3}</span>
            </div>
        `;

        // Build pricing section
        let priceHTML = `<div class="product-price">$${product.price}`;
        if (product.original_price && product.original_price > product.price) {
            priceHTML += `<span class="original-price">$${product.original_price}</span>`;
        }
        priceHTML += `</div>`;

        return `
            <div class="product-card">
                <div class="product-image-wrapper">
                    ${discountBadge}
                    <a href="/product/${product.id}/" class="product-card-link">
                        <img src="${product.image || '/static/images/placeholder.png'}" alt="${product.name}" class="product-image">
                    </a>
                    <button class="quick-add-btn" data-id="${product.id}">Quick Add</button>
                </div>
                <div class="product-info">
                    <a href="/product/${product.id}/" class="product-card-link" style="text-decoration: none; color: inherit;">
                        <h3 class="product-title">${product.name}</h3>
                        <p class="product-color-variant">${product.color_name || product.category_name || 'Classic Color'}</p>
                    </a>
                    ${colorSwatches}
                    <div class="product-footer">
                        ${priceHTML}
                    </div>
                </div>
            </div>
        `;
    }

    renderPagination(data) {
        if (!data.next && !data.previous) {
            this.paginationElement.innerHTML = '';
            return;
        }

        let html = '';

        // Previous Button
        html += `
        <button class="pagination-btn" 
                ${!data.previous ? 'disabled' : ''}
                onclick="productManager.changePage(${this.currentPage - 1})">
            <i class="fas fa-chevron-left"></i>
        </button>
        `;

        // Page Numbers (Simplified)
        const totalPages = Math.ceil(data.count / 20); // Assuming page size 20
        for (let i = 1; i <= totalPages; i++) {
            if (i === 1 || i === totalPages || (i >= this.currentPage - 1 && i <= this.currentPage + 1)) {
                html += `
                <button class="pagination-btn ${i === this.currentPage ? 'active' : ''}"
                        onclick="productManager.changePage(${i})">
                    ${i}
                </button>
                `;
            } else if (i === this.currentPage - 2 || i === this.currentPage + 2) {
                html += `<span class="pagination-dots">...</span>`;
            }
        }

        // Next Button
        html += `
        <button class="pagination-btn" 
                ${!data.next ? 'disabled' : ''}
                onclick="productManager.changePage(${this.currentPage + 1})">
            <i class="fas fa-chevron-right"></i>
        </button>
        `;

        this.paginationElement.innerHTML = html;
    }

    changePage(page) {
        this.currentPage = page;
        this.loadProducts();
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    async addToCart(productId) {
        try {
            const response = await fetch('/api/cart/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCookie('csrftoken')
                },
                body: JSON.stringify({
                    product: productId,
                    quantity: 1
                })
            });

            if (response.ok) {
                // Show success message
                const btn = document.querySelector(`.quick-add-btn[data-id="${productId}"]`);
                const originalText = btn.textContent;
                btn.textContent = 'Added!';
                btn.style.backgroundColor = '#4CAF50';

                setTimeout(() => {
                    btn.textContent = originalText;
                    btn.style.backgroundColor = '';
                }, 2000);

                // Update cart count if exists
                this.updateCartCount();
            } else {
                const data = await response.json();
                console.error('Server Error:', data);
                alert(`Failed to add to cart: ${JSON.stringify(data)}`);
            }
        } catch (error) {
            console.error('Error adding to cart:', error);
            alert('Error adding to cart. Check console for details.');
        }
    }

    async updateCartCount() {
        try {
            const response = await fetch('/api/cart/');
            const data = await response.json();
            const countElement = document.querySelector('.cart-count');
            if (countElement) {
                countElement.textContent = data.items.length;
            }
        } catch (error) {
            console.error('Error updating cart count:', error);
        }
    }

    getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    window.productManager = new ProductManager();
});
