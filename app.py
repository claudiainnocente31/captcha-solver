from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import easyocr
import io
from PIL import Image
import numpy as np
import re

app = FastAPI()

# Deep Learning Model Load (पहली बार 3s लेता है, फिर 0.1s में काम करता है)
reader = easyocr.Reader(['en'], gpu=False)

@app.get("/")
def home():
    return {"message": "Free Deep AI Captcha Solver (0.1s Speed)"}

@app.post("/solve")
async def solve_captcha(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        image_np = np.array(image)

        # Deep Learning Run
        result = reader.readtext(image_np, detail=0, paragraph=False)
        text = "".join(result)

        # Only Alphanumeric & Math symbols
        clean_text = re.sub(r'[^A-Za-z0-9+\-*/=]', '', text).strip()

        # Math Solve (अगर हो तो)
        if any(op in clean_text for op in ['+', '-', '*', '/']):
            try:
                clean_text = str(eval(clean_text))
            except:
                pass

        return JSONResponse({"success": True, "captcha": clean_text})

    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)})