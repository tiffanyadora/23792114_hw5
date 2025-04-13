import random
import os
import requests
import logging
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from .models import Product, VisualContent
from django.views.decorators.csrf import csrf_exempt
import json

# Setup logging
logger = logging.getLogger(__name__)

# OpenWeather API Key
OPENWEATHER_API_KEY = os.environ.get('OPENWEATHER_API_KEY', '4a8f3d86c302c6d60364b37beed16d43')

def home(request):
    category = request.GET.get('category', None)
    
    categories = {
        "Apparel": "t-shirt.jpg",
        "Accessories": "cap.jpg",
        "Gifts": "keychain.jpg",
        "Others": "flag.jpg"
    }

    if category:
        products = Product.get_product_by_category(category)
    else:
        products = Product.get_all()

    return render(request, 'index.html', {
        'categories': categories,
        'products': products,
        'selected_category': category
    })


def product_detail(request):
    product_id = request.GET.get('id')
    if not product_id:
        raise Http404("Product ID missing")
    
    product = Product.get_by_id(product_id)
    if not product:
        raise Http404("Product not found")
    
    visuals = VisualContent.get_for_product(product_id)

    # Get all products except the current product
    all_products = [p for p in Product.get_all() if p.product_id != product_id]

    # Randomly select 4 suggested products (or fewer if not enough exist)
    suggested_products = random.sample(all_products, min(4, len(all_products)))

    # Split features into a list (the column must exist and isn't empty)
    product_features = product.feature.split(",") if product.feature else []

    # Get Pokemon data (server-side API call)
    pokemon_data = None
    if product.pokemon:
        try:
            pokemon_response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{product.pokemon.lower()}")
            if pokemon_response.status_code == 200:
                pokemon_json = pokemon_response.json()
                pokemon_data = {
                    'name': pokemon_json.get('name', '').capitalize(),
                    'sprite': pokemon_json.get('sprites', {}).get('front_default', ''),
                    'types': [t.get('type', {}).get('name', '').capitalize() for t in pokemon_json.get('types', [])],
                }
        except Exception as e:
            logger.error(f"Error fetching Pokemon data: {str(e)}")

    return render (request, 'store.html', {
        'product': product,
        'visuals': visuals,
        'suggested_products': suggested_products,
        'product_features': product_features,
        'pokemon_data': pokemon_data,
    })


def search (request):
    query = " ".join(request.GET.get('query', '').strip().lower().split())
    
    if not query:
        return render(request, 'search.html', {'results': [], 'query': None})
    
    products = [p for p in Product.get_all() if query in " ".join(p.name.lower().split())]
    
    return render(request, 'search.html', {'results': products, 'query': query})

@csrf_exempt
def add_product_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Add product to CSV
            product_data = {
                'id': data.get('product_id'),
                'name': data.get('name'),
                'description': data.get('description'),
                'feature': data.get('features'),
                'rating': data.get('rating'),
                'price': data.get('price'),
                'category': data.get('category'),
                'pokemon': data.get('pokemon', ''),
                'location': data.get('location', '')
            }
            Product.add_product(product_data)
            
            # Generate unique visual ID
            new_visual_id = str(VisualContent.get_next_visual_id())

            # Add visual to CSV
            image_name = data.get('imageName', '').split('.')
            visual_data = {
                'id': new_visual_id,
                'name': data.get('name'),
                'description': data.get('description'),
                'short_name': image_name[0],
                'file_type': image_name[1] if len(image_name) > 1 else 'jpg',
                'css_class': 'product-image',
                'product_id': data.get('product_id')
            }

            print("Saving Visual Data:", visual_data)  # Debugging

            VisualContent.add_visual(visual_data)
            
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


DATA_DIR = os.path.join(settings.BASE_DIR, "data")

def serve_csv(request, filename):    
    file_path = os.path.join(DATA_DIR, filename)
    
    if not os.path.exists(file_path):
        return JsonResponse({"error": "File not found"}, status=404)
    
    with open(file_path, "r", encoding="utf-8") as file:
        response = HttpResponse(file.read(), content_type="text/csv")
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        return response