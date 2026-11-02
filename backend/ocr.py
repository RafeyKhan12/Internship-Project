from PIL import Image
import pytesseract


def extract_text_from_image(image_path_or_file) -> str:
    if image_path_or_file is None:
        return ""

    try:
        image = Image.open(image_path_or_file)
        raw_text = pytesseract.image_to_string(image)
        return raw_text.strip()

    except pytesseract.TesseractNotFoundError:
        # The Tesseract OCR engine itself isn't installed/on PATH.
        print(
            "[ocr] Tesseract is not installed or not found on PATH. "
            "Install it (e.g. `brew install tesseract` or "
            "`apt-get install tesseract-ocr`) to enable OCR."
        )
        return ""
    except (OSError, ValueError) as e:
        # Covers corrupt/unreadable image files, unsupported formats, etc.
        print(f"[ocr] Could not read image for OCR: {e}")
        return ""
    except Exception as e:
        # Catch-all so an unexpected OCR failure never crashes the app.
        print(f"[ocr] Unexpected OCR error: {e}")
        return ""


# ---------------------------------------------------------------------------
# Demo / manual test entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # Replace this with the path to a sample prescription image to test.
    sample_image_path = "sample_prescription.png"

    print(f"Running OCR on: {sample_image_path}\n")
    extracted_text = extract_text_from_image(sample_image_path)

    if extracted_text:
        print("Extracted text:")
        print("-" * 40)
        print(extracted_text)
        print("-" * 40)
    else:
        print(
            "No text extracted. Make sure the file exists at the path above, "
            "Tesseract OCR is installed, and the image contains readable text."
        )
