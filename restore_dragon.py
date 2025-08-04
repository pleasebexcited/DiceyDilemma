from PIL import Image
import os

def restore_dragon_image():
    """Restore the dragon image to original dimensions"""
    input_path = "images/dragonType.jpg"
    output_path = "images/dragonType_restored.jpg"
    
    try:
        # Open the current cropped image
        with Image.open(input_path) as img:
            # Get current dimensions
            width, height = img.size
            print(f"Current image size: {width}x{height}")
            
            # Restore to original dimensions (approximately)
            # The original was likely around 1638x2048
            original_width = 1638
            original_height = 2048
            
            # Resize to original dimensions
            restored_img = img.resize((original_width, original_height), Image.Resampling.LANCZOS)
            print(f"Restored image size: {original_width}x{original_height}")
            
            # Save the restored image
            restored_img.save(output_path)
            print(f"Successfully restored image saved as: {output_path}")
            
    except FileNotFoundError:
        print(f"Error: Could not find {input_path}")
    except Exception as e:
        print(f"Error restoring image: {e}")

if __name__ == "__main__":
    restore_dragon_image() 