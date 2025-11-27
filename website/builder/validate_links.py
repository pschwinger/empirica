import os
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urlparse, unquote

OUTPUT_DIR = Path("../output_v2")

def validate_links():
    print("🔍 Starting Link Validation...")
    
    html_files = list(OUTPUT_DIR.glob("*.html"))
    errors = []
    checked_count = 0
    
    for file_path in html_files:
        with open(file_path, 'r') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
            
        links = soup.find_all('a')
        for link in links:
            href = link.get('href')
            if not href:
                continue
                
            checked_count += 1
            
            # Skip external links, anchors, and mailto
            if href.startswith(('http', 'https', 'mailto:', '#')):
                continue
                
            # Normalize path
            # If starts with /, it's relative to root (OUTPUT_DIR)
            # If relative, it's relative to current file (which is also in OUTPUT_DIR)
            
            if href.startswith('/'):
                target_path = OUTPUT_DIR / href.lstrip('/')
            else:
                target_path = OUTPUT_DIR / href
                
            # Remove anchor from target check
            if '#' in str(target_path):
                target_path = Path(str(target_path).split('#')[0])
                
            if not target_path.exists():
                errors.append(f"❌ Broken link in {file_path.name}: {href} -> {target_path} not found")
                
    print(f"✅ Checked {checked_count} links across {len(html_files)} files.")
    
    if errors:
        print(f"⚠️ Found {len(errors)} broken links:")
        for error in errors:
            print(error)
        exit(1)
    else:
        print("🎉 No broken links found!")

if __name__ == "__main__":
    validate_links()
