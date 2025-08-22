# NSFW Detector  

NSFW Detector adalah aplikasi **Python berbasis FastAPI** yang mampu mendeteksi apakah sebuah gambar mengandung konten NSFW (*Not Safe For Work*) atau tidak.  

## 🚀 Fitur Utama
- ✅ Menggunakan model HuggingFace: **Falconsai/nsfw_image_detection**  
- ✅ Mendukung **REST API** via FastAPI & Uvicorn  
- ✅ Sistem **cache berbasis hash** untuk mempercepat scan gambar yang sama  
- ✅ Output JSON berisi status, label, akurasi, dan waktu proses  
- ✅ Bisa dijalankan di **local, LAN, maupun public IP**  

Cocok untuk integrasi ke aplikasi lain (misalnya **bot, sistem moderasi, atau web service**).  

---

## ⚡ Install & Menjalankan  

### STEP 1  
Download Python versi terbaru (misalnya 3.13.7)  
👉 [Download Python](https://www.python.org/downloads/)  

### STEP 2  
Buat folder project dan masuk ke dalamnya:  
```bash
mkdir nsfw-detector
cd nsfw-detector
```

### STEP 3 (opsional, virtual environment)  
```bash
python -m venv venv
source venv/Scripts/activate   # Windows
```

### STEP 4  
Install dependensi:  
```bash
pip install torch torchvision torchaudio
pip install transformers pillow
pip install fastapi uvicorn[standard] requests
```

### STEP 5  
Jalankan script untuk deteksi langsung:  
```bash
python detect.py
```

### STEP 6 (opsional, jalankan versi API)  
```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```
