#!/usr/bin/env python3
"""
🔗 Links Helper - Centralized Link Management
Manages all links across the template system for easy testing and updates
"""

import json
from pathlib import Path

class LinksHelper:
    """Centralized link management for template system"""
    
    def __init__(self, links_config_path="components/links_config.json"):
        self.links_config_path = Path(links_config_path)
        self.links = self._load_links_config()
    
    def _load_links_config(self):
        """Load links configuration from JSON"""
        try:
            with open(self.links_config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"⚠️ Links config not found: {self.links_config_path}")
            return {}
    
    def get_internal_link(self, key):
        """Get internal site link"""
        return self.links.get("internal_links", {}).get(key, f"#{key}")
    
    def get_external_link(self, key):
        """Get external link"""
        return self.links.get("external_links", {}).get(key, f"#{key}")
    
    def get_documentation_link(self, key):
        """Get documentation link"""
        return self.links.get("documentation_links", {}).get(key, f"#{key}")
    
    def get_research_diagram(self, key):
        """Get research diagram path"""
        return self.links.get("research_diagrams", {}).get(key, f"#{key}")
    
    def get_interactive_figure(self, key):
        """Get interactive figure link"""
        return self.links.get("interactive_figures", {}).get(key, f"#{key}")
    
    def get_all_links(self):
        """Get all links for testing"""
        all_links = {}
        for category, links in self.links.items():
            if isinstance(links, dict):
                # Handle nested dictionaries (like link_patterns)
                for key, value in links.items():
                    if isinstance(value, str):
                        all_links[f"{category}_{key}"] = value
                    elif isinstance(value, dict):
                        for subkey, subvalue in value.items():
                            all_links[f"{category}_{key}_{subkey}"] = subvalue
        return all_links
    
    def validate_links(self):
        """Validate all links and return report"""
        all_links = self.get_all_links()
        report = {
            "total_links": len(all_links),
            "internal_links": [],
            "external_links": [],
            "file_links": [],
            "anchor_links": []
        }
        
        for key, url in all_links.items():
            if url.startswith("http"):
                report["external_links"].append({"key": key, "url": url})
            elif url.startswith("/"):
                if url.endswith((".html", ".md", ".svg", ".json")):
                    report["file_links"].append({"key": key, "url": url})
                else:
                    report["internal_links"].append({"key": key, "url": url})
            elif url.startswith("#"):
                report["anchor_links"].append({"key": key, "url": url})
        
        return report
    
    def generate_links_test_page(self):
        """Generate HTML page for testing all links"""
        all_links = self.get_all_links()
        
        html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Links Test Page - Empirica</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-50 p-8">
    <div class="max-w-4xl mx-auto">
        <h1 class="text-3xl font-bold text-gray-800 mb-8">🔗 Links Test Page</h1>
        <p class="text-gray-600 mb-8">Test all links in one place to ensure they work correctly.</p>
        
        <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
"""
        
        for key, url in all_links.items():
            status_class = "border-blue-200 hover:bg-blue-50" if not url.startswith("#") else "border-red-200 bg-red-50"
            
            html += f"""
            <a href="{url}" class="bg-white border {status_class} rounded-lg p-4 block transition-colors">
                <h3 class="font-semibold text-gray-800 mb-1">{key}</h3>
                <p class="text-sm text-gray-600">{url}</p>
            </a>
"""
        
        html += """
        </div>
        
        <div class="mt-8 bg-white rounded-lg p-6 border border-gray-200">
            <h2 class="text-xl font-bold text-gray-800 mb-4">🧪 Link Testing Instructions</h2>
            <ul class="text-gray-700 space-y-2">
                <li>• <strong>Blue borders:</strong> Should open correctly</li>
                <li>• <strong>Red borders:</strong> Placeholder links (need fixing)</li>
                <li>• Test each link to verify it works</li>
                <li>• Update <code class="bg-gray-100 px-2 py-1 rounded">links_config.json</code> for any broken links</li>
                <li>• Regenerate templates after link changes</li>
            </ul>
        </div>
    </div>
</body>
</html>
"""
        return html

# Example usage
if __name__ == "__main__":
    links = LinksHelper()
    
    # Generate test page
    test_html = links.generate_links_test_page()
    with open("../links_test.html", "w") as f:
        f.write(test_html)
    
    # Validation report
    report = links.validate_links()
    print("🔗 Links Validation Report:")
    print(f"   📊 Total links: {report['total_links']}")
    print(f"   🌐 External links: {len(report['external_links'])}")
    print(f"   📄 File links: {len(report['file_links'])}")
    print(f"   ⚙️ Internal links: {len(report['internal_links'])}")
    print(f"   ⚠️ Anchor placeholders: {len(report['anchor_links'])}")