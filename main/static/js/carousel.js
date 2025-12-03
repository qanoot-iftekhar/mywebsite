// Shoe Carousel JavaScript
class ShoeCarousel {
    constructor() {
        this.currentIndex = 0;
        this.shoes = [
            {
                name: "CLOUD SLIP-ON",
                price: "$89",
                image: "/static/images/slider-shoe-1.jpg"
            },
            {
                name: "RUNNER CLASSIC",
                price: "$95",
                image: "/static/images/slider-shoe-2.jpg"
            },
            {
                name: "SPORT TRAINER",
                price: "$105",
                image: "/static/images/slider-shoe-3.jpg"
            },
            {
                name: "PREMIUM LACE",
                price: "$99",
                image: "/static/images/slider-shoe-4.jpg"
            },
            {
                name: "COMFORT RUNNER",
                price: "$110",
                image: "/static/images/slider-shoe-5.jpg"
            }
        ];

        this.init();
    }

    init() {
        this.renderCarousel();
        this.setupEventListeners();
        this.updateProductInfo();
    }

    renderCarousel() {
        const track = document.querySelector('.shoe-track');
        if (!track) return;

        track.innerHTML = '';

        // Render all shoes
        this.shoes.forEach((shoe, index) => {
            const shoeItem = document.createElement('div');
            shoeItem.className = 'carousel-shoe-item';
            if (index === this.currentIndex) {
                shoeItem.classList.add('center');
            }
            shoeItem.innerHTML = `
                <img src="${shoe.image}" alt="${shoe.name}">
            `;
            track.appendChild(shoeItem);
        });

        this.updateSliderPosition();
    }

    updateSliderPosition() {
        const track = document.querySelector('.shoe-track');
        if (!track) return;

        const items = track.querySelectorAll('.carousel-shoe-item');
        items.forEach((item, index) => {
            item.classList.remove('center');
            if (index === this.currentIndex) {
                item.classList.add('center');
            }
        });

        // Calculate offset to center current shoe
        const offset = -this.currentIndex * 450; // 400px width + 50px gap
        track.style.transform = `translateX(calc(50% + ${offset}px - 200px))`;
    }

    updateProductInfo() {
        const currentShoe = this.shoes[this.currentIndex];
        const nameEl = document.querySelector('.carousel-product-name');
        const priceEl = document.querySelector('.carousel-product-price');

        if (nameEl) nameEl.textContent = currentShoe.name;
        if (priceEl) priceEl.textContent = currentShoe.price;
    }

    setupEventListeners() {
        const prevBtn = document.querySelector('.carousel-nav.prev');
        const nextBtn = document.querySelector('.carousel-nav.next');

        if (prevBtn) {
            prevBtn.addEventListener('click', () => this.prev());
        }

        if (nextBtn) {
            nextBtn.addEventListener('click', () => this.next());
        }

        // Shop buttons
        const shopMenBtn = document.querySelector('.shop-men-btn');
        const shopWomenBtn = document.querySelector('.shop-women-btn');

        if (shopMenBtn) {
            shopMenBtn.addEventListener('click', () => {
                window.location.href = '/products/?category=men';
            });
        }

        if (shopWomenBtn) {
            shopWomenBtn.addEventListener('click', () => {
                window.location.href = '/products/?category=women';
            });
        }
    }

    prev() {
        this.currentIndex = (this.currentIndex - 1 + this.shoes.length) % this.shoes.length;
        this.updateSliderPosition();
        this.updateProductInfo();
    }

    next() {
        this.currentIndex = (this.currentIndex + 1) % this.shoes.length;
        this.updateSliderPosition();
        this.updateProductInfo();
    }
}

// Initialize carousel when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    const carouselSection = document.querySelector('.shoe-carousel-section');
    if (carouselSection) {
        new ShoeCarousel();
    }
});
