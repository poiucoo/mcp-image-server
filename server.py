from fastapi import FastAPI, Response
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

# ✅ 新增這段
@app.get("/fetch_image_proxy")
def fetch_image_proxy(url: str):
    """
    讓 Gemini 可以直接用 URL 存取圖片。
    這個端點會抓取外部圖片並原樣回傳，保持 content-type。
    """
    try:
        res = requests.get(url, stream=True)
        res.raise_for_status()
        headers = {"Content-Type": res.headers.get("Content-Type", "image/jpeg")}
        return Response(content=res.content, media_type=headers["Content-Type"])
    except Exception as e:
        return {"status": "error", "message": str(e)}
