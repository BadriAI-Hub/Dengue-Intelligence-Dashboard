import streamlit as st
import folium
import json
import random

from streamlit_folium import st_folium


# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Sudan Dengue Dashboard",
    layout="wide"
)


# ==========================================
# CSS
# ==========================================

st.markdown(
    """
    <style>

    .stApp{
        background: linear-gradient(
            135deg,
            #3a0000,
            #7f0000,
            #b30000
        );
    }

    h1,h2,h3,p{
        color:white !important;
    }

    .glass{
        background: rgba(255,255,255,0.08);

        padding:20px;

        border-radius:20px;

        backdrop-filter: blur(10px);

        margin-bottom:20px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.title("🔐 Login")

st.sidebar.text_input("Username")

st.sidebar.text_input(
    "Password",
    type="password"
)

st.sidebar.button("Login")


# ==========================================
# HEADER
# ==========================================

st.markdown(
    """
    <div class="glass">

    <h1>
        🦟 Sudan Dengue Dashboard
    </h1>

    <p>
        AI Early Warning System
    </p>

    </div>
    """,
    unsafe_allow_html=True
)


# ==========================================
# METRICS
# ==========================================

c1, c2, c3, c4 = st.columns(4)

c1.metric("Cases", "338")
c2.metric("High Risk", "18")
c3.metric("Alerts", "12")
c4.metric("Accuracy", "89%")


# ==========================================
# LOAD GEOJSON
# ==========================================

geojson_data = None

try:

    with open(
        "sudan_localities.geojson",
        "r",
        encoding="utf-8"
    ) as f:

        geojson_data = json.load(f)

except Exception as e:

    st.error(f"GeoJSON Error: {e}")


# ==========================================
# MAP
# ==========================================

st.markdown(
    """
    <div class="glass">

    <h2>
        🗺 Sudan Risk Map
    </h2>

    </div>
    """,
    unsafe_allow_html=True
)


m = folium.Map(

    location=[15.5, 30.5],

    zoom_start=5,

    tiles="cartodbpositron"
)


# ==========================================
# COLORS
# ==========================================

colors = [
    "#ff0000",
    "#8b0000",
    "#ff9800",
    "#4caf50"
]


# ==========================================
# ADD GEOJSON
# ==========================================

if geojson_data:

    for feature in geojson_data["features"]:

        try:

            locality_name = feature["properties"].get(
                "name",
                "Unknown"
            )

            color = random.choice(colors)

            folium.GeoJson(

                feature,

                style_function=lambda x,
                color=color: {

                    "fillColor": color,

                    "color": "white",

                    "weight": 1,

                    "fillOpacity": 0.6
                },

                tooltip=locality_name

            ).add_to(m)

        except:

            pass


# ==========================================
# DISPLAY MAP
# ==========================================

st_folium(
    m,
    width=1200,
    height=700
)


# ==========================================
# ALERTS
# ==========================================

st.markdown(
    """
    <div class="glass">

    <h2>
        🚨 Alerts
    </h2>

    </div>
    """,
    unsafe_allow_html=True
)

st.error("Critical outbreak probability detected")
st.warning("Flood risk increasing")
st.info("Heavy rainfall expected")
st.success("Low risk localities stable")


# ==========================================
# FORECAST
# ==========================================

st.markdown(
    """
    <div class="glass">

    <h2>
        📈 Forecast
    </h2>

    </div>
    """,
    unsafe_allow_html=True
)

forecast_data = {
    "Week": ["W1","W2","W3","W4"],
    "Cases": [55,120,180,260]
}

st.line_chart(forecast_data)


# ==========================================
# SHAP
# ==========================================

st.markdown(
    """
    <div class="glass">

    <h2>
        🔍 SHAP Analysis
    </h2>

    </div>
    """,
    unsafe_allow_html=True
)

shap_data = {
    "Factor":[
        "Rainfall",
        "Humidity",
        "NDVI",
        "Flood"
    ],

    "Importance":[
        0.42,
        0.31,
        0.18,
        0.09
    ]
}

st.bar_chart(
    {
        "Importance":[
            0.42,
            0.31,
            0.18,
            0.09
        ]
    }
)


# ==========================================
# FOOTER
# ==========================================

st.markdown(
    """
    <hr>

    <center>

    <p style='color:white;'>

    DID Prototype v5

    </p>

    </center>
    """,
    unsafe_allow_html=True
)
