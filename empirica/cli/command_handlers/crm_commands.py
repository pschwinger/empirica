"""
CRM Command Handlers

Handles CLI commands for client relationship management.
"""

import json
import logging
from datetime import datetime
from ..cli_utils import handle_cli_error, print_header

logger = logging.getLogger(__name__)


def handle_crm_command(args):
    """Route CRM subcommands to appropriate handlers."""
    crm_command = getattr(args, 'crm_command', None)

    if not crm_command:
        print("Usage: empirica crm <command>")
        print("\nCommands:")
        print("  client-create   Create a new client")
        print("  client-list     List clients")
        print("  client-show     Show client details")
        print("  client-update   Update client")
        print("  client-archive  Archive a client")
        print("  client-bootstrap Get client context for AI grounding")
        return

    handlers = {
        'client-create': handle_client_create,
        'client-list': handle_client_list,
        'client-show': handle_client_show,
        'client-update': handle_client_update,
        'client-archive': handle_client_archive,
        'client-bootstrap': handle_client_bootstrap,
    }

    handler = handlers.get(crm_command)
    if handler:
        handler(args)
    else:
        print(f"Unknown CRM command: {crm_command}")


def handle_client_create(args):
    """Create a new client."""
    try:
        from empirica.modules.crm import ClientStore

        # Parse optional JSON fields
        contacts = None
        if args.contacts:
            try:
                contacts = json.loads(args.contacts)
            except json.JSONDecodeError:
                if hasattr(args, 'output') and args.output == 'json':
                    print(json.dumps({"ok": False, "error": "Invalid JSON in --contacts"}))
                else:
                    print("Error: Invalid JSON in --contacts")
                return

        tags = None
        if args.tags:
            try:
                tags = json.loads(args.tags)
            except json.JSONDecodeError:
                if hasattr(args, 'output') and args.output == 'json':
                    print(json.dumps({"ok": False, "error": "Invalid JSON in --tags"}))
                else:
                    print("Error: Invalid JSON in --tags")
                return

        store = ClientStore()
        try:
            client = store.create(
                name=args.name,
                description=getattr(args, 'description', None),
                notebooklm_url=getattr(args, 'notebooklm', None),
                contacts=contacts,
                client_type=getattr(args, 'client_type', 'prospect'),
                industry=getattr(args, 'industry', None),
                tags=tags,
                next_action=getattr(args, 'next_action', None),
            )

            if hasattr(args, 'output') and args.output == 'json':
                print(json.dumps({
                    "ok": True,
                    "client_id": client.client_id,
                    "name": client.name,
                    "message": f"Created client: {client.name}"
                }))
            else:
                print_header("✓ Client Created")
                print(f"\nClient ID: {client.client_id}")
                print(f"Name: {client.name}")
                if client.client_type:
                    print(f"Type: {client.client_type}")
                if client.notebooklm_url:
                    print(f"NotebookLM: {client.notebooklm_url}")

        finally:
            store.close()

    except Exception as e:
        if hasattr(args, 'output') and args.output == 'json':
            print(json.dumps({"ok": False, "error": str(e)}))
        else:
            print(f"Error: {e}")


def handle_client_list(args):
    """List clients with optional filtering."""
    try:
        from empirica.modules.crm import ClientStore

        store = ClientStore()
        try:
            clients = store.list(
                status=getattr(args, 'status', None),
                client_type=getattr(args, 'client_type', None),
                limit=getattr(args, 'limit', 50),
            )

            if hasattr(args, 'output') and args.output == 'json':
                print(json.dumps({
                    "ok": True,
                    "clients": [c.to_dict() for c in clients],
                    "count": len(clients)
                }))
            else:
                print_header("📋 Clients")
                if not clients:
                    print("\n📭 No clients found")
                    print("💡 Create a client with: empirica crm client-create --name 'Company'")
                else:
                    print(f"\nFound {len(clients)} clients:\n")
                    for c in clients:
                        status_icon = "🟢" if c.status == "active" else "🔴" if c.status == "archived" else "⚪"
                        type_label = f"[{c.client_type}]" if c.client_type else ""
                        print(f"  {status_icon} {c.name} {type_label}")
                        print(f"     ID: {c.client_id[:8]}...")
                        if c.next_action:
                            print(f"     Next: {c.next_action}")
                        print()

        finally:
            store.close()

    except Exception as e:
        if hasattr(args, 'output') and args.output == 'json':
            print(json.dumps({"ok": False, "error": str(e)}))
        else:
            print(f"Error: {e}")


def handle_client_show(args):
    """Show client details."""
    try:
        from empirica.modules.crm import ClientStore

        store = ClientStore()
        try:
            client = store.get(args.client_id)

            if client is None:
                if hasattr(args, 'output') and args.output == 'json':
                    print(json.dumps({"ok": False, "error": "Client not found"}))
                else:
                    print(f"Client not found: {args.client_id}")
                return

            if hasattr(args, 'output') and args.output == 'json':
                result = {"ok": True, "client": client.to_dict()}
                # TODO: Add engagements if --include-engagements
                print(json.dumps(result))
            else:
                print_header(f"📇 {client.name}")
                print(f"\nID: {client.client_id}")
                print(f"Type: {client.client_type}")
                print(f"Status: {client.status}")

                if client.description:
                    print(f"\nDescription: {client.description}")

                if client.industry:
                    print(f"Industry: {client.industry}")

                if client.notebooklm_url:
                    print(f"\nNotebookLM: {client.notebooklm_url}")

                if client.contacts:
                    print("\nContacts:")
                    for contact in client.contacts:
                        print(f"  - {contact.get('name', 'Unknown')}")
                        if contact.get('email'):
                            print(f"    Email: {contact['email']}")
                        if contact.get('role'):
                            print(f"    Role: {contact['role']}")

                if client.tags:
                    print(f"\nTags: {', '.join(client.tags)}")

                print(f"\n📊 Epistemic State:")
                print(f"  Relationship Health: {client.relationship_health:.2f}")
                print(f"  Knowledge Depth: {client.knowledge_depth:.2f}")

                if client.next_action:
                    print(f"\n⏭️ Next Action: {client.next_action}")

        finally:
            store.close()

    except Exception as e:
        if hasattr(args, 'output') and args.output == 'json':
            print(json.dumps({"ok": False, "error": str(e)}))
        else:
            print(f"Error: {e}")


def handle_client_update(args):
    """Update client fields."""
    try:
        from empirica.modules.crm import ClientStore

        # Parse add_contact if provided
        add_contact = None
        if getattr(args, 'add_contact', None):
            try:
                add_contact = json.loads(args.add_contact)
            except json.JSONDecodeError:
                if hasattr(args, 'output') and args.output == 'json':
                    print(json.dumps({"ok": False, "error": "Invalid JSON in --add-contact"}))
                else:
                    print("Error: Invalid JSON in --add-contact")
                return

        store = ClientStore()
        try:
            client = store.update(
                client_id=args.client_id,
                name=getattr(args, 'name', None),
                description=getattr(args, 'description', None),
                notebooklm_url=getattr(args, 'notebooklm', None),
                client_type=getattr(args, 'client_type', None),
                industry=getattr(args, 'industry', None),
                status=getattr(args, 'status', None),
                next_action=getattr(args, 'next_action', None),
                add_contact=add_contact,
                add_tag=getattr(args, 'add_tag', None),
            )

            if client is None:
                if hasattr(args, 'output') and args.output == 'json':
                    print(json.dumps({"ok": False, "error": "Client not found"}))
                else:
                    print(f"Client not found: {args.client_id}")
                return

            if hasattr(args, 'output') and args.output == 'json':
                print(json.dumps({
                    "ok": True,
                    "client_id": client.client_id,
                    "name": client.name,
                    "message": f"Updated client: {client.name}"
                }))
            else:
                print(f"✓ Updated client: {client.name}")

        finally:
            store.close()

    except Exception as e:
        if hasattr(args, 'output') and args.output == 'json':
            print(json.dumps({"ok": False, "error": str(e)}))
        else:
            print(f"Error: {e}")


def handle_client_archive(args):
    """Archive a client (soft delete)."""
    try:
        from empirica.modules.crm import ClientStore

        store = ClientStore()
        try:
            success = store.archive(args.client_id)

            if not success:
                if hasattr(args, 'output') and args.output == 'json':
                    print(json.dumps({"ok": False, "error": "Client not found"}))
                else:
                    print(f"Client not found: {args.client_id}")
                return

            if hasattr(args, 'output') and args.output == 'json':
                print(json.dumps({
                    "ok": True,
                    "client_id": args.client_id,
                    "message": "Client archived"
                }))
            else:
                print(f"✓ Archived client: {args.client_id}")

        finally:
            store.close()

    except Exception as e:
        if hasattr(args, 'output') and args.output == 'json':
            print(json.dumps({"ok": False, "error": str(e)}))
        else:
            print(f"Error: {e}")


def handle_client_bootstrap(args):
    """Get client context for AI grounding."""
    try:
        from empirica.modules.crm import ClientStore

        store = ClientStore()
        try:
            client = store.get(args.client_id)

            if client is None:
                if hasattr(args, 'output') and args.output == 'json':
                    print(json.dumps({"ok": False, "error": "Client not found"}))
                else:
                    print(f"Client not found: {args.client_id}")
                return

            # Build bootstrap context
            bootstrap = {
                "ok": True,
                "client": {
                    "client_id": client.client_id,
                    "name": client.name,
                    "description": client.description,
                    "notebooklm_url": client.notebooklm_url,
                    "contacts": client.contacts,
                    "client_type": client.client_type,
                    "industry": client.industry,
                    "tags": client.tags,
                    "relationship_health": client.relationship_health,
                    "knowledge_depth": client.knowledge_depth,
                },
                "active_engagements": [],  # TODO: Load from engagements table
                "client_memory": {
                    "findings": [],  # TODO: Load from client_findings
                    "unknowns": [],  # TODO: Load from client_unknowns
                },
                "recent_interactions": [],  # TODO: Load from client_interactions
                "next_action": client.next_action,
            }

            if hasattr(args, 'output') and args.output == 'json':
                print(json.dumps(bootstrap))
            else:
                print_header(f"🚀 Client Bootstrap: {client.name}")
                print(f"\nClient ID: {client.client_id}")
                print(f"Type: {client.client_type}")
                print(f"Status: {client.status}")

                if client.notebooklm_url:
                    print(f"\n📚 NotebookLM: {client.notebooklm_url}")

                print(f"\n📊 Epistemic State:")
                print(f"  Relationship Health: {client.relationship_health:.2f}")
                print(f"  Knowledge Depth: {client.knowledge_depth:.2f}")

                if client.next_action:
                    print(f"\n⏭️ Next Action: {client.next_action}")

        finally:
            store.close()

    except Exception as e:
        if hasattr(args, 'output') and args.output == 'json':
            print(json.dumps({"ok": False, "error": str(e)}))
        else:
            print(f"Error: {e}")
