from flask import Flask, render_template, request, jsonify
import requests
from config import Config
from cachetools import TTLCache

app = Flask(__name__)
app.config.from_object(Config)
cache = TTLCache(maxsize=100, ttl=300)  # Cache up to 100 items, with a time-to-live of 5 minutes

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    if request.method == 'POST':
        city = request.form['city'].lower()
        if city in cache:
            weather_data = cache[city]
        else:
            api_key = app.config['OPENWEATHERMAP_API_KEY']
            url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
            response = requests.get(url)
            if response.status_code == 200:
                weather_data = response.json()
                cache[city] = weather_data
            else:
                weather_data = {'error': 'City not found'}
    return render_template('index.html', weather_data=weather_data)

@app.route('/suggestions', methods=['GET'])
def suggestions():
    query = request.args.get('query', '').lower()
    geo_api_username = app.config['GEONAMES_USERNAME']
    
    url = f'http://api.geonames.org/searchJSON?name_startsWith={query}&maxRows=10&username={geo_api_username}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        suggestions = [city['name'] for city in data['geonames']]
        return jsonify(suggestions)
    return jsonify([])

if __name__ == '__main__':
    app.run(host='0.0.0.0')
