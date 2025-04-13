from django.urls import path
from .views import home, product_detail, search, add_product_api, serve_csv
from .api_views import api_products, api_product_detail, api_pokemon_data, api_weather_data

urlpatterns = [
    path('', home, name='home'),
    path('products/', product_detail, name='product_detail'),    
    path('search/', search, name='search'),
    path('api/add-product/', add_product_api, name='add_product_api'),
    path("data/<str:filename>/", serve_csv, name="serve_csv"),

    # New API endpoints
    path('api/products/', api_products, name='api_products'),
    path('api/products/<str:product_id>/', api_product_detail, name='api_product_detail'),
    path('api/pokemon/<str:pokemon_name>/', api_pokemon_data, name='api_pokemon_data'),
    path('api/weather/<str:city_name>/', api_weather_data, name='api_weather_data'),
]