import random
from PIL import Image

def create_random_grayscale_gif(width, height, frames, output_path):
    images = []
    for _ in range(frames):
        # Create a new grayscale image
        img = Image.new('L', (width, height))
        pixels = img.load()

        # Assign random grayscale values to each pixel
        for x in range(width):
            for y in range(height):
                gray_value = random.randint(0, 255)
                pixels[x, y] = gray_value

        images.append(img)

    # Save the sequence of images as a GIF
    images[0].save(output_path, save_all=True, append_images=images[1:], loop=0, duration=100)

# Parameters
width = 100
height = 100
frames = 10
output_path = 'random_grayscale.gif'

create_random_grayscale_gif(width, height, frames, output_path)
