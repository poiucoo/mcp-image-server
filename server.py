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

# ✅ 讓 Gemini 能直接讀取外部圖片
@app.get("/fetch_image_proxy")
def fetch_image_proxy(url: str):
    """
    這個端點會代理外部圖片（如 Google Drive、Imgur 等）
    並保持原本的 Content-Type，讓 AI 模型可直接載入。
    """
    try:
        res = requests.get(url, stream=True)
        res.raise_for_status()
        content_type = res.headers.get("Content-Type", "image/jpeg")
        return Response(content=res.content, media_type=content_type)
    except Exception as e:
        return {"status": "error", "message": str(e)}

# ✅ 新增這段：支援 .jpg 結尾的動態圖片路由
@app.get("/image/{file_id}.jpg")
def fetch_image_as_jpg(file_id: str):
    """
    用 Google Drive file_id 建立固定 .jpg 結尾的連結。
    e.g. /image/1j6mQ4k5OnEDpeu8JX7wS1DXKcMz6_m0w.jpg
    """
    try:
        url = f"https://drive.usercontent.google.com/download?id={file_id}&export=view"
        res = requests.get(url, stream=True)
        res.raise_for_status()
        return Response(content=res.content, media_type="image/jpeg")
    except Exception as e:
        return {"status": "error", "message": str(e)}
