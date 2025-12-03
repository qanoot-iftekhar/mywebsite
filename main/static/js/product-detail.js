// Product Detail Page - Size & Color Selection
let variantData = {};
let selectedColor = null;
let selectedSize = null;

document.addEventListener('DOMContentLoaded', function () {
    // Load variant data from hidden script tag
    const variantDataElement = document.getElementById('variantData');
    if (variantDataElement) {
        variantData = JSON.parse(variantDataElement.textContent);
        console.log('Variant Data Loaded:', variantData);
    }
});

// Change main product image
function changeMainImage(thumbnail) {
    const mainImage = document.getElementById('mainProductImage');
    mainImage.src = thumbnail.src;

    // Update active thumbnail
    document.querySelectorAll('.thumbnail').forEach(thumb => {
        thumb.classList.remove('active');
    });
    thumbnail.classList.add('active');
}

// Select Color
function selectColor(color, colorName) {
    selectedColor = color;

    // Update UI
    document.querySelectorAll('.color-option').forEach(option => {
        option.classList.remove('selected');
    });
    event.target.closest('.color-option').classList.add('selected');

    document.getElementById('selectedColorName').textContent = colorName;

    // Load available sizes for this color
    loadSizesForColor(color);

    // Reset size selection
    selectedSize = null;
    document.getElementById('selectedSizeName').textContent = 'Select a size';
    updateAddToCartButton();

    // Update image if color-specific image exists
    const colorData = variantData[color];
    if (colorData) {
        const firstSize = Object.keys(colorData)[0];
        if (colorData[firstSize].image) {
            document.getElementById('mainProductImage').src = colorData[firstSize].image;
        }
    }
}

// Load sizes based on selected color
function loadSizesForColor(color) {
    const sizeOptions = document.getElementById('sizeOptions');
    sizeOptions.innerHTML = '';

    if (!variantData[color]) {
        sizeOptions.innerHTML = '<p class="no-sizes">No sizes available for this color</p>';
        return;
    }

    const sizes = variantData[color];
    const sizeOrder = ['6', '7', '8', '9', '10', '11', '12'];

    sizeOrder.forEach(size => {
        if (sizes[size]) {
            const sizeData = sizes[size];
            const sizeButton = document.createElement('button');
            sizeButton.className = 'size-option';
            sizeButton.textContent = `UK ${size}`;
            sizeButton.setAttribute('data-size', size);

            // Check stock status
            if (!sizeData.is_in_stock) {
                sizeButton.classList.add('out-of-stock');
                sizeButton.disabled = true;
                sizeButton.title = 'Out of Stock';
            } else if (sizeData.is_low_stock) {
                sizeButton.classList.add('low-stock');
                sizeButton.title = `Only ${sizeData.stock} left!`;
            }

            sizeButton.onclick = () => selectSize(size, sizeData);
            sizeOptions.appendChild(sizeButton);
        }
    });
}

// Select Size
function selectSize(size, sizeData) {
    selectedSize = size;

    // Update UI
    document.querySelectorAll('.size-option').forEach(option => {
        option.classList.remove('selected');
    });
    event.target.classList.add('selected');

    document.getElementById('selectedSizeName').textContent = `UK ${size}`;

    // Show stock message
    const stockMessage = document.getElementById('stockMessage');
    if (sizeData.is_low_stock) {
        stockMessage.innerHTML = `<i class="fas fa-exclamation-circle"></i> Only ${sizeData.stock} left in stock!`;
        stockMessage.className = 'stock-message low-stock';
    } else if (sizeData.stock > 10) {
        stockMessage.innerHTML = `<i class="fas fa-check-circle"></i> In Stock`;
        stockMessage.className = 'stock-message in-stock';
    } else {
        stockMessage.innerHTML = '';
    }

    updateAddToCartButton();
}

// Update Add to Cart button state
function updateAddToCartButton() {
    const addToCartBtn = document.getElementById('addToCartBtn');

    if (selectedColor && selectedSize) {
        addToCartBtn.disabled = false;
        addToCartBtn.innerHTML = '<i class="fas fa-shopping-cart"></i> Add to Cart';
    } else {
        addToCartBtn.disabled = true;
        if (!selectedColor) {
            addToCartBtn.innerHTML = '<i class="fas fa-shopping-cart"></i> Select Color';
        } else if (!selectedSize) {
            addToCartBtn.innerHTML = '<i class="fas fa-shopping-cart"></i> Select Size';
        }
    }
}

// Add to Cart with size and color
async function addToCart() {
    if (!selectedColor || !selectedSize) {
        alert('Please select both color and size');
        return;
    }

    const productId = document.getElementById('product-id').value;
    const variantInfo = variantData[selectedColor][selectedSize];

    try {
        const response = await fetch('/api/cart/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                product: productId,
                quantity: 1,
                size: selectedSize,
                color: selectedColor,
                sku: variantInfo.sku
            })
        });

        if (response.ok) {
            // Show success message
            const addToCartBtn = document.getElementById('addToCartBtn');
            addToCartBtn.innerHTML = '<i class="fas fa-check"></i> Added to Cart!';
            addToCartBtn.classList.add('success');

            setTimeout(() => {
                addToCartBtn.innerHTML = '<i class="fas fa-shopping-cart"></i> Add to Cart';
                addToCartBtn.classList.remove('success');
            }, 2000);

            // Update cart count if function exists
            if (typeof updateCartCount === 'function') {
                // Fetch updated cart
                const cartResponse = await fetch('/api/cart/');
                const cartData = await cartResponse.json();
                updateCartCount(cartData.count || 0);
            }
        } else {
            const errorData = await response.json();
            alert(errorData.error || 'Failed to add to cart');
        }
    } catch (error) {
        console.error('Error adding to cart:', error);
        alert('An error occurred. Please try again.');
    }
}

// Get CSRF token
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
    return cookieValue;
}

// Toggle Wishlist
async function toggleWishlist() {
    const productId = document.getElementById('product-id').value;
    const wishlistBtn = document.querySelector('.btn-wishlist');
    const icon = wishlistBtn.querySelector('i');

    try {
        const response = await fetch(`/wishlist/toggle/${productId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            }
        });

        if (response.ok) {
            const data = await response.json();

            if (data.action === 'added') {
                icon.classList.remove('far');
                icon.classList.add('fas');
                icon.style.color = '#e74c3c'; // Red color
            } else {
                icon.classList.remove('fas');
                icon.classList.add('far');
                icon.style.color = ''; // Reset color
            }
        } else {
            // If 401 Unauthorized, redirect to login
            if (response.status === 401) {
                window.location.href = '/login/?next=' + window.location.pathname;
            } else {
                console.error('Failed to toggle wishlist');
            }
        }
    } catch (error) {
        console.error('Error toggling wishlist:', error);
    }
}
