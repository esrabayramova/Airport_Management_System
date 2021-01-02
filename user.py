import requests, json
Localhost = "http://127.0.0.1:5000"

class User:
    def __init__(self, city_from, city_to):
        self.city_from = city_from
        self.city_to = city_to

    def get_flights(self):
        link = Localhost+'/flights/'+self.city_from+'/'+self.city_to;
        resp = requests.get(link)
        injson = json.loads(resp.text)
        if len(injson) == 0:
            print('There is no such flight! ')
        else:
            print(resp.text)

if __name__ == '__main__':
    city_from = input('Enter the city of departure. ')
    city_to = input('Enter the destination. ')
    user = User(city_from, city_to)
    user.get_flights()