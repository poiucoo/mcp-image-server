from fastapi import FastAPI, Response
import requests, base64

app = FastAPI()

@app.get("/")
def root():
    return {"status": "running"}

@app.get("/fetch_image_base64")
def fetch_image_base64(url: str):
    """
    將圖片轉成 base64 格式（主要用於測試或非 AI 模型使用）
    """
    try:
        res = requests.get(url)
        res.raise_for_status()
        b64 = base64.b64encode(res.content).decode("utf-8")
        return {"status": "ok", "base64": b64}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/fetch_image_proxy")
def fetch_image_proxy(url: str):
    """
    讓 AI 模型（例如 Gemini、Runway、SDXL）可直接讀取圖片。
    這個端點會代理外部圖片並保持正確的 Content-Type。
    """
    try:
        res = requests.get(url, stream=True)
        res.raise_for_status()
        content_type = res.headers.get("Content-Type", "image/jpeg")
        return Response(content=res.content, media_type=content_type)
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/image/{file_id}.jpg")
def fetch_image_as_jpg(file_id: str):
    """
    使用 Google Drive file_id 建立 .jpg 結尾圖片連結。
    例如：https://mcp-image-server.zeabur.app/image/xxxx.jpg
    """
    try:
        url = f"https://drive.usercontent.google.com/download?id={file_id}&export=view"
        res = requests.get(url, stream=True)
        res.raise_for_status()
        # 嘗試判斷真實的 Content-Type
        content_type = res.headers.get("Content-Type", "image/jpeg")
        return Response(content=res.content, media_type=content_type)
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/image/{file_id}.png")
def fetch_image_as_png(file_id: str):
    """
    支援 .png 結尾的圖片連結。
    例如：https://mcp-image-server.zeabur.app/image/xxxx.png
    """
    try:
        url = f"https://drive.usercontent.google.com/download?id={file_id}&export=view"
        res = requests.get(url, stream=True)
        res.raise_for_status()
        # 若實際為 JPEG，也可直接讀取
        content_type = res.headers.get("Content-Type", "image/png")
        return Response(content=res.content, media_type=content_type)
    except Exception as e:
        return {"status": "error", "message": str(e)}
