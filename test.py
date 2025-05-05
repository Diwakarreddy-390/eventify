import os
image_name = "20240612181456_IMG_0868.JPG"
directory = "static/uploads"
image_path = os.path.join(directory, image_name)
print(os.path.exists(image_path))