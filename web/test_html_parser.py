from pathlib import Path
from bs4 import BeautifulSoup
import json

def html_to_blocks(html_file_path):
    """Convert existing HTML to content blocks using BeautifulSoup"""
    content = Path(html_file_path).read_text()
    soup = BeautifulSoup(content, 'html.parser')
    
    # Remove header and footer from the soup
    if soup.find('nav'):
        soup.find('nav').decompose()
    if soup.find('footer'):
        soup.find('footer').decompose()
    
    blocks = []
    print(f"DEBUG: soup.body: {soup.body}") # Debug print
    # Find all top-level sections in the body
    if soup.body:
        for section_tag in soup.body.find_all('section', recursive=False):
            block_type = "section" # Default type
            block_title = ""
            block_classes = section_tag.get('class', [])
            
            # Extract title from h1 or h2 within the section
            title_element = section_tag.find(['h1', 'h2'], recursive=False)
            if title_element:
                block_title = title_element.get_text(strip=True)
                title_element.decompose() # Remove title from content
            
            # Extract content: get all children of the section_tag,
            # convert them to string, and join them.
            # This will include all remaining tags and text within the section.
            block_content = "".join(str(child) for child in section_tag.children if child.name != 'section').strip()
            
            blocks.append({
                "type": block_type,
                "title": block_title,
                "content": block_content,
                "classes": " ".join(block_classes)
            })
    
    return blocks

if __name__ == "__main__":
    test_file = "test.html"
    extracted_blocks = html_to_blocks(test_file)
    print(json.dumps(extracted_blocks, indent=2))
