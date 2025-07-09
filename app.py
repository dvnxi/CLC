import streamlit as st
import pandas as pd

# Function to load reference ranges
@st.cache_data
def load_reference_ranges():
    df = pd.read_csv('cbc_reference_ranges.csv')
    return df

# Load initial data
df_ref = load_reference_ranges()
df_user = df_ref.copy()

# Sidebar and main page settings
st.sidebar.title("Navigation")
options = st.sidebar.radio("Choose a section:", ["Home", "Protocols", "Reference Ranges", "Lab Results Interpretation", "About"])

if options == "Home":
    st.header("Welcome to Clinical Lab Companion")
    st.write("This app is designed to assist MedTech students in the Philippines with their studies, providing access to protocols, reference ranges, and lab results interpretation.")
    st.write("Use the sidebar to navigate through the app.")
    st.write("Developed by Devon Daquioag, a Computer Engineering student at Centro Escolar University, Manila, with the"
    " support from his friends and colleagues in the MedTech program.")

if options == "Reference Ranges":
    st.header("Reference Ranges")
    st.write("Access reference ranges for common laboratory tests.")
    test = st.selectbox("Select a test:", ["Complete Blood Count (CBC)", "Liver Function Tests", "Renal Function Tests", "Electrolytes"])
    st.write(f"You selected: {test}")

    if test == "Complete Blood Count (CBC)":
        st.write("**Complete Blood Count (CBC) Reference Ranges**")

        # Let user edit the table directly
        edited_df = st.data_editor(
            df_user,
            num_rows="dynamic",
            key="cbc_editor",
            use_container_width=True
        )

        col1, col2 = st.columns([1, 1])
        with col1:
            analyze = st.button("Analyze", key="analyze_btn")
        with col2:
            reset = st.button("Reset to CSV", key="reset_btn")

        if reset:
            st.session_state["cbc_editor"] = df_ref.copy()
            st.experimental_rerun()

        if analyze:
            # Debug: print column names if error persists
            # st.write("Columns in DataFrame:", df_ref.columns.tolist())
            results_html = ""
            # Adjust these to match your CSV column names exactly
            lower_col = "Lower" if "Lower" in df_ref.columns else df_ref.columns[1]
            upper_col = "Upper" if "Upper" in df_ref.columns else df_ref.columns[2]
            test_col = "Test" if "Test" in df_ref.columns else df_ref.columns[0]
            for idx, row in edited_df.iterrows():
                try:
                    orig_lower = float(df_ref.iloc[idx][lower_col])
                    orig_upper = float(df_ref.iloc[idx][upper_col])
                    edited_lower = float(row[lower_col])
                    edited_upper = float(row[upper_col])
                except Exception:
                    color = "gray"
                    comment = "Invalid or missing value"
                    edited_lower = row.get(lower_col, "")
                    edited_upper = row.get(upper_col, "")
                else:
                    if edited_lower < orig_lower or edited_upper > orig_upper:
                        color = "red"
                        comment = "The values are outside the normal reference range"
                    elif orig_lower <= edited_lower <= edited_upper <= orig_upper:
                        color = "green"
                        comment = "The values are within normal range"
                    else:
                        color = "gray"
                        comment = "Check the values"

                results_html += f"""
                <p style='color:{color};' title='{comment}'>{row[test_col]}: {edited_lower} - {edited_upper}</p>
                """

            st.markdown(results_html, unsafe_allow_html=True)

        st.write("**Disclaimer:** These reference ranges are for educational purposes only. Always consult actual laboratory references and licensed professionals.")
