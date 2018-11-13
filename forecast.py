import requests
import random
import time
import string
import scipy
import api
from statistics import mean

# Equation constants
RETURN_LIM = 0.024
change_step = 0.005
change_change_step = 0.0001
last_score = 0
go_up = True

def spike_weight(array):
    print("inside spike weight function")

    a = (array[4])
    b = (array[3])

    difference = (a - b)*-1

    print("difference: "+str(difference))

    return(difference)

def countUpArray(arr):
    coefficient = 0
    count = 0

    for i in arr:
        if(i != None):
            count = count + 1
            coefficient = coefficient + i

    coefficient = coefficient / count
    return(coefficient)

def weight_exp(array):
    array.reverse()
    coef = 0
    coef2 = 0.75
    for i in array:
        coef = coef + coef2 * i
        coef2 = coef2 * 0.75
    return (coef)

def predicted_return(md, returns):
    """
    Returns the predicted returns for the next epoch.
    """
    spike_weight(returns)
    print("weight_exp = "+str(weight_exp(returns))+", spike weight * returns = "+str(spike_weight(returns)*returns))
    return(1.075084686 * (weight_exp(returns)+spike_weight(returns)*returns))
    #return(weight_exp(returns))

# Credentials
NAME = 'cookmewsxD'
PASSWORD = 'password'

#create_res = requests.post('http://egchallenge.tech/team/create', json={'team_name': NAME, 'password': 'password'}).json()
#print(create_res)

login_res = requests.post('http://egchallenge.tech/team/login', json={'team_name': NAME, 'password': PASSWORD}).json()
token = login_res['token']

while True:
    epoch_res = requests.get('http://egchallenge.tech/epoch').json()
    current_epoch = epoch_res['current_epoch']
    print(current_epoch)
    prediction_epoch = epoch_res['prediction_epoch']
    timestamp = epoch_res['unix_timestamp']
    print(f'current_epoch = {current_epoch}, prediction_epoch = {prediction_epoch}')

    marketdata = requests.get('http://egchallenge.tech/marketdata/latest').json()
    returns = []
    for epoch in range(current_epoch-5, current_epoch):
        returns.append(mean([x['epoch_return'] for x in requests.get('http://egchallenge.tech/marketdata/epoch/' + str(epoch)).json() if x['epoch_return'] is not None]))
    print(returns)

    predictions = []

    print(spike_weight(returns)+1)

    pred = 0.95 * (weight_exp(returns) * (spike_weight(returns)+1))
    #pred = (countUpArray(returns) + (weight_exp(returns)))
    #pred = 0.95 * (weight_exp(returns))
    print("pred = "+str(pred))

    for md in marketdata:
        if md['is_trading']:
            predictions.append({
                'instrument_id': md['instrument_id'],
                'predicted_return':  pred
            })

    pred_req = {'token': token, 'epoch': prediction_epoch, 'predictions': predictions}
    pred_res = requests.post('http://egchallenge.tech/predict', json=pred_req)
    print(f'Submitted {len(predictions)} predictions for epoch {prediction_epoch}')

    # Now get our scores for prior predictions
    scores_req = {'token': token}
    scores_res = requests.get('http://egchallenge.tech/scores', json=scores_req).json()
    for score in scores_res:
        epoch = score['epoch']
        sse = score['sse']
        print(f'epoch = {epoch}, sse = {sse}')
    
    # if last_score < sse:
    #     # we're doing worse!
    #     if go_up:
    #         # going up isn't working so go back down
    #         change_step -= change_change_step
    #         go_up = False
    #     else:
    #         # going down isn't working so go up!
    #         change_step += change_change_step
    #         go_up = True
    

    # print(change_step)
    
    # last_score = sse

    next_epoch_in = max(60.0 - (time.time() - timestamp), 0) + 1.0
    print(f'next epoch in {next_epoch_in} sec. Sleeping...')
    time.sleep(next_epoch_in)
