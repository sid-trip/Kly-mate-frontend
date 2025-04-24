# Kly-mate Frontend 🌦️

[![Framework](https://img.shields.io/badge/Framework-Streamlit-red.svg)](https://streamlit.io/) [![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)

This repository contains the Streamlit frontend application for the Kly-mate project. It provides a simple web interface to interact with the [Kly-mate Backend API](https://kly-mate.onrender.com/) , allowing users to fetch and view current weather conditions, Air Quality Index (AQI) data, and placeholder weather predictions for specified geographical coordinates.

**Live Application URL:** [https://kly-mate.streamlit.app/](https://kly-mate.streamlit.app/)

*(Optional: Insert Logo Here)*
## ✨ Features

* User interface to input latitude and longitude (defaults to Bengaluru).
* Button to trigger data fetching from the live backend API.
* Displays current weather details (Temperature, Feels Like, Humidity, Wind, Condition).
* Displays current AQI details (Index Value, key pollutants via expander).
* Displays placeholder temperature prediction fetched from the backend.
* Loading spinner (`st.spinner`) shown during API calls.
* Basic error handling and display for API communication issues.

## 🛠️ Technologies Used

* **Framework:** Streamlit
* **API Calls:** Requests
* **Language:** Python 3.9+
* **Deployment:** Streamlit Community Cloud

## 📂 Project Structure

```text
Klymate_frontend/
├── venv/
├── .gitignore
├── requirements.txt
├── streamlit_app.py
└── your_logo_filename.jpg
```
## 🚀 Setup and Installation

1.  **Clone the repository:**
    ```bash
    # Replace with your frontend repo URL
    git clone https://github.com/YourUsername/kly-mate-frontend.git
    cd Klymate_frontend
    ```

2.  **Create and activate a virtual environment (Recommended):**
    ```bash
    python -m venv venv
    # On Windows (PowerShell): .\venv\Scripts\Activate.ps1
    # On Linux/macOS: source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## ⚙️ Configuration

The URL for the deployed backend API is currently set within the `streamlit_app.py` script.

* **File:** `streamlit_app.py`
* **Variable:** `BACKEND_URL`
    ```python
    # Ensure this variable points to the live backend API
    BACKEND_URL = "https://kly-mate.onrender.com"
    ```

## ▶️ Running Locally

1.  Ensure your virtual environment is activated and dependencies are installed.
2.  Make sure the `BACKEND_URL` in `streamlit_app.py` is correct.
3.  Run the Streamlit application from the `Klymate_frontend` directory:
    ```bash
    streamlit run streamlit_app.py
    ```
4.  The application should open automatically in your web browser, likely at `http://localhost:8501`.

## 🔗 Backend API

This frontend consumes data from the Kly-mate Backend API.

* **Backend Live URL:** [https://kly-mate.onrender.com/](https://kly-mate.onrender.com/)
* **Backend API Documentation:** [https://kly-mate.onrender.com/docs](https://kly-mate.onrender.com/docs)

## ☁️ Deployment

This application is automatically deployed on [Streamlit Community Cloud](https://streamlit.io/cloud) from the `main` branch of this repository.

* **Live Frontend App:** [https://kly-mate.streamlit.app/](https://kly-mate.streamlit.app/)

## 🔮 Future Work

* Improve UI/UX design and data presentation (e.g., use charts, better layouts).
* Add input validation for latitude/longitude.
* Allow users to search by city name (would require backend changes).
* Display weather/AQI icons more visually.
* Implement user accounts or location saving features.
* Display the comparison between Kly-mate prediction and external forecasts (once backend supports it).

---
