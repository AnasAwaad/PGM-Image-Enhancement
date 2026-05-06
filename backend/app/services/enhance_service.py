import os
import tempfile

import cloudinary.uploader

from app.utils.fft import enhance_pgm
from app.utils.image_io import pgm_to_png, save_upload_as_pgm


def enhance_and_upload(file_storage, d0, a, b):
    with tempfile.TemporaryDirectory() as tmp_dir:
        in_path = os.path.join(tmp_dir, "input.pgm")
        out_path = os.path.join(tmp_dir, "output.pgm")
        png_path = os.path.join(tmp_dir, "output.png")

        save_upload_as_pgm(file_storage, in_path)
        enhance_pgm(in_path, out_path, d0=d0, a=a, b=b)
        pgm_to_png(out_path, png_path)

        result = cloudinary.uploader.upload(png_path, resource_type="image")
        url = result.get("secure_url") or result.get("url")
        if not url:
            raise ValueError("Cloudinary upload failed.")

        return url
