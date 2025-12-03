from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from main.models import Category, Product
import io
from PIL import Image


class Command(BaseCommand):
    help = 'Add 10 shoe products to the database'

    def handle(self, *args, **kwargs):
        # Create or get Shoes category
        shoes_category, created = Category.objects.get_or_create(
            slug='shoes',
            defaults={'name': 'Shoes'}
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS('Created "Shoes" category'))
        else:
            self.stdout.write(self.style.WARNING('Shoes category already exists'))

        # Define 10 shoe products
        shoes_data = [
            {
                'name': 'Classic Leather Sneakers',
                'description': 'Premium leather sneakers with comfortable cushioning. Perfect for casual wear and everyday activities. Features breathable lining and durable rubber sole.',
                'price': 89.99,
                'rating': 4.5,
                'featured': True,
            },
            {
                'name': 'Running Sports Shoes',
                'description': 'Lightweight running shoes designed for maximum performance. Advanced cushioning technology and breathable mesh upper for optimal comfort during workouts.',
                'price': 129.99,
                'rating': 4.7,
                'featured': True,
            },
            {
                'name': 'Formal Oxford Shoes',
                'description': 'Elegant Oxford shoes crafted from genuine leather. Perfect for business meetings and formal occasions. Classic design with modern comfort.',
                'price': 149.99,
                'rating': 4.6,
                'featured': False,
            },
            {
                'name': 'Casual Canvas Slip-Ons',
                'description': 'Comfortable canvas slip-on shoes for everyday wear. Easy to put on and take off. Available in multiple colors with cushioned insole.',
                'price': 49.99,
                'rating': 4.3,
                'featured': False,
            },
            {
                'name': 'High-Top Basketball Shoes',
                'description': 'Professional basketball shoes with ankle support and superior grip. Designed for court performance with responsive cushioning and durable construction.',
                'price': 159.99,
                'rating': 4.8,
                'featured': True,
            },
            {
                'name': 'Hiking Boots',
                'description': 'Waterproof hiking boots built for outdoor adventures. Rugged construction with excellent traction and ankle support. Perfect for trails and rough terrain.',
                'price': 179.99,
                'rating': 4.7,
                'featured': False,
            },
            {
                'name': 'Stylish Loafers',
                'description': 'Sophisticated leather loafers for smart-casual occasions. Slip-on design with premium craftsmanship. Versatile style that pairs well with any outfit.',
                'price': 99.99,
                'rating': 4.4,
                'featured': False,
            },
            {
                'name': 'Training Cross-Trainers',
                'description': 'Versatile cross-training shoes for gym workouts. Stable platform for weightlifting with flexibility for cardio. Breathable and supportive design.',
                'price': 119.99,
                'rating': 4.6,
                'featured': True,
            },
            {
                'name': 'Chelsea Boots',
                'description': 'Classic Chelsea boots with elastic side panels. Premium suede or leather construction. Perfect for both casual and semi-formal wear.',
                'price': 139.99,
                'rating': 4.5,
                'featured': False,
            },
            {
                'name': 'Minimalist Walking Shoes',
                'description': 'Lightweight walking shoes with minimalist design. Flexible sole promotes natural foot movement. Ideal for daily walks and light activities.',
                'price': 79.99,
                'rating': 4.4,
                'featured': False,
            },
        ]

        # Create products
        created_count = 0
        for shoe_data in shoes_data:
            # Check if product already exists
            if not Product.objects.filter(name=shoe_data['name']).exists():
                # Create a simple placeholder image
                img = Image.new('RGB', (800, 800), color=(200, 200, 200))
                
                # Add text to image (product name)
                from PIL import ImageDraw, ImageFont
                draw = ImageDraw.Draw(img)
                
                # Use default font
                text = shoe_data['name']
                # Draw text in center
                bbox = draw.textbbox((0, 0), text)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
                position = ((800 - text_width) // 2, (800 - text_height) // 2)
                draw.text(position, text, fill=(50, 50, 50))
                
                # Save image to bytes
                img_io = io.BytesIO()
                img.save(img_io, format='PNG')
                img_io.seek(0)
                
                # Create product
                product = Product.objects.create(
                    name=shoe_data['name'],
                    description=shoe_data['description'],
                    price=shoe_data['price'],
                    category=shoes_category,
                    rating=shoe_data['rating'],
                    featured=shoe_data['featured'],
                )
                
                # Save image
                product.image.save(
                    f"{shoe_data['name'].lower().replace(' ', '_')}.png",
                    ContentFile(img_io.getvalue()),
                    save=True
                )
                
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'Created product: {shoe_data["name"]}'))
            else:
                self.stdout.write(self.style.WARNING(f'Product already exists: {shoe_data["name"]}'))

        self.stdout.write(self.style.SUCCESS(f'\nSuccessfully created {created_count} shoe products!'))
        self.stdout.write(self.style.SUCCESS(f'Total shoes in database: {Product.objects.filter(category=shoes_category).count()}'))
