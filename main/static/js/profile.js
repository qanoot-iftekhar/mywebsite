// Profile Page Tab Navigation
document.addEventListener('DOMContentLoaded', function () {
    const navItems = document.querySelectorAll('.profile-nav .nav-item');
    const tabContents = document.querySelectorAll('.tab-content');

    navItems.forEach(item => {
        item.addEventListener('click', function (e) {
            // Skip if it's the logout link
            if (this.classList.contains('logout')) {
                return;
            }

            e.preventDefault();

            // Get tab ID from data attribute
            const tabId = this.dataset.tab;

            // Remove active class from all nav items and tabs
            navItems.forEach(nav => nav.classList.remove('active'));
            tabContents.forEach(tab => tab.classList.remove('active'));

            // Add active class to clicked nav and corresponding tab
            this.classList.add('active');
            document.getElementById(tabId).classList.add('active');

            // Update URL hash
            window.location.hash = tabId;
        });
    });

    // Check for hash on page load
    if (window.location.hash) {
        const hash = window.location.hash.substring(1);
        const targetNav = document.querySelector(`[data-tab="${hash}"]`);
        if (targetNav) {
            targetNav.click();
        }
    }
});

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
}

// Toggle Wishlist from Profile
async function toggleWishlistFromProfile(productId, btnElement) {
    if (!confirm('Are you sure you want to remove this item from your wishlist?')) {
        return;
    }

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

            if (data.action === 'removed') {
                // Remove the product card from the grid
                const card = btnElement.closest('.product-card');
                card.remove();

                // Check if grid is empty
                const grid = document.querySelector('.wishlist-grid');
                if (grid && grid.children.length === 0) {
                    // Show empty state
                    const container = document.getElementById('wishlist');
                    container.innerHTML = `
                        <h2>My Wishlist</h2>
                        <div class="empty-state">
                            <i class="far fa-heart"></i>
                            <h3>Your Wishlist is Empty</h3>
                            <p>Save items you love to find them easily later.</p>
                            <a href="/products/" class="btn btn-primary">Start Shopping</a>
                        </div>
                    `;
                }
            }
        } else {
            console.error('Failed to remove from wishlist');
        }
    } catch (error) {
        console.error('Error toggling wishlist:', error);
    }
}
