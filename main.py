import requests, json

def get_coordinates(address):
    # converting the address
    address = address.replace(' ','+')

    r = requests.get(f'https://geocode.maps.co/search?q={address}')
    my_json = r.content.decode('utf-8')
    data = json.loads(my_json)

    return round(float(data[0]['lat']),2), round(float(data[0]['lon']),2)

if __name__ == '__main__':
    address1 = '52 Av. de Bordeaux, 40200 Mimizan France'
    address2 = '619 Av. du Maréchal Lyautey, 40600 Biscarrosse France'

    print('address1 : ', get_coordinates(address1))
    print('address2 : ', get_coordinates(address2))