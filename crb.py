import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import datetime
import hashlib
from pathlib import Path

# ====================== سیستم لایسنس ۲۰ روزه — فقط خودت می‌تونی بسازی ======================
def generate_license(password: str):
    if password != "24434":  # ← رمز خودت رو عوض کن!
        st.error("رمز اشتباه است!")
        return
    
    expiry = (datetime.date.today() + datetime.timedelta(days=20)).strftime("%Y-%m-%d")
    secret = "IRAN-CBRN-DEFENSE-1404-TOPSECRET-2025"
    hash_code = hashlib.sha256(f"{expiry}{secret}".encode()).hexdigest()[:32]
    key = f"{expiry}|{hash_code}"
    
    Path("license.key").write_text(key)
    st.success("لایسنس ۲۰ روزه با موفقیت ساخته شد!")
    st.code(key)
    st.info("فایل license.key ذخیره شد — این فایل رو همراه app.py روی GitHub آپلود کن")
    st.balloons()

def check_license():
    if not Path("license.key").exists():
        return False, "فایل license.key موجود نیست"
    try:
        expiry, h = Path("license.key").read_text().strip().split("|")
        secret = "IRAN-CBRN-DEFENSE-1404-TOPSECRET-2025"
        if hashlib.sha256(f"{expiry}{secret}".encode()).hexdigest()[:32] != h:
            return False, "لایسنس نامعتبر یا تقلبی است"
        if datetime.date.today() > datetime.datetime.strptime(expiry, "%Y-%m-%d").date():
            return False, f"لایسنس منقضی شده — تاریخ انقضا: {expiry}"
        days = (datetime.datetime.strptime(expiry, "%Y-%m-%d").date() - datetime.date.today()).days
        return True, f"{days} روز باقی مانده"
    except:
        return False, "لایسنس خراب است"

# چک لایسنس
valid, message = check_license()
if not valid:
    st.error("نرم‌افزار قفل است!")
    st.warning(message)
    st.markdown("---")
    with st.expander("ساخت لایسنس جدید (فقط توسعه‌دهنده)", expanded=True):
        pw = st.text_input("رمز عبور", type="password")
        if st.button("ساخت لایسنس ۲۰ روزه"):
            generate_license(pw)
    st.stop()

st.sidebar.success(f"CB-Shield Pro\n{message}")

# ====================== پایگاه داده کامل ۶۵ عامل CBRN ======================
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
    "Cyanogen Chloride (CK)":        {"Mw": 61.5,  "LCt50": 11000, "Incap": 2500},
    "Arsine (SA)":                   {"Mw": 77.9,  "LCt50": 5000, "Incap": 500},
    "Phosgene (CG)":                 {"Mw": 98.9,  "LCt50": 3200, "Incap": 1600},
    "Diphosgene (DP)":               {"Mw": 197.8, "LCt50": 3200, "Incap": 800},
    "Chlorine (Cl2)":                {"Mw": 70.9,  "LCt50": 19000, "Incap": 3000},
    "Chloropicrin (PS)":             {"Mw": 164.4, "LCt50": 2000, "Incap": 400},
    "Perfluoroisobutylene (PFIB)":   {"Mw": 200.0, "LCt50": 300,  "Incap": 50},
    "BZ Agent":                      {"Mw": 337.4, "LCt50": 110000, "Incap": 20000},
    "Agent 15":                     {"Mw": 340.0, "LCt50": 100000, "Incap": 18000},
    "EA-3167":                      {"Mw": 350.0, "LCt50": 150000, "Incap": 25000},
    "CS Gas":                        {"Mw": 188.5, "LCt50": 60000, "Incap": 5},
    "CR Gas":                        {"Mw": 195.0, "LCt50": 60000, "Incap": 3},
    "CN Gas":                        {"Mw": 154.6, "LCt50": 8500,  "Incap": 20},
    "OC (Pepper Spray)":             {"Mw": 305.4, "LCt50": 100000, "Incap": 1},
    "PAVA":                         {"Mw": 293.4, "LCt50": 120000, "Incap": 2},
    "Adamsite (DM)":                 {"Mw": 277.6, "LCt50": 11000, "Incap": 150},
    "Ammonia":                       {"Mw": 17.0,  "LCt50": 5000, "Incap": 1500},
    "Methyl Isocyanate":             {"Mw": 57.1,  "LCt50": 300,  "Incap": 50},
    "Acrolein":                     {"Mw": 56.1,  "LCt50": 150,  "Incap": 20},
    "Formaldehyde (gas)":            {"Mw": 30.0,  "LCt50": 800,  "Incap": 100},
    "Hydrazine":                     {"Mw": 32.0,  "LCt50": 570,  "Incap": 100},
    "Bromine":                      {"Mw": 159.8, "LCt50": 1500, "Incap": 300},
    "Ricin":                        {"Mw": 64000, "LCt50": 3,     "Incap": 0.5},
    "Botulinum Toxin":              {"Mw": 150000, "LCt50": 0.001, "Incap": 0.0001},
    "Staph Enterotoxin B (SEB)":     {"Mw": 28354, "LCt50": 0.02, "Incap": 0.0003},
    "T-2 Mycotoxin":                {"Mw": 466.0, "LCt50": 200,  "Incap": 50},
    "Saxitoxin":                    {"Mw": 299.3, "LCt50": 0.01, "Incap": 0.002},
    "Tetrodotoxin":                  {"Mw": 319.3, "LCt50": 0.008, "Incap": 0.001},
    "Anthrax Spores":               {"Mw": 0,     "LCt50": 8000, "Incap": 2000},
    "Plague (Y. pestis)":           {"Mw": 0,     "LCt50": 100,  "Incap": 10},
    "Tularemia":                    {"Mw": 0,     "LCt50": 10,   "Incap": 1},
    "Q Fever":                      {"Mw": 0,     "LCt50": 10,   "Incap": 1},
    "Smallpox":                     {"Mw": 0,     "LCt50": 10,   "Incap": 1},
    "Ebola Virus":                   {"Mw": 0,     "LCt50": 1,    "Incap": 0.1},
    "Marburg Virus":                 {"Mw": 0,     "LCt50": 1,    "Incap": 0.1},
    "Brucellosis":                   {"Mw": 0,     "LCt50": 100,  "Incap": 10},
    "Glanders":                     {"Mw": 0,     "LCt50": 100,  "Incap": 10},
    "Melioidosis":                  {"Mw": 0,     "LCt50": 50,   "Incap": 5},
    "Rift Valley Fever":              {"Mw": 0,     "LCt50": 10,   "Incap": 1},
    "Hantavirus":                    {"Mw": 0,     "LCt50": 5,    "Incap": 0.5},
    "Nipah Virus":                  {"Mw": 0,     "LCt50": 2,    "Incap": 0.2},
}

# توابع سیگما
def get_sigma_y(stability, x):
    x = np.maximum(x, 1.0)
    params = {'A': 0.22, 'B': 0.16, 'C': 0.11, 'D': 0.08, 'E': 0.06, 'F': 0.04}
    return np.minimum(params.get(stability, 0.08) * x ** 0.9, 1000)

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

# تنظیمات صفحه
st.set_page_config(page_title="CB-Shield Pro - پدافند غیرعامل", layout="wide", page_icon="☣️")

st.markdown("""
<style>
    .big-font {font-size:60px !important; font-weight:bold; color:#8B0000; text-align:center; font-family:'Tahoma'}
    .header {font-size:28px; color:#006400; text-align:center;}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="big-font">CB-SHIELD PRO</p>', unsafe_allow_html=True)
st.markdown("<p class='header'>سامانه مدل‌سازی پراکندگی عوامل شیمیایی و بیولوژیکی<br>قرارگاه پدافند غیرعامل ایران</p>", unsafe_allow_html=True)
st.markdown("---")

# حالت‌های ذخیره شده
if 'data' not in st.session_state:
    st.session_state.data = {
        "chem": "Sarin (GB)", "stability": "", "wind_speed": 5.0, "Q": 1000.0,
        "duration_min": 10.0, "H": 0.0, "release_type": "Instantaneous",
        "x_rec": 1000.0, "y_rec": 0.0, "z_rec": 0.0
    }
data = st.session_state.data

# تب‌ها
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "۱. انتخاب عامل", "۲. پایداری جوی", "۳. پارامترهای رهاسازی", "۴. نقشه پراکندگی", "۵. پروفایل دوز"
])

with tab1:
    st.header("انتخاب عامل شیمیایی/بیولوژیکی")
    chem = st.selectbox("عامل", options=list(chemicals_db.keys()), index=0)
    agent = chemicals_db[chem]
    data["chem"] = chem
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"نام عامل: **{chem}**\nوزن مولکولی: {agent['Mw']:.1f} g/mol")
    with col2:
        st.error(f"LCt50: {agent['LCt50']} mg·min/m³")
        st.warning(f"دوز ناتوان‌کننده: {agent['Incap']} mg·min/m³")

with tab2:
    st.header("محاسبه کلاس پایداری پاسکیل-گیفورد")
    col1, col2 = st.columns(2)
    with col1:
        daynight = st.radio("زمان", ["روز", "شب"], horizontal=True)
        wind_speed = st.slider("سرعت باد (m/s)", 0.5, 15.0, data["wind_speed"], 0.1)
        data["wind_speed"] = wind_speed
    with col2:
        if daynight == "روز":
            sun = st.radio("شدت تابش خورشید", ["قوی", "متوسط", "ضعیف"], horizontal=True)
        else:
            cloud = st.radio("پوشش ابری", ["≤ ۳/۸", "> ۴/۸"], horizontal=True)
    if st.button("محاسبه کلاس پایداری", type="primary"):
        u = wind_speed
        cat = "<2" if u<2 else "2-3" if u<3 else "3-5" if u<5 else "5-6" if u<6 else ">6"
        if daynight == "روز":
            table = {"<2": {"قوی":"A","متوسط":"A-B","ضعیف":"B"},
                     "2-3": {"قوی":"A-B","متوسط":"B","ضعیف":"C"},
                     "3-5": {"قوی":"B","متوسط":"C","ضعیف":"C"},
                     "5-6": {"قوی":"C","متوسط":"C-D","ضعیف":"D"},
                     ">6": {"قوی":"C","متوسط":"D","ضعیف":"D"}}
            stab = table[cat][sun]
        else:
            stab = "F" if cloud == "≤ ۳/۸" else "E"
        final_stab = stab[0] if '-' in stab else stab
        data["stability"] = final_stab
        st.success(f"کلاس پایداری: **{final_stab}**")
        st.balloons()

with tab3:
    st.header("پارامترهای رهاسازی")
    release_type = st.radio("نوع رهاسازی", ["رهاسازی آنی (Puff)", "رهاسازی مداوم (Plume)"])
    data["release_type"] = "Instantaneous" if "آنی" in release_type else "Continuous"
    Q = st.number_input("مقدار رهاسازی (kg)", 1, 10000, int(data["Q"]))
    data["Q"] = Q
    if "مداوم" in release_type:
        duration = st.number_input("مدت زمان (دقیقه)", 0.1, 300.0, data["duration_min"] if data["duration_min"] > 0 else 10.0)
        data["duration_min"] = duration
    H = st.number_input("ارتفاع منبع (m)", 0.0, 200.0, data["H"])
    data["H"] = H
    col1, col2, col3 = st.columns(3)
    data["x_rec"] = col1.number_input("X گیرنده (m)", value=data["x_rec"])
    data["y_rec"] = col2.number_input("Y گیرنده (m)", value=data["y_rec"])
    data["z_rec"] = col3.number_input("Z گیرنده (m)", value=data["z_rec"])

with tab4:
    st.header("نقشه پراکندگی")
    if st.button("رسم نقشه پراکندگی", type="primary", use_container_width=True):
        if not data.get("stability"):
            st.error("ابتدا کلاس پایداری را محاسبه کنید!")
        else:
            with st.spinner("در حال محاسبه..."):
                x = np.linspace(50, 30000, 300)
                y = np.linspace(-15000, 15000, 300)
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
                fig.add_trace(go.Contour(x=x/1000, y=y/1000, z=dose, colorscale='Reds', showscale=False,
                                       contours=dict(start=agent['LCt50'], end=1e6, size=1000)))
                fig.add_trace(go.Contour(x=x/1000, y=y/1000, z=dose, colorscale='Oranges', opacity=0.7,
                                       contours=dict(start=agent['Incap'], end=agent['LCt50'])))
                fig.add_trace(go.Contour(x=x/1000, y=y/1000, z=dose, colorscale='Greens', opacity=0.3,
                                       contours=dict(start=0.1, end=agent['Incap'])))
                fig.add_scatter(x=[0], y=[0], mode="markers", marker=dict(size=16, color="black", symbol="x"), name="منبع")
                fig.update_layout(title=f"{chem} | کلاس {stab} | باد {u:.1f} m/s | Q={Q} kg",
                               xaxis_title="فاصله در جهت باد (km)", yaxis_title="فاصله عرضی (km)")
                st.plotly_chart(fig, use_container_width=True)

with tab5:
    st.header("پروفایل دوز و غلظت")
    if st.button("رسم نمودار پروفایل", type="primary"):
        if not data.get("stability"):
            st.error("کلاس پایداری مشخص نیست!")
        else:
            x_profile = np.linspace(50, 20000, 500)
            dose_profile = np.zeros_like(x_profile)
            u = max(data["wind_speed"], 0.5)
            Q_mg = data["Q"] * 1e6
            H = data["H"]
            stab = data["stability"]
            y_rec = data["y_rec"]
            z_rec = data["z_rec"]
            if data["release_type"] == "Continuous" and data["duration_min"] > 0:
                t_sec = data["duration_min"] * 60
                Q_rate = Q_mg / t_sec
                for i, xi in enumerate(x_profile):
                    sy = get_sigma_y(stab, xi)
                    sz = get_sigma_z(stab, xi)
                    if sy < 0.1 or sz < 0.1: continue
                    exp_y = np.exp(-0.5 * (y_rec / sy)**2)
                    exp_z = np.exp(-0.5 * ((z_rec - H) / sz)**2)
                    C = Q_rate / (2 * np.pi * u * sy * sz) * exp_y * exp_z
                    dose_profile[i] = C * t_sec
                fig2 = go.Figure()
                fig2.add_trace(go.Scatter(x=x_profile/1000, y=dose_profile, mode='lines', line=dict(width=4), name='دوز'))
                fig2.add_hline(y=agent['LCt50'], line_dash="dash", line_color="red", annotation_text="LCt50")
                fig2.add_hline(y=agent['Incap'], line_dash="dot", line_color="orange", annotation_text="Incap")
                fig2.update_layout(title="پروفایل دوز در محور باد", xaxis_title="فاصله (km)", yaxis_title="دوز (mg·min/m³)")
                st.plotly_chart(fig2, use_container_width=True)
            else:
                st.info("برای رهاسازی آنی، نمودار لحظه‌ای در نسخه بعدی اضافه می‌شود")

st.markdown("---")
st.markdown("**CB-Shield Pro © ۱۴۰۴ — محصول دانش‌بنیان بومی ایران**")
st.markdown("توسعه‌دهنده: [اسم شما] — با افتخار برای ایران")
