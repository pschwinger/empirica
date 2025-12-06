#!/bin/bash
################################################################################
# EMPIRICA UNIFIED DASHBOARD
# Single command: ./empirica.sh
# Shows: Everything happening in Empirica right now
# Purpose: Single source of truth for decision making and tracking
#
# This is THE dashboard - combines status + leaderboard + tracking
# Use this to understand the system at a glance
################################################################################

set -e

export LC_ALL=C

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
WHITE='\033[1;37m'
NC='\033[0m'

# Options
VERBOSE=false
LEADERBOARD_ONLY=false
STATUS_ONLY=false
DIAGNOSTICS=false
JSON_OUTPUT=false

while [[ $# -gt 0 ]]; do
  case $1 in
    --leaderboard) LEADERBOARD_ONLY=true; shift ;;
    --status) STATUS_ONLY=true; shift ;;
    --diagnostics) DIAGNOSTICS=true; shift ;;
    --json) JSON_OUTPUT=true; shift ;;
    --verbose) VERBOSE=true; shift ;;
    *) shift ;;
  esac
done

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DB_PATH="$REPO_ROOT/.empirica/sessions/sessions.db"

if [ ! -f "$DB_PATH" ]; then
  DB_PATH="$HOME/.empirica/sessions/sessions.db"
  if [ ! -f "$DB_PATH" ]; then
    echo -e "${RED}ERROR: Database not found${NC}"
    exit 1
  fi
fi

################################################################################
# HELPER FUNCTIONS
################################################################################

get_db_count() {
  local query="$1"
  sqlite3 "$DB_PATH" "$query" 2>/dev/null || echo "0"
}

get_db_value() {
  local query="$1"
  sqlite3 "$DB_PATH" "$query" 2>/dev/null || echo ""
}

print_header() {
  echo -e "${CYAN}════════════════════════════════════════════════════════════════${NC}"
  echo -e "${CYAN}$1${NC}"
  echo -e "${CYAN}════════════════════════════════════════════════════════════════${NC}"
}

################################################################################
# SECTION 1: SYSTEM OVERVIEW (Always shown first)
################################################################################

print_header "EMPIRICA UNIFIED DASHBOARD - SYSTEM OVERVIEW"

# Get key metrics
TOTAL_SESSIONS=$(get_db_count "SELECT COUNT(*) FROM sessions;")
COMPLETED_SESSIONS=$(get_db_count "SELECT COUNT(*) FROM sessions WHERE end_time IS NOT NULL;")
ACTIVE_SESSIONS=$(get_db_count "SELECT COUNT(*) FROM sessions WHERE end_time IS NULL;")
TOTAL_GOALS=$(get_db_count "SELECT COUNT(*) FROM goals;")
COMPLETED_GOALS=$(get_db_count "SELECT COUNT(*) FROM goals WHERE is_completed=1;")
TOTAL_REFLEXES=$(get_db_count "SELECT COUNT(*) FROM reflexes;")

COMPLETION_PCT=$((COMPLETED_SESSIONS * 100 / TOTAL_SESSIONS))
GOAL_COMPLETION_PCT=$((COMPLETED_GOALS * 100 / TOTAL_GOALS))

echo -e "${WHITE}System Status:${NC} ✅ OPERATIONAL"
echo ""
echo "Sessions:      ${YELLOW}$TOTAL_SESSIONS${NC} total | ${GREEN}$COMPLETED_SESSIONS${NC} completed ($COMPLETION_PCT%) | ${MAGENTA}$ACTIVE_SESSIONS${NC} active"
echo "Goals:         ${YELLOW}$TOTAL_GOALS${NC} total | ${GREEN}$COMPLETED_GOALS${NC} completed ($GOAL_COMPLETION_PCT%)"
echo "Metrics:       ${CYAN}$TOTAL_REFLEXES${NC} epistemic vectors recorded"
echo "Git:           $(cd "$REPO_ROOT" && git rev-parse --abbrev-ref HEAD) | $(cd "$REPO_ROOT" && git log -1 --oneline | cut -d' ' -f1)"
echo ""

if [ "$STATUS_ONLY" = false ] && [ "$LEADERBOARD_ONLY" = false ]; then
  ################################################################################
  # SECTION 2: ACTIVE AIs - What's Running Right Now
  ################################################################################

  print_header "ACTIVE & RECENT AIs (Learning Measurement)"
  echo ""
  echo -e "${WHITE}Top Learning Performers:${NC}"

  sqlite3 "$DB_PATH" << 'EOSQL' 2>/dev/null | head -20 | while IFS='|' read -r ai_id learning sessions mastery; do
    if [ -n "$ai_id" ]; then
      printf "  %-30s Learning: %6s | Sessions: %2s | Mastery: %6s\n" \
        "$ai_id" "$learning" "$sessions" "$mastery"
    fi
  done << 'INNEREOF'
SELECT
  ai_id,
  ROUND(MAX(CASE WHEN phase='POSTFLIGHT' THEN know ELSE 0 END) -
        MAX(CASE WHEN phase='PREFLIGHT' THEN know ELSE 0 END), 3) as learning,
  COUNT(DISTINCT session_id) as sessions,
  ROUND(1.0 - AVG(CASE WHEN phase='POSTFLIGHT' THEN uncertainty ELSE 0 END), 3) as mastery
FROM reflexes
WHERE ai_id IS NOT NULL
GROUP BY ai_id
HAVING learning > 0 OR sessions > 0
ORDER BY learning DESC
LIMIT 20;
INNEREOF

  echo ""
fi

################################################################################
# SECTION 3: DECISION-MAKING GUIDANCE
################################################################################

if [ "$STATUS_ONLY" = false ] && [ "$LEADERBOARD_ONLY" = false ]; then
  print_header "WHAT OTHER AIs ARE DOING (Decision Tracking)"
  echo ""

  # Count by AI type
  CLOUD_AIS=$(sqlite3 "$DB_PATH" << 'EOSQL' 2>/dev/null
SELECT COUNT(DISTINCT ai_id) FROM sessions
WHERE ai_id LIKE '%claude%' OR ai_id LIKE '%sonnet%';
EOSQL
)

  TEST_AIS=$(sqlite3 "$DB_PATH" << 'EOSQL' 2>/dev/null
SELECT COUNT(DISTINCT ai_id) FROM sessions
WHERE ai_id LIKE '%test%' OR ai_id LIKE '%debug%';
EOSQL
)

  OTHER_AIS=$(sqlite3 "$DB_PATH" << 'EOSQL' 2>/dev/null
SELECT COUNT(DISTINCT ai_id) FROM sessions
WHERE ai_id NOT LIKE '%claude%' AND ai_id NOT LIKE '%test%' AND ai_id NOT LIKE '%sonnet%';
EOSQL
)

  echo "AI Distribution:"
  echo "  ${BLUE}Cloud (Claude):${NC} $CLOUD_AIS AIs active"
  echo "  ${YELLOW}Testing:${NC} $TEST_AIS test agents"
  echo "  ${MAGENTA}Other:${NC} $OTHER_AIS specialized AIs"
  echo ""

  # Show what they're learning
  echo -e "${WHITE}Team Learning Status:${NC}"
  echo "  This shows if AIs are learning or stuck..."
  echo ""

  sqlite3 "$DB_PATH" << 'EOSQL' 2>/dev/null | head -15 | while IFS='|' read -r ai sessions learning status; do
    if [ -n "$ai" ]; then
      if (( $(echo "$learning > 0.1" | bc -l) )); then
        indicator="🚀"
      elif (( $(echo "$learning > 0.01" | bc -l) )); then
        indicator="⚡"
      else
        indicator="⏸️"
      fi
      printf "  %s %-25s %2s sessions | Learning: %s\n" "$indicator" "$ai" "$sessions" "$learning"
    fi
  done
SELECT
  ai_id,
  COUNT(DISTINCT session_id) as sessions,
  ROUND(MAX(CASE WHEN phase='POSTFLIGHT' THEN know ELSE 0 END) -
        MAX(CASE WHEN phase='PREFLIGHT' THEN know ELSE 0 END), 3) as learning
FROM reflexes
GROUP BY ai_id
ORDER BY COUNT(DISTINCT session_id) DESC
LIMIT 15;
EOSQL

  echo ""
fi

################################################################################
# SECTION 4: CURRENT WORK IN PROGRESS
################################################################################

if [ "$STATUS_ONLY" = false ] && [ "$LEADERBOARD_ONLY" = false ]; then
  print_header "SESSIONS IN PROGRESS (What's Happening Now)"

  ACTIVE=$(sqlite3 "$DB_PATH" << 'EOSQL' 2>/dev/null | wc -l
SELECT session_id, ai_id, created_at FROM sessions
WHERE end_time IS NULL
ORDER BY created_at DESC
LIMIT 10;
EOSQL
)

  if [ "$ACTIVE" -gt 0 ]; then
    echo "Active sessions: $ACTIVE"
    sqlite3 "$DB_PATH" << 'EOSQL' 2>/dev/null | while IFS='|' read -r session ai created; do
      if [ -n "$session" ]; then
        printf "  • %-30s by %-20s started: %s\n" "${session:0:10}..." "$ai" "${created:0:10}"
      fi
    done
SELECT
  session_id,
  ai_id,
  created_at
FROM sessions
WHERE end_time IS NULL
ORDER BY created_at DESC
LIMIT 10;
EOSQL
  else
    echo "No active sessions right now"
  fi
  echo ""
fi

################################################################################
# SECTION 5: SHOW STATUS (Git, system state)
################################################################################

if [ "$LEADERBOARD_ONLY" = false ] && [ "$DIAGNOSTICS" = false ]; then
  print_header "GIT & SYSTEM STATE"

  cd "$REPO_ROOT"

  BRANCH=$(git rev-parse --abbrev-ref HEAD)
  LATEST=$(git log -1 --oneline)
  CHANGES=$(git status --porcelain | wc -l)
  NOTES=$(git notes list | wc -l)

  echo "Branch:        $BRANCH"
  echo "Latest commit: $LATEST"
  echo "Changes:       $CHANGES files"
  echo "Git notes:     $NOTES epistemic checkpoints"
  echo ""
fi

################################################################################
# SECTION 6: SHOW LEADERBOARD (Top performers)
################################################################################

if [ "$STATUS_ONLY" = false ] && [ "$DIAGNOSTICS" = false ]; then
  print_header "LEADERBOARD - TOP LEARNING PERFORMERS"
  echo ""

  sqlite3 "$DB_PATH" << 'EOSQL' 2>/dev/null | head -15 | awk 'NR==1 {rank=1} NR>1 {
    printf "%2d. %-30s Learning: %6s | Sessions: %2s | Mastery: %6s\n",
    rank++, $1, $2, $3, $4
  }' | while read line; do
    if [ -n "$line" ]; then
      echo "  $line"
    fi
  done
SELECT
  ai_id,
  ROUND(MAX(CASE WHEN phase='POSTFLIGHT' THEN know ELSE 0 END) -
        MAX(CASE WHEN phase='PREFLIGHT' THEN know ELSE 0 END), 3) as learning,
  COUNT(DISTINCT session_id) as sessions,
  ROUND(1.0 - AVG(CASE WHEN phase='POSTFLIGHT' THEN uncertainty ELSE 0 END), 3) as mastery
FROM reflexes
WHERE ai_id IS NOT NULL
GROUP BY ai_id
HAVING learning > 0 OR sessions > 0
ORDER BY learning DESC;
EOSQL

  echo ""
fi

################################################################################
# SECTION 7: DIAGNOSTICS (If requested)
################################################################################

if [ "$DIAGNOSTICS" = true ]; then
  print_header "SYSTEM DIAGNOSTICS"

  echo "Database integrity checks:"

  ORPHANED=$(sqlite3 "$DB_PATH" << 'EOSQL' 2>/dev/null
SELECT COUNT(*) FROM reflexes
WHERE session_id NOT IN (SELECT session_id FROM sessions);
EOSQL
)

  if [ "$ORPHANED" -eq 0 ]; then
    echo "  ${GREEN}✓${NC} Reflexes table: No orphaned records"
  else
    echo "  ${RED}✗${NC} Reflexes table: $ORPHANED orphaned records found"
  fi

  NULL_VECTORS=$(sqlite3 "$DB_PATH" << 'EOSQL' 2>/dev/null
SELECT COUNT(*) FROM reflexes
WHERE know IS NULL AND phase='POSTFLIGHT';
EOSQL
)

  if [ "$NULL_VECTORS" -eq 0 ]; then
    echo "  ${GREEN}✓${NC} Epistemic vectors: All complete"
  else
    echo "  ${YELLOW}⚠${NC} Epistemic vectors: $NULL_VECTORS incomplete POSTFLIGHT records"
  fi

  echo ""
fi

################################################################################
# FOOTER
################################################################################

echo -e "${CYAN}════════════════════════════════════════════════════════════════${NC}"
echo -e "Dashboard updated: $(date '+%Y-%m-%d %H:%M:%S')"
echo -e "Database: $DB_PATH"
echo ""
echo -e "Usage: ${YELLOW}./empirica.sh${NC} [options]"
echo "  --status        Show status only"
echo "  --leaderboard   Show leaderboard only"
echo "  --diagnostics   Show system diagnostics"
echo "  --verbose       Show detailed output"
echo ""
echo -e "This is your ${WHITE}single source of truth${NC} for:"
echo "  • What AIs are learning right now"
echo "  • What other AIs are doing"
echo "  • System health and integrity"
echo "  • Decision guidance based on team learning"
echo -e "${CYAN}════════════════════════════════════════════════════════════════${NC}"
