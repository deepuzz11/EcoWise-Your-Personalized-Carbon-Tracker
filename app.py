from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Your Weatherstack API key
WEATHERSTACK_API_KEY = "24816188c0e653158c176b56e77d421e"


@app.route("/")
def home():
    return render_template("dashboard.html")


@app.route("/weather-insights")
def weather_insights():
    city = request.args.get('city', 'Delhi')
    url = f"http://api.weatherstack.com/current?access_key={WEATHERSTACK_API_KEY}&query={city}"
    response = requests.get(url).json()

    if 'error' in response:
        return jsonify({'error': 'Failed to fetch weather data'}), 400

    weather_data = response['current']
    temperature = weather_data['temperature']
    description = weather_data['weather_descriptions'][0]
    icon = weather_data['weather_icons'][0]

    # Provide dynamic background based on weather
    weather_bg = f"url('{icon}')"

    return jsonify({
        'city': city,
        'temperature': temperature,
        'description': description,
        'weather_bg': weather_bg
    })


@app.route("/track", methods=["GET", "POST"])
def track():
    if request.method == "POST":
        # Process user input data
        travel = float(request.form.get("travel", 0))
        electricity = float(request.form.get("electricity", 0))
        water = float(request.form.get("water", 0))
        waste = float(request.form.get("waste", 0))

        total_footprint = calculate_footprint(
            {"travel": travel, "electricity": electricity, "water": water, "waste": waste}
        )
        return render_template("track.html", total_footprint=total_footprint)
    return render_template("track.html", total_footprint=None)


def calculate_footprint(data):
    travel_coefficient = 0.2  # kg CO2/km
    electricity_coefficient = 0.5  # kg CO2/kWh
    water_coefficient = 0.001  # kg CO2/liter
    waste_coefficient = 0.05  # kg CO2/kg waste

    travel_footprint = data.get("travel", 0) * travel_coefficient
    electricity_footprint = data.get("electricity", 0) * electricity_coefficient
    water_footprint = data.get("water", 0) * water_coefficient
    waste_footprint = data.get("waste", 0) * waste_coefficient

    total_footprint = travel_footprint + electricity_footprint + water_footprint + waste_footprint
    return total_footprint


if __name__ == "__main__":
    app.run(debug=True)
