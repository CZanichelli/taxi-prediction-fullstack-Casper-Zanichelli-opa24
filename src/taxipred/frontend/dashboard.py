import streamlit as st
from taxipred.utils.helpers import read_api_endpoint
from taxipred.backend.data_processing import TRAFFIC_ENCODING_MAP
import pandas as pd
import json
import requests

ADMIN_PASSWORD = "ResekollenAdmin2025"

def set_url_background(image_url):
    """Sätter en bakgrundsbild med hjälp av CSS och URL."""
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("{image_url}");
            background-size: cover;
            background-attachment: fixed; 
            background-position: center;
            color: black;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


def login_form():
    
    st.sidebar.header("Admin-inloggning")
    
    with st.sidebar.form("login_form"):
        password = st.text_input("Lösenord", type="password")
        submitted = st.form_submit_button("Logga in")
        
        if submitted:
            if password == ADMIN_PASSWORD:
                st.session_state["logged_in"] = True
                st.sidebar.success("Inloggning lyckades!")
            else:
                st.session_state["logged_in"] = False
                st.sidebar.error("Felaktigt lösenord.")
    
def main_menu():
    
    st.set_page_config(layout="wide")
    
    
    IMAGE_URL = "https://images.pexels.com/photos/19295734/pexels-photo-19295734/free-photo-of-skylt-bil-tak-taxi.jpeg" 
    set_url_background(IMAGE_URL) 
    
    
    st.sidebar.title("App-Navigering")
    
   
    if st.session_state.get("logged_in", False):
        menu_options = ["Prisprediktion", "Databasanalys (Admin)"]
    else:
        menu_options = ["Prisprediktion"]

    selection = st.sidebar.radio("Gå till:", menu_options)
    
    return selection


def main():
    st.set_page_config(layout="wide")
    st.title("🗺️ Resekollens: Taxiprisprediktion")

    if not st.session_state.get("logged_in", False):
        login_form()

    selection = main_menu()

    if selection == "Prisprediktion":
        
        st.subheader("1. Prediktera din resa")
        
        #User input 
        col1, col2 = st.columns([1, 2])

        with col1:
            st.subheader("Ange information om resan")

            distance = st.number_input(
                "Sträcka (km):",
                min_value=1.0,
                max_value=100.0,
                value=5.0
            )
            duration = st.number_input(
                "Tid (Minuter):",
                min_value=5.0,
                max_value=160.0,
                value=10.0
            )

            traffic_text = st.selectbox(
                "Trafiksituation (Låg/Medel/Hög):",
                options=list(TRAFFIC_ENCODING_MAP.keys()),
                index=1
            )
            # Translate text to number
            traffic_values = TRAFFIC_ENCODING_MAP[traffic_text]

            st.markdown("---")

            #predictionbutton
            predict_button = st.button("Beräkna Pris (USD)")
        
        with col2:

            #Logic for API-call

            if predict_button:

                payload = {
                    "Trip_Distance_km": distance,
                    "Trip_Duration_Minutes": duration,
                    "Traffic_Encoded": traffic_values
                }

                API_URL = "http://127.0.0.1:8000/predict"

                try:
                    #Post-call
                    response = requests.post(API_URL, json=payload)
                    response.raise_for_status()

                    #Show Result
                    result = response.json()
                    st.success(f"### Beräknat pris: {result['predicted_price']} USD")
                    st.write(f"Sträcka: {distance} km, Tid: {duration} min, Trafik: {traffic_text}")

                except requests.exceptions.RequestException as e:
                    st.error(f"error: {e}")

    elif selection == "Databasanalys (Admin)":
        if st.session_state["logged_in"]:
            st.subheader("📊 Adminvy: Fullständiga Dataresultat")
            try:
                data = read_api_endpoint("/data/data")
                df = pd.DataFrame(data.json())
                st.dataframe(df, use_container_width=True)
            except Exception as e:
                st.warning(f"error: {e}")

            pass # Placeholder
        else:
            st.error("Åtkomst nekad. Vänligen logga in som administratör.")       

if __name__ == "__main__":
    main()
