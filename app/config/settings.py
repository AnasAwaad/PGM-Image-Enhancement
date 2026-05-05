import os


class Settings:
    def __init__(
        self,
        cloudinary_url,
        cloud_name,
        api_key,
        api_secret,
        enable_cors,
        app_title,
        app_version,
    ):
        self.cloudinary_url = cloudinary_url
        self.cloud_name = cloud_name
        self.api_key = api_key
        self.api_secret = api_secret
        self.enable_cors = enable_cors
        self.app_title = app_title
        self.app_version = app_version

    @staticmethod
    def from_env():
        enable_cors = os.getenv("ENABLE_CORS", "true").lower() == "true"
        return Settings(
            cloudinary_url=os.getenv("CLOUDINARY_URL"),
            cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
            api_key=os.getenv("CLOUDINARY_API_KEY"),
            api_secret=os.getenv("CLOUDINARY_API_SECRET"),
            enable_cors=enable_cors,
            app_title=os.getenv("APP_TITLE", "PGM Enhancement API"),
            app_version=os.getenv("APP_VERSION", "1.0.0"),
        )

    def validate_cloudinary(self):
        if self.cloudinary_url:
            return
        if not (self.cloud_name and self.api_key and self.api_secret):
            raise ValueError(
                "Cloudinary config missing. Set CLOUDINARY_URL or CLOUDINARY_CLOUD_NAME, "
                "CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET."
            )

    def swagger_template(self):
        return {
            "swagger": "2.0",
            "info": {
                "title": self.app_title,
                "description": "Upload an image and receive the enhanced result URL.",
                "version": self.app_version,
            },
        }

    def swagger_config(self):
        return {
            "headers": [],
            "specs": [
                {
                    "endpoint": "apispec_1",
                    "route": "/apispec_1.json",
                    "rule_filter": lambda rule: True,
                    "model_filter": lambda tag: True,
                }
            ],
            "static_url_path": "/flasgger_static",
            "swagger_ui": True,
            "specs_route": "/apidocs/",
        }
