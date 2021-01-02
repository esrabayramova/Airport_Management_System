import requests, json
Localhost = "http://127.0.0.1:5000"

class Admin_user:
    def __init__(self, login_name, password):
        self.login_name = login_name
        self.password = password

    def auth_admin(self):
        resp = requests.post(Localhost + '/authentication_authorization', data={'login_name':self.login_name, 'password':self.password})
        auth_token = resp.json()
        #print(auth_token['token'])
        #print(auth_token['s'])
        return auth_token

    def add_flight(self, id, fromc, toc, arrt, dept, info, num):
        add = requests.post(Localhost+'/flights', {'id_flight':id, 'from_city':fromc, 'to_city':toc, 'time_arrival':arrt, 'time_departure':dept, 'info_flight':info, 'num_of_passngrs':num})
        return add.text

    def update_flight(self, id, fromc, toc, arrt, dept, info, num):
        update = requests.put(Localhost+'/flights', {'id_flight':id, 'from_city':fromc, 'to_city':toc, 'time_arrival':arrt, 'time_departure':dept, 'info_flight':info, 'num_of_passngrs':num})
        return update.text

    def delete_flight(self, id):
        delete_fl = requests.delete(Localhost+'/flights', data={'id_flight':id})
        return delete_fl.text

    def get_flight(self, city_from, city_to):
        get = requests.get(Localhost+'/flights', {'from_city':city_from, 'to_city':city_to})
        injson = json.loads(get.text)
        if len(injson) == 0:
            print('There is no such flight! ')
        else:
            print(get.text)

    def get_all_flights(self):
        getf = requests.get(Localhost+'/flights/all')
        injson = json.loads(getf.text)
        if len(injson) == 0:
            print('There are no flights currently! ')
        else:
            print(getf.text)

    def end_sessn(self, token):
        delete = requests.delete(Localhost+'/end_session', data={'token':token})

if __name__ == '__main__':
    login_name = input('Enter the login name: ')
    password = input('Enter password: ')
    admin = Admin_user(login_name, password)
    x = admin.auth_admin()
    tkn = x['token']   #token
    sessions_arr = x['s']   #the array of tokens
    #print(tkn)
    #print(sessions_arr)

    if tkn == 0 or tkn not in sessions_arr:
        print("Could not authenticate. Wrong login name or password. ")
    else:
        print('Authentication successful. ')
        while True:
            op = input('Which operation? Add, delete, update, get, get_all or end. ')
            if (op.lower() == 'get'):
                city_from = input('Enter the city of departure. ')
                city_to = input('Enter the destination.')
                admin.get_flight(city_from, city_to)

            elif (op.lower() == 'add'):
                id = int(input('Enter flight_id(integer): '))
                city_from = input('Enter the city of departure: ')
                city_to = input('Enter the destination: ')
                departure_time = input('Enter departure time: ')
                arrival_time = input('Enter arrival time. ')
                flight_info = input('Enter flight info. ')
                number_of_passengers = int(input('Enter the number of the passengers: '))
                msg = admin.add_flight(id, city_from, city_to, arrival_time, departure_time, flight_info, number_of_passengers)
                print(msg)

            elif (op.lower() == 'delete'):
                id = int(input('Enter the id of the flight you want to delete: '))
                msg = admin.delete_flight(id)
                print(msg)

            elif (op.lower() == 'update'):
                id = int(input('Enter the id of the flight you want to change: '))
                city_from = input('Enter the new city of departure: ')
                city_to = input('Enter the new destination: ')
                departure_time = input('Enter new departure time: ')
                arrival_time = input('Enter new arrival time. ')
                flight_info = input('Enter new flight info. ')
                number_of_passengers = int(input('Enter the number of the passengers: '))
                msg = admin.update_flight(id, city_from, city_to, arrival_time, departure_time, flight_info,
                                 number_of_passengers)
                print(msg)

            elif (op.lower() == 'get_all'):
                admin.get_all_flights()

            elif (op.lower() == 'end'):
                admin.end_sessn(tkn)
                break
            else:
                print('Wrong operation')
                continue