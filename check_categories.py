import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mywebsite.settings')
django.setup()

from main.models import Category, Product

def check_data():
    print("Checking Categories:")
    categories = Category.objects.all()
    for cat in categories:
        print(f"- {cat.name} (slug: {cat.slug})")
        product_count = Product.objects.filter(category=cat).count()
        print(f"  Products: {product_count}")

    print("\nChecking 'men' category specifically:")
    try:
        men_cat = Category.objects.get(slug='men')
        print(f"Found 'men' category. ID: {men_cat.id}")
        print(f"Products in 'men': {Product.objects.filter(category=men_cat).count()}")
    except Category.DoesNotExist:
        print("'men' category NOT FOUND.")

if __name__ == "__main__":
    check_data()
