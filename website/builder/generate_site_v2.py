import os
import json
import re
import shutil
from pathlib import Path
import markdown
from jinja2 import Environment, FileSystemLoader

import argparse

# Parse command line arguments
parser = argparse.ArgumentParser(description='Generate Empirica website.')
parser.add_argument('--content-dir', type=str, default="../content", help='Path to content directory')
parser.add_argument('--output-dir', type=str, default="../output_v2", help='Path to output directory')
args = parser.parse_args()

# Configuration
CONTENT_DIR = Path(args.content_dir)
OUTPUT_DIR = Path(args.output_dir)
TEMPLATE_DIR = Path("templates")
LINKS_CONFIG_PATH = Path("links_config.json")

# Ensure output directory exists
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Copy Assets
ASSETS_DIR = Path("../assets")
OUTPUT_ASSETS_DIR = OUTPUT_DIR / "assets"
if ASSETS_DIR.exists():
    if OUTPUT_ASSETS_DIR.exists():
        shutil.rmtree(OUTPUT_ASSETS_DIR)
    shutil.copytree(ASSETS_DIR, OUTPUT_ASSETS_DIR)
    print(f"✅ Copied assets to {OUTPUT_ASSETS_DIR}")

# Load Links Config
with open(LINKS_CONFIG_PATH, 'r') as f:
    LINKS_CONFIG = json.load(f)

# Setup Jinja2
env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

from bs4 import BeautifulSoup

def process_markdown_file(filename):
    """Load and parse markdown file, replacing ASCII diagrams with SVGs."""
    path = CONTENT_DIR / filename
    if not path.exists():
        print(f"⚠️ Warning: Content file not found: {filename}")
        return ""
    with open(path, 'r') as f:
        content = f.read()
        
    # Replace Architecture Diagram
    # Simple approach: find the code block and replace it
    if "USER INTERACTION LAYER" in content and "PERSISTENCE LAYER" in content:
        # Find the start and end of the code block
        start_marker = "```\n┌"
        end_marker = "```"
        
        start_idx = content.find(start_marker)
        if start_idx != -1:
            # Find the closing backticks after the diagram
            end_idx = content.find(end_marker, start_idx + len(start_marker))
            if end_idx != -1:
                # Replace the entire code block
                diagram_block = content[start_idx:end_idx + len(end_marker)]
                replacement = '\n![Empirica Architecture](/assets/diagrams/architecture-overview.svg)\n'
                content = content.replace(diagram_block, replacement)
        
    return content

def extract_metadata(md_content):
    """Extracts title (H1) and description (first paragraph) from markdown."""
    lines = md_content.split('\n')
    title = "Empirica"
    description = "The meta-framework for AI self-awareness."
    
    # Find H1
    for i, line in enumerate(lines):
        if line.startswith('# '):
            title = line.replace('# ', '').strip()
            # Look for description in next few lines
            for j in range(i + 1, min(i + 10, len(lines))):
                if lines[j].strip() and not lines[j].startswith('#') and not lines[j].startswith('['):
                    # Strip markdown formatting from description
                    desc = lines[j].strip()
                    # Remove ** for bold
                    desc = desc.replace('**', '')
                    # Remove * for italic
                    desc = desc.replace('*', '')
                    # Remove ` for inline code
                    desc = desc.replace('`', '')
                    description = desc
                    break
            break
            
    # Remove H1 from content to avoid duplication
    filtered_lines = [line for line in lines if not line.startswith('# ' + title)]
    return title, description, '\n'.join(filtered_lines)

# replace_ascii_diagrams function removed as we handle it in markdown processing

def process_bento_content(md_content, split_by_h3=False):
    """Convert markdown content into a Bento Grid layout.
    
    Args:
        md_content: Markdown content to process
        split_by_h3: If True, split by H3 headers instead of H2
    """
    # Preprocess markdown to ensure lists render correctly
    # Add blank line before lists if missing
    lines = md_content.split('\n')
    processed_lines = []
    for i, line in enumerate(lines):
        # Check if this line starts a list (bullet or numbered)
        stripped = line.strip()
        is_list = (stripped.startswith(('-', '*', '+')) or 
                   (len(stripped) > 2 and stripped[0].isdigit() and stripped[1:3] in ['. ', ') ']))
        if is_list:
            # Check if previous line is not blank
            if i > 0 and processed_lines and processed_lines[-1].strip():
                # Add blank line before list
                processed_lines.append('')
        processed_lines.append(line)
    
    md_content = '\n'.join(processed_lines)
    
    # Split by H2 or H3 headers depending on flag
    if split_by_h3:
        sections = re.split(r'(^###\s+.*$)', md_content, flags=re.MULTILINE)
    else:
        sections = re.split(r'(^##\s+.*$)', md_content, flags=re.MULTILINE)
    
    html_output = '<div class="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 p-6">'
    
    # First chunk is usually intro text (before first H2)
    intro = sections[0].strip()
    if intro:
        # Remove H1 from intro since it's already in the page header
        intro_lines = intro.split('\n')
        filtered_intro = []
        skip_next_blank = False
        for line in intro_lines:
            if line.strip().startswith('# '):
                skip_next_blank = True
                continue
            if skip_next_blank and not line.strip():
                skip_next_blank = False
                continue
            filtered_intro.append(line)
        intro = '\n'.join(filtered_intro).strip()
        
        if intro:  # Only add panel if there's content after removing H1
            html = markdown.markdown(intro, extensions=['extra', 'attr_list', 'codehilite'])
            html_output += f'<div class="col-span-full glass-panel p-8 rounded-2xl mb-8 prose prose-invert prose-lg max-w-none">{html}</div>'
    
    # Process sections (H2 + content)
    for i in range(1, len(sections), 2):
        if i+1 >= len(sections):
            break
        header = sections[i].strip().replace('## ', '')
        content = sections[i+1].strip()
        
        # Convert content to HTML with extensions
        content_html = markdown.markdown(content, extensions=['extra', 'attr_list', 'codehilite'])
        # Note: link fixing will be done at page level, not here
        
        # Create a card with proper prose sizing and overflow handling
        html_output += f'''
        <div class="glass-card p-6 rounded-xl glow-effect flex flex-col h-full">
            <h3 class="text-xl font-bold text-indigo-400 mb-4 break-words">{header}</h3>
            <div class="prose prose-invert prose-lg max-w-none flex-grow overflow-hidden">
                <div class="break-words overflow-x-auto">
                    {content_html}
                </div>
            </div>
        </div>
        '''
    
    html_output += '</div>'
    return html_output

def generate_pages():
    """Generate all pages defined in links config."""
    
    nav_items = LINKS_CONFIG.get('navigation', [])
    
    # Map internal links to markdown files (reverse mapping logic or manual list)
    # We'll iterate through the known 18 files mapping
    page_mapping = {
        "index.html": "index.md",
        "epistemics.html": "epistemics.md",
        "features.html": "features.md",
        "use-cases.html": "use-cases.md",
        "developers/cli-interface.html": "developers/cli-interface.md",
        "mcp-integration.html": "mcp-integration.md",
        "skills.html": "skills.md",
        "developers/system-prompts.html": "developers/system-prompts.md",
        "developers/architecture.html": "developers/architecture.md",
        "developers/collaboration.html": "developers/collaboration.md",
        "ai-vs-agent.html": "ai_vs_agent.md",
        "developers/components.html": "developers/components.md",
        "getting-started.html": "getting-started.md",
        "developers/api-reference.html": "developers/api-reference.md",
        "examples.html": "examples.md",
        "faqs.html": "faqs.md",
        "contact.html": "contact.md",
        "docs.html": "docs.md",
        "MAKING_GIT_SEXY_AGAIN.html": "git-integration.md"
    }
    
    # Pages that are in developers/ subdirectory
    DEVELOPER_PAGES = {
        "architecture", "api-reference", "cli-interface", 
        "collaboration", "components", "system-prompts"
    }
    
    def fix_internal_links(content_html, current_page_path):
        """Fix internal markdown links to point to correct paths."""
        import re as regex_mod
        
        # Determine if current page is in developers/ folder
        is_in_developers = current_page_path.startswith("developers/")
        
        def replace_link(match):
            full_match = match.group(0)
            link_path = match.group(1)
            
            # Skip external links and anchors
            if link_path.startswith(('http://', 'https://', '#', '/')):
                return full_match
            
            # Extract base filename without .html or .md
            base_name = link_path.replace('.html', '').replace('.md', '')
            
            # Handle anchor links (e.g., examples.md#anchor)
            anchor = ''
            if '#' in base_name:
                base_name, anchor = base_name.split('#', 1)
                anchor = '#' + anchor
            
            # Check if this should be a developer page
            if base_name in DEVELOPER_PAGES:
                if is_in_developers:
                    # Already in developers/, use relative path
                    return f'href="{base_name}.html{anchor}"'
                else:
                    # Not in developers/, need to add prefix
                    return f'href="developers/{base_name}.html{anchor}"'
            else:
                # Not a developer page
                if is_in_developers:
                    # In developers/, need to go up
                    if not link_path.startswith('../'):
                        return f'href="../{base_name}.html{anchor}"'
                    else:
                        return full_match
                else:
                    # In root, use as-is (but convert .md to .html)
                    return f'href="{base_name}.html{anchor}"'
        
        # Fix all href links
        content_html = regex_mod.sub(r'href="([^"]+)"', replace_link, content_html)
        return content_html

    base_template = env.get_template("base.html")

    for html_filename, md_filename in page_mapping.items():
        print(f"Generating {html_filename}...")
        
        raw_md_content = process_markdown_file(md_filename)
        
        # Extract Metadata (H1 and description)
        page_title, page_description, body_md = extract_metadata(raw_md_content)
        
        # Remove first paragraph/description from ALL pages to avoid duplication with header
        # This handles both **bold** subtitles and regular paragraph descriptions
        body_lines = body_md.split('\n')
        filtered_body = []
        found_first_content = False
        skip_mode = True  # Start in skip mode to remove first paragraph
        
        for i, line in enumerate(body_lines):
            stripped = line.strip()
            
            # Skip empty lines at the start
            if not found_first_content and not stripped:
                continue
            
            # Skip the first paragraph (whether bold or not)
            if skip_mode:
                # If we hit a heading or HR, stop skipping
                if stripped.startswith(('#', '---', '```')):
                    skip_mode = False
                    found_first_content = True
                # If we hit an empty line after some content, we've passed the first paragraph
                elif found_first_content and not stripped:
                    skip_mode = False
                    continue
                # Mark that we've found content
                elif stripped:
                    found_first_content = True
                    continue
            
            filtered_body.append(line)
        
        body_md = '\n'.join(filtered_body)
        
        # Special Handling for Homepage
        if html_filename == "index.html":
            # Find where Foundation Infrastructure starts
            foundation_start = body_md.find('## Foundation Infrastructure')
            
            if foundation_start > -1:
                # Remove the "Foundation Infrastructure" H2 header itself
                # Find the end of that line
                foundation_line_end = body_md.find('\n', foundation_start)
                if foundation_line_end > -1:
                    # Remove just the H2 line
                    body_md = body_md[:foundation_start] + body_md[foundation_line_end+1:]
            
            # Process ALL content as standard markdown (no bento boxes)
            # Preprocess for lists
            lines = body_md.split('\n')
            processed_lines = []
            for i, line in enumerate(lines):
                stripped = line.strip()
                is_list = (stripped.startswith(('-', '*', '+')) or 
                           (len(stripped) > 2 and stripped[0].isdigit() and stripped[1:3] in ['. ', ') ']))
                if is_list:
                    if i > 0 and processed_lines and processed_lines[-1].strip():
                        processed_lines.append('')
                processed_lines.append(line)
            body_md = '\n'.join(processed_lines)
            
            # Convert to HTML
            content_html = markdown.markdown(body_md, extensions=['extra', 'attr_list', 'codehilite', 'md_in_html'])
            
            # Inject Hero Section (self-contained, no duplicate content)
            hero_html = '''
            <div class="relative overflow-hidden pt-24 pb-32">
                <div class="max-w-7xl mx-auto px-6 text-center relative z-10">
                    <div class="inline-flex items-center rounded-full border border-indigo-500/30 bg-indigo-500/10 px-3 py-1 text-sm font-medium text-indigo-300 backdrop-blur-sm mb-8">
                        <span class="flex h-2 w-2 rounded-full bg-indigo-500 mr-2 animate-pulse"></span>
                        Epistemic Self-Awareness for AI
                    </div>
                    <h1 class="text-6xl md:text-8xl font-bold tracking-tight mb-8 text-white">
                        We Gave AI a Mirror.<br/>
                        <span class="text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 to-cyan-400">Now It Can See Itself Think.</span>
                    </h1>
                    <p class="text-xl text-slate-300 max-w-2xl mx-auto mb-12">
                        <a href="/MAKING_GIT_SEXY_AGAIN.html" class="font-semibold text-white hover:text-indigo-300 transition-colors">Making Git Sexy Again Through Metacognition.</a><br/>
                        Empirica is the foundation infrastructure for epistemic self-aware AI — agents that genuinely know what they know.
                    </p>
                    <div class="flex flex-col sm:flex-row justify-center gap-6">
                        <a href="/mcp-integration.html" class="bg-indigo-600 hover:bg-indigo-500 text-white px-8 py-4 rounded-lg font-semibold transition-all hover:scale-105 shadow-lg shadow-indigo-500/25 flex items-center justify-center">
                            Try with MCP
                        </a>
                        <a href="/developers/cli-interface.html" class="glass-panel hover:bg-white/10 text-white px-8 py-4 rounded-lg font-semibold transition-all flex items-center justify-center">
                            Install CLI
                        </a>
                    </div>
                </div>
                
                <!-- Background Glow -->
                <div class="absolute top-0 left-1/2 -translate-x-1/2 w-full h-full max-w-7xl pointer-events-none">
                    <div class="absolute top-20 left-1/4 w-96 h-96 bg-indigo-500/10 rounded-full blur-3xl"></div>
                    <div class="absolute top-40 right-1/4 w-96 h-96 bg-cyan-500/10 rounded-full blur-3xl"></div>
                </div>
            </div>
            '''
            
            # Manual fix: Process markdown inside glass-card divs
            import re as regex_module
            def process_glass_card(match):
                full_div = match.group(0)
                content_match = regex_module.search(r'<div[^>]*>(.*?)</div>', full_div, regex_module.DOTALL)
                if content_match:
                    inner_content = content_match.group(1)
                    processed_inner = markdown.markdown(inner_content.strip(), extensions=['extra'])
                    opening_tag = regex_module.match(r'<div[^>]*>', full_div).group(0)
                    return opening_tag + '\n' + processed_inner + '\n</div>'
                return full_div
            
            content_html = regex_module.sub(
                r'<div class="glass-card[^>]*>.*?</div>',
                process_glass_card,
                content_html,
                flags=regex_module.DOTALL
            )
            
            # Fix links
            content_html = re.sub(r'href="([^"]+)\.md"', r'href="\1.html"', content_html)
            
            # Combine hero and content
            final_content = hero_html + f'''
            <div class="max-w-6xl mx-auto px-6 pb-20">
                <div class="prose prose-invert prose-lg max-w-none">
                    {content_html}
                </div>
            </div>
            '''
            
            # Render Template
            output_html = base_template.render(
                content=final_content,
                nav_items=LINKS_CONFIG['navigation'],
                title="Home",
                description=page_description,
                is_homepage=True
            )
            
        # Check for manual bento box tags in content
        # Users can wrap sections with <!-- BENTO_START --> and <!-- BENTO_END -->
        elif '<!-- BENTO_START -->' in body_md and '<!-- BENTO_END -->' in body_md:
            # Process content with manual bento sections
            parts = []
            remaining = body_md
            
            while '<!-- BENTO_START -->' in remaining:
                # Find bento section
                bento_start = remaining.find('<!-- BENTO_START -->')
                bento_end = remaining.find('<!-- BENTO_END -->')
                
                if bento_end == -1:
                    break
                
                # Extract parts
                before_bento = remaining[:bento_start]
                bento_content = remaining[bento_start + len('<!-- BENTO_START -->'):bento_end]
                
                # Process before as standard content
                if before_bento.strip():
                    before_html = markdown.markdown(before_bento, extensions=['extra', 'attr_list', 'codehilite'])
                    parts.append(f'''
                    <div class="max-w-4xl mx-auto px-6 py-12">
                        <div class="prose prose-invert prose-lg max-w-none">
                            {before_html}
                        </div>
                    </div>
                    ''')
                
                # Process bento section
                bento_html = process_bento_content(bento_content.strip(), split_by_h3=False)
                parts.append(bento_html)
                
                # Continue with remaining content
                remaining = remaining[bento_end + len('<!-- BENTO_END -->'):]
            
            # Process any remaining content
            if remaining.strip():
                remaining_html = markdown.markdown(remaining, extensions=['extra', 'attr_list', 'codehilite'])
                parts.append(f'''
                <div class="max-w-4xl mx-auto px-6 py-12">
                    <div class="prose prose-invert prose-lg max-w-none">
                        {remaining_html}
                    </div>
                </div>
                ''')
            
            final_content = ''.join(parts)
            
            # Fix internal links
            final_content = fix_internal_links(final_content, html_filename)
        
        # Special handling for components - only create bento boxes for the 11 components
        elif html_filename == "developers/components.html":
            # Split content to isolate "The 11 Components" section
            components_section_start = body_md.find('## The 11 Components')
            components_section_end = body_md.find('## Component Architecture')
            
            if components_section_start > -1 and components_section_end > -1:
                # Split into three parts: before, components, after
                before_components = body_md[:components_section_start].strip()
                components_section = body_md[components_section_start:components_section_end].strip()
                after_components = body_md[components_section_end:].strip()
                
                # Process before and after as standard content
                before_html = markdown.markdown(before_components, extensions=['extra', 'attr_list', 'codehilite']) if before_components else ''
                after_html = markdown.markdown(after_components, extensions=['extra', 'attr_list', 'codehilite']) if after_components else ''
                
                # Process components section as bento grid (split by H3)
                components_html = process_bento_content(components_section, split_by_h3=True)
                
                # Combine all parts
                final_content = f'''
                <div class="max-w-4xl mx-auto px-6 py-12">
                    <div class="prose prose-invert prose-lg max-w-none">
                        {before_html}
                    </div>
                </div>
                {components_html}
                <div class="max-w-4xl mx-auto px-6 py-12">
                    <div class="prose prose-invert prose-lg max-w-none">
                        {after_html}
                    </div>
                </div>
                '''
            else:
                # Fallback: treat as standard page
                final_content = f'''
                <div class="max-w-4xl mx-auto px-6 py-12">
                    <div class="prose prose-invert prose-lg max-w-none">
                        {markdown.markdown(body_md, extensions=['extra', 'attr_list', 'codehilite'])}
                    </div>
                </div>
                '''
            
            # Fix internal links
            final_content = fix_internal_links(final_content, html_filename)
            
            output_html = base_template.render(
                content=final_content,
                nav_items=LINKS_CONFIG['navigation'],
                title=page_title,
                description=page_description,
                page_title=page_title,
                page_description=page_description,
                is_homepage=False,
                breadcrumbs=[page_title]
            )
        
        else:
            # Standard Page Generation
            
            # Preprocess markdown to ensure lists render correctly
            lines = body_md.split('\n')
            processed_lines = []
            for i, line in enumerate(lines):
                stripped = line.strip()
                is_list = (stripped.startswith(('-', '*', '+')) or 
                           (len(stripped) > 2 and stripped[0].isdigit() and stripped[1:3] in ['. ', ') ']))
                if is_list:
                    if i > 0 and processed_lines and processed_lines[-1].strip():
                        processed_lines.append('')
                processed_lines.append(line)
            body_md = '\n'.join(processed_lines)
            
            # Convert Markdown to HTML
            content_html = markdown.markdown(body_md, extensions=['extra', 'attr_list', 'codehilite'])
            
            # Fix internal links
            content_html = fix_internal_links(content_html, html_filename)
            
            # Fix Links
            content_html = re.sub(r'href="([^"]+)\.md"', r'href="\1.html"', content_html)
            
            # Replace Diagrams - Handled in process_markdown_file
            # content_html = replace_ascii_diagrams(content_html)
            
            # Wrap in container (removed glass-panel to prevent nesting)
            final_content = f'''
            <div class="max-w-4xl mx-auto px-6 py-12">
                <div class="prose prose-invert prose-lg max-w-none">
                    {content_html}
                </div>
            </div>
            '''
            
            output_html = base_template.render(
                content=final_content,
                nav_items=LINKS_CONFIG['navigation'],
                title=page_title,
                description=page_description,
                page_title=page_title,
                page_description=page_description,
                is_homepage=False,
                breadcrumbs=[page_title]
            )
        
        # Write to file
        output_path = OUTPUT_DIR / html_filename
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            f.write(output_html)

    print("✅ All pages generated successfully.")

if __name__ == "__main__":
    generate_pages()
