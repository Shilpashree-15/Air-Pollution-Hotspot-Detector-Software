from flask import Flask, render_template, request
import datetime

# --- CORRECTION 1: Changed _name_ to __name__ ---
app = Flask(__name__)

# ---------- MOCK AQI DATA (NO API REQUIRED) ----------
# Includes AQI, PM2.5, PM10, and CO for the dashboard cards and logic
AQI_DATA = {
    "bengaluru": {"aqi": 178, "pm25": 108, "pm10": 178, "co": 3.2, "status": ""},
    "delhi": {"aqi": 410, "pm25": 350, "pm10": 420, "co": 12.5, "status": ""},
    "mumbai": {"aqi": 220, "pm25": 165, "pm10": 205, "co": 5.8, "status": ""},
    "chennai": {"aqi": 155, "pm25": 85, "pm10": 140, "co": 2.5, "status": ""},
    "hyderabad": {"aqi": 180, "pm25": 100, "pm10": 160, "co": 3.0, "status": ""},
    "kolkata": {"aqi": 260, "pm25": 200, "pm10": 250, "co": 7.5, "status": ""},
    "mysuru": {"aqi": 110, "pm25": 60, "pm10": 95, "co": 1.8, "status": ""},
    "pune": {"aqi": 140, "pm25": 80, "pm10": 130, "co": 2.2, "status": ""}
}

# Hotspot data used for the banner (fixed mock hotspot)
HOTSPOT_CITY = "Delhi"
HOTSPOT_AQI = 410
HOTSPOT_STATUS = "Hazardous"

# Helper function to determine status/color
def get_status_info(aqi):
    if aqi <= 50:
        return "Good", "good", "green"
    elif aqi <= 100:
        return "Moderate", "moderate", "orange"
    elif aqi <= 150:
        return "Unhealthy for Sensitive Groups", "unhealthy-sensitive", "red"
    elif aqi <= 200:
        return "Unhealthy", "unhealthy", "purple"
    elif aqi <= 300:
        return "Very Unhealthy", "very-unhealthy", "darkred"
    else:
        return "Hazardous", "hazardous", "black"

# Helper function to get pollutant status
def get_pollutant_status(value, type):
    if type == 'PM25':
        if value <= 35: return "Low"
        elif value <= 70: return "Moderate"
        else: return "High"
    elif type == 'PM10':
        if value <= 50: return "Low"
        elif value <= 100: return "Moderate"
        else: return "High"
    elif type == 'CO':
        if value <= 4: return "Low"
        elif value <= 8: return "Moderate"
        else: return "High"

@app.route("/")
def home():
    # Default city to show on the dashboard on initial load
    default_city = "bengaluru"
    return render_dashboard(default_city)

@app.route("/search", methods=["POST"])
def search():
    city = request.form['city'].lower()
    return render_dashboard(city)

def render_dashboard(city_name):
    city = city_name.lower()
    time = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    # 1. Determine the data source (Mock list or Fallback)
    if city in AQI_DATA:
        data = AQI_DATA[city]
    else:
        # FALLBACK MOCK DATA for any unlisted city
        data = {"aqi": 130, "pm25": 75, "pm10": 110, "co": 1.5, "status": "Fallback"}
        
    # 2. Process Data
    aqi = data['aqi']
    # The get_status_info function returns status, color_class, and color_name. 
    # The Flask template only uses status and color_class (renamed to COLOR).
    status, color, _ = get_status_info(aqi)

    pm25_status = get_pollutant_status(data['pm25'], 'PM25')
    pm10_status = get_pollutant_status(data['pm10'], 'PM10')
    co_status = get_pollutant_status(data['co'], 'CO')

    # 3. Render the dashboard for the city
    return render_template("dashboard.html",
                           CITY=city.capitalize(),
                           AQI=aqi,
                           STATUS=status,
                           COLOR=color,
                           PM25=data['pm25'],
                           PM10=data['pm10'],
                           CO=data['co'],
                           PM25_STATUS=pm25_status,
                           PM10_STATUS=pm10_status,
                           CO_STATUS=co_status,
                           HOTSPOT_CITY=HOTSPOT_CITY.capitalize(),
                           HOTSPOT_AQI=HOTSPOT_AQI,
                           HOTSPOT_STATUS=HOTSPOT_STATUS,
                           TIME=time)


# --- CORRECTION 2: Changed _name_ and _main_ to __name__ and __main__ ---
if __name__ == "__main__":
    app.run(debug=True)