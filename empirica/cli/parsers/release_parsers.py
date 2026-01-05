"""Release command parsers."""


def add_release_parsers(subparsers):
    """Add release command parsers"""
    # Release readiness check
    release_parser = subparsers.add_parser(
        'release-ready',
        help='Epistemic release assessment - verifies version sync, architecture health, security, and documentation'
    )
    release_parser.add_argument(
        '--project-root',
        help='Root directory of the project (default: current directory)'
    )
    release_parser.add_argument(
        '--quick',
        action='store_true',
        help='Quick check (skip architecture assessment)'
    )
    release_parser.add_argument(
        '--output',
        choices=['human', 'json'],
        default='human',
        help='Output format'
    )

    # Docs assessment
    docs_parser = subparsers.add_parser(
        'docs-assess',
        help='Epistemic documentation assessment - measures docs coverage against actual features'
    )
    docs_parser.add_argument(
        '--project-root',
        help='Root directory of the project (default: current directory)'
    )
    docs_parser.add_argument(
        '--verbose',
        action='store_true',
        help='Show detailed undocumented items'
    )
    docs_parser.add_argument(
        '--output',
        choices=['human', 'json'],
        default='human',
        help='Output format'
    )
