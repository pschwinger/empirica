#!/usr/bin/env python3
import json
import os
import shutil
from pathlib import Path
import jinja2
from jsonschema import validate, ValidationError

class WebsiteBuilder:
    def __init__(self):
        self.env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))
        self.load_schemas()
        self.setup_filters()
    
    def load_schemas(self):
        """Load JSON schemas for validation"""
        with open('schemas/page-schema.json') as f:
            self.page_schema = json.load(f)
        with open('schemas/site-config.json') as f:
            self.site_config = json.load(f)
    
    def setup_filters(self):
        """Add custom Jinja2 filters"""
        self.env.filters['markdown'] = lambda x: f"<!-- markdown: {x} -->"
        self.env.filters['active_nav'] = self.active_nav_filter
    
    def active_nav_filter(self, current, target):
        """Highlight active navigation"""
        return 'active' if current == target else ''
    
    def validate_page(self, page_data):
        """Validate page against schema"""
        try:
            validate(instance=page_data, schema=self.page_schema)
            return True, "Valid"
        except ValidationError as e:
            return False, str(e)
    
    def build_page(self, page_file):
        """Build a single page"""
        with open(f"content/{page_file}") as f:
            page_data = json.load(f)
        
        # Validate
        is_valid, message = self.validate_page(page_data)
        if not is_valid:
            print(f"❌ Validation failed for {page_file}: {message}")
            return False
        
        # Merge with site config
        page_data.update(self.site_config)
        
        # Select layout
        layout = f"layouts/{page_data['layout']}.html"
        
        # Render
        template = self.env.get_template(layout)
        html = template.render(**page_data)
        
        # Write to dist
        output_file = f"dist/{page_data['page_id']}.html"
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        with open(output_file, 'w') as f:
            f.write(html)
        
        print(f"✅ Built {output_file}")
        return True
    
    def build_all(self):
        """Build entire site"""
        if os.path.exists('dist'):
            shutil.rmtree('dist')
        shutil.copytree('assets', 'dist/assets')
        
        success_count = 0
        for page_file in Path('content').glob('*.json'):
            if self.build_page(page_file.name):
                success_count += 1
        
        print(f"\n✅ Built {success_count} pages successfully!")
        return success_count

if __name__ == "__main__":
    builder = WebsiteBuilder()
    builder.build_all()
