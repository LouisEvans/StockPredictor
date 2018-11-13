import requests
import string

TEAM_NAME = 'monksmews'
TEAM_PASSWORD = 'cookmews'

DEBUG = False

def login():
    """
    Login to the REST API and return the token
    """
    login_res = requests.post('http://egchallenge.tech/team/login', json={'team_name': TEAM_NAME, 'password': TEAM_PASSWORD}).json()
    if DEBUG: print(login_res)
    return login_res['token']

def get_epoch():
    """
    Returns the epoch data as a json object
    """
    x = requests.get('http://egchallenge.tech/epoch').json()
    if DEBUG: print(x)
    return x

def get_instrument_data(id):
    """
    Given an instrument id, return the market data for that instrument
    """
    x = requests.get('http://egchallenge.tech/marketdata/instrument/' + str(id)).json()
    if DEBUG: print(x)
    return x

def get_num_instruments():
    """
    Return the current number of instruments
    """
    print(len(requests.get('http://egchallenge.tech/instruments').json()))


def instrument_data():
    """"
    Gets the name of the instrument
    """
    data = requests.get('http://egchallenge.tech/instruments').json()[0]
    print(data['company_name'])

def instrument_name_to_id(message):
    """"
    User inputs a company name and this return the iD of the company
    """
    data = requests.get('http://egchallenge.tech/instruments').json()
    for i in data:
        if i['company_name'] == message:
            company_id = i['id']
    return company_id



if __name__ == '__main__':
    token = login()

    get_instrument_data(2)

