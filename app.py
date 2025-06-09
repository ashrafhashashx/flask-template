from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(100), nullable=False)

@app.route("/")
def home():
    messages = Message.query.all()
    return "<br>".join([f"{m.id}: {m.text}" for m in messages])

@app.route("/add")
def add_message():
    text = request.args.get("text", "Hello from Flask!")
    msg = Message(text=text)
    db.session.add(msg)
    db.session.commit()
    return f"Added: {msg.text}"

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
