#!/usr/bin/env python3
"""
QR Code Generator - Pydroid Optimized
=====================================
Simple QR code generator that works reliably on mobile.
"""

import argparse
from pathlib import Path

try:
    import qrcode
    from PIL import Image
except ImportError:
    print("❌ Missing dependencies!")
    print("Please run: pip install qrcode[pil] pillow")
    exit(1)


def generate_qr(data: str, filename: str = "qr_code.png", size: int = 400):
    """Generate QR code."""
    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        
        if size != 400:
            img = img.resize((size, size), Image.LANCZOS)

        filepath = Path(filename)
        img.save(filepath)
        
        print(f"✅ QR Code successfully created!")
        print(f"📁 Saved to: {filepath.resolve()}")
        print(f"🔗 Content: {data[:70]}{'...' if len(data) > 70 else ''}")
        
    except Exception as e:
        print(f"❌ Error generating QR code: {e}")


def main():
    parser = argparse.ArgumentParser(description="📱 QR Code Generator")
    parser.add_argument("data", nargs="?", default=None, 
                        help="Text or URL to encode")
    parser.add_argument("-o", "--output", default="qr_code.png",
                        help="Output filename (default: qr_code.png)")
    parser.add_argument("-s", "--size", type=int, default=400,
                        help="Size in pixels (default: 400)")
    parser.add_argument("-p", "--prompt", action="store_true",
                        help="Interactive mode (recommended on Pydroid)")

    args = parser.parse_args()

    if args.prompt or not args.data:
        print("📝 Enter text or URL for QR code:")
        data = input("> ").strip()
    else:
        data = args.data

    if not data:
        print("❌ Error: No data provided!")
        return

    generate_qr(data, args.output, args.size)


if __name__ == "__main__":
    main()
