import dbm
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"

# already going to have some build in functionality from flask alchemy db
class Drink(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # maximum 80 characters
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(120))

    def __repr__(self):
        return f"{self.name} - {self.description}"


@app.route("/")
def index():
    return "Hello!"


@app.route("/drinks")
def get_drinks():
    drinks = Drink.query.all()
    output = []

    for drink in drinks:
        output.append({"name": drink.name, "description": drink.description})

    return {"drinks": output}


@app.route("/drinks/<id>")
def get_drink(id):
    drink = Drink.query.get_or_404(id)
    return {"name": drink.name, "description": drink.description}


@app.route("/drinks", methods=["POST"])
def add_drink():
    drink = Drink(name=request.json["name"], description=request.json["description"])
    db.session.add(drink)
    db.session.commit()
    return {"id": drink.id}


@app.route("/drinks/<id>", methods=["DELETE"])
def delete_drink(id):
    drink = Drink.query.get(id)
    if drink is None:
        response = jsonify(
            {"status": 404, "error": "not found", "message": "invalid id"}
        )
        response.status_code = 404
        return response

    db.session.delete(drink)
    db.session.commit()

    return jsonify({"status": 200, "success": "Deleted!"})


# Warning: Silently ignoring app.run() because the application is run from the flask command line executable.
# Consider putting app.run() behind an if __name__ == "__main__" guard to silence this warning.
if __name__ == "__main__":
    app.run()
