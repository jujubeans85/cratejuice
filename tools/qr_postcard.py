#!/usr/bin/env python3
"""
QR Postcard Generator for CrateJuice playlists.

Generates a PDF postcard with QR codes for playlist tracks.
"""

import argparse
import json
import sys
from pathlib import Path

import qrcode
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib import colors


def load_playlist(playlist_path):
    """Load playlist data from JSON file."""
    try:
        with open(playlist_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Playlist file not found: {playlist_path}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in playlist file: {e}", file=sys.stderr)
        sys.exit(1)


def generate_qr_code(data, size=4):
    """Generate a QR code image for the given data."""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=size,
        border=2,
    )
    qr.add_data(data)
    qr.make(fit=True)
    return qr.make_image(fill_color="black", back_color="white")


def create_postcard_pdf(playlist_data, output_path, title=None):
    """Create a PDF postcard with QR codes for playlist tracks."""
    # Ensure output directory exists
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Create PDF canvas
    c = canvas.Canvas(str(output_path), pagesize=letter)
    width, height = letter
    
    # Use provided title or playlist title
    display_title = title or playlist_data.get('title', 'CrateJuice Playlist')
    
    # Draw title
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(width / 2, height - 1 * inch, display_title)
    
    # Draw playlist description if available
    description = playlist_data.get('description', '')
    if description:
        c.setFont("Helvetica", 12)
        c.drawCentredString(width / 2, height - 1.5 * inch, description)
    
    # Draw tracks with QR codes
    tracks = playlist_data.get('tracks', [])
    if not tracks:
        c.setFont("Helvetica", 14)
        c.drawCentredString(width / 2, height / 2, "No tracks found in playlist")
        c.save()
        return
    
    y_position = height - 2.5 * inch
    qr_size = 1.2 * inch
    margin = 0.5 * inch
    
    for idx, track in enumerate(tracks):
        # Check if we need a new page
        if y_position < 1.5 * inch:
            c.showPage()
            y_position = height - 1 * inch
            c.setFont("Helvetica-Bold", 18)
            c.drawCentredString(width / 2, y_position, f"{display_title} (continued)")
            y_position -= 0.5 * inch
        
        # Generate QR code for track URL
        track_url = track.get('url', '')
        if track_url:
            # Save QR code to temporary file
            qr_img = generate_qr_code(track_url, size=10)
            temp_qr_path = f"/tmp/qr_temp_{idx}.png"
            qr_img.save(temp_qr_path)
            
            # Draw QR code
            c.drawImage(temp_qr_path, margin, y_position - qr_size, 
                       width=qr_size, height=qr_size)
            
            # Clean up temp file
            Path(temp_qr_path).unlink()
        
        # Draw track info
        text_x = margin + qr_size + 0.3 * inch
        text_y = y_position - 0.3 * inch
        
        c.setFont("Helvetica-Bold", 14)
        track_title = track.get('title', 'Unknown Track')
        c.drawString(text_x, text_y, track_title)
        
        text_y -= 0.25 * inch
        c.setFont("Helvetica", 11)
        artist = track.get('artist', 'Unknown Artist')
        c.drawString(text_x, text_y, f"Artist: {artist}")
        
        text_y -= 0.25 * inch
        duration = track.get('duration', '')
        if duration:
            c.drawString(text_x, text_y, f"Duration: {duration}")
        
        text_y -= 0.25 * inch
        if track_url:
            c.setFont("Helvetica", 9)
            # Truncate URL if too long
            display_url = track_url if len(track_url) < 60 else track_url[:57] + "..."
            c.drawString(text_x, text_y, display_url)
        
        # Draw separator line
        y_position -= qr_size + 0.3 * inch
        c.setStrokeColor(colors.grey)
        c.setLineWidth(0.5)
        c.line(margin, y_position, width - margin, y_position)
        y_position -= 0.3 * inch
    
    # Save the PDF
    c.save()
    print(f"✓ QR postcard generated: {output_path}")


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description='Generate QR code postcards from CrateJuice playlists',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Example:
  python3 tools/qr_postcard.py --playlist content/data/playlist_8.json \\
                                --out postcards/playlist_8.pdf \\
                                --title "CrateJuice v0"
        """
    )
    
    parser.add_argument(
        '--playlist',
        required=True,
        help='Path to the playlist JSON file'
    )
    
    parser.add_argument(
        '--out',
        required=True,
        help='Output path for the PDF postcard'
    )
    
    parser.add_argument(
        '--title',
        help='Title for the postcard (overrides playlist title)'
    )
    
    args = parser.parse_args()
    
    # Load playlist data
    playlist_data = load_playlist(args.playlist)
    
    # Generate postcard
    create_postcard_pdf(playlist_data, args.out, args.title)


if __name__ == '__main__':
    main()
