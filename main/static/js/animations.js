/**
 * Premium Animations Controller
 * Handles scroll animations, parallax, and reveal effects
 */

class AnimationController {
    constructor() {
        this.init();
    }

    init() {
        this.setupScrollReveal();
        this.setupParallax();
        this.setupCounters();
        this.setupStaggeredAnimations();
    }

    /**
     * Scroll Reveal - Fade in elements as they enter viewport
     */
    setupScrollReveal() {
        const revealElements = document.querySelectorAll('.scroll-reveal');

        if (!revealElements.length) return;

        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('revealed');
                    // Optional: unobserve after reveal for performance
                    // observer.unobserve(entry.target);
                }
            });
        }, observerOptions);

        revealElements.forEach(el => observer.observe(el));
    }

    /**
     * Parallax Scrolling Effect
     */
    setupParallax() {
        const parallaxElements = document.querySelectorAll('.parallax');

        if (!parallaxElements.length) return;

        let ticking = false;

        const updateParallax = () => {
            const scrollY = window.pageYOffset;

            parallaxElements.forEach(el => {
                const speed = el.dataset.speed || 0.5;
                const yPos = -(scrollY * speed);
                el.style.transform = `translate3d(0, ${yPos}px, 0)`;
            });

            ticking = false;
        };

        window.addEventListener('scroll', () => {
            if (!ticking) {
                window.requestAnimationFrame(updateParallax);
                ticking = true;
            }
        });
    }

    /**
     * Counter Animations - Count up numbers
     */
    setupCounters() {
        const counters = document.querySelectorAll('.counter');

        if (!counters.length) return;

        const animateCounter = (counter) => {
            const target = parseInt(counter.dataset.target || counter.textContent);
            const duration = parseInt(counter.dataset.duration || 2000);
            const step = target / (duration / 16); // 60fps
            let current = 0;

            const updateCounter = () => {
                current += step;
                if (current < target) {
                    counter.textContent = Math.floor(current);
                    requestAnimationFrame(updateCounter);
                } else {
                    counter.textContent = target;
                }
            };

            updateCounter();
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting && !entry.target.classList.contains('counted')) {
                    entry.target.classList.add('counted');
                    animateCounter(entry.target);
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.5 });

        counters.forEach(counter => observer.observe(counter));
    }

    /**
     * Staggered Animations for Lists
     */
    setupStaggeredAnimations() {
        const containers = document.querySelectorAll('[data-stagger]');

        containers.forEach(container => {
            const children = container.children;
            const delay = parseInt(container.dataset.staggerDelay || 100);

            Array.from(children).forEach((child, index) => {
                child.style.transitionDelay = `${index * delay}ms`;
                child.classList.add('scroll-reveal');
            });
        });
    }
}

/**
 * Scroll Progress Indicator
 */
class ScrollProgress {
    constructor() {
        this.createProgressBar();
        this.updateProgress();
    }

    createProgressBar() {
        const progressBar = document.createElement('div');
        progressBar.id = 'scroll-progress';
        progressBar.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            height: 3px;
            background: linear-gradient(90deg, #212a2f, #3498db);
            width: 0%;
            z-index: 9999;
            transition: width 0.1s ease-out;
        `;
        document.body.appendChild(progressBar);
        this.progressBar = progressBar;
    }

    updateProgress() {
        let ticking = false;

        window.addEventListener('scroll', () => {
            if (!ticking) {
                window.requestAnimationFrame(() => {
                    const windowHeight = document.documentElement.scrollHeight - window.innerHeight;
                    const scrolled = (window.pageYOffset / windowHeight) * 100;
                    this.progressBar.style.width = scrolled + '%';
                    ticking = false;
                });
                ticking = true;
            }
        });
    }
}

/**
 * Smooth Scroll to Anchor
 */
function smoothScrollToAnchor() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href === '#') return;

            e.preventDefault();
            const target = document.querySelector(href);

            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

/**
 * Image Lazy Load with Fade In
 */
class LazyImageLoader {
    constructor() {
        this.images = document.querySelectorAll('img[data-src]');
        this.init();
    }

    init() {
        if (!this.images.length) return;

        const imageObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.style.opacity = '0';
                    img.style.transition = 'opacity 0.5s ease-in';

                    img.addEventListener('load', () => {
                        img.style.opacity = '1';
                        img.removeAttribute('data-src');
                    });

                    imageObserver.unobserve(img);
                }
            });
        });

        this.images.forEach(img => imageObserver.observe(img));
    }
}

/**
 * Page Visibility Change Handler
 */
function handleVisibilityChange() {
    document.addEventListener('visibilitychange', () => {
        if (document.hidden) {
            // Pause animations when tab is hidden
            document.body.classList.add('animations-paused');
        } else {
            document.body.classList.remove('animations-paused');
        }
    });
}

/**
 * Initialize All Animations
 */
document.addEventListener('DOMContentLoaded', () => {
    // Main animation controller
    new AnimationController();

    // Scroll progress bar
    new ScrollProgress();

    // Smooth scroll
    smoothScrollToAnchor();

    // Lazy load images
    new LazyImageLoader();

    // Handle visibility changes
    handleVisibilityChange();

    // Add reveal class to elements after short delay
    setTimeout(() => {
        document.querySelectorAll('.fade-in-on-load').forEach(el => {
            el.style.opacity = '0';
            el.style.transform = 'translateY(20px)';
            el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';

            requestAnimationFrame(() => {
                el.style.opacity = '1';
                el.style.transform = 'translateY(0)';
            });
        });
    }, 100);
});

// Export for use in other scripts
window.AnimationController = AnimationController;
