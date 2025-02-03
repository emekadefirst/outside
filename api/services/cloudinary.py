import os
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv
from cloudinary.utils import cloudinary_url

load_dotenv()

cloudinary.config(
    cloud_name=os.getenv("CLOUD_NAME"),
    api_key=os.getenv("API_KEY"),
    api_secret=os.getenv("API_SECRET"),
    secure=True,
)


def cloud(file, name: str):
    try:

        upload_result = cloudinary.uploader.upload(file, public_id=name)
        optimize_url, _ = cloudinary_url(name, fetch_format="auto", quality="auto")
        auto_crop_url, _ = cloudinary_url(name, crop="auto", gravity="auto")
        return optimize_url
    except Exception as e:
        print(f"An error occurred during upload: {str(e)}")
        return None


def cloud_doc(file, name: str):
    try:
        upload_result = cloudinary.uploader.upload(
            file,
            public_id=name,
            resource_type="auto",
            use_filename=True,
            unique_filename=False,
            pages=True,
        )
        return upload_result["secure_url"]
    except Exception as e:
        print(f"An error occurred during upload: {str(e)}")
        return None


# print(cloud("C:/Users/VICTOR/Desktop/dfweb/static/dfi.png", "profile"))
