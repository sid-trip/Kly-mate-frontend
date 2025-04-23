# streamlit_app.py
import streamlit as st
import requests
import json
from pathlib import Path # To handle file paths for the logo

# --- Page Configuration (Set Title, Icon, Layout) ---
# This should be the first Streamlit command in your script
st.set_page_config(
    page_title="Kly-mate",
    page_icon="☁️", # You can use an emoji or a path to a favicon file
    layout="centered", # Use "wide" or "centered"
    initial_sidebar_state="collapsed" # Start with sidebar collapsed
)

# --- Logo ---
# Construct the path to the logo file relative to this script
# Assumes the logo image is in the SAME directory as streamlit_app.py
# !!! UPDATE 'your_logo_filename.jpg' to the actual filename !!!
logo_path = Path(__file__).parent / "WhatsApp Image 2025-04-21 at 21.00.11_a09c7720.jpg" #<-- CHANGE FILENAME

if logo_path.exists():
    st.image(str(logo_path), width=150) # Adjust width as needed
else:
    st.warning("Logo file not found. Please place it in the same directory as the script.")

# --- App Title and Description ---
st.title("Kly-mate Weather Dashboard")
st.caption("Real-time weather, air quality index (AQI), and placeholder forecast.")
st.markdown("---")

# --- User Inputs ---
st.subheader("📍 Location Input")
# Use columns for a cleaner input layout
col_lat, col_lon = st.columns(2)
with col_lat:
    # Defaulting to Bengaluru
    lat = st.number_input("Enter Latitude:", value=12.9716, format="%.4f", help="Example: 12.9716 for Bengaluru")
with col_lon:
    lon = st.number_input("Enter Longitude:", value=77.5946, format="%.4f", help="Example: 77.5946 for Bengaluru")

# --- Backend API URL (Needs to be Correct!) ---
# !!! VERY IMPORTANT: Use your ACTUAL deployed backend URL !!!
BACKEND_URL = "https://kly-mate.onrender.com" # <-- MAKE SURE THIS IS YOUR CORRECT RENDER URL!

# --- Fetch Data Button ---
if st.button("🔄 Fetch Data & Predict", type="primary", use_container_width=True):
    st.markdown("---")

    # --- Use Spinner during API calls ---
    with st.spinner("🛰️ Contacting Kly-mate API on Render... Please wait (this might take 30s+ if the backend was idle)."):
        try:
            # --- Call /data/now endpoint ---
            data_url = f"{BACKEND_URL}/data/now?lat={lat}&lon={lon}"
            data_response = requests.get(data_url, timeout=45)
            data_response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
            data_json = data_response.json()

            # --- Call /predict/nextday/temperature endpoint ---
            predict_url = f"{BACKEND_URL}/predict/nextday/temperature?lat={lat}&lon={lon}"
            predict_response = requests.get(predict_url, timeout=45)
            predict_response.raise_for_status()
            predict_json = predict_response.json()

            # --- Data Extraction (Safely get data using .get()) ---
            location_data = data_json.get('location', {})
            weather_data = data_json.get('current_weather', {})
            aqi_data = data_json.get('current_aqi', {})
            backend_error = data_json.get('error_message') # Check for errors passed from backend

            predicted_temp = predict_json.get('predicted_temperature_next_day')
            prediction_error = predict_json.get('error_message')

            # --- Display Location ---
            st.subheader(f"📍 Current Conditions for {location_data.get('city', 'Selected Location')}")
            st.caption(f"Lat: {location_data.get('latitude', 'N/A')}, Lon: {location_data.get('longitude', 'N/A')}")

            # --- Display Weather Data ---
            st.markdown("##### ☀️ Weather")
            if weather_data:
                col_w1, col_w2, col_w3 = st.columns(3)
                col_w1.metric("Temperature",
                              f"{weather_data.get('temperature', '--')}°C",
                              delta=f"{weather_data.get('feels_like', '--')}°C Feels Like",
                              delta_color="inverse", # Color delta based on value
                              help="Current temperature and 'feels like' temperature.")
                col_w2.metric("Humidity", f"{weather_data.get('humidity', '--')}%",
                              help="Relative humidity.")
                col_w3.metric("Wind", f"{weather_data.get('wind_speed', '--')} m/s",
                              help="Wind speed.")

                # Weather Description and Icon
                description = weather_data.get('description', 'N/A').capitalize()
                icon_code = weather_data.get('icon')
                if icon_code:
                    icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
                    st.markdown(f"**Condition:** {description} <img src='{icon_url}' width='40' style='vertical-align:middle;'>", unsafe_allow_html=True)
                else:
                    st.markdown(f"**Condition:** {description}")

                # Expander for more details
                with st.expander("More Weather Details"):
                    st.markdown(f"""
                    - **Min/Max Temp:** {weather_data.get('temp_min', '--')}°C / {weather_data.get('temp_max', '--')}°C
                    - **Pressure:** {weather_data.get('pressure', '--')} hPa
                    """)
            else:
                st.warning("Weather data could not be retrieved.")
                if backend_error and "Weather Error" in backend_error:
                    st.caption(f"Backend Note: {backend_error}")


            # --- Display AQI Data ---
            st.markdown("##### 💨 Air Quality Index (AQI)")
            if aqi_data:
                aqi_value = aqi_data.get('aqi')
                aqi_help = "Air Quality Index based on OpenWeatherMap scale (1=Good, 2=Fair, 3=Moderate, 4=Poor, 5=Very Poor)."
                if aqi_value == 1:
                    st.metric("AQI", f"{aqi_value} (Good)", help=aqi_help)
                elif aqi_value == 2:
                    st.metric("AQI", f"{aqi_value} (Fair)", help=aqi_help)
                elif aqi_value == 3:
                    st.metric("AQI", f"{aqi_value} (Moderate)", help=aqi_help, delta="Potential minor impact", delta_color="inverse")
                elif aqi_value == 4:
                    st.metric("AQI", f"{aqi_value} (Poor)", help=aqi_help, delta="Potential health impact", delta_color="inverse")
                elif aqi_value == 5:
                    st.metric("AQI", f"{aqi_value} (Very Poor)", help=aqi_help, delta="Significant health impact", delta_color="inverse")
                else:
                     st.metric("AQI", f"{aqi_value if aqi_value is not None else '--'}", help=aqi_help)

                # Expander for pollutant details
                with st.expander("Pollutant Details (μg/m³))"):
                     st.markdown(f"""
                     - **PM2.5:** {aqi_data.get('pm2_5', '--')}
                     - **PM10:** {aqi_data.get('pm10', '--')}
                     - **O₃ (Ozone):** {aqi_data.get('o3', '--')}
                     - **NO₂ (Nitrogen Dioxide):** {aqi_data.get('no2', '--')}
                     - **SO₂ (Sulphur Dioxide):** {aqi_data.get('so2', '--')}
                     - **CO (Carbon Monoxide):** {aqi_data.get('co', '--')}
                     """)
            else:
                st.warning("AQI data could not be retrieved.")
                if backend_error and "AQI Error" in backend_error:
                    st.caption(f"Backend Note: {backend_error}")


            # --- Display Prediction ---
            st.markdown("##### 📈 Placeholder Temperature Prediction")
            if prediction_error:
                st.warning(f"Prediction Error: {prediction_error}")
            elif predicted_temp is not None:
                st.metric("Predicted Temp (Next Day - Placeholder)", f"{predicted_temp}°C",
                          help="This is a basic placeholder prediction (Current Temp + 1°C).")
            else:
                st.write("Prediction data not available.")

            st.success("✅ Done!") # Final success message

        # --- Error Handling for API Calls ---
        except requests.exceptions.Timeout:
            st.error(f"⏳ Error: Request timed out connecting to backend API ({BACKEND_URL}). The backend might be starting up if it was idle. Please try again in a minute.")
        except requests.exceptions.HTTPError as e:
             st.error(f"❌ Error: Backend API returned an HTTP error: {e.response.status_code}")
             st.write("This might happen if the backend couldn't fetch data from external sources (e.g., OpenWeatherMap) or if there was an internal issue.")
             try:
                 st.caption("Backend error details:")
                 st.json(e.response.json())
             except json.JSONDecodeError:
                 st.caption("Backend response (non-JSON):")
                 st.text(e.response.text) # Show raw text if not JSON
        except requests.exceptions.RequestException as e:
            st.error(f"🔗 Error connecting to backend API at {BACKEND_URL}. Please check the URL and ensure the backend is running. Error: {e}")
        except json.JSONDecodeError:
            st.error("🔧 Error: Could not decode JSON response from backend. This might indicate an unexpected backend error.")
            st.caption("Check backend logs on Render for more details.")
        except Exception as e:
            st.error(f" streamlit app: {e}")
            st.caption("This might be an issue in the Streamlit code itself or how it handled the response.")
    # --- Spinner automatically disappears ---
    st.markdown("---") # Separator line

# --- Footer ---
st.markdown("---")
st.caption("Kly-mate Demo | Built with FastAPI & Streamlit")