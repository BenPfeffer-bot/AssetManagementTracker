"""
QR Code Generator for Portfolio Tracker
Generates QR code and shareable materials for the published app
"""

import qrcode
from PIL import Image, ImageDraw, ImageFont
import os

# App URL
APP_URL = "https://benpfeffer-bot-assetmanagementtracker-app-t75mzr.streamlit.app/"

# Create output directory
OUTPUT_DIR = "shareable_materials"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_basic_qr():
    """Generate basic QR code"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(APP_URL)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(f"{OUTPUT_DIR}/qr_code_basic.png")
    print(f"✅ Basic QR code saved: {OUTPUT_DIR}/qr_code_basic.png")
    return img

def generate_branded_qr():
    """Generate branded QR code with colors"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(APP_URL)
    qr.make(fit=True)
    
    # Use brand colors
    img = qr.make_image(fill_color="#667eea", back_color="white")
    img.save(f"{OUTPUT_DIR}/qr_code_branded.png")
    print(f"✅ Branded QR code saved: {OUTPUT_DIR}/qr_code_branded.png")
    return img

def generate_large_qr():
    """Generate high-resolution QR code for printing"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=20,  # Larger box size for printing
        border=4,
    )
    qr.add_data(APP_URL)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(f"{OUTPUT_DIR}/qr_code_print_large.png")
    print(f"✅ Print-quality QR code saved: {OUTPUT_DIR}/qr_code_print_large.png")
    return img

def generate_info_card():
    """Generate an information card with QR code and details"""
    # Create a new image (800x600 pixels)
    width, height = 800, 600
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)
    
    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=8,
        border=2,
    )
    qr.add_data(APP_URL)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="#667eea", back_color="white")
    
    # Resize QR code
    qr_size = 300
    qr_img = qr_img.resize((qr_size, qr_size), Image.Resampling.LANCZOS)
    
    # Paste QR code centered
    qr_position = ((width - qr_size) // 2, 80)
    img.paste(qr_img, qr_position)
    
    # Add text (using default font since custom fonts may not be available)
    try:
        title_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 36)
        url_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 18)
        desc_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 16)
    except:
        # Fallback to default font
        title_font = ImageFont.load_default()
        url_font = ImageFont.load_default()
        desc_font = ImageFont.load_default()
    
    # Draw title
    title = "Portfolio Tracker Dashboard"
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    draw.text(((width - title_width) // 2, 20), title, fill="#667eea", font=title_font)
    
    # Draw instruction
    instruction = "Scan to access the platform"
    inst_bbox = draw.textbbox((0, 0), instruction, font=desc_font)
    inst_width = inst_bbox[2] - inst_bbox[0]
    draw.text(((width - inst_width) // 2, 400), instruction, fill="#1e293b", font=desc_font)
    
    # Draw URL
    url_bbox = draw.textbbox((0, 0), APP_URL, font=url_font)
    url_width = url_bbox[2] - url_bbox[0]
    draw.text(((width - url_width) // 2, 440), APP_URL, fill="#667eea", font=url_font)
    
    # Draw footer
    footer = "Real-time Portfolio Analysis & Management"
    footer_bbox = draw.textbbox((0, 0), footer, font=desc_font)
    footer_width = footer_bbox[2] - footer_bbox[0]
    draw.text(((width - footer_width) // 2, 520), footer, fill="#64748b", font=desc_font)
    
    img.save(f"{OUTPUT_DIR}/access_card.png")
    print(f"✅ Access card saved: {OUTPUT_DIR}/access_card.png")

def main():
    print("🎨 Generating QR codes and shareable materials...")
    print(f"📱 App URL: {APP_URL}")
    print()
    
    # Generate different versions
    generate_basic_qr()
    generate_branded_qr()
    generate_large_qr()
    generate_info_card()
    
    print()
    print("✅ All materials generated successfully!")
    print(f"📁 Check the '{OUTPUT_DIR}/' folder for all files")
    print()
    print("📋 Files created:")
    print(f"   1. qr_code_basic.png - Standard black & white QR code")
    print(f"   2. qr_code_branded.png - Purple-branded QR code")
    print(f"   3. qr_code_print_large.png - High-res for printing")
    print(f"   4. access_card.png - Complete info card with QR code")

if __name__ == "__main__":
    main()

