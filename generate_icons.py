import os
from PIL import Image

def create_icons():
    # Source image path
    source_img_path = r"c:\Users\prosp\Desktop\WEBSITES\Royal Exercutive Empire\Web\Images\BG\logo bg.png"
    
    # Destination directory for icons
    dest_dir = r"c:\Users\prosp\Desktop\WEBSITES\Royal Exercutive Empire\Web\Images\icons"
    
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
        
    sizes = [72, 96, 128, 144, 152, 192, 384, 512]
    
    try:
        with Image.open(source_img_path) as img:
            # PWA icons should ideally be square. Let's create a square version if needed,
            # or just resize it (assuming it is roughly square or centered).
            # For best results, we paste it into a transparent square if it's not square.
            width, height = img.size
            max_dim = max(width, height)
            
            # Create a transparent square background
            square_img = Image.new('RGBA', (max_dim, max_dim), (0, 0, 0, 0))
            
            # Paste the original image centered
            offset_x = (max_dim - width) // 2
            offset_y = (max_dim - height) // 2
            square_img.paste(img, (offset_x, offset_y))
            
            for size in sizes:
                resized_img = square_img.resize((size, size), Image.Resampling.LANCZOS)
                output_path = os.path.join(dest_dir, f"icon-{size}x{size}.png")
                resized_img.save(output_path, "PNG")
                print(f"Created: {output_path}")
                
            print("Successfully generated all PWA icons.")
    except Exception as e:
        print(f"Error generating icons: {e}")

if __name__ == "__main__":
    create_icons()
