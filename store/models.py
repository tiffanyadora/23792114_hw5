from django.db import models

import csv
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PRODUCTS_FILE = os.path.join(BASE_DIR, 'static', 'data', 'product.csv')
VISUALS_FILE = os.path.join(BASE_DIR, 'static', 'data', 'visualcontent.csv')

class Product:
    # Constructor for Product class
    # It initializes the Product's attributes when a new instance is created

    # Update: added Pokemon and Location columns
    def __init__(self, id, name, description, feature, rating, price, category, pokemon, location):
        self.product_id = id
        self.name = name
        self.description = description
        self.feature = feature
        self.rating = float(rating)
        self.price = float(price)
        self.category = category
        self.pokemon = pokemon
        self.location = location

    # Setter for new price of a product
    def set_price(self, new_price):
        self.price = float(new_price)
    
    # Setter for new rating of a product
    def set_rating(self, new_rating):
        self.rating = float(new_rating)

    @classmethod
    # Helper (Getter) method to read products from CSV and return a list of dictionaries.
    # Update: added the Pokemon and Location rows of each product 
    def read_products(cls):
        with open(PRODUCTS_FILE, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            return [
                {
                    "id": row.get("ID", ""),
                    "name": row.get("Name", ""),
                    "description": row.get("Description", ""),
                    "feature": row.get("Feature", ""),
                    "rating": row.get("Average Rating", 0),
                    "price": row.get("Price", 0),
                    "category": row.get("Category", ""),
                    "pokemon": row.get("Pokemon", ""),
                    "location": row.get("Location", ""),
                }
                for row in reader
            ]

    @classmethod
    # Getter method to fetch all products from Product CSV
    def get_all(cls):
        return [cls(**product) for product in cls.read_products()]
    
    @classmethod
    def get_product_by_category(cls, category):
        products = [
            cls(**product) for product in cls.read_products() 
            if product["category"].lower() == category.lower()
        ]
        return products

    @classmethod
    # Getter method to fetch a single product by its ID
    def get_by_id(cls, product_id):
        for product in cls.read_products():
            if product["id"] == product_id:
                return cls(**product)
        return None

    # Getter method to fetch image file name from VisualContent CSV
    def get_image_name(self):
        visuals = VisualContent.get_for_product(self.product_id)
        if visuals:
            visual = visuals[0]
            file_name = f"{visual.short_name}.{visual.file_type}"
            return file_name.replace(" ", "_") 
        return "default.jpg" 

    @classmethod
    def add_product(cls, product_data):
        with open(PRODUCTS_FILE, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([
                product_data['id'],
                product_data['name'],
                product_data['description'],
                product_data['feature'],
                product_data['rating'],
                product_data['price'],
                product_data['category'],
                product_data.get('pokemon', ''),
                product_data.get('location', '')
            ])
        return True
    
    # Convert product to JSON serializable dictionary
    def to_json(self):
        return {
            'id': self.product_id,
            'name': self.name,
            'description': self.description,
            'feature': self.feature,
            'rating': self.rating,
            'price': self.price,
            'category': self.category,
            'pokemon': self.pokemon,
            'location': self.location,
            'image': self.get_image_name()
        }

class VisualContent:
    # Constructor for VisualContent class
    # It initializes all attributes related to visual content    
    def __init__(self, id, name, description, short_name, file_type, css_class, product_id):
        self.id = id
        self.name = name
        self.description = description
        self.short_name = short_name
        self.file_type = file_type
        self.css_class = css_class
        self.product_id = product_id

    # Getter method to fetch all visual content associated with a specific product
    @classmethod
    def get_for_product(cls, product_id):
        visuals = []
        with open (VISUALS_FILE, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["Product ID"] == product_id:
                    formatted_row = {
                        "id" : row["ID"],
                        "name" : row["Name"],
                        "description" : row["Description"],
                        "short_name" : row["Short Name"],
                        "file_type" : row["File Type"],
                        "css_class" : row["CSS Class"],
                        "product_id" : row["Product ID"],
                    }
                    visuals.append(cls(**formatted_row))
        return visuals
    
    @classmethod
    def add_visual(cls, visual_data):
        with open(VISUALS_FILE, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([
                visual_data['id'],
                visual_data['name'],
                visual_data['description'],
                visual_data['short_name'],
                visual_data['file_type'],
                visual_data['css_class'],
                visual_data['product_id']
            ])
        return True
    
    # This is to return an HTML <img> tag for the visual contents
    def get_html(self,css_override=None):
        css_class = css_override if css_override else self.css_class
        return f'<img class="{css_class}" alt="{self.description}" src="/static/images/{self.short_name}.{self.file_type}">'
    
    def get_next_visual_id():
        try:
            with open(VISUALS_FILE, newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                visual_ids = [int(row["ID"]) for row in reader if row["ID"].isdigit()]
                return max(visual_ids) + 1 if visual_ids else 1
        except FileNotFoundError:
            return 1
        
    # Convert visual content to JSON serializable dictionary
    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'short_name': self.short_name,
            'file_type': self.file_type,
            'css_class': self.css_class,
            'product_id': self.product_id,
            'img_url': f"/static/images/{self.short_name}.{self.file_type}"
        }