from flask import Flask, request, make_response, jsonify
import json
import os

from flask_cors import cross_origin
import requests
import ssl
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context
app = Flask(__name__)
# geting and sending response to dialogflow
@app.route('/webhook', methods=['POST'])
@cross_origin()
def webhook():
    req = request.get_json(silent=True, force=True)
    #print("Request:")
    #print(json.dumps(req, indent=4))
    res = processRequest(req)
    res = json.dumps(res, indent=4)
    #print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r
# processing the request from dialogflow
def processRequest(req):
    sessionID=req.get('responseId')
    result = req.get("queryResult")
    parameters = result.get("parameters")
    city = parameters.get("geo-city")
    if (intent=='city_name_res'):
        api_key = "8150a9b11d6ad38250c60d1fba44ec7b"
        api_request = requests.get("https://api.openweathermap.org/data/2.5/weather?q="
                                   + city+ "&units=metric&appid=" + api_key)
        api = json.loads(api_request.content)
        #Temperatures
        y = api['main']
        current_temprature = str(y['temp'])
        fulfillmentText = "Today the weather in " + name + " is " + current_temprature + " °C"
        return {
            "fulfillmentText": fulfillmentText,
            "displayText": fulfillmentText
        }

if __name__ == '__main__':
    app.run(debug=True)