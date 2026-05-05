from flask import Blueprint, current_app, jsonify, request

from app.services.enhance_service import enhance_and_upload

enhance_bp = Blueprint("enhance", __name__)


@enhance_bp.post("/enhance")
def enhance():
    """
    Upload an image, enhance it, upload to Cloudinary, and return the URL.
    ---
    consumes:
      - multipart/form-data
    parameters:
      - name: file
        in: formData
        type: file
        required: true
        description: PGM (P2/P5), PNG, or JPG.
      - name: d0
        in: formData
        type: number
        required: false
        default: 45
      - name: a
        in: formData
        type: number
        required: false
        default: 1.0
      - name: b
        in: formData
        type: number
        required: false
        default: 0.8
    responses:
      200:
        description: Cloudinary URL for enhanced image
        schema:
          type: object
          properties:
            url:
              type: string
    """
    if "file" not in request.files:
        return jsonify(error="Missing file"), 400

    uploaded = request.files["file"]
    if uploaded.filename == "":
        return jsonify(error="Empty filename"), 400

    try:
        d0 = float(request.form.get("d0", 45))
        a = float(request.form.get("a", 1.0))
        b = float(request.form.get("b", 0.8))
    except ValueError:
        return jsonify(error="Invalid numeric parameters"), 400

    try:
        url = enhance_and_upload(uploaded, d0=d0, a=a, b=b)
    except ValueError as exc:
        return jsonify(error=str(exc)), 400
    except Exception as exc:
        current_app.logger.exception("Processing failed")
        return jsonify(error="Processing failed"), 500

    return jsonify(url=url)
