import hashlib
import os
import requests
import socket
import time
from fastapi import FastAPI, Query
from transformers import AutoImageProcessor, AutoModelForImageClassification
from PIL import Image
import torch
import torch.nn.functional as F
from io import BytesIO

app = FastAPI()
CACHE_FILE = "sudah_pernah_cek.txt"

# --- fungsi buat hash file ---
def get_bytes_hash(content, algo="md5"):
    h = hashlib.new(algo)
    h.update(content)
    return h.hexdigest()

# --- load cache ---
cache = {}
if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            file_hash, label, conf = line.split(",")
            cache[file_hash] = (label, conf)

# --- load model sekali saja ---
processor = AutoImageProcessor.from_pretrained(
    "Falconsai/nsfw_image_detection",
    use_fast=True
)
model = AutoModelForImageClassification.from_pretrained("Falconsai/nsfw_image_detection")
model.eval()

@app.on_event("startup")
def startup_event():
    # Ambil host & port dari ENV (fallback ke default)
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", 8000))

    sample_path = "/cek_nsfw?url=https://example.com/foto.jpg"

    # local url
    local_url = f"http://127.0.0.1:{port}{sample_path}"

    # lan ip url
    lan_ip = socket.gethostbyname(socket.gethostname())
    lan_url = f"http://{lan_ip}:{port}{sample_path}"

    # public ip url
    try:
        public_ip = requests.get("https://api.ipify.org").text.strip()
        public_url = f"http://{public_ip}:{port}{sample_path}"
    except:
        public_url = "(gagal ambil IP publik)"

    print("\n🚀 NSFW Detector API is running!")
    print(f"   Local URL   : {local_url}")
    print(f"   Network URL : {lan_url}")
    print(f"   Public URL  : {public_url}\n")

@app.get("/cek_nsfw")
def cek_nsfw(url: str = Query(..., description="URL gambar untuk dicek")):
    start_time = time.perf_counter()
    try:
        # download gambar
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        img_bytes = resp.content

        # hash konten gambar
        file_hash = get_bytes_hash(img_bytes)

        # cek cache
        if file_hash in cache:
            label, conf = cache[file_hash]
            elapsed = (time.perf_counter() - start_time)  # detik float
            elapsed_str = f"{elapsed:.1f}".replace(".", ",") + " Detik"
            print(f"[CACHE] {url} → {label} ({conf}%) in {elapsed_str}")
            return {
                "status": True,
                "message": "cache foto",
                "data": {
                    "url": url,
                    "hasil": label,
                    "akurasi": float(conf),
                    "waktu_proses": elapsed_str
                }
            }

        # convert ke PIL
        image = Image.open(BytesIO(img_bytes))

        # siapkan input
        inputs = processor(images=image, return_tensors="pt")

        # prediksi
        with torch.no_grad():
            outputs = model(**inputs)

        logits = outputs.logits
        predicted_class_id = logits.argmax(-1).item()
        label = model.config.id2label[predicted_class_id]

        probs = F.softmax(logits, dim=-1)
        confidence = probs[0][predicted_class_id].item() * 100

        # simpan ke cache
        with open(CACHE_FILE, "a") as f:
            f.write(f"{file_hash},{label},{confidence:.2f}\n")
        cache[file_hash] = (label, f"{confidence:.2f}")

        elapsed = (time.perf_counter() - start_time)
        elapsed_str = f"{elapsed:.1f}".replace(".", ",") + " Detik"
        print(f"[SCAN] {url} → {label} ({round(confidence,2)}%) in {elapsed_str}")
        return {
            "status": True,
            "message": "fresh foto scan",
            "data": {
                "url": url,
                "hasil": label,
                "akurasi": round(confidence, 2),
                "waktu_proses": elapsed_str
            }
        }

    except Exception as e:
        elapsed = (time.perf_counter() - start_time)
        elapsed_str = f"{elapsed:.1f}".replace(".", ",") + " Detik"
        print(f"[ERROR] {url} → {str(e)} in {elapsed_str}")
        return {
            "status": False,
            "message": str(e),
            "data": {
                "url": url,
                "hasil": None,
                "akurasi": None,
                "waktu_proses": elapsed_str
            }
        }
