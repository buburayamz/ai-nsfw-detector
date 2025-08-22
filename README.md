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

## ⚠️ Peringatan Konten NSFW

Di dalam repository ini terdapat file contoh **`1.jpg`** yang **mengandung konten NSFW (Not Safe For Work)**.  
Namun file tersebut **sudah disensor** dan hanya digunakan sebagai **contoh input untuk keperluan pengujian deteksi NSFW**.  

🔹 Mohon **berhati-hati** saat membuka file ini.  
🔹 File ini **tidak dimaksudkan untuk konsumsi pribadi**, melainkan hanya untuk **tujuan teknis (testing / penelitian)**.  
🔹 Jika tidak nyaman, silakan **abaikan atau hapus file `1.jpg`** dari direktori lokal Anda.  

---

## ⚡ Install & Menjalankan  

### STEP 1 - (Windows)  
Download Python versi terbaru (misalnya 3.13.7)  
👉 [Download Python For Windows](https://www.python.org/downloads/)  

Download Git Bash versi terbaru
👉 [Download Git Bash For Windows](https://git-scm.com/downloads/win)  

### STEP 2  
Clone project dan masuk ke dalamnya (pake Terminal atau Git Bash):  
```bash
git clone https://github.com/buburayamz/ai-nsfw-detector
cd ai-nsfw-detector
```

### STEP 3 (opsional, virtual environment)  
```bash
python -m venv venv
source venv/Scripts/activate   # Windows
source venv/bin/activate  # Ubuntu / Linux / macOS
```

### STEP 4  
Install dependensi:  
```bash
pip install torch torchvision torchaudio
pip install transformers pillow
pip install fastapi uvicorn[standard] requests
```

### STEP 5  
Jalankan script untuk deteksi langsung :  
```bash
python detect.py 1.jpg
```

### STEP 6 (opsional, jalankan versi API)  
```bash
python run.py --host 0.0.0.0 --port 8080
```
