import streamlit as st
import pandas as pd
import json

# Sidebar and main page settings
st.sidebar.title("Navigation")
options = st.sidebar.radio("Choose a section:", ["Home", "Protocols", "Ranges Reference", "Lab Results Interpretation", "About", "References"])

if options == "Home":
    st.header("Welcome to Clinical Lab Companion")
    st.write("This app is designed to assist MedTech students in the Philippines with their studies, providing access to protocols, reference ranges, and lab results interpretation.")
    st.write("Use the sidebar to navigate through the app.")
    #st.write("Developed by Devon Daquioag, a Computer Engineering student at Centro Escolar University, Manila, with the"
    #" support from his friends and colleagues in the MedTech program.")
















if options == "Ranges Reference":
    st.header("Reference Ranges")
    st.write("Access reference ranges for common laboratory tests.")
    test = st.selectbox("Select a test:", ["Complete Blood Count (CBC)", "Liver Function Test", "Renal Function Test", "Electrolytes"])
    st.write(f"You selected: {test}")

    if test == "Complete Blood Count (CBC)":
        st.write("**Complete Blood Count (CBC) Reference Ranges**")
        df_cbc = pd.read_csv('cbc_reference_ranges.csv')
        st.dataframe(df_cbc)

        st.write("**Disclaimer:** These reference ranges are for educational purposes only. Always consult actual laboratory references and licensed professionals.")
    
    if test == "Liver Function Test":
        st.write("**Liver Function Test Reference Ranges**")
        df_lft = pd.read_csv('lft_reference_ranges.csv')
        st.dataframe(df_lft)

        st.write("**Disclaimer:** These reference ranges are for educational purposes only. Always consult actual laboratory references and licensed professionals.")












if options == "References":

    with open('references.json') as f:
        data = json.load(f)
        st.header("References")
        for ref in data["references"]:
            st.markdown(f"- **{ref['title']}** ({ref['url']})")