/**
 * Micro-Interactions
 * Button ripples, toast notifications, cart animations, loading states
 */

/**
 * Ripple Effect on Buttons
 */
class RippleEffect {
    constructor() {
        this.init();
    }

    init() {
        document.addEventListener('click', (e) => {
            const button = e.target.closest('.btn, .ripple-container, button');
            if (!button) return;

            const ripple = document.createElement('span');
            const rect = button.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;

            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            ripple.classList.add('ripple');

            button.appendChild(ripple);

            setTimeout(() => ripple.remove(), 600);
        });
    }
}

/**
 * Toast Notifications
 */
class Toast {
    static show(message, type = 'info', duration = 3000) {
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.textContent = message;

        const icon = this.getIcon(type);
        if (icon) {
            toast.innerHTML = `<i class="${icon}"></i> ${message}`;
        }

        document.body.appendChild(toast);

        // Trigger animation
        setTimeout(() => toast.style.opacity = '1', 10);

        // Auto remove
        setTimeout(() => {
            toast.style.opacity = '0';
            toast.style.transform = 'translateY(20px)';
            setTimeout(() => toast.remove(), 300);
        }, duration);
    }

    static getIcon(type) {
        const icons = {
            success: 'fas fa-check-circle',
            error: 'fas fa-exclamation-circle',
            warning: 'fas fa-exclamation-triangle',
            info: 'fas fa-info-circle'
        };
        return icons[type] || '';
    }

    static success(message, duration) {
        this.show(message, 'success', duration);
    }

    static error(message, duration) {
        this.show(message, 'error', duration);
    }

    static warning(message, duration) {
        this.show(message, 'warning', duration);
    }

    static info(message, duration) {
        this.show(message, 'info', duration);
    }
}

/**
 * Cart Addition Animation
 */
class CartAnimation {
    static flyToCart(productElement, cartIcon) {
        if (!productElement || !cartIcon) return;

        const clone = productElement.cloneNode(true);
        clone.style.cssText = `
            position: fixed;
            width: 50px;
            height: 50px;
            z-index: 10000;
            pointer-events: none;
            transition: all 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        `;

        const startRect = productElement.getBoundingClientRect();
        const endRect = cartIcon.getBoundingClientRect();

        clone.style.left = startRect.left + 'px';
        clone.style.top = startRect.top + 'px';

        document.body.appendChild(clone);

        requestAnimationFrame(() => {
            clone.style.left = endRect.left + 'px';
            clone.style.top = endRect.top + 'px';
            clone.style.transform = 'scale(0.2)';
            clone.style.opacity = '0';
        });

        setTimeout(() => {
            clone.remove();
            // Animate cart icon
            cartIcon.style.transform = 'scale(1.2)';
            setTimeout(() => cartIcon.style.transform = 'scale(1)', 200);
        }, 800);
    }

    static updateCartCount(count, animated = true) {
        const badge = document.querySelector('.cart-count, .cart-badge');
        if (!badge) return;

        if (animated) {
            badge.style.transform = 'scale(1.5)';
            setTimeout(() => badge.style.transform = 'scale(1)', 200);
        }

        badge.textContent = count;
        badge.classList.add('pulse');
        setTimeout(() => badge.classList.remove('pulse'), 600);
    }
}

/**
 * Loading States
 */
class LoadingState {
    static show(element, text = 'Loading...') {
        if (!element) return;

        element.disabled = true;
        element.dataset.originalText = element.textContent;
        element.innerHTML = `
            <span class="spinner" style="width: 20px; height: 20px; border-width: 2px; display: inline-block; margin-right: 8px;"></span>
            ${text}
        `;
    }

    static hide(element) {
        if (!element) return;

        element.disabled = false;
        element.textContent = element.dataset.originalText || 'Submit';
        delete element.dataset.originalText;
    }

    static showOnPage() {
        const overlay = document.createElement('div');
        overlay.id = 'page-loader';
        overlay.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(255, 255, 255, 0.9);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 99999;
        `;
        overlay.innerHTML = '<div class="spinner" style="width: 60px; height: 60px;"></div>';
        document.body.appendChild(overlay);
    }

    static hideOnPage() {
        const loader = document.getElementById('page-loader');
        if (loader) {
            loader.style.opacity = '0';
            setTimeout(() => loader.remove(), 300);
        }
    }
}

/**
 * Form Input Animations
 */
class FormAnimations {
    static init() {
        // Floating labels
        document.querySelectorAll('.form-control, input, textarea').forEach(input => {
            if (input.value) {
                input.classList.add('has-value');
            }

            input.addEventListener('focus', () => {
                input.parentElement?.classList.add('focused');
            });

            input.addEventListener('blur', () => {
                input.parentElement?.classList.remove('focused');
                if (input.value) {
                    input.classList.add('has-value');
                } else {
                    input.classList.remove('has-value');
                }
            });

            input.addEventListener('input', () => {
                if (input.value) {
                    input.classList.add('has-value');
                } else {
                    input.classList.remove('has-value');
                }
            });
        });
    }
}

/**
 * Product Card Animations
 */
class ProductCardAnimations {
    static init() {
        document.querySelectorAll('.product-card').forEach(card => {
            card.addEventListener('mouseenter', function () {
                this.style.transform = 'translateY(-8px)';
                const img = this.querySelector('img');
                if (img) {
                    img.style.transform = 'scale(1.1)';
                }
            });

            card.addEventListener('mouseleave', function () {
                this.style.transform = 'translateY(0)';
                const img = this.querySelector('img');
                if (img) {
                    img.style.transform = 'scale(1)';
                }
            });
        });
    }
}

/**
 * Modal Animations
 */
class ModalAnimations {
    static show(modalId) {
        const modal = document.getElementById(modalId);
        if (!modal) return;

        modal.style.display = 'flex';
        modal.style.opacity = '0';

        requestAnimationFrame(() => {
            modal.style.opacity = '1';
            const content = modal.querySelector('.modal-content, .modal-dialog');
            if (content) {
                content.style.transform = 'scale(0.9)';
                content.style.transition = 'transform 0.3s ease';
                requestAnimationFrame(() => {
                    content.style.transform = 'scale(1)';
                });
            }
        });
    }

    static hide(modalId) {
        const modal = document.getElementById(modalId);
        if (!modal) return;

        modal.style.opacity = '0';
        const content = modal.querySelector('.modal-content, .modal-dialog');
        if (content) {
            content.style.transform = 'scale(0.9)';
        }

        setTimeout(() => {
            modal.style.display = 'none';
        }, 300);
    }
}

/**
 * Number Counter Animation for Stats
 */
class NumberCounter {
    static animate(element, start, end, duration = 2000) {
        const range = end - start;
        const increment = range / (duration / 16);
        let current = start;

        const timer = setInterval(() => {
            current += increment;
            if (current >= end) {
                element.textContent = end;
                clearInterval(timer);
            } else {
                element.textContent = Math.floor(current);
            }
        }, 16);
    }
}

/**
 * Initialize All Micro-Interactions
 */
document.addEventListener('DOMContentLoaded', () => {
    // Ripple effects
    new RippleEffect();

    // Form animations
    FormAnimations.init();

    // Product card animations
    ProductCardAnimations.init();

    // Add smooth class to body after load
    document.body.classList.add('animations-ready');
});

// Export for global use
window.Toast = Toast;
window.CartAnimation = CartAnimation;
window.LoadingState = LoadingState;
window.ModalAnimations = ModalAnimations;
window.NumberCounter = NumberCounter;
