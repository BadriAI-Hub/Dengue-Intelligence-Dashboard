import streamlit as st
import folium
import json
import random
import pandas as pd

from folium.plugins import HeatMap
from streamlit_folium import folium_static


# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Dengue Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>

/* =========================
MAIN BACKGROUND
========================= */

.stApp{
    background: linear-gradient(
        135deg,
        #140000,
        #5c0000,
        #a30000
    );
}


/* =========================
TEXT
========================= */

h1,h2,h3,h4,p,label,span{
    color:white !important;
}


/* =========================
GLASS EFFECT
========================= */

.glass{
    background: rgba(255,255,255,0.08);

    padding:20px;

    border-radius:20px;

    backdrop-filter: blur(12px);

    margin-bottom:20px;

    box-shadow:0 8px 32px rgba(0,0,0,0.25);
}


/* =========================
METRICS
========================= */

[data-testid="metric-container"]{

    background: rgba(255,255,255,0.08);

    border-radius:15px;

    padding:15px;

    border:1px solid rgba(255,255,255,0.1);
}


/* =========================
SIDEBAR
========================= */

[data-testid="stSidebar"]{

    background: linear-gradient(
        180deg,
        #ffffff,
        #f3f3f3
    );

    border-right:3px solid #8b0000;
}


/* Sidebar text */

[data-testid="stSidebar"] *{

    color:#111111 !important;
}


/* Inputs */

.stTextInput input{

    background:white !important;

    color:black !important;

    border-radius:10px !important;
}


/* Buttons */

.stButton button{

    background:#8b0000 !important;

    color:white !important;

    border:none !important;

    border-radius:10px !important;

    font-weight:bold !important;
}


/* =========================
TOP MENU ICON
========================= */

button[kind="header"]{

    color:white !important;
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.title("🔐 Login")

username = st.sidebar.text_input(
    "Username"
)

password = st.sidebar.text_input(
    "Password",
    type="password"
)

if st.sidebar.button("Login"):

    st.sidebar.success(
        f"Welcome {username}"
    )

st.sidebar.markdown("---")

st.sidebar.write(
    "DID Early Warning System"
)

st.sidebar.info(
    "AI-powered dengue surveillance for Khartoum State."
)


# =====================================================
# HEADER
# =====================================================

st.markdown("""
<div class="glass">

<h1>
🦟 Dengue Intelligent Dashboard (DID)
</h1>

<p>
AI-Powered Early Warning & Climate Surveillance System
</p>

</div>
""", unsafe_allow_html=True)


# =====================================================
# METRICS
# =====================================================

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.metric("Active Cases", "338")

with m2:
    st.metric("Hotspots", "12")

with m3:
    st.metric("Alerts", "7")

with m4:
    st.metric("Model Accuracy", "89%")


# =====================================================
# MAP TITLE
# =====================================================

st.markdown("""
<div class="glass">

<h2>
🔥 Khartoum HeatMap
</h2>

</div>
""", unsafe_allow_html=True)


# =====================================================
# KHARTOUM MAP
# =====================================================

m = folium.Map(

    location=[15.55, 32.53],

    zoom_start=10,

    tiles="cartodbpositron"
)


# =====================================================
# KHARTOUM HEAT POINTS
# =====================================================

heat_data = [

    [15.60, 32.53, 300],   # Khartoum center

    [15.64, 32.49, 250],   # Omdurman

    [15.67, 32.62, 220],   # Bahri

    [15.58, 32.57, 200],

    [15.70, 32.60, 180],

    [15.63, 32.55, 260],

    [15.61, 32.50, 150],

    [15.68, 32.52, 170],

    [15.57, 32.61, 140],

    [15.65, 32.58, 280]
]


# =====================================================
# HEATMAP LAYER
# =====================================================

HeatMap(

    heat_data,

    radius=35,

    blur=25,

    max_zoom=12,

    min_opacity=0.4

).add_to(m)


# =====================================================
# CASE MARKERS
# =====================================================

for point in heat_data:

    lat = point[0]
    lon = point[1]
    cases = point[2]

    folium.CircleMarker(

        location=[lat, lon],

        radius=6,

        color="red",

        fill=True,

        fill_color="red",

        fill_opacity=0.8,

        popup=f"Cases: {cases}"

    ).add_to(m)


# =====================================================
# DISPLAY MAP
# =====================================================

folium_static(

    m,

    width=1200,

    height=700
)


# =====================================================
# ALERTS
# =====================================================

st.markdown("""
<div class="glass">

<h2>
🚨 Active Alerts
</h2>

</div>
""", unsafe_allow_html=True)

st.error(
    "Critical outbreak probability detected in Khartoum center"
)

st.warning(
    "Heavy rainfall expected this week"
)

st.warning(
    "Flood risk increasing near Nile areas"
)

st.info(
    "Mosquito density increased by 23%"
)

st.success(
    "Southern districts remain stable"
)


# =====================================================
# TABS
# =====================================================

tab1, tab2, tab3 = st.tabs([
    "📈 Forecast",
    "🌡 Climate",
    "🔍 SHAP"
])


# =====================================================
# FORECAST TAB
# =====================================================

with tab1:

    st.subheader(
        "📈 Multi-Variable Dengue Forecast"
    )forecast_df = pd.DataFrame({

    "Week": [
        "W1",
        "W2",
        "W3",
        "W4",
        "W5",
        "W6"
    ],

    "Actual Cases": [
        45,
        72,
        118,
        155,
        None,
        None
    ],

    "Predicted Cases": [
        50,
        75,
        120,
        165,
        210,
        260
    ],

    "Temperature": [
        31,
        32,
        34,
        35,
        36,
        37
    ],

    "Humidity": [
        68,
        70,
        74,
        78,
        80,
        83
    ],

    "Rainfall": [
        12,
        18,
        25,
        30,
        42,
        55
    ],

    "NDVI": [
        0.42,
        0.48,
        0.53,
        0.61,
        0.66,
        0.72
    ],

    # =========================================
    # NEW VARIABLES
    # =========================================

    "Flood Risk": [
        "Low",
        "Medium",
        "Medium",
        "High",
        "High",
        "Critical"
    ],

    "Stagnant Water": [
        18,
        24,
        35,
        42,
        57,
        73
    ],

    "Displacement Camps": [
        4,
        5,
        6,
        7,
        9,
        11
    ],

    "Population Density": [
        1200,
        1350,
        1480,
        1600,
        1780,
        1950
    ]
})

    st.line_chart(
        forecast_df.set_index("Week")[
            [
                "Actual Cases",
                "Predicted Cases"
            ]
        ]
    )

    st.dataframe(
        forecast_df,
        use_container_width=True
    )


# =====================================================
# CLIMATE TAB
# =====================================================

with tab2:

    c1, c2, c3, c4, c5 = st.columns(5)

    with c1:
        st.metric("Temperature", "34°C")

    with c2:
        st.metric("Humidity", "74%")

    with c3:
        st.metric("Rainfall", "22 mm")

    with c4:
        st.metric("NDVI", "0.61")

    with c5:
        st.metric("Flood Risk", "High")


# =====================================================
# SHAP TAB
# =====================================================

with tab3:

    shap_df = pd.DataFrame({

        "Factor": [
            "Rainfall",
            "Humidity",
            "NDVI",
            "Flood Risk",
            "Temperature"
        ],

        "Importance": [
            0.42,
            0.30,
            0.15,
            0.08,
            0.05
        ]
    })

    st.bar_chart(
        shap_df.set_index("Factor")
    )


# =====================================================
# PIPELINE STATUS
# =====================================================

st.markdown("""
<div class="glass">

<h2>
⚙ Pipeline Status
</h2>

</div>
""", unsafe_allow_html=True)

p1, p2, p3, p4 = st.columns(4)

with p1:
    st.success("1️⃣ Ingestion")

with p2:
    st.info("2️⃣ Processing")

with p3:
    st.warning("3️⃣ LSTM Prediction")

with p4:
    st.success("4️⃣ Notifications")


# =====================================================
# FOOTER
# =====================================================

st.markdown("""
<hr>

<center>

<p style='color:white;'>

DID Prototype HeatMap Version
|
Khartoum State + Streamlit + Folium

</p>

</center>
""", unsafe_allow_html=True)
