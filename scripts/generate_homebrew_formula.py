#!/usr/bin/env python3
"""
Generate complete Homebrew formula with all dependencies.

This script:
1. Reads requirements.txt
2. Fetches SHA256 hashes for each dependency from PyPI
3. Generates a complete Homebrew formula with all resources
4. Updates the main package SHA256

Usage:
    python3 scripts/generate_homebrew_formula.py
"""

import re
import sys
import hashlib
import subprocess
from pathlib import Path
from urllib.request import urlopen
from urllib.error import URLError

def get_package_info_from_pypi(package_name, version=None):
    """Fetch package info from PyPI JSON API."""
    try:
        url = f"https://pypi.org/pypi/{package_name}/json"
        with urlopen(url, timeout=10) as response:
            import json
            data = json.loads(response.read().decode())
            
        if version:
            release = data['releases'].get(version)
            if not release:
                print(f"⚠️  Version {version} not found for {package_name}")
                return None
        else:
            version = data['info']['version']
            release = data['releases'][version]
        
        # Find source distribution (.tar.gz)
        for file_info in release:
            if file_info['packagetype'] == 'sdist':
                return {
                    'name': package_name,
                    'version': version,
                    'url': file_info['url'],
                    'sha256': file_info['digests']['sha256']
                }
        
        print(f"⚠️  No source distribution found for {package_name}")
        return None
    except (URLError, KeyError, json.JSONDecodeError) as e:
        print(f"❌ Error fetching {package_name}: {e}")
        return None


def parse_requirements(requirements_file):
    """Parse requirements.txt and extract package names with version constraints."""
    packages = []
    with open(requirements_file) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            # Extract package name and version
            match = re.match(r'^([a-zA-Z0-9_-]+)([>=<]+)?([0-9.]+)?', line)
            if match:
                name = match.group(1)
                operator = match.group(2)
                version = match.group(3)
                packages.append({'name': name, 'version': version})
    
    return packages


def generate_resource_stanza(package_info):
    """Generate Homebrew resource stanza."""
    return f'''  resource "{package_info['name']}" do
    url "{package_info['url']}"
    sha256 "{package_info['sha256']}"
  end
'''


def main():
    project_root = Path(__file__).parent.parent
    requirements_file = project_root / "requirements.txt"
    formula_template = project_root / "packaging/homebrew/empirica.rb"
    
    print("🍺 Generating Homebrew Formula for Empirica")
    print("=" * 50)
    
    # Get main package SHA256
    dist_dir = project_root / "dist"
    tarball = list(dist_dir.glob("empirica-*.tar.gz"))
    if not tarball:
        print("❌ No tarball found in dist/. Run 'python -m build' first.")
        sys.exit(1)
    
    with open(tarball[0], 'rb') as f:
        main_sha256 = hashlib.sha256(f.read()).hexdigest()
    
    print(f"✅ Main package SHA256: {main_sha256}")
    
    # Parse requirements
    print(f"\n📦 Parsing {requirements_file}...")
    packages = parse_requirements(requirements_file)
    print(f"Found {len(packages)} dependencies")
    
    # Fetch dependency info from PyPI
    print("\n🔍 Fetching dependency info from PyPI...")
    resources = []
    for pkg in packages:
        print(f"  - {pkg['name']}...", end='')
        info = get_package_info_from_pypi(pkg['name'], pkg.get('version'))
        if info:
            resources.append(info)
            print(f" ✅ {info['version']}")
        else:
            print(" ❌ Failed")
    
    # Generate resource stanzas
    print(f"\n✨ Generating formula with {len(resources)} resources...")
    resource_stanzas = '\n'.join(generate_resource_stanza(r) for r in resources)
    
    # Read template and update
    with open(formula_template) as f:
        formula_content = f.read()
    
    # Update SHA256
    formula_content = re.sub(
        r'sha256 "[a-f0-9]{64}"',
        f'sha256 "{main_sha256}"',
        formula_content,
        count=1
    )
    
    # Replace placeholder resources section
    formula_content = re.sub(
        r'  # Runtime Python dependencies.*?# Add more resources as needed - see requirements\.txt',
        f'  # Runtime Python dependencies (auto-generated)\n{resource_stanzas}\n  # End auto-generated resources',
        formula_content,
        flags=re.DOTALL
    )
    
    # Write updated formula
    output_file = project_root / "packaging/homebrew/empirica-generated.rb"
    with open(output_file, 'w') as f:
        f.write(formula_content)
    
    print(f"\n✅ Formula generated: {output_file}")
    print("\nNext steps:")
    print("  1. Review the generated formula")
    print("  2. Test locally: brew install --build-from-source ./packaging/homebrew/empirica-generated.rb")
    print("  3. Create a tap repository: brew tap empirica/tap")
    print("  4. Submit to Homebrew core (optional)")


if __name__ == '__main__':
    main()
