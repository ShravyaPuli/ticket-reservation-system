from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
import uuid
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.urandom(24)

# In-memory data storage
trains = [
    {
        "id": "12345",
        "name": "Rajdhani Express",
        "source": "New Delhi",
        "destination": "Mumbai",
        "departure": "16:00",
        "arrival": "08:30",
        "price": 1200,
        "class_types": ["Sleeper", "AC 3-Tier", "AC 2-Tier", "AC First Class"]
    },
    {
        "id": "22222",
        "name": "Shatabdi Express",
        "source": "Chennai",
        "destination": "Bangalore",
        "departure": "06:00",
        "arrival": "12:30",
        "price": 850,
        "class_types": ["Chair Car", "Executive Class"]
    },
    {
        "id": "33333",
        "name": "Duronto Express",
        "source": "Kolkata",
        "destination": "Delhi",
        "departure": "22:00",
        "arrival": "10:45",
        "price": 1500,
        "class_types": ["Sleeper", "AC 3-Tier", "AC 2-Tier"]
    },
    {
        "id": "44444",
        "name": "Vande Bharat Express",
        "source": "Ahmedabad",
        "destination": "Mumbai",
        "departure": "07:30",
        "arrival": "13:45",
        "price": 1050,
        "class_types": ["Chair Car", "Executive Class"]
    }
]

buses = [
    {
        "id": "B1001",
        "name": "Volvo AC Sleeper",
        "source": "Hyderabad",
        "destination": "Bangalore",
        "departure": "21:00",
        "arrival": "06:00",
        "price": 950,
        "class_types": ["AC Sleeper", "AC Seater"]
    },
    {
        "id": "B1002",
        "name": "Shrinath Travels",
        "source": "Jaipur",
        "destination": "Delhi",
        "departure": "18:30",
        "arrival": "23:45",
        "price": 450,
        "class_types": ["Non-AC Seater", "AC Seater"]
    },
    {
        "id": "B1003",
        "name": "SRS Travels",
        "source": "Chennai",
        "destination": "Coimbatore",
        "departure": "22:30",
        "arrival": "05:45",
        "price": 700,
        "class_types": ["AC Sleeper", "AC Semi-Sleeper"]
    }
]

# Store bookings
bookings = {}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/trains')
def train_list():
    return render_template('train_list.html', trains=trains)

@app.route('/buses')
def bus_list():
    return render_template('bus_list.html', buses=buses)

@app.route('/select_seat/<transport_type>/<transport_id>')
def select_seat(transport_type, transport_id):
    if transport_type == 'train':
        for train in trains:
            if train['id'] == transport_id:
                return render_template('select_seat.html', transport=train, transport_type=transport_type)
    else:
        for bus in buses:
            if bus['id'] == transport_id:
                return render_template('select_seat.html', transport=bus, transport_type=transport_type)
    
    flash('Invalid selection')
    return redirect(url_for('home'))

@app.route('/passenger_info/<transport_type>/<transport_id>', methods=['GET', 'POST'])
def passenger_info(transport_type, transport_id):
    if request.method == 'POST':
        class_type = request.form.get('class_type')
        seats = request.form.get('seats', type=int)
        
        if transport_type == 'train':
            transport = next((t for t in trains if t['id'] == transport_id), None)
        else:
            transport = next((b for b in buses if b['id'] == transport_id), None)
        
        if not transport:
            flash('Invalid selection')
            return redirect(url_for('home'))
        
        session['booking_details'] = {
            'transport_type': transport_type,
            'transport_id': transport_id,
            'class_type': class_type,
            'seats': seats,
            'price': transport['price'] * seats
        }
        
        return render_template('passenger_info.html', transport=transport, 
                              seats=seats, class_type=class_type)
    
    return redirect(url_for('home'))

@app.route('/confirm_booking', methods=['POST'])
def confirm_booking():
    if 'booking_details' not in session:
        flash('Session expired. Please start again.')
        return redirect(url_for('home'))
    
    booking_details = session['booking_details']
    passengers = []
    
    # Get passenger details from form
    for i in range(1, booking_details['seats'] + 1):
        passenger = {
            'name': request.form.get(f'name_{i}'),
            'age': request.form.get(f'age_{i}'),
            'gender': request.form.get(f'gender_{i}'),
            'seat_number': f"{booking_details['class_type']}-{i}"
        }
        passengers.append(passenger)
    
    # Generate booking ID
    booking_id = str(uuid.uuid4())[:8].upper()
    
    # Get transport details
    if booking_details['transport_type'] == 'train':
        transport = next((t for t in trains if t['id'] == booking_details['transport_id']), None)
    else:
        transport = next((b for b in buses if b['id'] == booking_details['transport_id']), None)
    
    if not transport:
        flash('Invalid selection')
        return redirect(url_for('home'))
    
    # Create booking record
    booking = {
        'booking_id': booking_id,
        'transport_type': booking_details['transport_type'],
        'transport': transport,
        'class_type': booking_details['class_type'],
        'passengers': passengers,
        'total_price': booking_details['price'],
        'booking_date': datetime.now().strftime('%d-%m-%Y %H:%M'),
        'journey_date': datetime.now().strftime('%d-%m-%Y'),  # In a real app, this would be selected by user
        'status': 'Confirmed'
    }
    
    # Save booking
    bookings[booking_id] = booking
    
    # Clear session data
    session.pop('booking_details', None)
    
    return render_template('booking_confirmation.html', booking=booking)

@app.route('/my_bookings', methods=['GET', 'POST'])
def my_bookings():
    if request.method == 'POST':
        booking_id = request.form.get('booking_id').strip().upper()
        if booking_id in bookings:
            return render_template('booking_details.html', booking=bookings[booking_id])
        flash('Booking not found')
    
    return render_template('my_bookings.html')

@app.route('/cancel_booking/<booking_id>')
def cancel_booking(booking_id):
    if booking_id in bookings:
        booking = bookings[booking_id]
        booking['status'] = 'Cancelled'
        flash('Booking cancelled successfully')
        return render_template('booking_details.html', booking=booking)
    
    flash('Booking not found')
    return redirect(url_for('my_bookings'))

if __name__ == '__main__':
    app.run(debug=True) 