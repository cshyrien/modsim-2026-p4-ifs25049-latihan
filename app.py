import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

st.set_page_config(page_title="Simulasi Tangki Air", layout="wide")

# =========================
# HEADER
# =========================

st.title("💧 Simulasi Kontinu Sistem Tangki Air")

st.write(
"""
Aplikasi ini mensimulasikan sistem tangki air dengan aliran masuk dan keluar.
Ubah parameter di sidebar untuk melihat perubahan ketinggian air secara real-time.
"""
)

st.success("✅ Simulasi berhasil dijalankan!")

# =========================
# SIDEBAR INPUT
# =========================

st.sidebar.header("Parameter Sistem")

radius = st.sidebar.slider("Radius tangki (m)", 0.5, 3.0, 1.0)
height_max = st.sidebar.slider("Tinggi maksimum tangki (m)", 1.0, 5.0, 3.0)

Q_in = st.sidebar.slider("Debit masuk Qin (m³/menit)", 0.0, 1.0, 0.5)
Q_out = st.sidebar.slider("Debit keluar Qout (m³/menit)", 0.0, 1.0, 0.2)

area = np.pi * radius**2

# =========================
# MODEL
# =========================

def water_tank_model(t, h):
    dhdt = (Q_in - Q_out) / area

    if h[0] >= height_max and dhdt > 0:
        dhdt = 0

    if h[0] <= 0 and dhdt < 0:
        dhdt = 0

    return [dhdt]

# =========================
# SIMULASI
# =========================

t_eval = np.linspace(0,60,200)

solution = solve_ivp(
    water_tank_model,
    [0,60],
    [0],
    t_eval=t_eval
)

time = solution.t
height = solution.y[0]

# =========================
# ANALISIS
# =========================

volume_max = area * height_max
time_fill = volume_max / Q_in if Q_in>0 else 0
time_empty = volume_max / Q_out if Q_out>0 else 0
height_avg = np.mean(height)

# =========================
# METRIC BOX (kayak gambar)
# =========================

col1,col2,col3,col4 = st.columns(4)

col1.metric("Waktu Tangki Penuh", f"{time_fill:.1f} menit")
col2.metric("Volume Maksimum", f"{volume_max:.2f} m³")
col3.metric("Debit Masuk", f"{Q_in:.2f} m³/min")
col4.metric("Debit Keluar", f"{Q_out:.2f} m³/min")

col5,col6,col7,col8 = st.columns(4)

col5.metric("Tinggi Maks Tangki", f"{height_max:.1f} m")
col6.metric("Rata-rata Tinggi Air", f"{height_avg:.2f} m")
col7.metric("Radius Tangki", f"{radius:.2f} m")
col8.metric("Luas Penampang", f"{area:.2f} m²")

# =========================
# TABS (kayak yang di gambar)
# =========================

tab1,tab2,tab3 = st.tabs(["📈 Profil Ketinggian", "📊 Analisis", "📂 Data"])

# ===== TAB 1 =====

with tab1:

    st.subheader("Profil Ketinggian Air")

    fig, ax = plt.subplots()

    ax.plot(time,height)
    ax.axhline(height_max, linestyle="--")

    ax.set_xlabel("Waktu")
    ax.set_ylabel("Ketinggian Air")
    ax.grid()

    st.pyplot(fig)

# ===== TAB 2 =====

with tab2:

    st.write("### Analisis Sistem")

    if Q_in > Q_out:
        st.info("Air dalam tangki akan meningkat seiring waktu.")
    elif Q_in == Q_out:
        st.info("Sistem berada pada kondisi stabil.")
    else:
        st.warning("Air dalam tangki akan berkurang.")

# ===== TAB 3 =====

with tab3:

    st.write("### Data Simulasi")

    st.dataframe({
        "Waktu": time,
        "Ketinggian Air": height
    })