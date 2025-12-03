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

// Attach event listeners when DOM is ready
document.addEventListener('DOMContentLoaded', function () {
    // Quantity decrease buttons
    document.querySelectorAll('.qty-decrease').forEach(btn => {
        btn.addEventListener('click', function () {
            const productId = this.dataset.productId;
            const currentQty = parseInt(this.dataset.quantity);
            const size = this.dataset.size;
            const color = this.dataset.color;

            updateQuantity(productId, currentQty, -1, size, color);
        });
    });

    // Quantity increase buttons
    document.querySelectorAll('.qty-increase').forEach(btn => {
        btn.addEventListener('click', function () {
            const productId = this.dataset.productId;
            const currentQty = parseInt(this.dataset.quantity);
            const size = this.dataset.size;
            const color = this.dataset.color;

            updateQuantity(productId, currentQty, 1, size, color);
        });
    });

    // Remove item buttons
    document.querySelectorAll('.remove-cart-item').forEach(btn => {
        btn.addEventListener('click', function () {
            const productId = this.dataset.productId;
            const size = this.dataset.size;
            const color = this.dataset.color;

            removeFromCart(productId, size, color);
        });
    });
});

async function updateQuantity(productId, currentQty, change, size, color) {
    const newQty = currentQty + change;

    if (newQty < 1) return;

    try {
        const response = await fetch('/api/cart/', {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                product_id: productId,
                quantity: newQty,
                size: size || '',
                color: color || ''
            })
        });

        if (response.ok) {
            location.reload();
        } else {
            const data = await response.json();
            console.error('Failed to update cart:', data);
            alert('Failed to update cart. Please try again.');
        }
    } catch (error) {
        console.error('Error updating cart:', error);
        alert('Error updating cart. Please try again.');
    }
}

async function removeFromCart(productId, size, color) {
    if (!confirm('Are you sure you want to remove this item?')) return;

    try {
        const response = await fetch('/api/cart/', {
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

        if (response.ok) {
            location.reload();
        } else {
            const data = await response.json();
            console.error('Failed to remove item:', data);
            alert('Failed to remove item. Please try again.');
        }
    } catch (error) {
        console.error('Error removing item:', error);
        alert('Error removing item. Please try again.');
    }
}

async function applyCoupon() {
    const couponCode = document.getElementById('couponCode').value.trim();
    const messageDiv = document.getElementById('couponMessage');

    if (!couponCode) {
        messageDiv.style.color = '#e74c3c';
        messageDiv.textContent = 'Please enter a coupon code.';
        return;
    }

    // For now, just show a message. You can implement actual coupon logic later.
    messageDiv.style.color = '#e74c3c';
    messageDiv.textContent = 'Invalid coupon code. Please try again.';
}
