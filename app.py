import streamlit as st
import pandas as pd
import folium
import json

from streamlit_folium import st_folium


# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Sudan Dengue Dashboard",
    layout="wide"
)


# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown(
    """
    <style>

    .stApp {
        background: linear-gradient(
            135deg,
            #2b0000,
            #7f0000,
            #c1121f
        );
    }

    h1, h2, h3, h4, p, label {
        color: white !important;
    }

    .glass {
        background: rgba(255,255,255,0.08);

        backdrop-filter: blur(10px);

        border-radius: 20px;

        padding: 20px;

        margin-bottom: 20px;

        box-shadow: 0 8px 32px rgba(0,0,0,0.2);
    }

    </style>
    """,
    unsafe_allow_html=True
)


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
    "Dengue Intelligent Dashboard"
)


# =====================================================
# HEADER
# =====================================================

st.markdown(
    """
    <div class="glass">

        <h1>
            🦟 Sudan Dengue Intelligent Dashboard
        </h1>

        <p>
            AI-Powered Early Warning System
        </p>

    </div>
    """,
    unsafe_allow_html=True
)


# =====================================================
# METRICS
# =====================================================

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.metric(
        "Active Cases",
        "338"
    )

with m2:
    st.metric(
        "High Risk Areas",
        "5"
    )

with m3:
    st.metric(
        "Alerts",
        "12"
    )

with m4:
    st.metric(
        "Model Accuracy",
        "89%"
    )


# =====================================================
# LOAD GEOJSON
# =====================================================

geojson_data = None

try:

    with open(
        "sudan_localities.geojson",
        "r",
        encoding="utf-8"
    ) as f:

        geojson_data = json.load(f)

except Exception as e:

    st.error(
        f"GeoJSON Error: {e}"
    )


# =====================================================
# MAP TITLE
# =====================================================

st.markdown(
    """
    <div class="glass">

        <h2>
            🗺 Sudan Dengue Risk Map
        </h2>

    </div>
    """,
    unsafe_allow_html=True
)


# =====================================================
# CREATE MAP
# =====================================================

m = folium.Map(

    location=[15.5, 30.5],

    zoom_start=5,

    tiles="cartodbpositron",

    control_scale=True
)


# =====================================================
# AFFECTED AREAS ONLY
# =====================================================

affected_areas = {

    "Khartoum": {
        "risk": "Critical",
        "cases": 240,
        "color": "#ff0000"
    },

    "Bahri": {
        "risk": "High",
        "cases": 180,
        "color": "#b30000"
    },

    "Omdurman": {
        "risk": "Medium",
        "cases": 95,
        "color": "#ff9800"
    },

    "Nyala": {
        "risk": "High",
        "cases": 150,
        "color": "#d32f2f"
    },

    "Port Sudan": {
        "risk": "Low",
        "cases": 40,
        "color": "#4caf50"
    }
}


# =====================================================
# STYLE FUNCTION
# =====================================================

def style_function(feature):

    locality = feature["properties"].get(
        "name",
        ""
    )

    # المناطق المصابة فقط
    if locality in affected_areas:

        return {

            "fillColor":
            affected_areas[locality]["color"],

            "color": "white",

            "weight": 1.5,

            "fillOpacity": 0.75
        }

    # بقية السودان
    return {

        "fillColor": "#d9d9d9",

        "color": "#888",

        "weight": 0.5,

        "fillOpacity": 0.15
    }


# =====================================================
# ADD GEOJSON
# =====================================================

if geojson_data:

    folium.GeoJson(

        geojson_data,

        style_function=style_function,

        tooltip=folium.GeoJsonTooltip(

            fields=["name"],

            aliases=["Locality:"]
        )

    ).add_to(m)


# =====================================================
# ADD CASE LABELS
# =====================================================

if geojson_data:

    for feature in geojson_data["features"]:

        locality = feature["properties"].get(
            "name",
            ""
        )

        # فقط المناطق المصابة
        if locality not in affected_areas:

            continue

        try:

            geometry = feature["geometry"]

            coords = geometry["coordinates"]

            # Polygon
            if geometry["type"] == "Polygon":

                point = coords[0][0]

                lon = point[0]

                lat = point[1]

            # MultiPolygon
            elif geometry["type"] == "MultiPolygon":

                point = coords[0][0][0]

                lon = point[0]

                lat = point[1]

            else:

                continue


            cases = affected_areas[
                locality
            ]["cases"]

            color = affected_areas[
                locality
            ]["color"]


            folium.Marker(

                location=[lat, lon],

                icon=folium.DivIcon(

                    html=f"""
                    <div style='
                        font-size:14px;
                        font-weight:bold;
                        color:white;
                        background:{color};
                        border-radius:50%;
                        width:34px;
                        height:34px;
                        text-align:center;
                        line-height:34px;
                        border:2px solid white;
                        box-shadow:0 0 10px rgba(0,0,0,0.4);
                    '>

                    {cases}

                    </div>
                    """
                )

            ).add_to(m)

        except:

            pass


# =====================================================
# DISPLAY MAP
# =====================================================

st_folium(

    m,

    width=1200,

    height=700,

    returned_objects=[]
)


# =====================================================
# ALERTS SECTION
# =====================================================

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

a1, a2 = st.columns(2)

with a1:

    st.error(
        "Critical outbreak probability in Khartoum"
    )

    st.warning(
        "Flood risk increasing in Nile areas"
    )

    st.info(
        "Heavy rainfall expected this week"
    )

with a2:

    st.warning(
        "Mosquito density increased by 23%"
    )

    st.success(
        "Low-risk localities remain stable"
    )

    st.info(
        "LSTM forecast updated successfully"
    )


# =====================================================
# TABS
# =====================================================

tab1, tab2, tab3 = st.tabs(
    [
        "📈 Forecast",
        "🌡 Climate",
        "🔍 SHAP"
    ]
)


# =====================================================
# FORECAST TAB
# =====================================================

with tab1:

    st.subheader(
        "📈 Multi-Variable Forecast"
    )

    forecast_df = pd.DataFrame({

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

        "Flood Risk": [
            1,
            1,
            2,
            2,
            3,
            3
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

    c1.metric(
        "Temperature",
        "34°C"
    )

    c2.metric(
        "Humidity",
        "74%"
    )

    c3.metric(
        "Rainfall",
        "22 mm"
    )

    c4.metric(
        "NDVI",
        "0.61"
    )

    c5.metric(
        "Flood Risk",
        "High"
    )


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

st.markdown(
    """
    <div class="glass">

        <h2>
            ⚙ Pipeline Status
        </h2>

    </div>
    """,
    unsafe_allow_html=True
)

p1, p2, p3, p4 = st.columns(4)

p1.success("1️⃣ Ingestion")
p2.info("2️⃣ Processing")
p3.warning("3️⃣ LSTM Prediction")
p4.success("4️⃣ Notifications")


# =====================================================
# FOOTER
# =====================================================

st.markdown(
    """
    <hr>

    <center>

    <p style='color:white;'>

    DID Prototype v6

    </p>

    </center>
    """,
    unsafe_allow_html=True
)
