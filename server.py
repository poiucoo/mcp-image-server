from fastapi import FastAPI
import requests, base64

app = FastAPI()

@app.get("/")
def root():
    return {"status": "running"}

@app.get("/fetch_image_base64")
def fetch_image_base64(url: str):
    try:
        res = requests.get(url)
        res.raise_for_status()
        b64 = base64.b64encode(res.content).decode("utf-8")
        return {"status": "ok", "base64": b64}
    except Exception as e:
        return {"status": "error", "message": str(e)}
