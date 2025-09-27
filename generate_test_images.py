"""
Generate test images for medicine verification prototype
Creates realistic medicine package images with text and barcodes
"""

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os
import random
from datetime import datetime, timedelta

def create_medicine_package_image(medicine_data, output_path):
    """Create a realistic medicine package image"""
    
    # Create base image
    width, height = 400, 300
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)
    
    # Try to use a system font, fallback to default if not available
    try:
        title_font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 24)
        subtitle_font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 16)
        small_font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 12)
    except:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    
    # Draw medicine package design
    # Header with brand name
    draw.rectangle([10, 10, width-10, 50], fill='#4CAF50', outline='#2E7D32', width=2)
    draw.text((20, 25), medicine_data['Brand_Name'], fill='white', font=title_font)
    
    # Generic name
    draw.text((20, 60), f"Generic: {medicine_data['Generic_Name']}", fill='black', font=subtitle_font)
    
    # Manufacturer
    draw.text((20, 85), f"Manufacturer: {medicine_data['Manufacturer']}", fill='black', font=subtitle_font)
    
    # Batch number
    draw.text((20, 110), f"Batch: {medicine_data['Batch_Number']}", fill='black', font=small_font)
    
    # Manufacturing and expiry dates
    draw.text((20, 130), f"MFG: {medicine_data['MFG_Date']}", fill='black', font=small_font)
    draw.text((20, 150), f"EXP: {medicine_data['EXP_Date']}", fill='black', font=small_font)
    
    # Barcode area (simplified representation)
    barcode_x = 20
    barcode_y = 180
    barcode_width = 200
    barcode_height = 40
    
    # Draw barcode lines
    for i in range(0, barcode_width, 3):
        line_height = random.randint(20, barcode_height-5)
        draw.rectangle([barcode_x + i, barcode_y, barcode_x + i + 1, barcode_y + line_height], fill='black')
    
    # Barcode number
    draw.text((barcode_x, barcode_y + 45), medicine_data['Barcode_Data'], fill='black', font=small_font)
    
    # Dosage information
    dosage_text = medicine_data['Brand_Name'].split()[-1]  # Extract dosage from brand name
    draw.text((20, 240), f"Dosage: {dosage_text}", fill='black', font=small_font)
    
    # Storage instructions
    draw.text((20, 260), "Store in cool, dry place", fill='gray', font=small_font)
    
    # Save image
    img.save(output_path)
    return img

def create_counterfeit_image(medicine_data, output_path):
    """Create a counterfeit medicine package with intentional errors"""
    
    # Create base image
    width, height = 400, 300
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)
    
    try:
        title_font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 24)
        subtitle_font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 16)
        small_font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 12)
    except:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    
    # Draw counterfeit package with errors
    # Header with misspelled brand name
    draw.rectangle([10, 10, width-10, 50], fill='#FF5722', outline='#D32F2F', width=2)
    fake_brand = medicine_data['Brand_Name'].replace('a', 'o').replace('e', 'i')  # Intentional misspelling
    draw.text((20, 25), fake_brand, fill='white', font=title_font)
    
    # Generic name with error
    draw.text((20, 60), f"Generic: {medicine_data['Generic_Name']}", fill='black', font=subtitle_font)
    
    # Wrong manufacturer
    draw.text((20, 85), f"Manufacturer: {medicine_data['Manufacturer']} Ltd", fill='black', font=subtitle_font)
    
    # Wrong batch number format
    fake_batch = f"FAKE{random.randint(1000, 9999)}"
    draw.text((20, 110), f"Batch: {fake_batch}", fill='red', font=small_font)
    
    # Expired dates
    expired_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
    draw.text((20, 130), f"MFG: {expired_date}", fill='red', font=small_font)
    draw.text((20, 150), f"EXP: {expired_date}", fill='red', font=small_font)
    
    # Invalid barcode
    barcode_x = 20
    barcode_y = 180
    barcode_width = 200
    barcode_height = 40
    
    # Draw irregular barcode
    for i in range(0, barcode_width, 5):
        line_height = random.randint(10, barcode_height-10)
        draw.rectangle([barcode_x + i, barcode_y, barcode_x + i + 2, barcode_y + line_height], fill='red')
    
    # Invalid barcode number
    fake_barcode = "9999999999999"
    draw.text((barcode_x, barcode_y + 45), fake_barcode, fill='red', font=small_font)
    
    # Warning text
    draw.text((20, 240), "⚠️ COUNTERFEIT DETECTED", fill='red', font=small_font)
    draw.text((20, 260), "Do not use - Report immediately", fill='red', font=small_font)
    
    # Save image
    img.save(output_path)
    return img

def generate_test_images():
    """Generate comprehensive test images"""
    
    # Create test_images directory
    os.makedirs('test_images', exist_ok=True)
    
    # Import medicine database
    from medicine_database import create_medicine_database
    
    # Get medicine database
    medicine_db = create_medicine_database()
    
    print(f"Generating test images for {len(medicine_db)} medicines...")
    
    # Generate authentic medicine images
    authentic_count = 0
    for i, medicine in medicine_db.iterrows():
        if authentic_count >= 20:  # Limit to 20 authentic images
            break
        
        # Skip counterfeit medicines for authentic images
        if 'Fake' in medicine['Brand_Name'] or 'Counterfeit' in medicine['Brand_Name']:
            continue
            
        output_path = f"test_images/authentic_{medicine['Brand_Name'].replace(' ', '_').replace('/', '_')}.png"
        create_medicine_package_image(medicine, output_path)
        authentic_count += 1
        print(f"Generated authentic image: {medicine['Brand_Name']}")
    
    # Generate counterfeit images
    counterfeit_count = 0
    for i, medicine in medicine_db.iterrows():
        if counterfeit_count >= 10:  # Limit to 10 counterfeit images
            break
            
        # Only create counterfeit images for real medicines
        if 'Fake' in medicine['Brand_Name'] or 'Counterfeit' in medicine['Brand_Name']:
            continue
            
        output_path = f"test_images/counterfeit_{medicine['Brand_Name'].replace(' ', '_').replace('/', '_')}.png"
        create_counterfeit_image(medicine, output_path)
        counterfeit_count += 1
        print(f"Generated counterfeit image: {medicine['Brand_Name']}")
    
    # Generate some specific test cases
    test_cases = [
        {
            'Brand_Name': 'Paracetamol 500mg',
            'Generic_Name': 'Acetaminophen',
            'Manufacturer': 'Sun Pharma',
            'Batch_Number': 'SP2024001',
            'Barcode_Data': '8901234567890',
            'MFG_Date': '2024-01-15',
            'EXP_Date': '2027-01-15'
        },
        {
            'Brand_Name': 'Amoxicillin 250mg',
            'Generic_Name': 'Amoxicillin',
            'Manufacturer': 'Cipla',
            'Batch_Number': 'CP2024002',
            'Barcode_Data': '8901234567891',
            'MFG_Date': '2024-02-01',
            'EXP_Date': '2026-02-01'
        },
        {
            'Brand_Name': 'Metformin 500mg',
            'Generic_Name': 'Metformin HCl',
            'Manufacturer': 'Dr. Reddy\'s',
            'Batch_Number': 'DR2024003',
            'Barcode_Data': '8901234567892',
            'MFG_Date': '2024-01-20',
            'EXP_Date': '2027-01-20'
        }
    ]
    
    for i, test_case in enumerate(test_cases):
        # Authentic version
        output_path = f"test_images/test_authentic_{i+1}.png"
        create_medicine_package_image(test_case, output_path)
        print(f"Generated test authentic image {i+1}")
        
        # Counterfeit version
        output_path = f"test_images/test_counterfeit_{i+1}.png"
        create_counterfeit_image(test_case, output_path)
        print(f"Generated test counterfeit image {i+1}")
    
    print(f"\n✅ Generated {authentic_count + counterfeit_count + 6} test images in 'test_images' directory")
    print("📁 Test images include:")
    print("   • Authentic medicine packages")
    print("   • Counterfeit medicine packages")
    print("   • Various manufacturers")
    print("   • Different medicine categories")
    print("\n🧪 You can now test your prototype with these images!")

if __name__ == "__main__":
    generate_test_images()
