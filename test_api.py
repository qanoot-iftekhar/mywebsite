import os
import django

# Setup Django environment BEFORE other imports
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mywebsite.settings')
django.setup()

from django.conf import settings
from rest_framework.test import APIRequestFactory
from main.api_views import ProductListAPIView
from main.models import Product

def test_products_api():
    print("Testing Products API...")
    
    # Add testserver to ALLOWED_HOSTS
    if 'testserver' not in settings.ALLOWED_HOSTS:
        settings.ALLOWED_HOSTS.append('testserver')
    
    # Check database count
    count = Product.objects.count()
    print(f"Total products in database: {count}")
    
    if count == 0:
        print("WARNING: No products found in database!")
        return

    # Create request
    factory = APIRequestFactory()
    request = factory.get('/api/products/')
    
    # Call view
    view = ProductListAPIView.as_view()
    response = view(request)
    
    print(f"Response Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.data
        print("Response Data Keys:", data.keys())
        
        if 'results' in data:
            results = data['results']
            print(f"Number of results in page 1: {len(results)}")
            if len(results) > 0:
                print("First product sample:", results[0])
        else:
            print("ERROR: 'results' key missing in response. Pagination might be off.")
            print("Data:", data)
    else:
        print("Error response:", response.data)

if __name__ == "__main__":
    test_products_api()
