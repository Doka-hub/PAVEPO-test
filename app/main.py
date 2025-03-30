from app.config.settings import get_settings
from app.config.app import create_app


settings = get_settings()
app = create_app(settings)
