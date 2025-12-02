#!/usr/bin/env python3
"""Test Dashboard API startup"""

import sys
sys.path.insert(0, '/home/yogapad/empirical-ai/empirica')

try:
    from empirica.api.app import create_app
    app = create_app()
    print("✅ API created successfully")
    print("\n📍 Registered Routes:")
    for rule in app.url_map.iter_rules():
        if 'api' in str(rule) or 'health' in str(rule):
            print(f"  {rule.rule} [{', '.join(rule.methods - {'OPTIONS', 'HEAD'})}]")
    print("\n✨ Dashboard API is ready to serve!")
except Exception as e:
    print(f"❌ Error creating API: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
