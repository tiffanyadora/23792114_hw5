import json
import os
import requests
import logging
from django.http import JsonResponse
from django.conf import settings
from .models import Product, VisualContent

# Setup logging
logger = logging.getLogger(__name__)

# OpenWeather API Key
OPENWEATHER_API_KEY = os.environ.get('OPENWEATHER_API_KEY')

# API endpoint to get all products
def api_products(request):
    try:
        products = Product.get_all()
        return JsonResponse({
            'success': True,
            'products': [product.to_json() for product in products]
        })
    except Exception as e:
        logger.error(f"Error fetching products: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': 'Error fetching products',
            'details': str(e)
        }, status=500)

# API endpoint to get Pokemon data from PokeAPI with error handling
def api_pokemon_data(request, pokemon_name):
    try:
        # Add timeout to prevent hanging requests
        response = requests.get(
            f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}", 
            timeout=5
        )
        
        if response.status_code == 404:
            logger.warning(f"Pokemon not found: {pokemon_name}")
            return JsonResponse({
                'success': False,
                'error': f'Pokemon {pokemon_name} not found',
                'error_type': 'NOT_FOUND'
            }, status=404)
        
        if response.status_code != 200:
            logger.error(f"PokeAPI error: Status {response.status_code} for {pokemon_name}")
            return JsonResponse({
                'success': False,
                'error': f'Pokemon API returned status code {response.status_code}',
                'error_type': 'API_ERROR'
            }, status=502)  # 502 Bad Gateway
            
        pokemon_data = response.json()
        
        data = {
            'success': True,
            'name': pokemon_data.get('name', '').capitalize(),
            'sprite': pokemon_data.get('sprites', {}).get('front_default', ''),
            'types': [t.get('type', {}).get('name', '').capitalize() for t in pokemon_data.get('types', [])],
            'height': pokemon_data.get('height', 0),
            'weight': pokemon_data.get('weight', 0),
            'stats': {s.get('stat', {}).get('name', ''): s.get('base_stat', 0) for s in pokemon_data.get('stats', [])}
        }
        
        return JsonResponse(data)
    except requests.exceptions.Timeout:
        logger.error(f"Timeout when fetching Pokemon data for: {pokemon_name}")
        return JsonResponse({
            'success': False,
            'error': 'Pokemon API request timed out',
            'error_type': 'TIMEOUT'
        }, status=504)  # 504 Gateway Timeout
    except requests.exceptions.ConnectionError:
        logger.error(f"Connection error when fetching Pokemon data for: {pokemon_name}")
        return JsonResponse({
            'success': False,
            'error': 'Could not connect to Pokemon API',
            'error_type': 'CONNECTION_ERROR'
        }, status=503)  # 503 Service Unavailable
    except Exception as e:
        logger.error(f"Error fetching Pokemon data: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': 'Error fetching Pokemon data',
            'error_type': 'UNKNOWN_ERROR',
            'details': str(e)
        }, status=500)

# API endpoint to get weather data from OpenWeatherMap with error handling
def api_weather_data(request, city_name):
    try:
        if not OPENWEATHER_API_KEY:
            logger.error("OpenWeather API key not configured")
            return JsonResponse({
                'success': False,
                'error': 'OpenWeather API key not configured',
                'error_type': 'CONFIGURATION_ERROR'
            }, status=500)
            
        # Add timeout to prevent hanging requests
        response = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={OPENWEATHER_API_KEY}&units=metric",
            timeout=5
        )
        
        if response.status_code == 404:
            logger.warning(f"City not found: {city_name}")
            return JsonResponse({
                'success': False,
                'error': f'Weather data for {city_name} not found',
                'error_type': 'NOT_FOUND'
            }, status=404)
        
        if response.status_code == 401:
            logger.error("Invalid OpenWeather API key")
            return JsonResponse({
                'success': False,
                'error': 'Invalid OpenWeather API key',
                'error_type': 'AUTH_ERROR'
            }, status=401)
            
        if response.status_code != 200:
            logger.error(f"OpenWeather API error: Status {response.status_code} for {city_name}")
            return JsonResponse({
                'success': False,
                'error': f'Weather API returned status code {response.status_code}',
                'error_type': 'API_ERROR'
            }, status=502)  # 502 Bad Gateway
            
        weather_data = response.json()
        
        # The default temperature is celcius, so we need to convert it to Fahrenheit
        temp_celsius = weather_data.get('main', {}).get('temp', 0)
        temp_fahrenheit = (temp_celsius * 9/5) + 32
        
        data = {
            'success': True,
            'city': city_name,
            'temperature_celsius': temp_celsius,
            'temperature_fahrenheit': temp_fahrenheit,
            'condition': weather_data.get('weather', [{}])[0].get('main', ''),
            'description': weather_data.get('weather', [{}])[0].get('description', ''),
            'icon': weather_data.get('weather', [{}])[0].get('icon', ''),
            'icon_url': f"https://openweathermap.org/img/wn/{weather_data.get('weather', [{}])[0].get('icon', '')}@2x.png",
            'humidity': weather_data.get('main', {}).get('humidity', 0),
            'wind_speed': weather_data.get('wind', {}).get('speed', 0),
            'timestamp': weather_data.get('dt', 0)
        }
        
        return JsonResponse(data)
    except requests.exceptions.Timeout:
        logger.error(f"Timeout when fetching weather data for: {city_name}")
        return JsonResponse({
            'success': False,
            'error': 'Weather API request timed out',
            'error_type': 'TIMEOUT'
        }, status=504)  # 504 Gateway Timeout
    except requests.exceptions.ConnectionError:
        logger.error(f"Connection error when fetching weather data for: {city_name}")
        return JsonResponse({
            'success': False,
            'error': 'Could not connect to Weather API',
            'error_type': 'CONNECTION_ERROR'
        }, status=503)  # 503 Service Unavailable
    except Exception as e:
        logger.error(f"Error fetching weather data: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': 'Error fetching weather data',
            'error_type': 'UNKNOWN_ERROR',
            'details': str(e)
        }, status=500)

# API endpoint to get a specific product's details with error handling  
def api_product_detail(request, product_id):
    try:
        product = Product.get_by_id(product_id)
        if not product:
            return JsonResponse({
                'success': False,
                'error': 'Product not found',
                'error_type': 'NOT_FOUND'
            }, status=404)
            
        visuals = VisualContent.get_for_product(product_id)
        
        # Get Pokemon data
        pokemon_data = None
        if product.pokemon:
            try:
                pokemon_response = requests.get(
                    f"https://pokeapi.co/api/v2/pokemon/{product.pokemon.lower()}",
                    timeout=3  # Short timeout to not delay the overall response
                )
                if pokemon_response.status_code == 200:
                    pokemon_json = pokemon_response.json()
                    pokemon_data = {
                        'name': pokemon_json.get('name', '').capitalize(),
                        'sprite': pokemon_json.get('sprites', {}).get('front_default', ''),
                        'types': [t.get('type', {}).get('name', '').capitalize() for t in pokemon_json.get('types', [])],
                        'height': pokemon_json.get('height', 0),
                        'weight': pokemon_json.get('weight', 0)
                    }
            except Exception as e:
                logger.error(f"Error fetching Pokemon data: {str(e)}")
                # Don't fail the whole request, just log the error and continue
                # pokemon_data remains None
        
        # Get Weather data
        weather_data = None
        if product.location:
            try:
                if OPENWEATHER_API_KEY:
                    weather_response = requests.get(
                        f"https://api.openweathermap.org/data/2.5/weather?q={product.location}&appid={OPENWEATHER_API_KEY}&units=metric",
                        timeout=3  # Short timeout to not delay the overall response
                    )
                    if weather_response.status_code == 200:
                        weather_json = weather_response.json()
                        temp_celsius = weather_json.get('main', {}).get('temp', 0)
                        temp_fahrenheit = (temp_celsius * 9/5) + 32
                        
                        weather_data = {
                            'city': product.location,
                            'temperature_celsius': temp_celsius,
                            'temperature_fahrenheit': temp_fahrenheit,
                            'condition': weather_json.get('weather', [{}])[0].get('main', ''),
                            'description': weather_json.get('weather', [{}])[0].get('description', ''),
                            'icon': weather_json.get('weather', [{}])[0].get('icon', '')
                        }
            except Exception as e:
                logger.error(f"Error fetching weather data: {str(e)}")
                # Don't fail the whole request, just log the error and continue
                # weather_data remains None
        
        return JsonResponse({
            'success': True,
            'product': product.to_json(),
            'visuals': [visual.to_json() for visual in visuals],
            'pokemon': pokemon_data,  # May be None, frontend handles this
            'weather': weather_data   # May be None, frontend handles this
        })
    except Exception as e:
        logger.error(f"Error fetching product details: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': 'Error fetching product details',
            'error_type': 'UNKNOWN_ERROR',
            'details': str(e)
        }, status=500)