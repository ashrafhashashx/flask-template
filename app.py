# Import necessary modules
from flask import Flask, request, render_template  # Flask for building web routes, request for reading URL parameters
from flask_sqlalchemy import SQLAlchemy   # SQLAlchemy is a database toolkit for Python
import os                                 # Used to access environment variables like the database URL

# Create the Flask application
app = Flask(__name__)

# Set up the database configuration using the environment variable "DATABASE_URL"
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")

# Disable a warning message (not harmful, but unnecessary)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy with the Flask app
db = SQLAlchemy(app)

# Define a model (table) for storing messages in the database
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)        # Unique ID for each message (auto-increment)
    text = db.Column(db.String(100), nullable=False)    # Text of the message (required field)

# # Route for the home page: shows all messages in the database
# @app.route("/")
# def home():
#     messages = Message.query.all()  # Fetch all messages
#     return "<br>".join([f"{m.id}: {m.text}" for m in messages])  # Show messages as simple HTML
#
# # Route to add a new message: /add?text=YourMessage
# @app.route("/add")
# def add_message():
#     text = request.args.get("text", "Hello from Flask!")  # Get message text from URL parameter
#     msg = Message(text=text)                              # Create new Message object
#     db.session.add(msg)                                   # Add it to the session
#     db.session.commit()                                   # Save it to the database
#     return f"Added: {msg.text}"                           # Confirmation

@app.route("/", methods=["GET"])
def home():
    messages = Message.query.all()
    return render_template("home.html", messages=messages)

@app.route("/add", methods=["POST"])
def add_message():
    text = request.form.get("text")
    msg = Message(text=text)
    db.session.add(msg)
    db.session.commit()
    return "Message added! <a href='/'>Go back</a>"

# Create the database tables (only runs if they don't exist yet)
with app.app_context():
    db.create_all()

# Start the app if run locally
if __name__ == "__main__":
    app.run(debug=True)
