import socket
import requests
import uvicorn
import argparse
from app import app   # import FastAPI app dari app.py

def print_urls(host, port):
    sample_path = "/cek_nsfw?url=https://example.com/foto.jpg"
    local_url = f"http://127.0.0.1:{port}{sample_path}"
    lan_ip = socket.gethostbyname(socket.gethostname())
    lan_url = f"http://{lan_ip}:{port}{sample_path}"
    try:
        public_ip = requests.get("https://api.ipify.org").text.strip()
        public_url = f"http://{public_ip}:{port}{sample_path}"
    except:
        public_url = "(gagal ambil IP publik)"

    print("\n🚀 NSFW Detector API is running")
    print(f"   Local URL   : {local_url}")
    print(f"   Network URL : {lan_url}")
    print(f"   Public URL  : {public_url}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()

    # print info server
    print_urls(args.host, args.port)

    # jalankan uvicorn
    uvicorn.run(app, host=args.host, port=args.port)
