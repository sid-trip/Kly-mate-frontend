import streamlit as st
import requests
import json # Import json to handle potential parsing errors

st.title("Kly-mate Weather")

# --- Use Coordinates (Option 1: Hardcoded for now) ---
lat = 12.9716
lon = 77.5946
st.write(f"Showing data for Bengaluru (Lat: {lat}, Lon: {lon})")

# --- OR Use Input fields (Option 2: Uncomment below if you prefer) ---
# lat = st.number_input("Enter Latitude:", value=12.9716, format="%.4f")
# lon = st.number_input("Enter Longitude:", value=77.5946, format="%.4f")

# --- !!! VERY IMPORTANT: Use your ACTUAL deployed backend URL !!! ---
BACKEND_URL = "https://kly-mate.onrender.com" # <-- MAKE SURE THIS IS YOUR CORRECT RENDER URL!

if st.button("Get Current Data & Prediction"):
    st.markdown("---") # Separator line
    # --- Show spinner while fetching ---
    with st.spinner("Fetching data from Kly-mate API..."):
        try:
            # --- Call /data/now endpoint ---
            data_url = f"{BACKEND_URL}/data/now?lat={lat}&lon={lon}"
            # st.write(f"Calling: {data_url}") # Optional: Show URL being called
            data_response = requests.get(data_url, timeout=30) # Increased timeout slightly
            data_response.raise_for_status() # Check for HTTP errors (like 4xx, 5xx)
            st.subheader("Current Weather / AQI Data")
            st.json(data_response.json()) # Display the raw JSON

            # --- Call /predict/nextday/temperature endpoint ---
            predict_url = f"{BACKEND_URL}/predict/nextday/temperature?lat={lat}&lon={lon}"
            # st.write(f"Calling: {predict_url}") # Optional: Show URL being called
            predict_response = requests.get(predict_url, timeout=30) # Increased timeout slightly
            predict_response.raise_for_status() # Check for HTTP errors
            st.subheader("Placeholder Temperature Prediction")
            st.json(predict_response.json()) # Display the raw JSON

            st.success("Data loaded successfully!")

        except requests.exceptions.Timeout:
            st.error(f"Error: Request timed out connecting to backend API ({BACKEND_URL}).")
        except requests.exceptions.HTTPError as e:
             st.error(f"Error: Backend API returned an HTTP error: {e.response.status_code}")
             try:
                 # Try to display error detail from backend if available
                 st.json(e.response.json())
             except json.JSONDecodeError:
                 st.text(e.response.text) # Show raw text if not JSON
        except requests.exceptions.RequestException as e:
            st.error(f"Error connecting to backend API: {e}")
        except json.JSONDecodeError:
            st.error("Error: Could not decode JSON response from backend. This might indicate an unexpected backend error.")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
    # --- Spinner automatically disappears ---
    st.markdown("---") # Separator line