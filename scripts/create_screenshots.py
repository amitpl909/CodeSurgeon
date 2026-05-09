#!/usr/bin/env python3
"""Generate placeholder PNG files for story screenshots."""

import os
from pathlib import Path

# Create directory
stories_dir = Path("docs/assets/stories")
stories_dir.mkdir(parents=True, exist_ok=True)

# Try to use PIL if available
try:
    from PIL import Image, ImageDraw, ImageFont
    
    stories = [
        ("US-01", "Analyze Code Snippet", "User inputs Python code and clicks Analyze"),
        ("US-02", "Generate Fix", "System displays bug fix with explanation"),
        ("US-03", "Empty Code Validation", "Error message for empty code input"),
        ("US-04", "Syntax Error Handling", "Syntax error details are shown"),
        ("US-05", "GitHub PR Analysis", "GitHub PR analysis results displayed"),
        ("US-06", "Fix Copy to Clipboard", "Copy button enabled for fix code"),
        ("US-07", "LLM Timeout Error", "Timeout error message displayed"),
        ("US-08", "Analysis Metrics", "Metrics shown: critical/high/low counts"),
        ("US-09", "No GitHub Token", "Analysis works without GitHub token"),
    ]
    
    for idx, (story_id, title, description) in enumerate(stories, 1):
        filename = stories_dir / f"us_{idx:02d}_expected.png"
        
        # Create image
        img = Image.new('RGB', (800, 600), color='white')
        draw = ImageDraw.Draw(img)
        
        # Try to load font
        try:
            font_title = ImageFont.truetype("arial.ttf", 24)
            font_text = ImageFont.truetype("arial.ttf", 14)
        except:
            font_title = ImageFont.load_default()
            font_text = ImageFont.load_default()
        
        # Draw layout
        draw.rectangle([0, 0, 800, 600], outline='#0288d1', width=2)
        draw.rectangle([0, 0, 800, 80], fill='#e8f4f8')
        draw.text((20, 15), story_id, fill='#01579b', font=font_title)
        draw.text((20, 50), title, fill='#0288d1', font=font_text)
        draw.text((20, 100), f"Expected: {description}", fill='#333333', font=font_text)
        draw.rectangle([20, 150, 780, 580], outline='#ccc', width=1)
        draw.text((40, 300), "[CodeSurgeon Dashboard - Expected Output]", fill='#999999', font=font_text)
        
        img.save(str(filename))
        print(f"✓ {filename}")

except ImportError:
    print("PIL not available, creating text placeholders instead...")
    for idx in range(1, 10):
        filename = stories_dir / f"us_{idx:02d}_expected.png"
        # Create empty file to satisfy git
        filename.touch()
        print(f"✓ {filename} (placeholder)")

print("\n✓ All 9 story screenshot files created")
