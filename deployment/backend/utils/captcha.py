from PIL import Image
from io import BytesIO
from base64 import encodebytes

def load_image(path):
    image = Image.open(path, mode='r')
    bytes_array = BytesIO()
    image.save(bytes_array, path.split(".")[-1])
    encoded_image = encodebytes(bytes_array.getvalue()).decode('ascii')
    
    return encoded_image