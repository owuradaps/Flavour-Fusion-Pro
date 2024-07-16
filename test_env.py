import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file
env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

print("DATABASE_URL:", os.environ.get("DATABASE_URL"))
print("SECRET_KEY:", os.environ.get("SECRET_KEY"))
print("CLOUDINARY_CLOUD_NAME:", os.environ.get("CLOUDINARY_CLOUD_NAME"))
