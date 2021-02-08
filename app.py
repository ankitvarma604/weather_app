from flask import Flask, request, make_response, jsonify
import json
import os
import pyowm
from flask_cors import cross_origin
import requests
api_key = "8150a9b11d6ad38250c60d1fba44ec7b"
owm = pyowm.OWM(api_key)

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
    observation = owm.weather_at_place(city)
    w = observation.get_weather()
    celsius_temp = w.get_temperature('celsius')
    temp_max_celsius = str(celsius_temp.get('temp_max'))
    #Temperatures
    fulfillmentText = "Today the weather in " + city + " is " + temp_max_celsius + " °C"
    return {
        "fulfillmentText": fulfillmentText,
        "displayText": fulfillmentText
        }
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')