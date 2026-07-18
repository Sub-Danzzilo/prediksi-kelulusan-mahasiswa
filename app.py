# pyrefly: ignore [missing-import]
import streamlit as st
import pandas as pd
import pickle
import os
import sklearn

# --- Page Configuration ---
st.set_page_config(
    page_title="Prediksi Kelulusan Mahasiswa",
    page_icon="🎓",
    layout="centered"
)

st.title("🎓 Deteksi Dini Kelulusan Mahasiswa")
st.markdown("Aplikasi untuk memprediksi probabilitas kelulusan mahasiswa pada Semester 4.")
st.divider()

# --- Load Model ---
@st.cache_resource
def load_model():
    model_path = os.path.join("models", "model.pkl")
    with open(model_path, "rb") as f:
        model = pickle.load(f)
    return model

try:
    model = load_model()
except Exception as e:
    st.error(f"Gagal memuat model: {e}")
    st.stop()

# --- UI Layout: Two Columns ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("👤 Data Diri")
    jenis_kelamin = st.selectbox("Jenis Kelamin", options=["Laki-laki", "Perempuan"])
    status_mahasiswa = st.selectbox("Status Mahasiswa", options=["Tidak Bekerja", "Bekerja"])
    status_nikah = st.selectbox("Status Nikah", options=["Belum Menikah", "Menikah"])
    umur = st.number_input("Umur", min_value=17, max_value=40, value=20, step=1)

def clamp_ips(key):
    val = str(st.session_state[key])
    val = val.replace("+", "").replace(",", ".")
    try:
        f_val = float(val)
        if f_val < 0.0:
            st.session_state[key] = "0.00"
        elif f_val > 4.0:
            st.session_state[key] = "4.00"
        else:
            st.session_state[key] = f"{f_val:.2f}"
    except ValueError:
        st.session_state[key] = "0.00"

for i in range(1, 5):
    if f"ips_{i}" not in st.session_state:
        st.session_state[f"ips_{i}"] = "0.00"

with col2:
    st.subheader("📚 Nilai Akademik")
    ips_1_str = st.text_input("IPS Semester 1", key="ips_1", on_change=clamp_ips, args=("ips_1",))
    ips_2_str = st.text_input("IPS Semester 2", key="ips_2", on_change=clamp_ips, args=("ips_2",))
    ips_3_str = st.text_input("IPS Semester 3", key="ips_3", on_change=clamp_ips, args=("ips_3",))
    ips_4_str = st.text_input("IPS Semester 4", key="ips_4", on_change=clamp_ips, args=("ips_4",))
    
    ips_1 = float(ips_1_str) if ips_1_str else 0.0
    ips_2 = float(ips_2_str) if ips_2_str else 0.0
    ips_3 = float(ips_3_str) if ips_3_str else 0.0
    ips_4 = float(ips_4_str) if ips_4_str else 0.0

st.divider()

# --- Execution Button ---
if st.button("Prediksi Sekarang!", use_container_width=True, type="primary"):
    # 1. Transformasi Data (Preprocessing)
    jk_val = 1 if jenis_kelamin == "Laki-laki" else 0
    sm_val = 1 if status_mahasiswa == "Bekerja" else 0
    sn_val = 1 if status_nikah == "Menikah" else 0
    
    # 2. Konstruksi DataFrame
    # Menggunakan nama kolom berhuruf kapital sesuai format training
    data = {
        "JENIS_KELAMIN": [jk_val],
        "STATUS_MAHASISWA": [sm_val],
        "UMUR": [umur],
        "STATUS_NIKAH": [sn_val],
        "IPS_1": [ips_1],
        "IPS_2": [ips_2],
        "IPS_3": [ips_3],
        "IPS_4": [ips_4]
    }
    
    df = pd.DataFrame(data)
    
    # 3. Prediksi Model
    try:
        prediction = model.predict(df)[0]
        
        # 4. Output UI
        if prediction == 1:
            st.success("LULUS TEPAT WAKTU")
            st.balloons()
        else:
            st.error("LULUS TERLAMBAT")
            
    except Exception as e:
        st.error(f"Terjadi kesalahan saat melakukan prediksi: {e}")
