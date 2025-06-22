# Import necessary modules
from json import dumps, dump
from pathlib import Path

from flask import Flask, request, render_template  # Flask for building web routes, request for reading URL parameters
from flask_sqlalchemy import SQLAlchemy   # SQLAlchemy is a database toolkit for Python
import os                                 # Used to access environment variables like the database URL

OUTPUT_PATH = Path('OUTPUT')

# Create the Flask application
app = Flask(__name__)

# Set up the database configuration using the environment variable "DATABASE_URL"
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")

# Disable a warning message (not harmful, but unnecessary)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy with the Flask app
db = SQLAlchemy(app)

# Define a model (table) for storing messages in the database
class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)

@app.route("/", methods=["GET"])
def home():
    people = Person.query.all()
    return render_template("home.html", people=people)

@app.route("/add", methods=["POST"])
def add_person():
    # Create a dictionary from form data
    data = {
        "name": request.form.get("name"),
        "email": request.form.get("email"),
        "age": int(request.form.get("age"))
    }


    # Save it to the database
    person = Person(**data)
    db.session.add(person)
    db.session.commit()

    return "Person added! <a href='/'>Go back</a>"

@app.route("/delete/<int:msg_id>", methods=["POST"])
def delete_message(msg_id):
    person = Person.query.get_or_404(msg_id)
    db.session.delete(person)
    db.session.commit()
    return "Person deleted! <a href='/'>Go back</a>"


@app.route("/debug")
def debug_data():
    people = Person.query.all()

    # Turn all people into a list of dictionaries
    data = []
    for person in people:
        entry = {
            "id": person.id,
            "name": person.name,
            "email": person.email,
            "age": person.age
        }
        data.append(entry)

    # Display as plain text
    return f"<pre>{data}</pre>"


# Create the database tables (only runs if they don't exist yet)
with app.app_context():
    db.create_all()

# Start the app if run locally
if __name__ == "__main__":
    app.run(debug=True)
