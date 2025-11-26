import streamlit as st
import pickle
import numpy as np
import plotly.express as px
from pathlib import Path
import base64

# ==============================
# Load Saved Model + Preprocessors
# ==============================
with open("carbon.pkl", "rb") as obj1:
    data = pickle.load(obj1)

# ==============================
# Page Configuration
# ==============================
st.set_page_config(page_title="Carbon Footprint Calculator", page_icon="🌱", layout="wide")

# ==============================
# Custom CSS for Dark Theme + Styling
# ==============================
st.markdown("""
    <style>
        /* App Background */
        .stApp {
            background: linear-gradient(135deg, #1e1e2f, #121212);
            font-family: 'Segoe UI', sans-serif;
        }

        /* Title Styling */
        h1 {
            color: #a5d6a7;
            text-align: center;
            font-size: 3em;
            font-weight: bold;
            text-shadow: 0px 0px 15px #4caf50;
            margin-bottom: 5px;
        }

        /* Subtitle Styling */
        .subtitle {
            text-align: center;
            color: #e0f2f1;
            font-size: 1.2em;
            margin-bottom: 25px;
        }

        /* Input Widgets */
        .stSelectbox, .stNumberInput, .stMultiSelect {
            border-radius: 10px !important;
            padding: 6px !important;
            background-color: #2b2b3b !important;
            box-shadow: 0 2px 6px rgba(0,0,0,0.3);
            margin-bottom: 10px;
        }

        /* Input Text, Placeholder, and Selected Values */
        .stSelectbox div[data-baseweb="select"] > div,
        .stNumberInput input,
        .stMultiSelect div[data-baseweb="select"] > div {
            color: #f1f1f1 !important;
            font-weight: 500;
        }

        /* Widget Labels */
        label {
            color: #cfd8dc !important;
            font-weight: 600;
        }

        /* Expander Styling */
        .stExpander {
            border-radius: 10px;
            background-color: #2c2c3c;
            box-shadow: 0 2px 4px rgba(0,0,0,0.3);
        }
        .stExpander p, .stExpander div[role="region"] {
            color: #e0f2e9 !important;
        }

        /* Buttons */
        div.stButton > button {
            background: linear-gradient(90deg, #43a047, #1b5e20);
            color: white;
            font-weight: bold;
            border-radius: 25px;
            padding: 12px 24px;
            transition: 0.3s ease-in-out;
            display: block;
            margin: 20px auto;
        }
        div.stButton > button:hover {
            background: linear-gradient(90deg, #2e7d32, #004d40);
            transform: scale(1.05);
        }

        /* Result Messages */
        .stSuccess, .stInfo, .stWarning, .stError {
            border-radius: 12px !important;
            padding: 15px !important;
            font-size: 16px;
            font-weight: 500;
            margin-top: 10px;
            color: #263238 !important;
            background-color: #e8f5e9 !important;
        }

        /* Center Image */
        .centered-img {
            display: block;
            margin-left: auto;
            margin-right: auto;
        }
    </style>
""", unsafe_allow_html=True)

# ==============================
# Header and Hero Banner
# ==============================

img_path = Path("Carbon Footprint Awareness Illustration.png")

if img_path.exists():
    st.markdown(
        f"""
        <div style="text-align: center;">
            <img src="data:image/png;base64,{base64.b64encode(open(img_path, "rb").read()).decode()}" 
                 alt="Carbon Footprint" 
                 style="width: 400px; max-width: 80%; border-radius: 12px; box-shadow: 0px 4px 15px rgba(0,0,0,0.5);">
            <p style="color: #b2dfdb; font-size: 16px; margin-top: 8px;">
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown(
    "<h1 style='text-align:center; color:#e0f2e9; font-size: 3em;'>🌍 Carbon Footprint Calculator</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align:center; color:#b2dfdb; font-size:18px;'>Understand your impact on the environment and explore ways to reduce it.</p>",
    unsafe_allow_html=True
)

# ==============================
# Sidebar with Tips
# ==============================
st.sidebar.title("💡 Tips to Reduce Carbon Emissions")
st.sidebar.markdown("""
- 🚶 Walk, cycle, or use public transport instead of driving.
- 💡 Switch to energy-efficient appliances and lighting.
- 🍃 Reduce meat consumption; choose plant-based meals.
- 🔄 Recycle and reuse materials whenever possible.
- 🌞 Use renewable energy sources like solar.
- 🛒 Buy local and sustainable products.
- 👕 Reduce fast fashion purchases; reuse clothes.
- ✈️ Minimize unnecessary flights.
""")

# ==============================
# Mapping Dictionaries for Categorical → Numerical
# ==============================
shower_often = {"Daily": 0, "Less Frequently": 1, "Twice a Day": 2, "More Frequently": 3}
waste_bag_size = {"Small": 0, "Medium": 1, "Large": 2, "Extra Large": 3}
traveling_by_air = {"Never": 0, "Rarely": 1, "Frequently": 2, "Very Frequently": 3}
energy_efficiency = {"No": 0, "Sometimes": 1, "Yes": 2}

# ==============================
# Input Sections with Expanders and Columns
# ==============================
with st.expander("🏠 Lifestyle & Household Habits", expanded=True):
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Personal Habits")
        shower = st.selectbox("How often do you take a shower?", list(shower_often.keys()))
        shower_val = shower_often[shower]

        grocery_bill = st.number_input("Monthly grocery bill (₹)?", min_value=0.0, value=0.0, step=100.0)

        travelling_air = st.selectbox("How often do you travel by air?", list(traveling_by_air.keys()))
        travelling_air_val = traveling_by_air[travelling_air]

        vehicle_distance = st.number_input("Kilometers traveled by vehicle per month?", min_value=0.0, value=0.0, step=10.0)

    with col2:
        st.markdown("### Waste & Energy")
        waste_bag = st.selectbox("Typical waste bag size?", list(waste_bag_size.keys()))
        waste_bag_val = waste_bag_size[waste_bag]

        waste_bag_count = st.number_input("Waste bags used per week?", min_value=0, value=0, step=1)

        new_clothes = st.number_input("New clothes purchased per month?", min_value=0, value=0, step=1)

        energy = st.selectbox("Is your household energy-efficient?", list(energy_efficiency.keys()))
        energy_val = energy_efficiency[energy]

with st.expander("🌿 Additional Preferences", expanded=True):
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Lifestyle Choices")
        diet = st.selectbox("What is your diet preference?", data['diet'])
        energy_source = st.selectbox("Primary heating energy source?", data['heat'])

    with col2:
        st.markdown("### Transport & Recycling")
        transport = st.selectbox("Primary mode of transport?", data['transport'])
        vehicle = st.selectbox("Main vehicle type?", data['vehicle_type'])

# Multi-select inputs
st.markdown("### Recycling & Cooking")
recycling = st.multiselect("Which items do you recycle at home?", data['list_recycling'], help="Select all that apply")
cooking = st.multiselect("Main cooking energy sources?", data['list_cooking'], help="Select all that apply")

# ==============================
# Input Validation & Prediction
# ==============================
if st.button("Predict Carbon Footprint"):
    if not all([shower, grocery_bill >= 0, travelling_air, vehicle_distance >= 0, waste_bag, waste_bag_count >= 0, new_clothes >= 0, energy, diet, energy_source, transport, vehicle]):
        st.warning("⚠️ Please fill in all required fields before predicting.")
    else:
        # Transform Inputs
        onehot_values = data['onehot'].transform([[diet, energy_source, transport, vehicle]]).flatten().reshape(1, -1)
        recycling_val = data['mb_recycling'].transform([recycling]).flatten().reshape(1, -1)
        cooking_val = data['mb_cooking'].transform([cooking]).flatten().reshape(1, -1)

        a = np.array([[shower_val, grocery_bill, travelling_air_val, vehicle_distance,
                       waste_bag_val, waste_bag_count, new_clothes, energy_val]])
        b = np.hstack([a, onehot_values, recycling_val, cooking_val])

        # Prediction
        b = b.reshape(1, -1)
        test = data['scaler'].transform(b)
        poly_features = data['poly'].transform(test)
        predicted_value = data['model'].predict(poly_features)[0]

        # Display results
        st.markdown(f"### 🌍 Estimated Carbon Footprint: **{predicted_value:.2f} kg CO₂e / month**")

        if predicted_value < 2000:
            st.success("✅ Low carbon footprint (sustainable lifestyle).")
        elif predicted_value < 4000:
            st.info("ℹ️ Moderate carbon footprint. Some improvements can help.")
        elif predicted_value < 6500:
            st.warning("⚠️ High carbon footprint. Consider reducing energy, transport, or waste.")
        else:
            st.error("🚨 Very high carbon footprint! Urgent action recommended.")

        # Visualization
        thresholds = [2000, 4000, 6500]
        labels = ['Low', 'Moderate', 'High', 'Very High']
        colors = ['#00cc00', '#66b3ff', '#ff9900', '#ff3333']

        fig = px.bar(
            x=['Your Footprint'],
            y=[predicted_value],
            color=['Your Footprint'],
            color_discrete_sequence=[colors[min(len(labels) - 1, [i for i, t in enumerate(thresholds) if predicted_value < t][0] if predicted_value < thresholds[-1] else len(thresholds))]],
            labels={'y': 'Carbon Footprint (kg CO₂e / month)', 'x': ''},
            title="Your Carbon Footprint"
        )
        fig.add_hline(y=2000, line_dash="dash", line_color="#00cc00", annotation_text="Low", annotation_position="top left")
        fig.add_hline(y=4000, line_dash="dash", line_color="#66b3ff", annotation_text="Moderate", annotation_position="top left")
        fig.add_hline(y=6500, line_dash="dash", line_color="#ff3333", annotation_text="High", annotation_position="top left")
        st.plotly_chart(fig, use_container_width=True)
