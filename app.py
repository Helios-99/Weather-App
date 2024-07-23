from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    weather_data = None
    forecast_data = None
    if request.method == "POST":
        city = request.form["city"]
        weather_data, forecast_data = get_weather(city)
    return render_template("index.html", weather_data=weather_data, forecast_data=forecast_data)

@app.route("/autocomplete", methods=["GET"])
def autocomplete():
    term = request.args.get("term")
    response = requests.get(f"http://api.geonames.org/searchJSON?name_startsWith={term}&maxRows=10&username={os.environ.get('GEONAMES_USERNAME')}")
    data = response.json()
    cities = [f"{place['name']}, {place['countryName']}" for place in data['geonames']]
    return jsonify(cities)

def get_weather(city):
    api_key = os.environ.get('OPENWEATHERMAP_API_KEY')
    weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api_key}"
    forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&units=metric&appid={api_key}"
    weather_response = requests.get(weather_url).json()
    forecast_response = requests.get(forecast_url).json()

    if weather_response.get("cod") != 200:
        return None, None
    
    forecast_by_day = {}
    for forecast in forecast_response["list"]:
        date = forecast["dt_txt"].split(" ")[0]
        if date not in forecast_by_day:
            forecast_by_day[date] = []
        forecast_by_day[date].append(forecast)

    return weather_response, forecast_by_day

if __name__ == '__main__':
    #app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
    app.run(host='0.0.0.0')
