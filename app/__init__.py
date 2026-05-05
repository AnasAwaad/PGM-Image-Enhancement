from flask import Flask
from dotenv import load_dotenv

from app.config.cloudinary_config import init_cloudinary
from app.config.settings import Settings
from app.controllers.enhance_controller import enhance_bp
from app.extensions import cors
from flasgger import Swagger

swagger = Swagger(template=None)


def create_app():
    app = Flask(__name__)

    load_dotenv()

    settings = Settings.from_env()
    settings.validate_cloudinary()

    app.config["SWAGGER"] = settings.swagger_config()
    swagger.template = settings.swagger_template()
    swagger.init_app(app)

    if settings.enable_cors:
        cors.init_app(app, resources={r"/api/*": {"origins": "*"}})

    init_cloudinary(settings)

    app.register_blueprint(enhance_bp, url_prefix="/api")
    app.settings = settings

    return app
