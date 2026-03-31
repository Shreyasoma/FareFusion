# 🚖 FareFusion

### AI-Based Smart Ride Price Comparison & Recommendation System

FareFusion is an AI-powered web application that compares estimated ride fares across multiple ride services and intelligently recommends the **best ride option** based on multiple decision factors such as price, estimated arrival time, and ride type.

This system is designed as an MSc-level academic project focused on intelligent decision systems, smart transportation, and user-centric design.

---

## 📌 Project Overview

In urban environments, users often switch between multiple ride-booking applications (e.g., Uber, Ola, Rapido) to compare prices manually. This process is inefficient and time-consuming.

FareFusion solves this problem by:

- Allowing users to enter pickup and drop locations once
- Estimating fares using AI-based prediction logic
- Comparing multiple ride options
- Recommending the **best ride**, not just the cheapest

This project uses mock datasets and open-source APIs to ensure academic safety and lifetime free implementation.

---

## 🎯 Key Features

- 🌙 Dark / Light Theme Toggle
- ✨ Animated AI Typing Tagline
- 🚗 Selectable Ride Cards (Auto, Cab, Bike)
- 📍 Location Input for Pickup & Drop
- 🧠 AI-Based Multi-Criteria Recommendation System
- 📊 Fare Prediction using Regression Logic
- ⚖ Weighted Decision Model for Best Ride Selection
- 📦 Clean Modular Architecture
- 💻 Fully Responsive UI

---

## 🧠 AI Logic & Recommendation Strategy

FareFusion does **not** simply choose the cheapest ride.

Instead, it implements a **Weighted Multi-Criteria Decision Model**:
Best Ride Score =
(Weight₁ × Price Score) +
(Weight₂ × ETA Score) +
(Weight₃ × Rating Score)

Example:

- Price Weight: 0.5
- Time Weight: 0.3
- Rating Weight: 0.2

The ride with the optimal combined score is recommended as:

> 🟢 AI Recommended Ride

This approach ensures balanced decision-making rather than price-only comparison.

---

## 🧩 Modules

### 1️⃣ User Interface Module

- Location inputs
- Ride selection
- Compare button
- Result display

### 2️⃣ Backend Processing Module

- Handles user requests
- Communicates with AI engine
- Processes recommendation logic

### 3️⃣ AI Prediction Module

- Implements regression-based fare prediction
- Applies weighted scoring logic

### 4️⃣ Database Module

- Stores mock ride datasets
- Stores pricing parameters
- Stores route information

### 5️⃣ Admin Module (Optional)

- Dataset management
- System monitoring

---

## 🛠 Technology Stack

| Layer    | Technology Used                           |
| -------- | ----------------------------------------- |
| Frontend | HTML, CSS, JavaScript                     |
| Backend  | Python (Flask)                            |
| AI Logic | Python, scikit-learn                      |
| Database | MongoDB / MySQL                           |
| Maps API | OpenStreetMap / OSRM (Free & Open Source) |
| Hosting  | Localhost / Render                        |

---

## 📊 Data Strategy

Since official ride-booking APIs are restricted:

- Mock datasets are created manually
- Fare prediction is simulated using regression logic
- Surge pricing and time factors are modeled mathematically
- All outputs are clearly labeled as “Estimated Fare”

This ensures legal and academic compliance.

---

## 🎓 Academic Relevance

- Real-world transportation problem
- AI-based decision-making system
- Multi-criteria optimization
- Web-based intelligent application
- Suitable for MSc Computer Science evaluation

---

## 🔮 Future Enhancements

- Live ride-booking API integration (if permitted)
- User preference learning
- Surge price prediction model
- Mobile application version
- Voice-based ride search
- Historical analytics dashboard

---

## ⚠ Disclaimer

FareFusion does not connect to official ride-booking services.  
All pricing results are simulated for academic and demonstration purposes only.

---

## 👩‍💻 Author

Developed as part of MSc Computer Science academic project work.

---

## 📜 License

This project is intended for academic use and demonstration purposes.
