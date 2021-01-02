from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse
import random

app = Flask(__name__)
api = Api(app)
db = SQLAlchemy(app)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///airport_database_3.db'

class Admin(db.Model):
    admin_id = db.Column(db.Integer, primary_key=True)
    login_name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)

class Flight(db.Model):
    flight_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    city_from = db.Column(db.String(50), nullable=False)
    city_to = db.Column(db.String(50), nullable=False)
    flight_info = db.Column(db.String(250), nullable=False)
    arrival_time = db.Column(db.String(50), nullable=False)
    departure_time = db.Column(db.String(50), nullable=False)
    number_of_passengers = db.Column(db.Integer, nullable=False)
'''
flight_arguments = reqparse.RequestParser()
flight_arguments.add_argument('flight_id', type=int)
flight_arguments.add_argument('city_from', type=str)
flight_arguments.add_argument('city_to', type=str)
flight_arguments.add_argument('flight_info', type=str)
flight_arguments.add_argument('arrival-time', type=str)
flight_arguments.add_argument('departure_time', type=str)
flight_arguments.add_argument('number_of_passengers', type=str)
'''
'''
@app.route('/flights/<city_from><city_to>')
def get_flights(city_from, city_to):
    content = ''
    flights = db.Flight.query.filter_by(city_from = city_from, city_to = city_to).all()
    for flight in flights:
        content += 'From: '+flight.city_from+'\n'
        content += 'To: ' + flight.city_to+'\n'
        content += 'Arrival time: ' + flight.arrival_time + '\n'
        content += 'Departure time: ' + flight.departure_time + '\n'
        content += '\n\n\n'

    if len(content) == 0:
        return 'There are no such flights! '
    else:
        return content
'''

class User(Resource):
    def get(self, city_from, city_to):
        flights_arr = []
        flights = Flight.query.filter_by(city_from = city_from, city_to=city_to).all()
        #return flights
        for flight in flights:
            flights_json = {'flight_id':flight.flight_id, 'city_from' : flight.city_from, 'city_to' : flight.city_to, 'arrival_time':flight.arrival_time, 'departure_time':flight.departure_time, 'flight_info':flight.flight_info, 'number_of_passengers':flight.number_of_passengers}
            flights_arr.append(flights_json)

        return flights_arr

sessions = []   #tokens

class Admin_Funcs(Resource):
    def get(self):
        flight_arguments = reqparse.RequestParser()
        flight_arguments.add_argument('from_city', type=str)
        flight_arguments.add_argument('to_city', type=str)
        args = flight_arguments.parse_args()

        flights_arr = []
        flights = Flight.query.filter_by(city_from = args.from_city, city_to = args.to_city).all()
        for flight in flights:
            flights_json = {'flight_id': flight.flight_id, 'city_from': flight.city_from, 'city_to': flight.city_to, 'number_of_passengers':flight.number_of_passengers, 'flight_info':flight.flight_info, 'arrival_time':flight.arrival_time, 'departure-time':flight.departure_time}
            flights_arr.append(flights_json)

        return flights_arr

    def post(self):
        new_flight_arguments = reqparse.RequestParser()
        new_flight_arguments.add_argument("id_flight", type=int)
        new_flight_arguments.add_argument("from_city", type=str)
        new_flight_arguments.add_argument("to_city", type=str)
        new_flight_arguments.add_argument("time_arrival", type=str)
        new_flight_arguments.add_argument("time_departure", type=str)
        new_flight_arguments.add_argument("info_flight", type=str)
        new_flight_arguments.add_argument("num_of_passngrs", type=int)
        args = new_flight_arguments.parse_args()

        old_flight = Flight.query.filter_by(flight_id=args.id_flight).first()
        if (old_flight):
            return 'There is a flight with this id. Try to update it or enter new id. '
        else:
            new_flight = Flight(flight_id=args.id_flight, city_from=args.from_city, city_to=args.to_city, arrival_time=args.time_arrival, departure_time=args.time_departure, flight_info=args.info_flight, number_of_passengers=args.num_of_passngrs)
            db.session.add(new_flight)
            db.session.commit()
            return 'Flight added! '

    def put(self):
        update_flight_args = reqparse.RequestParser()
        update_flight_args.add_argument('id_flight', type=int)
        update_flight_args.add_argument('from_city', type=str)
        update_flight_args.add_argument('to_city', type=str)
        update_flight_args.add_argument('time_arrival', type=str)
        update_flight_args.add_argument('time_departure', type=str)
        update_flight_args.add_argument('info_flight', type=str)
        update_flight_args.add_argument('num_of_passngrs', type=int)
        args = update_flight_args.parse_args()

        flight = Flight.query.filter_by(flight_id=args.id_flight).first()
        if (flight):
            flight.flight_id = args.id_flight
            flight.city_from = args.from_city
            flight.city_to = args.to_city
            flight.arrival_time = args.time_arrival
            flight.departure_time = args.time_departure
            flight.flight_info = args.info_flight
            flight.number_of_passengers = args.num_of_passngrs

            db.session.commit()
            return 'Flight updated! '
        else:
            return 'Flight does not exist! '

    def delete(self):
        delete_flight_args = reqparse.RequestParser()
        delete_flight_args.add_argument('id_flight', type=int)
        args = delete_flight_args.parse_args()

        flight = Flight.query.filter_by(flight_id = args.id_flight).first()
        if (flight):
            db.session.delete(flight)
            db.session.commit()
            return 'Flight deleted! '
        else:
            return 'Flight does not exist. '

class Auth(Resource):
    def post(self):
        auth_token = ''
        admin_login_arguments = reqparse.RequestParser()
        admin_login_arguments.add_argument('login_name', type=str)
        admin_login_arguments.add_argument('password', type=str)
        args = admin_login_arguments.parse_args()

        admin = Admin.query.filter_by(login_name = args.login_name, password = args.password).first()
        if (admin):
            new_token = random.randint(1, 1000000)
            sessions.append(new_token)
            return {'token' : new_token, 's':sessions}
        else:
            return {'token': 0, 's' : sessions}

class All_Flights(Resource):
    def get(self):
        flights_arr = []
        flights = Flight.query.all()
        # return flights
        for flight in flights:
            flights_json = {'flight_id': flight.flight_id, 'city_from': flight.city_from, 'city_to': flight.city_to, 'arrival_time':flight.arrival_time, 'departure_time':flight.departure_time, 'flight_info':flight.flight_info, 'number_of_passengers':flight.number_of_passengers}
            flights_arr.append(flights_json)

        return flights_arr

class End_Session(Resource):
    def delete(self):
        arg = reqparse.RequestParser()
        arg.add_argument('token', type=int)
        args = arg.parse_args()

        if args.token in sessions:
            sessions.remove(args.token)

if __name__ == '__main__':
    api.add_resource(User,'/flights/<string:city_from>/<string:city_to>')
    api.add_resource(Auth, '/authentication_authorization')
    api.add_resource(Admin_Funcs, '/flights')
    api.add_resource(End_Session, '/end_session')
    api.add_resource(All_Flights, '/flights/all')
    #db.create_all()   !!! if database does not exist
    #flight_1 = Flight(flight_id=1, city_from='Baku', city_to='Istanbul', flight_info='Cheap and convenient', arrival_time='2 jan 17:00', departure_time='2 jan 19:00', number_of_passengers=200)
    #db.session.add(flight_1)
    #db.session.commit()
    app.run(debug = True)