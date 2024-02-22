import requests
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather_db.db'
db = SQLAlchemy(app)


class WeatherCheck(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(30), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    max_temp = db.Column(db.Float)
    min_temp = db.Column(db.Float)
    total_precipitation = db.Column(db.Float)
    humidity = db.Column(db.Integer)
    sunrise_hour = db.Column(db.String(10))
    sunset_hour = db.Column(db.String(10))


@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    city = None

    if request.method == 'POST':
        city = request.form['city']
        weather_data = take_weather_data(city)
        save_to_db(city, weather_data)

    weather_data = WeatherCheck.query.filter_by(city=city).all()

    return render_template('index.html', weather_data=weather_data)


def take_weather_data(city):
    api_key = 'e9d578dff0564d11bb1195846242002'
    base_url = 'http://api.weatherapi.com/v1/forecast.json'

    params = {
        'key': api_key,
        'q': city,
        'days': 3
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        forecast_days = data['forecast']['forecastday']
        return forecast_days
    else:
        return None


def save_to_db(city, weather_data):
    with app.app_context():
        for day in weather_data:
            existing_entry = WeatherCheck.query.filter_by(date=day['date'], city=city).first()

            if existing_entry:
                existing_entry.max_temp = day['day']['maxtemp_c']
                existing_entry.min_temp = day['day']['mintemp_c']
                existing_entry.total_precipitation = day['day']['totalprecip_mm']
                existing_entry.humidity = day['day']['avghumidity']
                existing_entry.sunrise_hour = day['astro']['sunrise']
                existing_entry.sunset_hour = day['astro']['sunset']
            else:
                db.session.add(WeatherCheck(
                    date=day['date'],
                    city=city,
                    max_temp=day['day']['maxtemp_c'],
                    min_temp=day['day']['mintemp_c'],
                    total_precipitation=day['day']['totalprecip_mm'],
                    humidity=day['day']['avghumidity'],
                    sunrise_hour=day['astro']['sunrise'],
                    sunset_hour=day['astro']['sunset']
                ))

        db.session.commit()


def create_tables():
    with app.app_context():
        db.create_all()


if __name__ == "__main__":
    #create_tables()
    app.run(debug=True)