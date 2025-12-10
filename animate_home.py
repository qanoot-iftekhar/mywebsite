import re

# Read home.html
with open('main/templates/home.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Add scroll-reveal to sections and parallax to hero
replacements = [
    # Hero section - add parallax to image
    ('class="hero-banner"', 'class="hero-banner parallax" data-speed="0.3"'),
    
    # Hero content - fade in
    ('class="hero-content"', 'class="hero-content scroll-reveal"'),
    
    # Category cards - change fade-in to scroll-reveal with stagger
    ('class="categories-grid"', 'class="categories-grid" data-stagger'),
    ('class="category-card fade-in"', 'class="category-card scroll-reveal card-hover img-zoom-container"'),
    
    # Featured product sections
    ('class="featured-image fade-in"', 'class="featured-image scroll-reveal"'),
    ('class="featured-content fade-in"', 'class="featured-content scroll-reveal"'),
    
    # Sustainability section
    ('class="sustainability-banner"', 'class="sustainability-banner scroll-reveal"'),
    
    # Product cards in bestsellers
    ('class="products-grid"', 'class="products-grid" data-stagger'),
    ('class="product-card fade-in"', 'class="product-card scroll-reveal card-hover"'),
    
    # Large category cards
    ('class="categories-grid-large"', 'class="categories-grid-large" data-stagger'),
    ('class="category-large fade-in"', 'class="category-large scroll-reveal hover-lift"'),
    
    # Review cards
    ('class="reviews-grid"', 'class="reviews-grid" data-stagger'),
    ('class="review-card fade-in"', 'class="review-card scroll-reveal"'),
    
    # Section headers
    ('class="section-header"', 'class="section-header scroll-reveal"'),
]

for old, new in replacements:
    content = content.replace(old, new)

# Add image zoom class to product images
content = re.sub(
    r'(<div class="product-image">)',
    r'<div class="product-image img-zoom-container">',
    content
)

# Add img-zoom class to images within product-image divs
content = re.sub(
    r'(<div class="product-image[^>]*>[\s\S]*?<img [^>]*)(>)',
    r'\1 class="img-zoom"\2',
    content
)

# Write back
with open('main/templates/home.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Home page updated with premium animations!")
print("  - Hero parallax effect")
print("  - Scroll reveals on all sections")
print("  - Staggered product grid animations")
print("  - Card hover effects")
print("  - Image zoom on hover")
