from fastapi import FastAPI, UploadFile, File, Form
import requests
import os
import io
from PIL import Image
from dotenv import load_dotenv

# Load local .env file (ignored in production)
load_dotenv()

app = FastAPI()

OCR_SPACE_API_KEY = os.getenv("OCR_SPACE_API_KEY")
OCR_SPACE_ENDPOINT = "https://api.ocr.space/parse/image"

@app.post("/ocr")
async def ocr(file: UploadFile = File(None), url: str = Form(None)):
    if not OCR_SPACE_API_KEY:
        return {"error": "OCR API key not configured"}

    payload = {"apikey": OCR_SPACE_API_KEY, "language": "eng"}

    # Case 1: File upload
    if file:
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")  # convert to RGB
        buf = io.BytesIO()
        image.save(buf, format="JPEG", quality=70)  # compress
        buf.seek(0)
        files = {"file": (file.filename, buf.read())}
        response = requests.post(OCR_SPACE_ENDPOINT, data=payload, files=files)

    # Case 2: URL input
    elif url:
        r = requests.get(url, stream=True)
        if r.status_code != 200 or "text/html" in r.headers.get("Content-Type", ""):
            return {"error": "URL did not return an image. Use a direct download link."}

        image = Image.open(io.BytesIO(r.content)).convert("RGB")  # convert to RGB
        buf = io.BytesIO()
        image.save(buf, format="JPEG", quality=70)  # compress
        buf.seek(0)
        files = {"file": ("remote.jpg", buf.read())}
        response = requests.post(OCR_SPACE_ENDPOINT, data=payload, files=files)

    else:
        return {"error": "No file or URL provided"}

    # Parse OCR.space response
    result = response.json()
    if "ParsedResults" in result:
        text = result["ParsedResults"][0]["ParsedText"]
        return {"ocr_text": text}
    else:
        return {"error": result.get("ErrorMessage", "OCR failed")}
