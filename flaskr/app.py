from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

from random import randint
import os

# App config
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/ubuntu/webpage/flaskr/database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_AUTOFLUSH'] = False
    db.init_app(app)
    return app

app = create_app()
app.app_context().push()

# Prices generation
types = ["Fotovoltaic", "Vodni", "Tepelna", "Jaderna"]
prices = [
        [randint(100, 150) * 100 for i in range(5)],
        [randint(150, 225) * 100 for i in range(5)],
        [randint(250, 375) * 100 for i in range(5)],
        [randint(500, 750) * 100 for i in range(5)]
        ]

# Database declaration
class Company(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), nullable = False)
    finance = db.Column(db.Integer, nullable = False)

    plants = db.relationship("Plant", back_populates = "company")
    users = db.relationship("User", back_populates = "company")
    

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), nullable = False)
    finance = db.Column(db.Integer, nullable = False)

    company_id = db.Column(db.Integer, db.ForeignKey("company.id"))
    company = db.relationship("Company", back_populates = "users")

    plants = db.relationship("Plant", back_populates = "owner")

    def __repr__(self):
        return str(self.id)

class Plant(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    type = db.Column(db.Integer, nullable = False)
    # 0 - foto, 1 - water, 2 - heat, 3 - nuclear
    cost = db.Column(db.Integer, nullable = False)
    age = db.Column(db.Integer, nullable = False)
    active = db.Column(db.Boolean, nullable = False)

    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    company_id = db.Column(db.Integer, db.ForeignKey("company.id"))

    owner = db.relationship("User", back_populates = "plants")
    company = db.relationship("Company", back_populates = "plants")

    def __repr__(self):
        return str(self.id) 


# App routes
@app.route("/")
def index():
    return render_template('others/index.html')

@app.route("/akce")
def akce():
    return render_template('others/akce.html')


@app.route("/powerplants")
def powerplants():
    users = User.query.order_by(User.name)
    companies = Company.query.all()
    return render_template('powerplants/index.html', users = users, companies = companies)

@app.route("/powerplants/users/<int:id>")
def user_page(id):
    user = User.query.get(id)
    plants = Plant.query.filter_by(owner_id = user.id).order_by(Plant.type)
    count = plants.count()
    return render_template('powerplants/user.html', user = user, types = types, plants = plants, count = count)

@app.route("/powerplants/companies/<int:id>")
def company_page(id):
    company = Company.query.get(id)
    plants = Plant.query.filter_by(company_id = company.id).order_by(Plant.type)
    count = plants.count()
    return render_template('powerplants/company.html', company = company, types = types, plants = plants, count = count)

@app.route("/powerplants/plants")
def plant_page():
    return render_template("powerplants/plants.html", types = types, prices = prices, amount = 4)

@app.route("/powerplants/rules")
def rules_page():
    return render_template("powerplants/rules.html")

if __name__ == '__main__':
    app.run(host="0.0.0.0")


