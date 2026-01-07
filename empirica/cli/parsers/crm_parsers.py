"""CRM module command parsers."""


def add_crm_parsers(subparsers):
    """Add CRM command parsers (crm subcommand group)."""

    # CRM subcommand group
    crm_parser = subparsers.add_parser('crm', help='CRM - Client Relationship Management')
    crm_subparsers = crm_parser.add_subparsers(dest='crm_command', help='CRM commands')

    # client-create
    client_create = crm_subparsers.add_parser('client-create', help='Create a new client')
    client_create.add_argument('--name', required=True, help='Client name')
    client_create.add_argument('--description', help='Client description')
    client_create.add_argument('--notebooklm', help='NotebookLM URL for this client')
    client_create.add_argument('--type', dest='client_type', default='prospect',
                               choices=['prospect', 'active', 'partner', 'churned'],
                               help='Client type (default: prospect)')
    client_create.add_argument('--industry', help='Industry classification')
    client_create.add_argument('--contacts', help='JSON array of contacts: [{name, email, role}]')
    client_create.add_argument('--tags', help='JSON array of tags')
    client_create.add_argument('--next-action', help='Next action to take')
    client_create.add_argument('--output', choices=['human', 'json'], default='json',
                               help='Output format')

    # client-list
    client_list = crm_subparsers.add_parser('client-list', help='List clients')
    client_list.add_argument('--status', choices=['active', 'inactive', 'archived'],
                             help='Filter by status')
    client_list.add_argument('--type', dest='client_type',
                             choices=['prospect', 'active', 'partner', 'churned'],
                             help='Filter by client type')
    client_list.add_argument('--limit', type=int, default=50, help='Max clients to show')
    client_list.add_argument('--output', choices=['human', 'json'], default='json',
                             help='Output format')

    # client-show
    client_show = crm_subparsers.add_parser('client-show', help='Show client details')
    client_show.add_argument('--client-id', required=True, help='Client ID')
    client_show.add_argument('--include-engagements', action='store_true',
                             help='Include active engagements')
    client_show.add_argument('--output', choices=['human', 'json'], default='json',
                             help='Output format')

    # client-update
    client_update = crm_subparsers.add_parser('client-update', help='Update client')
    client_update.add_argument('--client-id', required=True, help='Client ID')
    client_update.add_argument('--name', help='New name')
    client_update.add_argument('--description', help='New description')
    client_update.add_argument('--notebooklm', help='New NotebookLM URL')
    client_update.add_argument('--type', dest='client_type',
                               choices=['prospect', 'active', 'partner', 'churned'],
                               help='New type')
    client_update.add_argument('--industry', help='New industry')
    client_update.add_argument('--status', choices=['active', 'inactive', 'archived'],
                               help='New status')
    client_update.add_argument('--add-contact', help='Contact to add: {name, email, role}')
    client_update.add_argument('--add-tag', help='Tag to add')
    client_update.add_argument('--next-action', help='Next action')
    client_update.add_argument('--output', choices=['human', 'json'], default='json',
                               help='Output format')

    # client-archive
    client_archive = crm_subparsers.add_parser('client-archive', help='Archive a client')
    client_archive.add_argument('--client-id', required=True, help='Client ID to archive')
    client_archive.add_argument('--output', choices=['human', 'json'], default='json',
                                help='Output format')

    # client-bootstrap
    client_bootstrap = crm_subparsers.add_parser('client-bootstrap',
                                                  help='Get client context for AI grounding')
    client_bootstrap.add_argument('--client-id', required=True, help='Client ID')
    client_bootstrap.add_argument('--output', choices=['human', 'json'], default='json',
                                  help='Output format')
