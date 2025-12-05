# Bootstrap Removal - ONLY Bootstrap

## Decision: Keep All Commands Except Bootstrap

### What We're Removing:
❌ bootstrap command (serves no purpose - sessions auto-created)

### What We're KEEPING:
✅ ALL checkpoint commands (needed for CASCADE/git state)
✅ ALL identity commands (Phase 2 crypto)
✅ ALL investigation commands (CASCADE workflow)
✅ ALL utility commands (they serve purposes)
✅ ALL workflow commands (core functionality)

## Reason:
Commands map CASCADE states to git and enable deeper integration.
Bootstrap is the ONLY thing that's pure theater (just creates sessions).

## Implementation:
1. Remove bootstrap CLI command
2. Remove bootstrap.py file
3. Make commands auto-create sessions if needed
4. Update docs to remove bootstrap references

## Starting...
