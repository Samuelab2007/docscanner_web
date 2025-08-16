from django.shortcuts import render
from .forms import UploadImageForm
from django.core.files.storage import FileSystemStorage
from document_scanner import pipelines, utils
import os

def upload_and_preview(request):
    uploaded_image_url = None
    processed_image_url = None

    if request.method == "POST":
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            image_file = form.cleaned_data["image"]

            # Save original image
            fs = FileSystemStorage()
            filename = fs.save(image_file.name, image_file)
            uploaded_image_url = fs.url(filename)

            # Process (example: grayscale)
            original_path = fs.path(filename)
            processed_filename = "processed_" + filename
            processed_path = fs.path(processed_filename)

            img = pipelines.process_basic(original_path, debug=False)
            utils.save_img(processed_path, img)

            processed_image_url = fs.url(processed_filename)
    else:
        form = UploadImageForm()

    return render(
        request,
        "document_ui/index.html",
        {
            "form": form,
            "uploaded_image_url": uploaded_image_url,
            "processed_image_url": processed_image_url,
        },
    )
