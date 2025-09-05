# FoodPrint-Forecast

## Sistem Prediksi Limbah Pangan Rumah Tangga

FoodPrint Forecast adalah sistem inovatif yang memprediksi limbah pangan rumah tangga menggunakan model Prophet (Python) yang di-training dari foto isi kulkas pengguna. Sistem ini memberikan resep otomatis untuk bahan yang hampir basi dan menghitung potensi emisi yang dihindarkan, dengan leaderboard komunitas.

## Fitur Utama

- Prediksi limbah pangan berdasarkan foto isi kulkas
- Rekomendasi resep untuk bahan yang akan kadaluarsa
- Perhitungan emisi karbon yang berhasil dihindari
- Leaderboard komunitas untuk mendorong partisipasi

## Teknologi yang Digunakan

- Python dengan library Prophet untuk prediksi time series
- OpenCV dan TensorFlow untuk pengenalan gambar
- Flask untuk backend API
- HTML/CSS/JavaScript untuk antarmuka pengguna

## Instalasi

1. Clone repository ini
2. Install dependencies: `pip install -r requirements.txt`
3. Jalankan aplikasi: `python src/main.py`

## Penggunaan

1. Upload foto isi kulkas Anda
2. Sistem akan menganalisis dan memprediksi potensi limbah
3. Dapatkan rekomendasi resep untuk mencegah pemborosan
4. Lihat dampak lingkungan dari tindakan Anda