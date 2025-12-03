import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mywebsite.settings')
django.setup()

from main.models import Category, Product

def fix_data():
    print("Fixing data...")
    
    # Create Men and Women categories
    men_cat, created = Category.objects.get_or_create(name='Men', slug='men')
    if created:
        print("Created 'Men' category")
    else:
        print("'Men' category already exists")
        
    women_cat, created = Category.objects.get_or_create(name='Women', slug='women')
    if created:
        print("Created 'Women' category")
    else:
        print("'Women' category already exists")
        
    # Get existing products
    products = Product.objects.all()
    print(f"Found {products.count()} products")
    
    # Assign products to Men/Women if they are in generic categories
    # We'll just distribute them for now to ensure data exists
    for i, product in enumerate(products):
        if product.category.slug not in ['men', 'women']:
            # Assign to Men or Women randomly or alternating
            new_cat = men_cat if i % 2 == 0 else women_cat
            old_cat_name = product.category.name
            product.category = new_cat
            product.save()
            print(f"Moved '{product.name}' from '{old_cat_name}' to '{new_cat.name}'")
            
    print("Data fix complete.")
    print(f"Products in Men: {Product.objects.filter(category=men_cat).count()}")
    print(f"Products in Women: {Product.objects.filter(category=women_cat).count()}")

if __name__ == "__main__":
    fix_data()
