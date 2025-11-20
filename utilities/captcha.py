import time
import json
import base64
from io import BytesIO
from PIL import Image
import pytesseract
import zlib
import brotli
import zstandard as zstd  # pip install zstandard

def solve_captcha(driver, fragment="/user/captcha-image", timeout=10):
    """
    Captures and solves a CAPTCHA from a Selenium Wire driver request.

    Args:
        driver: Selenium Wire driver
        fragment: Partial URL of CAPTCHA API to filter requests
        timeout: Maximum seconds to wait for the CAPTCHA request

    Returns:
        Captcha text (str) if detected, else None
    """

    # 1️⃣ Filter network requests to only relevant ones
    driver.scopes = [f"*{fragment}*"]
    captcha_req = None

    # 2️⃣ Wait for request to appear
    for _ in range(int(timeout * 4)):  # polling every 0.25s
        for req in driver.requests:
            if fragment in req.path and req.response:
                captcha_req = req
                break
        if captcha_req:
            break
        time.sleep(0.25)

    if not captcha_req:
        print("[Captcha] No CAPTCHA request detected.")
        return None

    # 3️⃣ Decompress response if needed
    body = captcha_req.response.body
    encoding = captcha_req.response.headers.get("Content-Encoding", "").lower()

    try:
        if "br" in encoding:
            body = brotli.decompress(body)
        elif "gzip" in encoding:
            body = zlib.decompress(body, zlib.MAX_WBITS | 16)
        elif "deflate" in encoding:
            body = zlib.decompress(body)
        elif "zstd" in encoding:
            buffer = BytesIO(body)
            dctx = zstd.ZstdDecompressor(max_window_size=2147483648)
            with dctx.stream_reader(buffer) as reader:
                body = reader.read()  # read full decompressed stream
    except Exception as e:
        print(f"[Captcha] Decompression failed ({encoding}): {e}")
        return None

    # 4️⃣ Try to parse JSON first (text or Base64 image)
    try:
        for enc in ("utf-8", "latin-1"):
            try:
                data = json.loads(body.decode(enc))
                # Plain text CAPTCHA
                captcha_text = data.get("captcha_text") or data.get("text")
                if captcha_text:
                    print("[Captcha] Found text in JSON:", captcha_text)
                    return captcha_text
                # Base64-encoded image
                if "image_base64" in data:
                    img_data = base64.b64decode(data["image_base64"])
                    img = Image.open(BytesIO(img_data))
                    captcha_text = pytesseract.image_to_string(img).strip()
                    print("[Captcha] OCR from Base64 image:", captcha_text)
                    return captcha_text
            except (UnicodeDecodeError, json.JSONDecodeError):
                continue
    except Exception as e:
        print("[Captcha] JSON parsing failed:", e)

    # 5️⃣ Fallback: raw image OCR
    try:
        img = Image.open(BytesIO(body))
        captcha_text = pytesseract.image_to_string(img).strip()
        print("[Captcha] OCR from raw image:", captcha_text)
        return captcha_text
    except Exception as e:
        print("[Captcha] Raw image OCR failed:", e)

    print("[Captcha] Could not detect CAPTCHA.")
    return None
