# Product Requirements Document (PRD): Streamlit Web App

## 1. Tujuan Produk

Aplikasi berbasis web (*Dashboard*) yang digunakan sebagai *Rapid Prototyping* untuk memvisualisasikan model *Machine Learning* (**Deteksi Dini Kelulusan Mahasiswa Pada Semester 4**). Aplikasi ini memungkinkan tim *Data Science* untuk menguji model secara interaktif melalui *browser* tanpa perlu memikirkan arsitektur *backend* yang rumit.

## 2. Target Pengguna

- Tim Internal (Data Scientist, Analyst) untuk *testing* prediksi model.
- *Stakeholder* (Dosen/Universitas) untuk melihat purwarupa logika AI sebelum diintegrasikan secara masif.

## 3. Spesifikasi UI/UX (Antarmuka)

Desain antarmuka dibuat menggunakan *layouting* dua kolom agar terlihat padat dan profesional.

**Kolom Kiri (Data Diri):**

- `Jenis Kelamin`: Input *Dropdown* (Pilihan: "Laki-laki", "Perempuan").
- `Status Mahasiswa`: Input *Dropdown* (Pilihan: "Tidak Bekerja", "Bekerja").
- `Status Nikah`: Input *Dropdown* (Pilihan: "Belum Menikah", "Menikah").
- `Umur`: Input *Number* / Ketik Angka (Batasan: Min 17, Max 40, Default 20).

**Kolom Kanan (Nilai Akademik):**

- `IPS Semester 1`: Input *Number* / Ketik Angka (Batasan: 0.00 - 4.00).
- `IPS Semester 2`: Input *Number* / Ketik Angka (Batasan: 0.00 - 4.00).
- `IPS Semester 3`: Input *Number* / Ketik Angka (Batasan: 0.00 - 4.00).
- `IPS Semester 4`: Input *Number* / Ketik Angka (Batasan: 0.00 - 4.00).

**Tombol Eksekusi:**

- Tombol lebar penuh (Use Container Width) bertuliskan **"Prediksi Sekarang!"**.

## 4. Alur Logika Sistem (Data Flow)

1. **Penerimaan Input:** Sistem menerima *string* (teks) dari pilihan pengguna di UI.
2. **Transformasi Data (Preprocessing):**
   - "Laki-laki" ➔ `1`, "Perempuan" ➔ `0`.
   - "Bekerja" ➔ `1`, "Tidak Bekerja" ➔ `0`.
   - "Menikah" ➔ `1`, "Belum Menikah" ➔ `0`.
3. **Konstruksi DataFrame:** Data dibentuk menjadi satu baris `pandas.DataFrame` dengan nama kolom berhuruf kapital (menyesuaikan format *training*).
4. **Prediksi Model:** `model.pkl` menerima *DataFrame* dan mengembalikan angka `0` atau `1`.
5. **Output UI:** 
   - Jika `1`: Tampilkan teks sukses berwarna hijau ("LULUS TEPAT WAKTU") dan efek balon terbang.
   - Jika `0`: Tampilkan peringatan berwarna merah ("LULUS TERLAMBAT").

## 5. Deployment & Version Control

- **Platform:** Streamlit Community Cloud.
- **Dependencies:** `streamlit`, `pandas`, `scikit-learn` (tercantum di *root* `requirements.txt`).
- **File Entry Point:** `app.py`.
- **Version Control (Git):** Dilarang keras mengunggah folder *Virtual Environment* (`venv/`, `env/`) atau *cache* Python (`__pycache__/`) ke dalam repositori. Semua pengecualian ini sudah diatur secara otomatis di dalam file `.gitignore` tingkat *root*.
