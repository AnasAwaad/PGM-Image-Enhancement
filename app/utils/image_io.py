import io

from PIL import Image


def _is_pgm_bytes(data):
    return data[:2] in (b"P2", b"P5")


def save_upload_as_pgm(file_storage, target_path):
    data = file_storage.read()
    file_storage.stream.seek(0)

    if _is_pgm_bytes(data):
        with open(target_path, "wb") as f:
            f.write(data)
        return

    try:
        image = Image.open(io.BytesIO(data))
        image = image.convert("L")
        image.save(target_path, format="PPM")
    except Exception as exc:
        raise ValueError("Unsupported image format. Use PGM, PNG, or JPG.") from exc


def pgm_to_png(pgm_path, png_path):
    image = Image.open(pgm_path).convert("L")
    image.save(png_path, format="PNG")
