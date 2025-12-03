// ===================================
// ALLBIRDS-STYLE JAVASCRIPT
// Navigation, Cart, Search Functionality
// ===================================

document.addEventListener('DOMContentLoaded', function () {
    console.log('Allbirds-style website loaded');

    // ===================================
    // MOBILE MENU TOGGLE
    // ===================================
    const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
    const navMenu = document.querySelector('.nav-menu');
    const navItems = document.querySelectorAll('.nav-item.has-mega-menu');

    if (mobileMenuToggle) {
        mobileMenuToggle.addEventListener('click', function () {
            navMenu.classList.toggle('active');
            this.classList.toggle('active');
        });
    }

    // Mobile mega menu toggle
    navItems.forEach(item => {
        const link = item.querySelector('.nav-link');
        if (link && window.innerWidth <= 768) {
            link.addEventListener('click', function (e) {
                if (window.innerWidth <= 768) {
                    e.preventDefault();
                    item.classList.toggle('active');
                }
            });
        }
    });

    // ===================================
    // SEARCH FUNCTIONALITY
    // ===================================
    const searchBtn = document.querySelector('.search-btn');
    const searchOverlay = document.getElementById('searchOverlay');
    const closeSearchBtn = document.getElementById('closeSearchBtn');
    const searchInput = document.getElementById('searchInput');

    function openSearch() {
        if (searchOverlay) {
            searchOverlay.classList.add('active');
            setTimeout(() => {
                if (searchInput) searchInput.focus();
            }, 100);
        }
    }

    function closeSearch() {
        if (searchOverlay) {
            searchOverlay.classList.remove('active');
            if (searchInput) searchInput.value = '';
        }
    }

    if (searchBtn) {
        searchBtn.addEventListener('click', openSearch);
    }

    if (closeSearchBtn) {
        closeSearchBtn.addEventListener('click', closeSearch);
    }

    // Close search on Escape key
    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && searchOverlay && searchOverlay.classList.contains('active')) {
            closeSearch();
        }
    });

    // ===================================
    // CART PANEL FUNCTIONALITY
    // ===================================
    const openCartBtn = document.getElementById('openCartBtn');
    const closeCartBtn = document.getElementById('closeCartBtn');
    const cartPanel = document.getElementById('cartPanel');
    const cartOverlay = document.getElementById('cartOverlay');

    function openCart() {
        if (cartPanel && cartOverlay) {
            cartPanel.classList.add('active');
            cartOverlay.classList.add('active');
            document.body.style.overflow = 'hidden';
            fetchCart();
        }
    }

    function closeCart() {
        if (cartPanel && cartOverlay) {
            cartPanel.classList.remove('active');
            cartOverlay.classList.remove('active');
            document.body.style.overflow = '';
        }
    }

    if (openCartBtn) {
        openCartBtn.addEventListener('click', function (e) {
            e.preventDefault();
            openCart();
        });
    }

    if (closeCartBtn) {
        closeCartBtn.addEventListener('click', closeCart);
    }

    if (cartOverlay) {
        cartOverlay.addEventListener('click', closeCart);
    }

    // Close cart on Escape key
    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && cartPanel && cartPanel.classList.contains('active')) {
            closeCart();
        }
    });

    // ===================================
    // CART API & RENDERING
    // ===================================
    async function fetchCart() {
        try {
            const response = await fetch('/api/cart/');
            const data = await response.json();

            renderCartItems(data.items);
            updateCartCount(data.count || (data.items ? data.items.length : 0));
        } catch (error) {
            console.error('Error fetching cart:', error);
        }
    }

    function renderCartItems(items) {
        const cartItemsContainer = document.getElementById('cartItems');
        const cartEmptyState = document.getElementById('cartEmptyState');
        const cartFooter = document.getElementById('cartFooter');
        const subtotalElement = document.querySelector('.subtotal-amount');

        if (!items || items.length === 0) {
            if (cartItemsContainer) cartItemsContainer.style.display = 'none';
            if (cartEmptyState) cartEmptyState.style.display = 'block';
            if (cartFooter) cartFooter.style.display = 'none';
            return;
        }

        if (cartItemsContainer) cartItemsContainer.style.display = 'block';
        if (cartEmptyState) cartEmptyState.style.display = 'none';
        if (cartFooter) cartFooter.style.display = 'block';

        let html = '';
        let subtotal = 0;

        items.forEach(item => {
            const price = parseFloat(item.product_price || 0);
            const total = price * item.quantity;
            subtotal += total;

            const variantInfo = [];
            if (item.color) variantInfo.push(`Color: ${item.color}`);
            if (item.size) variantInfo.push(`Size: UK ${item.size}`);
            const variantString = variantInfo.length > 0 ? variantInfo.join(', ') : '';

            html += `
                <div class="cart-item" style="display: flex; gap: 15px; margin-bottom: 20px; padding-bottom: 20px; border-bottom: 1px solid #eee;">
                    <div class="cart-item-image" style="width: 80px; height: 80px; background: #f5f5f5;">
                        <img src="${item.product_image || '/static/images/placeholder.png'}" alt="${item.product_name}" style="width: 100%; height: 100%; object-fit: cover;">
                    </div>
                    <div class="cart-item-details" style="flex: 1;">
                        <h4 style="margin: 0 0 5px; font-size: 14px;">${item.product_name}</h4>
                        <p class="cart-item-price" style="margin: 0 0 5px; color: #666;">$${price.toFixed(2)}</p>
                        ${variantString ? `<p style="margin: 0 0 10px; font-size: 12px; color: #888;">${variantString}</p>` : ''}
                        <div class="cart-item-controls" style="display: flex; justify-content: space-between; align-items: center;">
                            <div class="quantity-control" style="display: flex; align-items: center; gap: 10px; border: 1px solid #ddd; padding: 2px 8px;">
                                <button onclick="updateCartItem('${item.product_id}', ${item.quantity - 1}, '${item.size || ''}', '${item.color || ''}')" style="border: none; background: none; cursor: pointer;">-</button>
                                <span>${item.quantity}</span>
                                <button onclick="updateCartItem('${item.product_id}', ${item.quantity + 1}, '${item.size || ''}', '${item.color || ''}')" style="border: none; background: none; cursor: pointer;">+</button>
                            </div>
                            <button class="remove-item" onclick="removeCartItem('${item.product_id}', '${item.size || ''}', '${item.color || ''}')" style="border: none; background: none; text-decoration: underline; color: #999; cursor: pointer; font-size: 12px;">Remove</button>
                        </div>
                    </div>
                </div>
            `;
        });

        if (cartItemsContainer) cartItemsContainer.innerHTML = html;
        if (subtotalElement) subtotalElement.textContent = '$' + subtotal.toFixed(2);

        const progressBar = document.querySelector('.shipping-progress-fill');
        if (progressBar) {
            const percentage = Math.min((subtotal / 75) * 100, 100);
            progressBar.style.width = percentage + '%';
        }
    }

    function updateCartCount(count) {
        const cartCountElements = document.querySelectorAll('.cart-count, .cart-item-count');
        cartCountElements.forEach(element => {
            element.textContent = count;
        });
    }

    // ===================================
    // GLOBAL CART FUNCTIONS
    // ===================================
    window.updateCartItem = async function (productId, newQuantity, size, color) {
        if (newQuantity < 1) {
            return;
        }

        try {
            const response = await fetch('/api/cart/', {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({
                    product_id: productId,
                    quantity: newQuantity,
                    size: size || '',
                    color: color || ''
                })
            });

            if (response.ok) {
                fetchCart();
            } else {
                console.error('Failed to update cart');
            }
        } catch (error) {
            console.error('Error updating cart:', error);
        }
    };

    window.removeCartItem = async function (productId, size, color) {
        try {
            await fetch('/api/cart/', {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({
                    product_id: productId,
                    size: size || '',
                    color: color || ''
                })
            });
            fetchCart();
        } catch (error) {
            console.error('Error removing item:', error);
        }
    };

    function getCookie(name) {
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

    // ===================================
    // STICKY HEADER ON SCROLL
    // ===================================
    const header = document.querySelector('.header');

    window.addEventListener('scroll', function () {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;

        if (scrollTop > 10 && header) {
            header.style.boxShadow = '0 2px 8px rgba(0, 0, 0, 0.1)';
        } else if (header) {
            header.style.boxShadow = 'none';
        }
    }, false);

    // ===================================
    // SMOOTH SCROLL FOR ANCHOR LINKS
    // ===================================
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href !== '#' && href !== '#!') {
                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });

    // ===================================
    // NEWSLETTER FORM
    // ===================================
    const newsletterForm = document.querySelector('.newsletter-form');
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', function (e) {
            e.preventDefault();
            const emailInput = this.querySelector('input[type="email"]');
            if (emailInput && emailInput.value) {
                alert('Thank you for subscribing! You will receive our latest updates.');
                emailInput.value = '';
            }
        });
    }

    // ===================================
    // FADE-IN ANIMATION ON SCROLL
    // ===================================
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function (entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    document.querySelectorAll('.fade-in').forEach(element => {
        element.style.opacity = '0';
        element.style.transform = 'translateY(20px)';
        element.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(element);
    });

    // ===================================
    // INITIALIZE CART COUNT
    // ===================================
    fetchCart();

    // ===================================
    // WINDOW RESIZE HANDLER
    // ===================================
    let resizeTimer;
    window.addEventListener('resize', function () {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(function () {
            if (window.innerWidth > 768 && navMenu) {
                navMenu.classList.remove('active');
                if (mobileMenuToggle) {
                    mobileMenuToggle.classList.remove('active');
                }
            }
        }, 250);
    });
});