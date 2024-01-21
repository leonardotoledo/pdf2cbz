import fitz  # PyMuPDF
from PIL import Image
import os
import sys
import shutil
import zipfile
from concurrent.futures import ThreadPoolExecutor


def convert_page_to_image(page, page_number, temp_dir):
    image = page.get_pixmap()
    pil_image = Image.frombytes("RGB", (image.width, image.height), image.samples)
    image_path = os.path.join(temp_dir, f"page_{page_number + 1}.png")
    pil_image.save(image_path)


def convert_pdf_to_cbz(pdf_path, cbz_path):
    # Create a temporary directory to store extracted images
    temp_dir = "temp_images"
    os.makedirs(temp_dir, exist_ok=True)

    # Open the PDF file
    pdf_document = fitz.open(pdf_path)

    # Use ThreadPoolExecutor for parallel conversion
    with ThreadPoolExecutor() as executor:
        # Create a list of futures for the image conversion tasks
        futures = []

        print("Extracting images from PDF...")
        # Submit image conversion tasks for each page
        for page_number in range(pdf_document.page_count):
            page = pdf_document[page_number]
            future = executor.submit(convert_page_to_image, page, page_number, temp_dir)
            futures.append(future)

        # Wait for all tasks to complete
        for future in futures:
            future.result()

    # Close the PDF document
    pdf_document.close()

    # Create a ZIP file
    with zipfile.ZipFile(cbz_path, 'w', zipfile.ZIP_DEFLATED) as cbz_file:
        # Add each image to the ZIP file
        print("Creating CBZ file...")
        for root, _, files in os.walk(temp_dir):
            for file in files:
                image_path = os.path.join(root, file)
                cbz_file.write(image_path, os.path.relpath(image_path, temp_dir))

    # Remove the temporary directory and its contents
    shutil.rmtree(temp_dir)

    print("Done!")


if __name__ == "__main__":
    pdf_file_path = sys.argv[1]
    cbz_file_path = os.path.splitext(pdf_file_path)[0] + ".cbz"

    convert_pdf_to_cbz(pdf_file_path, cbz_file_path)
