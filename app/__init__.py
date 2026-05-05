from flask import Flask
from dotenv import load_dotenv
from flasgger import Swagger

from app.config.cloudinary_config import init_cloudinary
from app.config.settings import Settings
from app.controllers.enhance_controller import enhance_bp
from app.extensions import cors

swagger = Swagger()

def create_app():
    app = Flask(__name__)

    load_dotenv()

    settings = Settings.from_env()
    settings.validate_cloudinary()

    # ✅ الحل هنا
    swagger.template = settings.swagger_template()
    swagger.config = settings.swagger_config()
    swagger.init_app(app)

    if settings.enable_cors:
        cors.init_app(app, resources={r"/api/*": {"origins": "*"}})

    init_cloudinary(settings)

    app.register_blueprint(enhance_bp, url_prefix="/api")
    app.settings = settings

    return app