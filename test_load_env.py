import os
from dotenv import load_dotenv, find_dotenv
from pathlib import Path

# Load environment variables from .env file
dotenv_path = find_dotenv()
if not dotenv_path:
    print("Could not find .env file")
else:
    load_dotenv(dotenv_path)

    print("DATABASE_URL:", os.environ.get("DATABASE_URL"))
    print("SECRET_KEY:", os.environ.get("SECRET_KEY"))
    print("CLOUDINARY_CLOUD_NAME:", os.environ.get("CLOUDINARY_CLOUD_NAME"))
