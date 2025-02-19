from flask import Blueprint, jsonify, request
from models import db, Restaurant, Pizza, RestaurantPizza

routes = Blueprint("routes", __name__)

# Get all restaurants
@routes.route("/restaurants", methods=["GET"])
def get_restaurants():
    restaurants = Restaurant.query.all()
    return jsonify([restaurant.to_dict() for restaurant in restaurants]), 200

# Get a single restaurant by ID
@routes.route("/restaurants/<int:id>", methods=["GET"])
def get_restaurant(id):
    restaurant = Restaurant.query.get(id)
    if restaurant:
        return jsonify(restaurant.to_dict()), 200
    return jsonify({"error": "Restaurant not found"}), 404

# Delete a restaurant by ID
@routes.route("/restaurants/<int:id>", methods=["DELETE"])
def delete_restaurant(id):
    restaurant = Restaurant.query.get(id)
    if restaurant:
        db.session.delete(restaurant)
        db.session.commit()
        return jsonify({"message": "Restaurant deleted"}), 200
    return jsonify({"error": "Restaurant not found"}), 404

# Get all pizzas
@routes.route("/pizzas", methods=["GET"])
def get_pizzas():
    pizzas = Pizza.query.all()
    return jsonify([pizza.to_dict() for pizza in pizzas]), 200

# Add a new RestaurantPizza
@routes.route("/restaurant_pizzas", methods=["POST"])
def create_restaurant_pizza():
    data = request.get_json()
    price = data.get("price")
    pizza_id = data.get("pizza_id")
    restaurant_id = data.get("restaurant_id")
    
    if not price or not pizza_id or not restaurant_id:
        return jsonify({"error": "Missing required fields"}), 400
    
    if not (1 <= price <= 30):
        return jsonify({"error": "Price must be between 1 and 30"}), 400
    
    restaurant = Restaurant.query.get(restaurant_id)
    pizza = Pizza.query.get(pizza_id)
    
    if not restaurant or not pizza:
        return jsonify({"error": "Invalid restaurant or pizza ID"}), 404
    
    new_restaurant_pizza = RestaurantPizza(price=price, restaurant_id=restaurant_id, pizza_id=pizza_id)
    db.session.add(new_restaurant_pizza)
    db.session.commit()
    
    return jsonify(pizza.to_dict()), 201
