import streamlit as st
from taxipred.utils.helpers import read_api_endpoint
from taxipred.backend.data_processing import TRAFFIC_ENCODING_MAP
import pandas as pd



def main():
    st.set_page_config(layout="wide")
    st.title("Resekollens: Taxiprisprediktion")

    col1, col2 =([1, 2])

    with col1:
        st.subheader("1. Inmatning")

        distance = st.number_input(
            "Sträcka (km):",
            min_value=1.0,
            max_value=100.0,
            value=5.0

        )

if __name__ == "__main__":
    main()
