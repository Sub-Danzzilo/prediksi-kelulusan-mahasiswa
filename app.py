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

with col2:
    st.subheader("📚 Nilai Akademik")
    ips_1 = st.number_input("IPS Semester 1", min_value=0.00, max_value=4.00, value=0.00, step=0.01)
    ips_2 = st.number_input("IPS Semester 2", min_value=0.00, max_value=4.00, value=0.00, step=0.01)
    ips_3 = st.number_input("IPS Semester 3", min_value=0.00, max_value=4.00, value=0.00, step=0.01)
    ips_4 = st.number_input("IPS Semester 4", min_value=0.00, max_value=4.00, value=0.00, step=0.01)

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
