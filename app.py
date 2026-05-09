import streamlit as st
import pandas as pd
import folium

from streamlit_folium import st_folium


# -----------------------------------
# PAGE CONFIG
# -----------------------------------

st.set_page_config(
    page_title="DID Dashboard",
    layout="wide"
)


# -----------------------------------
# CUSTOM CSS
# -----------------------------------

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

    .glass {
        background: rgba(255,255,255,0.08);
        backdrop-filter: blur(10px);

        border-radius: 20px;

        padding: 20px;

        margin-bottom: 20px;

        box-shadow: 0 8px 32px rgba(0,0,0,0.2);
    }

    h1,h2,h3,h4,p,label {
        color: white !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# -----------------------------------
# SIDEBAR
# -----------------------------------

st.sidebar.title("🔐 Login")

username = st.sidebar.text_input(
    "Username"
)

password = st.sidebar.text_input(
    "Password",
    type="password"
)

login_btn = st.sidebar.button(
    "Login"
)

if login_btn:
    st.sidebar.success(
        f"Welcome {username}"
    )

st.sidebar.markdown("---")

st.sidebar.write(
    "Dengue Intelligent Dashboard"
)


# -----------------------------------
# HEADER
# -----------------------------------

st.markdown(
    """
    <div class="glass">
        <h1>
            🦟 Dengue Intelligent Dashboard
        </h1>

        <p>
            AI-Powered Early Warning System
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


# -----------------------------------
# METRICS
# -----------------------------------

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


# -----------------------------------
# MAIN LAYOUT
# -----------------------------------

left, right = st.columns([2,1])


# -----------------------------------
# MAP
# -----------------------------------

with left:

    st.markdown(
        """
        <div class="glass">
        <h2>🗺 Khartoum Risk Map</h2>
        """,
        unsafe_allow_html=True
    )

    m = folium.Map(
        location=[15.55, 32.55],
        zoom_start=8
    )

    districts = [

        (
            "Khartoum",
            [15.60, 32.53],
            "Critical",
            "red"
        ),

        (
            "Omdurman",
            [15.45, 32.40],
            "High",
            "darkred"
        ),

        (
            "Bahri",
            [15.70, 32.65],
            "Medium",
            "orange"
        ),

        (
            "Jabal Awliya",
            [15.20, 32.30],
            "Low",
            "green"
        )
    ]

    for district in districts:

        name = district[0]
        coords = district[1]
        risk = district[2]
        color = district[3]

        folium.CircleMarker(
            location=coords,
            radius=15,
            popup=f"{name} - {risk}",
            color=color,
            fill=True,
            fill_color=color
        ).add_to(m)

    st_folium(
        m,
        width=800,
        height=500
    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


# -----------------------------------
# ALERTS
# -----------------------------------

with right:

    st.markdown(
        """
        <div class="glass">
        <h2>🚨 Alerts</h2>
        """,
        unsafe_allow_html=True
    )

    st.error(
        "Critical outbreak probability in Khartoum"
    )

    st.warning(
        "High mosquito activity in Omdurman"
    )

    st.info(
        "Heavy rainfall expected this week"
    )

    st.success(
        "Low risk in Jabal Awliya"
    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


# -----------------------------------
# TABS
# -----------------------------------

tab1, tab2, tab3 = st.tabs(
    [
        "📈 Forecast",
        "🌡 Climate",
        "🔍 SHAP"
    ]
)


# -----------------------------------
# FORECAST TAB
# -----------------------------------

with tab1:

    df = pd.DataFrame({

        "Week": [
            "W1",
            "W2",
            "W3",
            "W4",
            "W5"
        ],

        "Actual": [
            40,
            70,
            120,
            150,
            180
        ],

        "Predicted": [
            45,
            75,
            118,
            160,
            210
        ]
    })

    st.line_chart(
        df.set_index("Week")
    )


# -----------------------------------
# CLIMATE TAB
# -----------------------------------

with tab2:

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "Temperature",
            "34°C"
        )

    with c2:
        st.metric(
            "Humidity",
            "74%"
        )

    with c3:
        st.metric(
            "Rainfall",
            "22 mm"
        )

    with c4:
        st.metric(
            "NDVI",
            "0.61"
        )


# -----------------------------------
# SHAP TAB
# -----------------------------------

with tab3:

    shap_df = pd.DataFrame({

        "Factor": [
            "Rainfall",
            "Humidity",
            "NDVI",
            "Temperature"
        ],

        "Importance": [
            0.40,
            0.30,
            0.20,
            0.10
        ]
    })

    st.bar_chart(
        shap_df.set_index("Factor")
    )


# -----------------------------------
# PIPELINE STATUS
# -----------------------------------

st.markdown(
    """
    <div class="glass">
        <h2>⚙ Pipeline Status</h2>
    </div>
    """,
    unsafe_allow_html=True
)

p1, p2, p3, p4 = st.columns(4)

with p1:
    st.success("1️⃣ Ingestion")

with p2:
    st.info("2️⃣ Processing")

with p3:
    st.warning("3️⃣ LSTM")

with p4:
    st.success("4️⃣ Notifications")


# -----------------------------------
# FOOTER
# -----------------------------------

st.markdown(
    """
    <hr>

    <center>

    <p style="color:white;">
        DID Prototype v1
    </p>

    </center>
    """,
    unsafe_allow_html=True
)
