from naoqi import ALProxy

from constants import IP, PORT
from PIL import Image

camProxy = ALProxy("ALVideoDevice", IP, PORT)

def save_image():
    """
    First get an image from Nao, then show it on the screen with PIL.
    """
  
    global camProxy
    resolution = 2    # VGA
    colorSpace = 11   # RGB
  
    videoClient = camProxy.subscribe("python_client", resolution, colorSpace, 5)
  
    # Get a camera image.
    # image[6] contains the image data passed as an array of ASCII chars.
    naoImage = camProxy.getImageRemote(videoClient)
    
    camProxy.unsubscribe(videoClient)
  
    # Get the image size and pixel array.
    imageWidth = naoImage[0]
    imageHeight = naoImage[1]
    array = naoImage[6]
  
    # Create a PIL Image from our pixel array.
    im = Image.frombytes("RGB", (imageWidth, imageHeight), array)
  
    # Save the image.
    im.save("image.png", "PNG")
    