from PIL import Image

IMG = Image.open('/Users/eaffie/Documents/hawaii/photos/airplane_sunrise.png')
NEW_WIDTH = 350

# Get original dimensions
original_width, original_height = IMG.size
print(f'orig width is {original_width} & orig height is {original_height}')

# Calculate the aspect ratio
aspect_ratio = original_height / original_width
print(f'aspect ratio is {aspect_ratio} ')

# Calculate the new height to maintain aspect ratio
new_height = int(NEW_WIDTH * aspect_ratio)
print(f'Given new_width == {NEW_WIDTH}, after calculation: new_height = int(new_width * aspect_ratio), new height is {new_height}')

# Resize the image using the calculated dimensions
resized_img = IMG.resize((NEW_WIDTH, new_height), Image.Resampling.LANCZOS) # Use a high-quality filter

# Save the resized image
resized_img.save("/Users/eaffie/Documents/hawaii/photos/smaller_airplane_sunrise.png")

