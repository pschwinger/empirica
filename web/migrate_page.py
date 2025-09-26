#!/usr/bin/env python3
import os
import re
from pathlib import Path

def extract_body_content(html_file):
    """Extract the main content from existing HTML file"""
    with open(html_file, 'r') as f:
        content = f.read()
    
    # Remove existing header/footer if present
    content = re.sub(r'<nav[^>]*>.*?</nav>', '', content, flags=re.DOTALL)
    content = re.sub(r'<footer[^>]*>.*?</footer>', '', content, flags=re.DOTALL)
    
    # Extract content between header and footer
    body_match = re.search(r'<body[^>]*>(.*?)</body>', content, re.DOTALL)
    if body_match:
        return body_match.group(1).strip()
    return content

def extract_title(html_file):
    """Extract the title from the HTML file"""
    with open(html_file, 'r') as f:
        content = f.read()
    title_match = re.search(r'<title>(.*?)</title>', content)
    if title_match:
        return title_match.group(1)
    return "Semantic Self-Aware Kit"

def create_new_template(old_file, layout_type, active_nav, sidebar_type=None):
    """Create new template from old file"""
    content = extract_body_content(old_file)
    
    if layout_type == 'base':
        template = f'''{{% extends "base.html" %}}

{{% block title %}}{extract_title(old_file)}{{% endblock %}}

{{% block navigation %}}
{{% set active_nav = '{active_nav}' %}}
{{% include 'includes/header.html' %}}
{{% endblock %}}

{{% block content %}}
{content}
{{% endblock %}}'''
    
    elif layout_type == 'docs':
        template = f'''{{% extends "layouts/docs.html" %}}

{{% block title %}}{extract_title(old_file)}{{% endblock %}}

{{% block navigation %}}
{{% set active_nav = '{active_nav}' %}}
{{% include 'includes/header.html' %}}
{{% endblock %}}

{{% set sidebar_type = '{sidebar_type}' %}}

{{% block doc_content %}}
{content}
{{% endblock %}}'''
    
    return template

def migrate_all_pages():
    """Process all HTML files based on layout mapping"""
    layout_map = {
        'index.html': ('base', 'home', None),
        'components.html': ('docs', 'components', 'components'),
        'protocols.html': ('docs', 'protocols', 'protocols'),
        'documentation.html': ('docs', 'documentation', 'documentation'),
        'examples.html': ('docs', 'documentation', 'examples'),
        'learning-path.html': ('docs', 'documentation', 'learning'),
        'sovereign-ai.html': ('docs', 'sovereign-ai', 'sovereign')
    }

    html_files = [f for f in os.listdir('.') if f.endswith('.html') and not f.startswith('new_')]

    for html_file in html_files:
        if html_file in layout_map:
            layout, active_nav, sidebar = layout_map[html_file]
        else:
            layout, active_nav, sidebar = ('base', None, None)

        if Path(html_file).exists():
            new_content = create_new_template(html_file, layout, active_nav, sidebar)
            with open(f"new_{html_file}", 'w') as f:
                f.write(new_content)
            print(f"✅ Migrated {html_file}")

if __name__ == "__main__":
    # Clean up old new_ files before running
    for f in Path('.').glob('new_*.html'):
        os.remove(f)
    migrate_all_pages()