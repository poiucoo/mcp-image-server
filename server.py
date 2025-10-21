from fastapi import FastAPI, Response
import requests, base64

app = FastAPI()

@app.get("/")
def root():
    return {"status": "running"}

@app.get("/fetch_image_base64")
def fetch_image_base64(url: str):
    """將圖片轉成 base64 格式（主要用於測試或非 AI 模型使用）"""
    try:
        res = requests.get(url)
        res.raise_for_status()
        b64 = base64.b64encode(res.content).decode("utf-8")
        return {"status": "ok", "base64": b64}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/fetch_image_proxy")
def fetch_image_proxy(url: str):
    """代理外部圖片並保持 Content-Type"""
    try:
        res = requests.get(url, stream=True)
        res.raise_for_status()
        content_type = res.headers.get("Content-Type", "image/jpeg")
        return Response(content=res.content, media_type=content_type)
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/image/{file_id}.jpg")
def fetch_image_as_jpg(file_id: str):
    """支援 .jpg 圖片"""
    try:
        url = f"https://drive.usercontent.google.com/download?id={file_id}&export=view"
        res = requests.get(url, stream=True)
        res.raise_for_status()
        content_type = res.headers.get("Content-Type", "image/jpeg")
        return Response(content=res.content, media_type=content_type)
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/image/{file_id}.png")
def fetch_image_as_png(file_id: str):
    """支援 .png 圖片"""
    try:
        url = f"https://drive.usercontent.google.com/download?id={file_id}&export=view"
        res = requests.get(url, stream=True)
        res.raise_for_status()
        content_type = res.headers.get("Content-Type", "image/png")
        return Response(content=res.content, media_type=content_type)
    except Exception as e:
        return {"status": "error", "message": str(e)}

# -------------------------------
# 🔊 新增 mp3 音訊支援
# -------------------------------
@app.get("/audio/{file_id}.mp3")
def fetch_audio_as_mp3(file_id: str):
    """支援 .mp3 音訊"""
    try:
        url = f"https://drive.usercontent.google.com/download?id={file_id}&export=view"
        res = requests.get(url, stream=True)
        res.raise_for_status()
        content_type = res.headers.get("Content-Type", "audio/mpeg")
        return Response(content=res.content, media_type=content_type)
    except Exception as e:
        return {"status": "error", "message": str(e)}

# -------------------------------
# 🎥 新增 mp4 影片支援
# -------------------------------
@app.get("/video/{file_id}.mp4")
def fetch_video_as_mp4(file_id: str):
    """支援 .mp4 影片"""
    try:
        url = f"https://drive.usercontent.google.com/download?id={file_id}&export=view"
        res = requests.get(url, stream=True)
        res.raise_for_status()
        content_type = res.headers.get("Content-Type", "video/mp4")
        return Response(content=res.content, media_type=content_type)
    except Exception as e:
        return {"status": "error", "message": str(e)}
