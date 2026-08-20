from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import pytesseract
import io
from PIL import Image
import re

app = FastAPI()

# Render.com के सिस्टम पर Tesseract का पाथ
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

@app.get("/")
def home():
    return {"message": "Free Captcha Solver (Low Memory)"}

@app.post("/solve")
async def solve_captcha(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))

        # Tesseract कॉन्फिग (सिर्फ अल्फान्यूमेरिक + Math)
        custom_config = r'--oem 3 --psm 8 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+-*/='
        captcha_text = pytesseract.image_to_string(image, config=custom_config)

        clean_text = re.sub(r'[^A-Za-z0-9+\-*/=]', '', captcha_text).strip()

        # Math Solve (अगर हो तो)
        if any(op in clean_text for op in ['+', '-', '*', '/']):
            try:
                clean_text = str(eval(clean_text))
            except:
                pass

        return JSONResponse({"success": True, "captcha": clean_text})

    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)})
