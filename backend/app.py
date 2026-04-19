from flask import Flask, render_template, request, redirect, session
import requests
from sqlalchemy import func

# DB imports
from db import SessionLocal
from models import Platform, Route, FarePrediction, User

app = Flask(__name__)
app.secret_key = "super_secret_key" 


# ------------------ AUTH FLOW ------------------

@app.route("/")
def root():
    if "user_id" in session:
        if session.get("is_admin"):
            return redirect("/admin-dashboard")
        else:
            return redirect("/home")
    return redirect("/login")


@app.route("/home")
def home():
    if "user_id" not in session:
        return redirect("/login")
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        db = SessionLocal()

        user = User(
            name=request.form["name"],
            email=request.form["email"],
            password=request.form["password"],
            is_admin=False
        )

        db.add(user)
        db.commit()
        db.close()

        return redirect("/login")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        db = SessionLocal()

        user = db.query(User).filter(
            User.email == request.form["email"],
            User.password == request.form["password"]
        ).first()

        db.close()

        if user:
            session["user_id"] = user.user_id
            session["is_admin"] = user.is_admin
            session["user_email"] = user.email

            if user.is_admin:
                return redirect("/admin-dashboard")
            return redirect("/home")

        return "Invalid credentials"

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


# ------------------ ADMIN ------------------

@app.route("/admin-dashboard")
def admin_dashboard():
    if not session.get("is_admin"):
        return redirect("/login")

    db = SessionLocal()

    # Total stats
    total_routes = db.query(Route).count()
    total_predictions = db.query(FarePrediction).count()

    # 🔥 Ride Type Data
    ride_data = db.query(
        FarePrediction.ride_type,
        func.count(FarePrediction.prediction_id)
    ).group_by(FarePrediction.ride_type).all()

    ride_labels = [r[0] for r in ride_data]
    ride_values = [r[1] for r in ride_data]

    # 🔥 Platform Data
    platform_data = db.query(
        Platform.platform_name,
        func.count(FarePrediction.prediction_id)
    ).join(FarePrediction).group_by(Platform.platform_name).all()

    platform_labels = [p[0] for p in platform_data]
    platform_values = [p[1] for p in platform_data]

    # 🔥 Insights
    if ride_values:
        top_ride_type = ride_labels[ride_values.index(max(ride_values))]
    else:
        top_ride_type = "N/A"

    if platform_values:
        top_platform = platform_labels[platform_values.index(max(platform_values))]
    else:
        top_platform = "N/A"

    avg_fare = db.query(func.avg(FarePrediction.predicted_fare)).scalar()
    avg_fare = round(float(avg_fare), 2) if avg_fare else 0

    db.close()

    return render_template(
        "admin_dashboard.html",
        total_routes=total_routes,
        total_predictions=total_predictions,
        ride_labels=ride_labels,
        ride_values=ride_values,
        platform_labels=platform_labels,
        platform_values=platform_values,
        top_ride_type=top_ride_type,
        top_platform=top_platform,
        avg_fare=avg_fare
    )


# ------------------ MAIN APP ------------------

@app.route("/compare", methods=["POST"])
def compare():
    if "user_id" not in session:
        return redirect("/login")

    source = request.form["source"]
    destination = request.form["destination"]

    lat1, lon1 = get_coordinates(source)
    lat2, lon2 = get_coordinates(destination)

    if lat1 is None or lat2 is None:
        return "Location not found."

    distance = get_distance(lat1, lon1, lat2, lon2)

    if distance is None:
        return "Distance error."

    ride_type = request.form["ride_type"]

    services = get_services_from_db(ride_type)
    rides = predict_fares(distance, services)

    best_ride = select_best_ride(rides)

    # 🔥 best ride first
    rides = sorted(rides, key=lambda x: x["name"] != best_ride["name"])

    # 🔥 save to DB
    route_id = save_route(lat1, lon1, lat2, lon2, source, destination, distance)

    if route_id:
        save_predictions(route_id, rides, ride_type)

    return render_template(
        "results.html",
        source=source,
        destination=destination,
        distance=round(distance, 2),
        rides=rides,
        best_ride=best_ride
    )


@app.route("/history")
def history():
    if "user_id" not in session:
        return redirect("/login")

    db = SessionLocal()

    routes = db.query(Route).order_by(Route.route_id.desc()).all()
    history_data = []

    for route in routes:
        predictions = db.query(FarePrediction).filter(
            FarePrediction.route_id == route.route_id
        ).all()

        if not predictions:
            continue

        best = None
        best_score = float("inf")

        for p in predictions:
            platform = db.query(Platform).filter(
                Platform.platform_id == p.platform_id
            ).first()

            score = (0.5 * float(p.predicted_fare)) + \
                    (0.3 * platform.typical_wait_time) - \
                    (5 * float(platform.avg_rating))

            if score < best_score:
                best_score = score
                best = {
                    "platform": platform.platform_name,
                    "fare": float(p.predicted_fare)
                }

        history_data.append({
            "source": route.src_address,
            "destination": route.dest_address,
            "distance": float(route.distance_km),
            "best_platform": best["platform"],
            "best_fare": best["fare"]
        })

    db.close()

    return render_template("history.html", history=history_data)


# ------------------ DB FUNCTIONS ------------------

def get_services_from_db(ride_type):
    db = SessionLocal()

    if ride_type == "auto":
        services = db.query(Platform).filter(
            Platform.platform_name.ilike("%Auto%")
        ).all()

    elif ride_type == "bike":
        services = db.query(Platform).filter(
            Platform.platform_name.ilike("%Bike%")
        ).all()

    else:
        services = db.query(Platform).filter(
            ~Platform.platform_name.ilike("%Auto%"),
            ~Platform.platform_name.ilike("%Bike%")
        ).all()

    db.close()

    return [{
        "name": s.platform_name,
        "base": float(s.base_fare),
        "rate": float(s.per_km_rate),
        "eta": s.typical_wait_time,
        "rating": float(s.avg_rating)
    } for s in services]


def save_route(lat1, lon1, lat2, lon2, source, destination, distance):
    try:
        db = SessionLocal()

        route = Route(
            src_latitude=lat1,
            src_longitude=lon1,
            dest_latitude=lat2,
            dest_longitude=lon2,
            src_address=source,
            dest_address=destination,
            distance_km=distance
        )

        db.add(route)
        db.commit()
        db.refresh(route)

        route_id = route.route_id
        db.close()
        return route_id

    except Exception as e:
        print(e)
        return None


def save_predictions(route_id, rides, ride_type):
    db = SessionLocal()

    for ride in rides:
        platform = db.query(Platform).filter(
            Platform.platform_name == ride["name"]
        ).first()

        if platform:
            db.add(FarePrediction(
                route_id=route_id,
                platform_id=platform.platform_id,
                predicted_fare=ride["fare"],
                surge_applied=1.0,
                ride_type=ride_type
            ))

    db.commit()
    db.close()


# ------------------ APIs ------------------

def get_coordinates(place):
    try:
        res = requests.get(
            "https://nominatim.openstreetmap.org/search",
            params={"q": place, "format": "json"},
            headers={"User-Agent": "FareFusion"}
        )

        data = res.json()
        if not data:
            return None, None

        return float(data[0]["lat"]), float(data[0]["lon"])

    except:
        return None, None


def get_distance(lat1, lon1, lat2, lon2):
    try:
        url = f"http://router.project-osrm.org/route/v1/driving/{lon1},{lat1};{lon2},{lat2}?overview=false"
        res = requests.get(url)
        data = res.json()

        return data["routes"][0]["distance"] / 1000

    except:
        return None


# ------------------ LOGIC ------------------

def predict_fares(distance, services):
    return [{
        "name": s["name"],
        "fare": round(s["base"] + distance * s["rate"], 2),
        "eta": s["eta"],
        "rating": s["rating"]
    } for s in services]


def select_best_ride(rides):
    return min(
        rides,
        key=lambda r: (0.5*r["fare"] + 0.3*r["eta"] - 5*r["rating"])
    )


if __name__ == "__main__":
    app.run(debug=True)