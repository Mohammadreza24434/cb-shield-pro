import streamlit as st
import numpy as np
import plotly.graph_objects as go
import datetime
import hashlib
from pathlib import Path

# ====================== Fast & Secure 30-Day License ======================
def license_system():
    license_file = Path("license.key")
    DEV_PASSWORD = "24434"  # فقط تو این رمز رو عوض کن!

    if license_file.exists():
        try:
            expiry_str, code_hash = license_file.read_text().strip().split("|")
            expiry = datetime.datetime.strptime(expiry_str, "%Y-%m-%d").date()
            expected = hashlib.md5(f"{expiry_str}{DEV_PASSWORD}".encode()).hexdigest()[:8]
            if code_hash == expected and datetime.date.today() <= expiry:
                st.session_state.logged_in = True
                st.session_state.days_left = (expiry - datetime.date.today()).days
                return True
        except:
            pass

    st.markdown("<h1 style='text-align:center;color:#8B0000;font-size:60px;'>CB-SHIELD PRO</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center;color:#2c3e50;'>Advanced CBRN Dispersion Modeling</h3>", unsafe_allow_html=True)
    st.markdown("---")
    st.error("License Required")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        code = st.text_input("Enter License Code", type="password", placeholder="2025-12-15|abc123")
        if st.button("Activate", type="primary", use_container_width=True):
            if "|" in code and len(code.split("|")) == 2:
                expiry_str, code_hash = code.split("|")
                try:
                    expiry = datetime.datetime.strptime(expiry_str, "%Y-%m-%d").date()
                    expected = hashlib.md5(f"{expiry_str}{DEV_PASSWORD}".encode()).hexdigest()[:8]
                    if code_hash == expected and datetime.date.today() <= expiry:
                        license_file.write_text(code)
                        st.success(f"Access Granted! {st.session_state.days_left} days left")
                        st.session_state.logged_in = True
                        st.rerun()
                    else:
                        st.error("Invalid or expired license")
                except:
                    st.error("Wrong format")
            else:
                st.error("Use format: YYYY-MM-DD|xxxxxx")

        with st.expander("Developer: Generate 30-Day License"):
            pwd = st.text_input("Password", type="password")
            if st.button("Generate"):
                if pwd == DEV_PASSWORD:
                    expiry = (datetime.date.today() + datetime.timedelta(days=30)).strftime("%Y-%m-%d")
                    short_hash = hashlib.md5(f"{expiry}{DEV_PASSWORD}".encode()).hexdigest()[:8]
                    license_code = f"{expiry}|{short_hash}"
                    st.code(license_code)
                    st.success("30-day license ready!")
                else:
                    st.error("Wrong password")

    st.stop()

license_system()

# Logout
if st.sidebar.button("Logout", type="secondary"):
    if Path("license.key").exists():
        Path("license.key").unlink()
    st.session_state.clear()
    st.rerun()

st.sidebar.success(f"Active — {st.session_state.days_left} days")

# ====================== 65 CBRN Agents ======================
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

# Ultra-fast sigma (cached)
@st.cache_data
def get_sigma_y(stability, x):
    x = np.maximum(x, 1.0)
    p = {'A':0.22,'B':0.16,'C':0.11,'D':0.08,'E':0.06,'F':0.04}
    return np.minimum(p.get(stability,0.08)*x**0.9,1000)

@st.cache_data
def get_sigma_z(stability, x):
    x = np.maximum(x, 1.0)
    if stability == 'A':
        return np.where(x<100,0.20*x,np.where(x<500,0.24*x**0.75,0.15*x**0.80))
    p = {'B':0.12,'C':0.08,'D':0.06,'E':0.03,'F':0.016}
    e = {'B':1.0,'C':0.90,'D':0.85,'E':0.75,'F':0.70}
    return p.get(stability,0.06)*x**e.get(stability,0.85)

# Page
st.set_page_config(page_title="CB-Shield Pro", layout="wide", page_icon="☣️")
st.markdown("<h1 style='text-align:center;color:#8B0000;'>CB-SHIELD PRO</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center;color:#2c3e50;'>CBRN Dispersion Modeling System</h3>", unsafe_allow_html=True)
st.markdown("---")

if 'data' not in st.session_state:
    st.session_state.data = {"chem":"Sarin (GB)","stability":"","wind_speed":5.0,"Q":1000.0,"duration_min":10.0,"H":0.0,"release_type":"Instantaneous","x_rec":1000,"y_rec":0,"z_rec":0}
data = st.session_state.data

tab1,tab2,tab3,tab4,tab5 = st.tabs(["Agent","Stability","Release","Map","Profile"])

with tab1:
    st.header("Agent Selection")
    chem = st.selectbox("Agent", list(chemicals_db.keys()))
    agent = chemicals_db[chem]
    data["chem"] = chem
    st.info(f"**{chem}** | MW: {agent['Mw']:.1f}")
    st.error(f"LCt50: {agent['LCt50']}")
    st.warning(f"Incap: {agent['Incap']}")

with tab2:
    st.header("Stability Class")
    time = st.radio("Time", ["Day","Night"], horizontal=True)
    wind = st.slider("Wind (m/s)",0.5,15.0,data["wind_speed"],0.1)
    data["wind_speed"] = wind
    if time=="Day": solar = st.radio("Solar",["Strong","Moderate","Slight"])
    else: cloud = st.radio("Cloud",["≤3/8",">4/8"])
    if st.button("Calculate"):
        u = wind
        cat = "A" if u<2 else "B" if u<3 else "C" if u<5 else "D" if u<6 else "E"
        stab = {"A":{"Strong":"A","Moderate":"A-B","Slight":"B"},
                "B":{"Strong":"A-B","Moderate":"B","Slight":"C"},
                "C":{"Strong":"B","Moderate":"C","Slight":"C"},
                "D":{"Strong":"C","Moderate":"C-D","Slight":"D"},
                "E":{"Strong":"C","Moderate":"D","Slight":"D"}}[cat][solar] if time=="Day" else ("F" if cloud=="≤3/8" else "E")
        data["stability"] = stab[0] if '-' in stab else stab
        st.success(f"Class: **{data['stability']}**")

with tab3:
    st.header("Release Parameters")
    rtype = st.radio("Type",["Instantaneous","Continuous"])
    data["release_type"] = rtype
    Q = st.number_input("Amount (kg)",1,10000,int(data["Q"]))
    data["Q"] = Q
    if rtype=="Continuous":
        dur = st.number_input("Duration (min)",0.1,300.0,data["duration_min"])
        data["duration_min"] = dur
    H = st.number_input("Height (m)",0.0,200.0,data["H"])
    data["H"] = H
    c1,c2,c3 = st.columns(3)
    data["x_rec"] = c1.number_input("X",value=data["x_rec"])
    data["y_rec"] = c2.number_input("Y",value=data["y_rec"])
    data["z_rec"] = c3.number_input("Z",value=data["z_rec"])

with tab4:
    st.header("Dispersion Map")
    if st.button("Plot", type="primary"):
        if not data.get("stability"):
            st.error("Calculate stability first")
        else:
            with st.spinner("Fast calculation..."):
                x = np.linspace(100,25000,350)
                y = np.linspace(-10000,10000,350)
                X,Y = np.meshgrid(x,y)
                dose = np.zeros_like(X)
                u = max(data["wind_speed"],0.5)
                Q_mg = data["Q"]*1e6
                H = data["H"]
                stab = data["stability"]
                sy = get_sigma_y(stab,x)
                sz = get_sigma_z(stab,x)
                for i in range(len(x)):
                    if sy[i]<0.1 or sz[i]<0.1: continue
                    ey = np.exp(-0.5*(Y[:,i]/sy[i])**2)
                    ez = np.exp(-0.5*(H/sz[i])**2)
                    if data["release_type"]=="Instantaneous":
                        dose[:,i] = (Q_mg*np.sqrt(2/np.pi))/(u*sy[i]*sz[i])*ey*ez
                    else:
                        t = max(data["duration_min"]*60,1)
                        C = (Q_mg/t)/(2*np.pi*u*sy[i]*sz[i])*ey*ez
                        dose[:,i] = C*t
                fig = go.Figure()
                fig.add_trace(go.Contour(x=x/1000,y=y/1000,z=dose,colorscale='Reds',showscale=False,
                                       contours=dict(start=agent['LCt50'],end=1e6,size=500)))
                fig.add_trace(go.Contour(x=x/1000,y=y/1000,z=dose,colorscale='Oranges',opacity=0.7,
                                       contours=dict(start=agent['Incap'],end=agent['LCt50'])))
                fig.add_trace(go.Contour(x=x/1000,y=y/1000,z=dose,colorscale='Greens',opacity=0.3,
                                       contours=dict(start=0.1,end=agent['Incap'])))
                fig.add_scatter(x=[0],y=[0],mode="markers",marker=dict(size=16,color="black",symbol="x"))
                fig.update_layout(title=f"{chem} | Class {stab} | Wind {u:.1f} m/s",xaxis_title="km",yaxis_title="km")
                st.plotly_chart(fig,use_container_width=True)

with tab5:
    st.header("Dose Profile")
    if st.button("Plot"):
        if not data.get("stability"):
            st.error("Stability required")
        else:
            x = np.linspace(50,20000,500)
            dose = np.zeros_like(x)
            u = max(data["wind_speed"],0.5)
            Q_mg = data["Q"]*1e6
            H = data["H"]
            stab = data["stability"]
            y,z = data["y_rec"],data["z_rec"]
            t = max(data["duration_min"]*60,1) if data["release_type"]=="Continuous" else 1
            Q_rate = Q_mg/t
            for i,xi in enumerate(x):
                sy = get_sigma_y(stab,xi)
                sz = get_sigma_z(stab,xi)
                if sy<0.1 or sz<0.1: continue
                dose[i] = Q_rate/(2*np.pi*u*sy*sz)*np.exp(-0.5*(y/sy)**2)*np.exp(-0.5*((z-H)/sz)**2)*t
            fig = go.Figure(go.Scatter(x=x,y=dose,mode='lines',line=dict(width=3,color='#2980b9')))
            fig.add_hline(y=agent["LCt50"],line_dash="dash",line_color="red")
            fig.add_hline(y=agent["Incap"],line_dash="dot",line_color="orange")
            fig.update_layout(title="Centerline Dose",xaxis_title="Distance (m)",yaxis_title="Dose (mg·min/m³)")
            st.plotly_chart(fig,use_container_width=True)

st.markdown("**CB-Shield Pro © 2025 — Made in Iran**")
