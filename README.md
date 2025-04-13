# WildcatWear
### By: Tiffany Adora (23792114)

WildcatWear is an e-commerce website selling University of Arizona merchandise, built with Django for the backend and HTML/CSS/JavaScript on the frontend. For this assignment, the focus is on fetching and displaying data dynamically using both server-side endpoints and external APIs. 

New Features: real-time weather data, Pokémon content, and dynamic product details loaded via JavaScript.

This is a continuation of the WildcatWear-website project.

## API Integration Features

This website integrates three API sources:

1. **Pokémon API** (https://pokeapi.co/): Each product is associated with a Pokémon, displayed on the product detail page.
2. **OpenWeather API** (https://openweathermap.org/): Shows real-time weather for the location each product ships from.
3. **Custom API**: Server-side API endpoints to access product data from CSV files.

## API Endpoints

The following API endpoints are available:

- `/api/products/` - Get all products
- `/api/products/<product_id>/` - Get details for a specific product
- `/api/pokemon/<pokemon_name>/` - Get Pokémon data
- `/api/weather/<city_name>/` - Get weather data for a city

## OpenWeather API Key Setup

To use the weather functionality, you need to set up your OpenWeather API key environment variable:

1. Go to https://openweathermap.org/ and make a new account if you have not.
2. After logged in, click on your profile and go to "My API Keys"
3. Copy your API Key

### For Linux/Mac
```bash
export OPENWEATHER_API_KEY=your_api_key_here
```
### For Windows (Command Prompt)
```bash
set OPENWEATHER_API_KEY=your_api_key_here
```
### For Windows (Powershell)
```bash
$env:OPENWEATHER_API_KEY = "your_api_key_here"
```

## Error Handling

This application implements comprehensive error handling for API requests:

- **Server-side**: Each API endpoint has proper error handling for timeouts, connection errors, and invalid data.
- **Client-side**: The UI gracefully degrades if API data is unavailable, showing appropriate fallback content.

## How to Set-up

To run this project, please follow the steps below:

1. Clone the repository
    ```
    git clone [repository-url]
    cd wildcatwear
    ```
2. Set up a virtual environment
   ```
    # Windows
    python -m venv venv
    venv\Scripts\activate

    # Linux/Mac
    python -m venv venv
    source venv/bin/activate
    ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. **Collect static files**
    ```
    python manage.py collectstatic
    ```
    **This is very important.** If prompted, type "Yes" to copy all the static files.

5. Run the Django development server:
   ```bash
   python manage.py runserver
   ```
6. Open your browser and go to: http://127.0.0.1:8000/

## Test it out

1. Click on any product in the website
2. In the product page, there should be 2 containers below the product section:
   - Pokemon Mascot (Name, image of the pokemon, type, height, weight)
   - Shipping Location (Current Weather, temperature, humidity, wind, shipping information)

## Current Project Structure

```bash
wildcatwear/
|
├── static/                     # Static Files
|   ├── data/                     # CSV data files      
|   |   ├── product.csv           # Product information (Name, Desc, Price, etc.)
|   |   ├── visualcontent.csv     # Visual content information (ID, Name, File type,etc)
|   ├── css/        
|   |   ├── store.css           # Product page styles
|   |   ├── style.css           # Site-wide style
|   |   ├── utility-styles.css  # Utility classes
|   ├── js/                     # JavaScript files
│   │   ├── api-service.js      # JavaScript for API interactions
│   │   ├── product-data.js    # CSV parsing and data handling
│   │   ├── product-submission.js  # Product form handling
│   │   ├── product-navigation.js  # Product browsing
│   │   ├── search.js          # Live search functionality
│   │   ├── sorting.js         # Product sorting
│   │   ├── comment-system.js  # Product comments
│   │   └── like-system.js     # Product likes/favorites
|   ├── images/                 # Images assets
|
├── store/                      # Main application
|   ├── migrations/             # Django migrations
|   ├── templates/              # HTML templates
|   |   ├── index.html          # Home page template
|   |   ├── search.html         # Search results template
|   |   ├── store.html          # Product details template
|   |   ├── admin-tools.html    # Admin tools template
|   |
|   ├── templatetags/           # Custom template tags
|   |   ├── custom_filters.py   # Custom filters for template
|   |
|   ├── api_views.py            # API endpoint implementations
|   ├── models.py               # Data Model
|   ├── views.py                # page view handlers
|   ├── urls.py                 # App URL Routing
|   ├── tests.py                # Test script
|
├── wildcatwear/                # Project configuration
|   ├── settings.py             # Django settings  
|   ├── urls.py                 # Project URL Routing
|   ├── wsgi.py, asgi.py        # WSGI & ASGI config
|
├── manage.py                   # Django management script
├── db.sqlite3                  # SQLite database (not used for CSV-based data)
```
