from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/information'
mongo = PyMongo(app)

@app.route('/')
def index():
    trips = mongo.db.trips.find()
    return render_template('index.html', trips=trips)

@app.route('/add_trip', methods=['POST'])
def add_trip():
    destination = request.form.get('destination')
    date = request.form.get('date')
    hotel = request.form.get('hotel')
    places_to_visit = request.form.get('places_to_visit')
    budget = request.form.get('budget')
    mongo.db.trips.insert_one({
        'destination': destination,
        'date': date,
        'hotel': hotel,
        'places_to_visit': places_to_visit,
        'budget': budget
    })
    return redirect(url_for('index'))

@app.route('/trip/<trip_id>')
def trip_detail(trip_id):
    try:
        trip = mongo.db.trips.find_one({'_id': ObjectId(trip_id)})
        if trip:
            # Convert the ObjectId to a string for JSON serialization
            trip['_id'] = str(trip['_id'])
            return jsonify(trip)
        return jsonify({'error': 'Trip not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/edit_trip', methods=['POST'])
def edit_trip():
    trip_id = request.form.get('trip_id')
    destination = request.form.get('destination')
    date = request.form.get('date')
    hotel = request.form.get('hotel')
    places_to_visit = request.form.get('places_to_visit')
    budget = request.form.get('budget')

    mongo.db.trips.update_one(
        {'_id': ObjectId(trip_id)},
        {'$set': {
            'destination': destination,
            'date': date,
            'hotel': hotel,
            'places_to_visit': places_to_visit,
            'budget': budget
        }}
    )
    return redirect(url_for('index'))

@app.route('/delete_trip/<trip_id>', methods=['POST'])
def delete_trip(trip_id):
    mongo.db.trips.delete_one({'_id': ObjectId(trip_id)})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
