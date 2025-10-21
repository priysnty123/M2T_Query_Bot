# In server/upload_new_book.py

import os
from types import SimpleNamespace
# Import the function you just updated
from modules.load_vectorstore import load_vectorstore

# --- CONFIGURE YOUR UPLOAD HERE ---
# 1. Set the path to the new book you want to upload
NEW_BOOK_FILE_PATH = "C:/Users/Priyanshu/Downloads/Yajurveda_1.pdf"  # 👈 IMPORTANT: Use the full path to your PDF "C:\Users\Priyanshu\Downloads\Durga saptasati.pdf"

# 2. Choose a name for the new collection in your database
NEW_COLLECTION_NAME = "Yajurveda"  # 👈 You can change this to any name

# ------------------------------------

def run_upload():
    """
    Simulates a file upload to add a new book to a new collection.
    """
    if not os.path.exists(NEW_BOOK_FILE_PATH):
        print(f"❌ ERROR: File not found at '{NEW_BOOK_FILE_PATH}'")
        return

    print(f"Starting upload of '{os.path.basename(NEW_BOOK_FILE_PATH)}' to collection '{NEW_COLLECTION_NAME}'...")

    # We need to simulate the 'UploadFile' object that FastAPI uses
    with open(NEW_BOOK_FILE_PATH, "rb") as f:
        # SimpleNamespace creates an object that has .file and .filename attributes
        mock_file = SimpleNamespace(
            file=f,
            filename=os.path.basename(NEW_BOOK_FILE_PATH)
        )

        # Call the function with the simulated file and the new collection name
        load_vectorstore(files=[mock_file], collection_name=NEW_COLLECTION_NAME)

if __name__ == "__main__":
    run_upload()