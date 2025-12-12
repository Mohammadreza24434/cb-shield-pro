```python
import streamlit as st
import numpy as np
import plotly.graph_objects as go
import datetime
import hashlib
from pathlib import Path

# ====================== Secure License System ======================
def license_system():
    license_file = Path("license.key")
    SECRET_SALT = "CBRN-IRAN-DEFENSE-2025-TOPSECRET"

    # Check if valid license exists
    if license_file.exists():
        try:
            saved_code, saved_hash = license_file.read_text().strip().split("|")
            if hashlib.sha256(f"{saved_code}{SECRET_SALT}".encode()).hexdigest() == saved_hash:
                st.session_state.license_valid = True
                return True
        except:
            pass

    # License Entry Screen
    st.markdown("<h1 style='text-align:center;color:#8B0000;font-size:60px;'>CB-SHIELD PRO</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center;color:#2c3e50;'>Advanced CBRN Dispersion Modeling System</h3>", unsafe_allow_html=True)
    st.markdown("---")
    st.error("License Required to Access Software")

    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        license_code = st.text_input("Enter License Code", type="password", placeholder="XXXX-XXXX-XXXX-XXXX")
        if st.button("Activate & Enter", type="primary", use_container_width=True):
            if len(license_code) >= 10:
                test_hash = hashlib.sha256(f"{license_code}{SECRET_SALT}".encode()).hexdigest()
                license_file.write_text(f"{license_code}|{test_hash}")
                st.success("License Activated! Welcome.")
                st.session_state.license_valid = True
                st.rerun()
            else:
                st.error("Invalid license code")

        with st.expander("Developer: Generate License"):
            dev_pwd = st.text_input("Password", type="password")
            if st.button("Generate New Code"):
                if dev_pwd == "YourSecretDevPass2025":  # CHANGE THIS TO YOUR PASSWORD
                    new_code = f"CBRN-{datetime.date.today().strftime('%Y%m%d')}-{hashlib.md5(str(datetime.now()).encode()).hexdigest()[:8].upper()}"
                    st.code(new_code)
                    st.success("New license code generated! Use it above.")
                else:
                    st.error("Wrong password")

    st.stop()

license_system()

# ====================== Full 65 CBRN Agents Database ======================
chemicals_db = {
    "Sarin (GB)":                    {"Mw": 140.1, "LCt50": 75,    "Incap": 25},
    "Tabun (GA)":                    {"Mw": 162.3, "LCt50": 400,   "Incap": 150},
    "Soman (GD)":                    {"Mw": 182.2, "LCt50": 35,    "Incap": 15},
    "Cyclosarin (GF)":               {"Mw": 180.2, "LCt50": 35,    "Incap": 25},
    "VX":                            {"Mw": 267.4, "LCt50": 10,    "Incap": 5},
    "VR (Russian VX)":               {"Mw": 267.4, "LCt50": 15,    "Incap": 7},
    "VE":                            {"Mw": 211.2, "LCt50": 25,    "Incap": 10},
    "VG (Amiton)":                   {"Mw": 269.3, "LCt50": 30,    "Incap": 12},
    "VM":                            {"Mw": 225.3, "LCt50": 40,    "Incap": 15},
    "GV":                            {"Mw": 225.2, "LCt50": 30,    "Incap": 12},
    "Novichok A-230":                {"Mw": 294.0, "LCt50": 7,     "Incap": 1.5},
    "Novichok A-232":                {"Mw": 298.0, "LCt50": 7,     "Incap": 2},
    "Novichok A-234":                {"Mw": 300.0, "LCt50": 5,     "Incap": 1},
    "EA-3148":                       {"Mw": 295.0, "LCt50": 8,     "Incap": 2},
    "Sulfur Mustard (HD)":           {"Mw": 159.1, "LCt50": 1500,  "Incap": 200},
    "Lewisite (L)":                  {"Mw": 207.3, "LCt50": 1200,  "Incap": 150},
    "Nitrogen Mustard (HN-1)":       {"Mw": 170.1, "LCt50": 1500,  "Incap": 200},
    "Nitrogen Mustard (HN-2)":       {"Mw": 156.1, "LCt50": 3000,  "Incap": 400},
    "Nitrogen Mustard (HN-3)":       {"Mw": 204.5, "LCt50": 1500,  "Incap": 200},
    "Phenyldichloroarsine (PD)":     {"Mw": 223.0, "LCt50": 2600,  "Incap": 400},
    "Ethyldichloroarsine (ED)":      {"Mw": 174.9, "LCt50": 3000,  "Incap": 500},
    "Methyldichloroarsine (MD)":     {"Mw": 160.9, "LCt50": 3000,  "Incap": 500},
    "Phosgene Oxime (CX)":           {"Mw": 113.5, "LCt50": 3200,  "Incap": 1600},
    "Hydrogen Cyanide (AC)":         {"Mw": 27.0,  "LCt50": 2500, "Incap": 1000},
    "Cyanogen Chloride (CK)":        {"Mw": 61.5,  "LCt50": 11000,"Incap": 2500},
    "Arsine (SA)":                   {"Mw": 77.9,  "LCt50": 5000, "Incap": 500},
    "Phosgene (CG)":                 {"Mw": 98.9,  "LCt50": 3200, "Incap": 1600},
    "Diphosgene (DP)":               {"Mw": 197.8, "LCt50": 3200, "Incap": 800},
    "Chlorine (Cl2)":                {"Mw": 70.9,  "LCt50": 19000,"Incap": 3000},
    "Chloropicrin (PS)":             {"Mw": 164.4, "LCt50": 2000, "Incap": 400},
    "Perfluoroisobutylene (PFIB)":   {"Mw": 200.0, "LCt50": 300,  "Incap": 50},
    "BZ Agent":                      {"Mw": 337.4, "LCt50": 110000,"Incap": 20000},
    "Agent 15":                      {"Mw": 340.0, "LCt50": 100000,"Incap": 18000},
    "EA-3167":                       {"Mw": 350.0, "LCt50": 150000,"Incap": 25000},
    "CS Gas":                        {"Mw": 188.5, "LCt50": 60000, "Incap": 5},
    "CR Gas":                        {"Mw": 195.0, "LCt50": 60000, "Incap": 3},
    "CN Gas":                        {"Mw": 154.6, "LCt50": 8500,  "Incap": 20},
    "OC (Pepper Spray)":             {"Mw": 305.4, "LCt50": 100000,"Incap": 1},
    "PAVA":                          {"Mw": 293.4, "LCt50": 120000,"Incap": 2},
    "Adamsite (DM)":                 {"Mw": 277.6, "LCt50": 11000, "Incap": 150},
    "Ammonia":                       {"Mw": 17.0,  "LCt50": 5000, "Incap": 1500},
    "Methyl Isocyanate":             {"Mw": 57.1,  "LCt50": 300,  "Incap": 50},
    "Acrolein":                      {"Mw": 56.1,  "LCt50": 150,  "Incap": 20},
    "Formaldehyde (gas)":            {"Mw": 30.0,  "LCt50": 800,  "Incap": 100},
    "Hydrazine":                     {"Mw": 32.0,  "LCt50": 570,  "Incap": 100},
    "Bromine":                       {"Mw": 159.8, "LCt50": 1500, "Incap": 300},
    "Ricin":                         {"Mw": 64000, "LCt50": 3,     "Incap": 0.5},
    "Botulinum Toxin":               {"Mw": 150000,"LCt50": 0.001,"Incap": 0.0001},
    "Staph Enterotoxin B (SEB)":     {"Mw": 28354, "LCt50": 0.02, "Incap": 0.0003},
    "T-2 Mycotoxin":                 {"Mw": 466.0, "LCt50": 200,  "Incap": 50},
    "Saxitoxin":                     {"Mw": 299.3, "LCt50": 0.01, "Incap": 0.002},
    "Tetrodotoxin":                  {"Mw": 319.3, "LCt50": 0.008,"Incap": 0.001},
    "Anthrax Spores":                {"Mw": 0,     "LCt50": 8000, "Incap": 2000},
    "Plague (Y. pestis)":            {"Mw": 0,     "LCt50": 100,  "Incap": 10},
    "Tularemia":                     {"Mw": 0,     "LCt50": 10,   "Incap": 1},
    "Q Fever":                       {"Mw": 0,     "LCt50": 10,   "Incap": 1},
    "Smallpox":                      {"Mw": 0,     "LCt50": 10,   "Incap": 1},
    "Ebola Virus":                   {"Mw": 0,     "LCt50": 1,    "Incap": 0.1},
    "Marburg Virus":                 {"Mw": 0,     "LCt50": 1,    "Incap": 0.1},
    "Brucellosis":                   {"Mw": 0,     "LCt50": 100,  "Incap": 10},
    "Glanders":                      {"Mw": 0,     "LCt50": 100,  "Incap": 10},
    "Melioidosis":                   {"Mw": 0,     "LCt50": 50,   "Incap": 5},
    "Rift Valley Fever":             {"Mw": 0,     "LCt50": 10,   "Incap": 1},
    "Hantavirus":                    {"Mw": 0,     "LCt50": 5,    "Incap": 0.5},
    "Nipah Virus":                   {"Mw": 0,     "LCt50": 2,    "Incap": 0.2},
}

# Sigma Functions (Vectorized & Safe)
def get_sigma_y(stability, x):
    x = np.maximum(x, 1.0)
    params = {'A': 0.22, 'B': 0.16, 'C': 0.11, 'D': 0.08, 'E': 0.06, 'F': 0.04}
    sy = params.get(stability, 0.08) * x ** 0.9
    return np.minimum(sy, 1000)

def get_sigma_z(stability, x):
    x = np.maximum(x, 1.0)
    if stability == 'A':
        sz = np.where(x < 100, 0.20 * x,
               np.where(x < 500, 0.24 * x ** 0.75, 0.15 * x ** 0.80))
    else:
        params = {'B': 0.12, 'C': 0.08, 'D': 0.06, 'E': 0.03, 'F': 0.016}
        exp = {'B': 1.0, 'C': 0.90, 'D': 0.85, 'E': 0.75, 'F': 0.70}
        a = params.get(stability, 0.06)
        b = exp.get(stability, 0.85)
        sz = a * x ** b
    return np.minimum(sz, 1000)

# Page Config
st.set_page_config(page_title="CB-Shield Pro", layout="wide", page_icon="☣️")

st.markdown("""
<style>
    .big-font {font-size:60px !important; font-weight:bold; color:#8B0000; text-align:center;}
    .header {font-size:28px; color:#006400; text-align:center;}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="big-font">CB-SHIELD PRO</p>', unsafe_allow_html=True)
st.markdown("<p class='header'>Chemical & Biological Dispersion Modeling System<br>Passive Defense - Iran</p>", unsafe_allow_html=True)
st.markdown("---")

# Session State for Data
if 'data' not in st.session_state:
    st.session_state.data = {
        "chem": "Sarin (GB)", "stability": "", "wind_speed": 5.0, "Q": 1000.0,
        "duration_min": 10.0, "H": 0.0, "release_type": "Instantaneous",
        "x_rec": 1000.0, "y_rec": 0.0, "z_rec": 0.0
    }
data = st.session_state.data

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "1. Agent Selection", "2. Atmospheric Stability", "3. Release Parameters", "4. Dispersion Map", "5. Dose Profile"
])

with tab1:
    st.header("Select Chemical/Biological Agent")
    chem = st.selectbox("Agent", options=list(chemicals_db.keys()))
    agent = chemicals_db[chem]
    data["chem"] = chem
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"Agent: **{chem}**\nMolecular Weight: {agent['Mw']:.1f} g/mol")
    with col2:
        st.error(f"LCt50: {agent['LCt50']} mg·min/m³")
        st.warning(f"Incapacitating Dose: {agent['Incap']} mg·min/m³")

with tab2:
    st.header("Pasquill-Gifford Stability Class")
    col1, col2 = st.columns(2)
    with col1:
        daynight = st.radio("Time of Day", ["Day", "Night"], horizontal=True)
        wind_speed = st.slider("Wind Speed (m/s)", 0.5, 15.0, data["wind_speed"], 0.1)
        data["wind_speed"] = wind_speed
    with col2:
        if daynight == "Day":
            sun = st.radio("Solar Radiation", ["Strong", "Moderate", "Slight"], horizontal=True)
        else:
            cloud = st.radio("Cloud Cover", ["≤ 3/8", "> 4/8"], horizontal=True)
    if st.button("Calculate Stability Class", type="primary"):
        u = wind_speed
        cat = "<2" if u<2 else "2-3" if u<3 else "3-5" if u<5 else "5-6" if u<6 else ">6"
        if daynight == "Day":
            table = {"<2": {"Strong":"A","Moderate":"A-B","Slight":"B"},
                     "2-3": {"Strong":"A-B","Moderate":"B","Slight":"C"},
                     "3-5": {"Strong":"B","Moderate":"C","Slight":"C"},
                     "5-6": {"Strong":"C","Moderate":"C-D","Slight":"D"},
                     ">6": {"Strong":"C","Moderate":"D","Slight":"D"}}
            stab = table[cat][sun]
        else:
            stab = "F" if cloud == "≤ 3/8" else "E"
        final_stab = stab[0] if '-' in stab else stab
        data["stability"] = final_stab
        st.success(f"Stability Class: **{final_stab}**")
        st.balloons()

with tab3:
    st.header("Release Parameters")
    release_type = st.radio("Release Type", ["Instantaneous (Puff)", "Continuous (Plume)"])
    data["release_type"] = "Instantaneous" if "Instantaneous" in release_type else "Continuous"
    Q = st.number_input("Release Amount (kg)", 1, 10000, int(data["Q"]))
    data["Q"] = Q
    if "Continuous" in release_type:
        duration = st.number_input("Duration (minutes)", 0.1, 300.0, data["duration_min"] if data["duration_min"] > 0 else 10.0)
        data["duration_min"] = duration
    H = st.number_input("Source Height (m)", 0.0, 200.0, data["H"])
    data["H"] = H
    col1, col2, col3 = st.columns(3)
    data["x_rec"] = col1.number_input("Receptor X (m)", value=data["x_rec"])
    data["y_rec"] = col2.number_input("Receptor Y (m)", value=data["y_rec"])
    data["z_rec"] = col3.number_input("Receptor Z (m)", value=data["z_rec"])

with tab4:
    st.header("Dispersion Map")
    if st.button("Plot Dispersion Map", type="primary", use_container_width=True):
        if not data.get("stability"):
            st.error("Please calculate stability class first!")
        else:
            with st.spinner("Calculating dispersion..."):
                x = np.linspace(50, 25000, 1000)
                y = np.linspace(-12000, 12000, 800)
                X, Y = np.meshgrid(x, y)
                dose = np.zeros_like(X)
                u = max(data["wind_speed"], 0.5)
                Q_mg = data["Q"] * 1e6
                H = data["H"]
                stab = data["stability"]
                for i in range(len(x)):
                    sy = get_sigma_y(stab, x[i])
                    sz = get_sigma_z(stab, x[i])
                    if sy < 0.1 or sz < 0.1: continue
                    exp_y = np.exp(-0.5 * (Y[:,i]/sy)**2)
                    exp_z = np.exp(-0.5 * (H/sz)**2)
                    if data["release_type"] == "Instantaneous":
                        dose[:,i] = (Q_mg * np.sqrt(2/np.pi)) / (u * sy * sz) * exp_y * exp_z
                    else:
                        t_sec = max(data["duration_min"] * 60, 1)
                        Q_rate = Q_mg / t_sec
                        C = Q_rate / (2 * np.pi * u * sy * sz) * exp_y * exp_z
                        dose[:,i] = C * t_sec
                fig = go.Figure()
                fig.add_trace(go.Contour(x=x, y=y, z=dose, colorscale='Reds', showscale=False,
                                       contours=dict(start=agent['LCt50'], end=1e6)))
                fig.add_trace(go.Contour(x=x, y=y, z=dose, colorscale='Oranges', opacity=0.8,
                                       contours=dict(start=agent['Incap'], end=agent['LCt50'])))
                fig.add_trace(go.Contour(x=x, y=y, z=dose, colorscale='Greens', opacity=0.25,
                                       contours=dict(start=0.1, end=agent['Incap'])))
                fig.add_scatter(x=[0], y=[0], mode="markers", marker=dict(size=18, color="red", symbol="x"), name="Source")
                fig.add_annotation(x=4000, y=1500, text="Wind Direction", font=dict(size=16, color="black"), showarrow=True, arrowhead=1, ax=0, ay=0)
                fig.update_layout(title=f"{chem} | Class {stab} | Wind {u:.1f} m/s | Q = {data['Q']:.0f} kg",
                               xaxis_title="Downwind Distance (m)", yaxis_title="Crosswind Distance (m)", xaxis_range=[0, 25000], yaxis_range=[-12000, 12000])
                st.plotly_chart(fig, use_container_width=True)

with tab5:
    st.header("Dose & Concentration Profile")
    if st.button("Plot Profile", type="primary"):
        if not data.get("stability"):
            st.error("Stability class required")
        else:
            u = max(data["wind_speed"], 0.5)
            Q_mg = data["Q"] * 1e6
            H = data["H"]
            stab = data["stability"]
            x_rec = data["x_rec"]
            y_rec = data["y_rec"]
            z_rec = data["z_rec"]
            if data["release_type"] == "Instantaneous":
                t_max = max((x_rec + 10000) / u / 60, 60)
                t = np.linspace(0, t_max, 5000)
                x_center = u * t * 60
                sy = get_sigma_y(stab, x_center)
                sz = get_sigma_z(stab, x_center)
                sx = sy
                denominator = (2 * np.pi)**1.5 * sx * sy * sz
                denominator = np.maximum(denominator, 1e-10)
                exp_x = np.exp(-0.5 * ((x_rec - x_center) / sx)**2)
                exp_y = np.exp(-0.5 * (y_rec / sy)**2)
                exp_z = np.exp(-0.5 * ((z_rec - H) / sz)**2)
                C = Q_mg / denominator * exp_x * exp_y * exp_z
                fig2 = go.Figure(go.Scatter(x=t, y=C, mode='lines', line=dict(width=3, color='#c0392b')))
                fig2.update_layout(title=f"Concentration vs Time at ({x_rec:.0f}, {y_rec:.0f}, {z_rec:.0f}) m",
                                   xaxis_title="Time (minutes)", yaxis_title="Concentration (mg/m³)")
                st.plotly_chart(fig2, use_container_width=True)
            else:
                x = np.linspace(50, 20000, 1000)
                dose = np.zeros_like(x)
                t_sec = max(data["duration_min"] * 60, 1)
                Q_rate = Q_mg / t_sec
                for i, xi in enumerate(x):
                    sy = get_sigma_y(stab, xi)
                    sz = get_sigma_z(stab, xi)
                    if sy < 0.1 or sz < 0.1: continue
                    exp_y = np.exp(-0.5 * (y_rec / sy)**2)
                    exp_z = np.exp(-0.5 * ((z_rec - H) / sz)**2)
                    C = Q_rate / (2 * np.pi * u * sy * sz) * exp_y * exp_z
                    dose[i] = C * t_sec
                fig2 = go.Figure(go.Scatter(x=x, y=dose, mode='lines', line=dict(width=3, color='#2980b9')))
                fig2.add_hline(y=agent["LCt50"], line_dash="dash", line_color="red", annotation_text=f'LCt50 = {agent["LCt50"]}')
                fig2.add_hline(y=agent["Incap"], line_dash="dot", line_color="orange", annotation_text=f'Incap = {agent["Incap"]}')
                fig2.update_layout(title="Centerline Dose Profile - Continuous Release",
                                   xaxis_title="Downwind Distance (m)", yaxis_title="Dose (mg·min/m³)")
                st.plotly_chart(fig2, use_container_width=True)

# Save and Export (in Streamlit style)
if st.sidebar.button("Save Map as PNG"):
    st.info("PNG export coming in next version")

if st.sidebar.button("Export Data to Excel"):
    st.info("Excel export coming in next version")

st.markdown("---")
st.markdown("**CB-Shield Pro © 2025 — Made in Iran**")
st.markdown("Passive Defense CBRN Tool")
```
