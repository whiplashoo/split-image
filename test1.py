from PIL import Image

from split_image import split

split(Image.open("bridge.jpg"), 2, 2, "bridge.jpg", False)
