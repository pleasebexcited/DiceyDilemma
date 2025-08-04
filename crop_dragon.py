from PIL import Image
import os

def crop_dragon_image():
    """Crop 68 pixels off the bottom of dragonType.jpg (total)"""
    input_path = "images/dragonType.jpg"
    output_path = "images/dragonType_cropped.jpg"
    
    try:
        # Open the image
        with Image.open(input_path) as img:
            # Get current dimensions
            width, height = img.size
            print(f"Original image size: {width}x{height}")
            
            # Calculate new dimensions (crop 68 pixels from bottom)
            new_height = height - 68
            print(f"New image size: {width}x{new_height}")
            
            # Crop the image (left, top, right, bottom)
            # This crops from the top-left corner to width x (height-68)
            cropped_img = img.crop((0, 0, width, new_height))
            
            # Save the cropped image
            cropped_img.save(output_path)
            print(f"Successfully cropped image saved as: {output_path}")
            
            # Optionally, replace the original file
            # Uncomment the next two lines if you want to replace the original
            # cropped_img.save(input_path)
            # print(f"Replaced original file: {input_path}")
            
    except FileNotFoundError:
        print(f"Error: Could not find {input_path}")
    except Exception as e:
        print(f"Error cropping image: {e}")

if __name__ == "__main__":
    crop_dragon_image() 