from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///valentines.db'  # SQLite database URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

def random_pairer():
    # Use app.app_context() when creating tables
    with app.app_context():
    # Create tables if they don't exist
        db.create_all()

    # Check if the database is empty, and if so, run the random pairing logic
    if not ValentinesPair.query.first():

        guys = ["Cecil", "Hargine", "Caleb", "Phil", "Johnmark", "Immanuel"]
        girls = ["Fiona", "Yvonne", "Ericah", "Stacey", "Phoebe", "Gloria"]
        
        random.shuffle(guys)
        random.shuffle(girls)

        # Store the results in the database
        for guy, girl in zip(guys, girls):
            pair = ValentinesPair(guy=guy, girl=girl)
            db.session.add(pair)

        db.session.commit()

class ValentinesPair(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    guy = db.Column(db.String(50), nullable=False)
    girl = db.Column(db.String(50), nullable=False)

with app.app_context():
    random_pairer()

# Rest of your code...
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/find_partner', methods=['POST'])
def find_partner():
    name = request.form.get('name').capitalize()
    partner = ValentinesPair.query.filter((ValentinesPair.guy == name) | (ValentinesPair.girl == name)).first()

    return render_template('result.html', name=name, partner=partner)

@app.route('/clear_database', methods=['GET', 'POST'])
def clear_database():
    if request.method == 'POST':
        # Drop the entire table and recreate it
        db.session.execute(text('DROP TABLE IF EXISTS valentines_pair'))
        db.session.commit()
        
        # Create tables if they don't exist
        db.create_all()
        random_pairer()

        return redirect(url_for('index'))

    return render_template('clear_database.html')

if __name__ == '__main__':
    app.run(debug=True)