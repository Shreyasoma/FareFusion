from flask import Flask, render_template, request
import requests

app = Flask(__name__)

auto_services = [
    {"name": "Uber Auto", "base": 30, "rate": 10, "eta": 5, "rating": 4.5},
    {"name": "Ola Auto", "base": 25, "rate": 11, "eta": 8, "rating": 4.2},
    {"name": "Rapido Auto", "base": 28, "rate": 10.5, "eta": 6, "rating": 4.3}
]

cab_services = [
    {"name": "Uber Go", "base": 50, "rate": 15, "eta": 6, "rating": 4.6},
    {"name": "Ola Mini", "base": 45, "rate": 16, "eta": 9, "rating": 4.4},
    {"name": "Rapido Cab", "base": 48, "rate": 15.5, "eta": 7, "rating": 4.3}
]

bike_services = [
    {"name": "Rapido Bike", "base": 20, "rate": 7, "eta": 4, "rating": 4.5},
    {"name": "Uber Moto", "base": 22, "rate": 7.5, "eta": 3, "rating": 4.6},
    {"name": "Ola Bike", "base": 18, "rate": 8, "eta": 7, "rating": 4.2}
]

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/compare", methods=["POST"])
def compare():

    source = request.form["source"]
    destination = request.form["destination"]

    print("Source:", source)
    print("Destination:", destination)

    # Get coordinates
    lat1, lon1 = get_coordinates(source)
    lat2, lon2 = get_coordinates(destination)

    # Check if coordinates were found
    if lat1 is None or lat2 is None:
        return "Location not found. Please try another place."

    # Calculate distance
    distance = get_distance(lat1, lon1, lat2, lon2)

    if distance is None:
        return "Could not calculate distance."

    print("Distance:", distance, "km")
    ride_type = request.form["ride_type"]

    if ride_type == "auto":
        services = auto_services
    elif ride_type == "cab":
        services = cab_services
    else:
        services = bike_services

    rides = predict_fares(distance, services)

    best_ride = select_best_ride(rides)

    return render_template(
    "results.html",
    source=source,
    destination=destination,
    distance=round(distance,2),
    rides=rides,
    best_ride=best_ride
)

def get_coordinates(place):

    url = "https://nominatim.openstreetmap.org/search"

    params = {
        "q": place,
        "format": "json"
    }

    headers = {
        "User-Agent": "FareFusion-App"
    }

    try:
        response = requests.get(url, params=params, headers=headers)

        # Check if request worked
        if response.status_code != 200:
            print("Geocoding API error:", response.status_code)
            return None, None

        data = response.json()

        if len(data) == 0:
            print("No location found for:", place)
            return None, None

        lat = float(data[0]["lat"])
        lon = float(data[0]["lon"])

        return lat, lon

    except Exception as e:
        print("Geocoding error:", e)
        return None, None


def get_distance(lat1, lon1, lat2, lon2):

    url = f"http://router.project-osrm.org/route/v1/driving/{lon1},{lat1};{lon2},{lat2}?overview=false"

    try:
        response = requests.get(url)

        if response.status_code != 200:
            print("Distance API error:", response.status_code)
            return None

        data = response.json()

        distance = data["routes"][0]["distance"]

        return distance / 1000

    except Exception as e:
        print("Distance calculation error:", e)
        return None

def predict_fares(distance, services):

    results = []

    for service in services:

        fare = service["base"] + (distance * service["rate"])

        results.append({
            "name": service["name"],
            "fare": round(fare, 2),
            "eta": service["eta"],
            "rating": service["rating"]
        })

    return results

def select_best_ride(rides):

    best = None
    best_score = float("inf")

    for ride in rides:

        score = (0.5 * ride["fare"]) + (0.3 * ride["eta"]) - (5 * ride["rating"])

        if score < best_score:
            best_score = score
            best = ride

    return best

if __name__ == "__main__":
    app.run(debug=True)