import os
from pathlib import Path
import logging
from dotenv import load_dotenv
from flask_wtf.csrf import CSRFProtect

dotenv_path = Path(__file__).resolve().parent / '.env'
if dotenv_path.exists():
    load_dotenv(dotenv_path)

from moments import create_app  # noqa

config_name = os.getenv('FLASK_CONFIG', 'development')
app = create_app(config_name)

# Configurar el nivel de registro
app.logger.setLevel(logging.INFO)

# Configurar el formato del registro
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Habilitar la protección CSRF
csrf = CSRFProtect(app)
