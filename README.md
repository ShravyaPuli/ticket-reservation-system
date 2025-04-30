# Indian Ticket Reservation System

A simple ticket reservation system built with Python and Flask, designed for booking train and bus tickets in an Indian context. This application doesn't use a database and stores all data in memory.

## Features

- View and book train tickets
- View and book bus tickets
- Select seat class and quantity
- Enter passenger details
- Generate booking confirmation with unique booking ID
- View booking details using the booking ID
- Cancel bookings

## Technologies Used

- Python 3.8+
- Flask 2.0.1
- HTML/CSS
- In-memory data storage (no database)

## Installation

1. Clone this repository or download the code
2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
3. Activate the virtual environment:
   - Windows:
     ```
     venv\Scripts\activate
     ```
   - Mac/Linux:
     ```
     source venv/bin/activate
     ```
4. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Running the Application

1. Make sure your virtual environment is activated
2. Run the Flask application:
   ```
   python app.py
   ```
3. Open your web browser and navigate to:
   ```
   http://127.0.0.1:5000/
   ```

## Usage

1. **Home Page**:
   - Choose to book train or bus tickets
   - Access your existing bookings

2. **Booking Process**:
   - Select a train or bus
   - Choose class type and number of seats
   - Enter passenger details
   - Confirm your booking
   - Get a booking confirmation with a unique booking ID

3. **Managing Bookings**:
   - Use your booking ID to view booking details
   - Cancel your booking if needed

## Note

Since this application doesn't use a database, all data is stored in memory and will be reset when the server is restarted. In a production environment, you would want to use a proper database for data persistence.

## Indian Context Considerations

- Train and bus routes based on popular Indian cities
- Multiple class types for Indian trains (Sleeper, AC 3-Tier, etc.)
- Indian bus service types (AC, Non-AC, Sleeper, etc.)
- Interface design with colors inspired by the Indian flag #
