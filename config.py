import os

class Config:
    OPENWEATHERMAP_API_KEY = os.getenv('OPENWEATHERMAP_API_KEY')
    GEONAMES_USERNAME = os.getenv('GEONAMES_USERNAME')
