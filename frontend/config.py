import os
from dotenv import load_dotenv

load_dotenv()

# URL base del backend.
# - En desarrollo local usa el default (http://localhost:5000).
# - En Docker se sobreescribe con la variable de entorno BACKEND_URL
#   (por ejemplo: BACKEND_URL=http://backend:5000).
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:5000")
