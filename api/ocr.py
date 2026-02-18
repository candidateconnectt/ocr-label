from fastapi import FastAPI, UploadFile, File, Form
import pytesseract
from PIL import Image
import io
import requests

app = FastAPI()

@app.post("/ocr")
async def ocr(file: UploadFile = File(None), url: str = Form(None)):
    if file:
        image_bytes = await file.read()
    elif url:
        response = requests.get(url)
        image_bytes = response.content
    else:
        return {"error": "No file or URL provided"}

    image = Image.open(io.BytesIO(image_bytes))
    text = pytesseract.image_to_string(image)
    return {"ocr_text": text}
