from django.core.management.base import BaseCommand
from main.models import Product, ProductVariant, ProductImage
import random

class Command(BaseCommand):
    help = 'Create variants and images for existing products'

    def handle(self, *args, **kwargs):
        products = Product.objects.all()
        
        colors = ['black', 'white', 'grey', 'navy', 'beige']
        sizes = ['6', '7', '8', '9', '10', '11', '12']
        
        for product in products:
            self.stdout.write(f'Processing {product.name}...')
            
            # Create Variants
            # Each product gets 2-3 random colors
            product_colors = random.sample(colors, k=random.randint(2, 3))
            
            for color in product_colors:
                for size in sizes:
                    # Random stock between 0 and 20
                    stock = random.randint(0, 20)
                    
                    # Create variant
                    variant, created = ProductVariant.objects.get_or_create(
                        product=product,
                        color=color,
                        size=size,
                        defaults={
                            'stock': stock,
                            'sku': f'{product.id}-{color}-{size}'
                        }
                    )
                    
                    if created:
                        self.stdout.write(f'  Created variant: {color} - UK {size} (Stock: {stock})')
            
            # Create Additional Images (Simulated by reusing main image)
            if not product.images.exists() and product.image:
                ProductImage.objects.create(
                    product=product,
                    image=product.image,
                    alt_text=f"{product.name} - Side View",
                    order=1
                )
                ProductImage.objects.create(
                    product=product,
                    image=product.image,
                    alt_text=f"{product.name} - Top View",
                    order=2
                )
                self.stdout.write('  Created additional images')
                
        self.stdout.write(self.style.SUCCESS('Successfully created variants for all products'))
