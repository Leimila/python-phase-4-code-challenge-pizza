# #!/usr/bin/env python3
# from models import db, Restaurant, RestaurantPizza, Pizza
# from flask_migrate import Migrate
# from flask import Flask, request, make_response
# from flask_restful import Api, Resource
# import os

# BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

# app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# app.json.compact = False

# migrate = Migrate(app, db)

# db.init_app(app)

# api = Api(app)


# @app.route("/")
# def index():
#     return "<h1>Code challenge</h1>"


# if __name__ == "__main__":
#     app.run(port=5555, debug=True)
#!/usr/bin/env python3
import os
from flask import Flask, request, jsonify, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Restaurant, RestaurantPizza, Pizza

# Set up database configuration
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE_URI = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

# Initialize Flask app
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

# Initialize database & migrations
db.init_app(app)
migrate = Migrate(app, db)

# Initialize Flask-RESTful API
api = Api(app)

# Welcome route
@app.route("/")
def index():
    return "<h1>Code Challenge API</h1>"

# Define API resources
# class RestaurantsResource(Resource):
#     def get(self):
#         restaurants = Restaurant.query.all()
#         return jsonify([restaurant.to_dict() for restaurant in restaurants])

# api.add_resource(RestaurantsResource, "/restaurants")

# class Restaurantbyid(Resource):
#     def get(self, restaurant_id):
#         restaurant = Restaurant.query.get(restaurant_id)
#         return make_response(restaurant.to_dict(),200)

# api.add_resource (Restaurantbyid, '/restaurants/<int:restaurant_id>')
@app.route("/restaurants", methods=["GET"])
def get_restaurants():
    restaurants = Restaurant.query.all()
    return jsonify([restaurant.to_dict() for restaurant in restaurants]), 200

# Get a single restaurant by ID
@app.route("/restaurants/<int:id>", methods=["GET"])
def get_restaurant(id):
    restaurant = Restaurant.query.get(id)
    if restaurant:
        return jsonify(restaurant.to_dict()), 200
    return jsonify({"error": "Restaurant not found"}), 404

# Delete a restaurant by ID
@app.route("/restaurants/<int:id>", methods=["DELETE"])
def delete_restaurant(id):
    restaurant = Restaurant.query.get(id)
    if restaurant:
        db.session.delete(restaurant)
        db.session.commit()
        return jsonify({"message": "Restaurant deleted"}), 200
    return jsonify({"error": "Restaurant not found"}), 404

# Get all pizzas
@app.route("/pizzas", methods=["GET"])
def get_pizzas():
    pizzas = Pizza.query.all()
    return jsonify([pizza.to_dict() for pizza in pizzas]), 200

# Add a new RestaurantPizza
@app.route("/restaurant_pizzas", methods=["POST"])
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
if __name__ == "__main__":
    app.run(port=5555, debug=True)
