import hashlib
import os
import sys
from transformers import AutoImageProcessor, AutoModelForImageClassification
from PIL import Image
import torch
import torch.nn.functional as F

CACHE_FILE = "sudah_pernah_cek.txt"

# --- fungsi buat hash file ---
def get_file_hash(path, algo="md5"):
    h = hashlib.new(algo)
    with open(path, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

# --- cek argumen ---
if len(sys.argv) < 2:
    print("❌ Usage: python detect.py <nama_file_gambar>")
    sys.exit(1)

img_path = sys.argv[1]

if not os.path.exists(img_path):
    print(f"❌ File '{img_path}' tidak ditemukan.")
    sys.exit(1)

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

# --- hash file gambar ---
file_hash = get_file_hash(img_path)

if file_hash in cache:
    # kalau sudah ada di cache → langsung keluar, tanpa load model
    label, conf = cache[file_hash]
    print(f"[CACHE] {img_path} → {label} ({conf}% yakin)")
else:
    # baru load model kalau perlu
    processor = AutoImageProcessor.from_pretrained(
        "Falconsai/nsfw_image_detection",
        use_fast=True
    )
    model = AutoModelForImageClassification.from_pretrained("Falconsai/nsfw_image_detection")
    model.eval()

    # deteksi baru
    image = Image.open(img_path)
    inputs = processor(images=image, return_tensors="pt")

    with torch.no_grad():
        outputs = model(**inputs)

    logits = outputs.logits
    predicted_class_id = logits.argmax(-1).item()
    label = model.config.id2label[predicted_class_id]

    probs = F.softmax(logits, dim=-1)
    confidence = probs[0][predicted_class_id].item() * 100

    print(f"[SCAN] {img_path} → {label} ({confidence:.2f}% yakin)")

    # simpan ke cache
    with open(CACHE_FILE, "a") as f:
        f.write(f"{file_hash},{label},{confidence:.2f}\n")
