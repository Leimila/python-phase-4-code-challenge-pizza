
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


@app.route("/restaurants", methods=["GET"])
def get_restaurants():
    restaurants = Restaurant.query.all()
    return jsonify([
        {"id": r.id, "name": r.name, "address": r.address} for r in restaurants
    ]), 200
    
# Get a single restaurant by ID
@app.route("/restaurants/<int:id>", methods=["GET"])
def get_restaurant(id):
    restaurant = Restaurant.query.get(id)
    if restaurant:
        return jsonify(restaurant.to_dict()), 200
    return jsonify({"error": "Restaurant not found"}), 404


@app.route("/restaurants/<int:id>", methods=["DELETE"])
def delete_restaurant(id):
    restaurant = Restaurant.query.get(id)
    
    if not restaurant:
        return jsonify({"error": "Restaurant not found"}), 404

    # Delete associated restaurant_pizzas
    RestaurantPizza.query.filter_by(restaurant_id=id).delete()

    # Delete the restaurant itself
    db.session.delete(restaurant)
    db.session.commit()

    return '', 204  # 🔥 Return an empty response with status 204



# Get all pizzas
@app.route("/pizzas", methods=["GET"])
def get_pizzas():
    pizzas = Pizza.query.all()
    return jsonify([pizza.to_dict(only=("id", "name", "ingredients")) for pizza in pizzas]), 200
    # return jsonify([pizza.to_dict() for pizza in pizzas]), 200

@app.route("/restaurant_pizzas", methods=["GET"])
def get_restaurant_pizzas():
    restaurant_pizzas = RestaurantPizza.query.all()
    return jsonify([rp.to_dict() for rp in restaurant_pizzas]), 200

# Add a deleted Restaurant
@app.route("/restaurants", methods=["POST"])
def create_restaurant():
    data = request.get_json()
    name = data.get("name")
    address = data.get("address")

    if not name or not address:
        return jsonify({"error": "Missing name or address"}), 400

    new_restaurant = Restaurant(name=name, address=address)
    db.session.add(new_restaurant)
    db.session.commit()

    return jsonify(new_restaurant.to_dict()), 201




@app.route("/restaurant_pizzas", methods=["POST"])
def create_restaurant_pizza():
    data = request.get_json()
    try:
        new_pizza = RestaurantPizza(
            price = data['price'],
            restaurant_id = data['restaurant_id'],
            pizza_id = data["pizza_id"]
        )
        db.session.add(new_pizza)
        db.session.commit() 

        response = new_pizza.to_dict(rules=("pizza", "restaurant"))
        return make_response(jsonify(response), 201,)

    except Exception as e:
        return make_response(jsonify({"errors" : ['validation errors']}), 400)
        pass
    





if __name__ == "__main__":
    app.run(port=5555, debug=True)



