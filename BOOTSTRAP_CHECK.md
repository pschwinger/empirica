# Bootstrap Usage Check

## Question: Is bootstrap actually required or optional?

### Check 1: MCP Tools


### Check 2: Workflow Commands



## Analysis:

If workflow commands work without bootstrap (just need session_id), then:
- ✅ Bootstrap is OPTIONAL (convenience only)
- ✅ Can be removed safely
- ✅ Commands create/use sessions directly

If workflow commands REQUIRE bootstrap first, then:
- ❌ Bootstrap is REQUIRED
- ❌ Cannot be removed
- ❌ Need to keep it

Let me verify by checking if commands create sessions...

