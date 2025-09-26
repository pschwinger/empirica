#!/usr/bin/env python3
import re
import json
from pathlib import Path
from bs4 import BeautifulSoup
import copy

def html_to_blocks(html_file):
    """Convert existing HTML to content blocks using BeautifulSoup"""
    content = Path(html_file).read_text()
    soup = BeautifulSoup(content, 'html.parser')
    
    # Remove header and footer from the soup
    if soup.find('nav'):
        soup.find('nav').decompose()
    if soup.find('footer'):
        soup.find('footer').decompose()
    
    blocks = []
    # Find all top-level sections in the body
    if soup.body:
        for section_tag in soup.body.find_all('section', recursive=False):
            block_type = "section" # Default type
            block_title = ""
            block_classes = section_tag.get('class', [])
            
            # Create a copy of the section_tag to manipulate its contents
            # without affecting the original soup for other sections
            section_copy = copy.copy(section_tag)
            
            # Extract title from h1 or h2 within the copied section
            title_element = section_copy.find(['h1', 'h2'], recursive=False)
            if title_element:
                block_title = title_element.get_text(strip=True)
                title_element.decompose() # Remove title from content
            
            # Extract content: get the inner HTML of the copied section
            # after title removal. This will include all remaining tags and text.
            # Use .decode_contents() to get inner HTML as a string
            block_content = section_copy.decode_contents().strip()
            
            blocks.append({
                "type": block_type,
                "title": block_title,
                "content": block_content,
                "classes": " ".join(block_classes)
            })
    
    return blocks

def extract_meta(html_file):
    """Extract meta title and description from HTML"""
    content = Path(html_file).read_text()
    title_match = re.search(r'<title>(.*?)</title>', content)
    # For description, we'll just use the first <p> tag for now
    description_match = re.search(r'<p[^>]*>(.*?)</p>', content)
    
    title = title_match.group(1) if title_match else ""
    # Truncate title to 60 characters
    if len(title) > 60:
        title = title[:57] + "..." # Truncate and add ellipsis
    
    return {
        "title": title,
        "description": description_match.group(1) if description_match else ""
    }

def migrate_all_pages():
    """Convert all existing HTML to JSON"""
    html_files = list(Path('templates').glob('*.html'))
    
    for html_file in html_files:
        if html_file.name.startswith(('temp_', 'new_', 'base')):
            continue
            
        print(f" Processing {html_file}...")
        
        # Determine page type and active_nav
        if html_file.name == 'index.html':
            layout = 'home'
            active_nav = 'home'
        elif html_file.name == 'components.html':
            layout = 'docs'
            active_nav = 'components'
        elif html_file.name == 'protocols.html':
            layout = 'docs'
            active_nav = 'protocols'
        elif html_file.name == 'sovereign-ai.html':
            layout = 'docs'
            active_nav = 'sovereign-ai'
        elif html_file.name == 'documentation.html':
            layout = 'docs'
            active_nav = 'documentation'
        else:
            # Default for other pages
            layout = 'docs'
            active_nav = 'documentation' # Set to 'documentation' as a valid default
        
        # Extract meta
        meta = extract_meta(html_file)
        
        # Convert to blocks
        blocks = html_to_blocks(html_file)
        
        # Create JSON
        page_spec = {
            "page_id": html_file.stem,
            "layout": layout,
            "active_nav": active_nav,
            "meta": meta,
            "content_blocks": blocks
        }
        
        # Save
        with open(f"content/{html_file.stem}.json", 'w') as f:
            json.dump(page_spec, f, indent=2)
        
        print(f"✅ Created content/{html_file.stem}.json")

if __name__ == "__main__":
    migrate_all_pages()