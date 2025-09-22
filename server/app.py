#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, jsonify
from flask_restful import Api
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


@app.route("/")
def index():
    return "<h1>Code challenge</h1>"

@app.route('/restaurants',methods=["GET"])
def get_restaurants():
    restaurants=[r.to_dict() for r in Restaurant.query.all()]
    return jsonify(restaurants)

@app.route("/restaurants/<int:id>",methods=["GET","DELETE"])
def restaurant_by_id(id):
    restaurant=Restaurant.query.get(id)
    if not restaurant:
        return {"error":"Restaurant not found"},400
    if request.method=="GET":
        return restaurant.to_dict()
    if request.method=="DELETE":
        db.session.delete(restaurant)
        db.session.commit()
        return "",204
    



@app.route("/pizzas",methods=["GET"])
def get_pizzas():
    pizzas=[p.to_dict() for p in Pizza.query.all()]
    return jsonify(pizzas)

@app.route("/restaurant_pizzas",methods=["POST"])
def create_restaurant_pizza():
    data=request.get_json()
    try:
        new_rp=RestaurantPizza(
            price=data["price"],
            pizza_id=data["pizza_id"],
            restaurant_id=data["restaurant_id"],
        )
        db.session.add(new_rp)
        db.session.commit()
        return new_rp.pizza.to_dict(),201
    except:
        return{"errors":["validation errors"]},400   



if __name__ == "__main__":
    app.run(port=5555, debug=True)
