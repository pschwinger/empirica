# 🔌 Universal Meetings Adapter - Architecture Design

**Date:** 2025-12-19
**Context:** Designing the epistemic layer for all meeting tools

---

## The Strategic Decision: What to Build First?

### Your Instinct is Right 🎯

**Jira/Confluence = Too Complex for MVP**
- Enterprise auth (SSO, OAuth)
- Complex data models (sprints, epics, pages)
- Approval processes
- Rate limits and API quirks

**Better First Target: Something More Open**

---

## Recommended: Start with Discord

### Why Discord is PERFECT for MVP

**1. Simple but Real**
- ✅ Real-time chat (like Slack)
- ✅ Threading (context preservation)
- ✅ Bots are first-class citizens
- ✅ WebSocket API (easy real-time)
- ✅ Free tier (no enterprise sales needed)

**2. Developer-Friendly**
- ✅ Excellent documentation
- ✅ Simple OAuth (one token, no complexity)
- ✅ Fast iteration (no approval needed)
- ✅ Rich community (help available)
- ✅ Slash commands built-in

**3. Clear Use Cases**
- Open source communities use it (natural fit for MIT project)
- Dev teams use it (technical audience)
- Gaming guilds = perfect for testing at scale
-Streamer communities = high engagement

**4. Epistemic Opportunities**
```
User: "I think we should refactor the auth system"

Empirica Bot:
📊 Epistemic Assessment:
Confidence: Unknown
Missing context: Why? What's broken? Timeline?

💡 Run PREFLIGHT first:
/empirica assess "auth refactor"

This will help you understand:
- What you KNOW (current pain points)
- What you DON'T KNOW (effort, risks, alternatives)
- What you need to INVESTIGATE (technical feasibility)
```

**5. Platform Strategy**
- Discord first (prove concept)
- Slack second (reuse Discord learnings)
- Teams/Zoom third (enterprise market)

Discord = training wheels for the ecosystem.

---

## Alternative: Slack (Also Good)

### Why Slack Makes Sense

**Pros:**
- ✅ Huge market ($6.5B project management)
- ✅ Enterprise adoption (immediate revenue potential)
- ✅ Familiar to everyone
- ✅ Bolt SDK (well-documented)
- ✅ App directory (distribution channel)

**Cons:**
- ⚠️ Enterprise-focused (slower testing cycles)
- ⚠️ App approval process (delay to launch)
- ⚠️ Rate limits stricter (harder to experiment)

**Recommendation:** Slack as SECOND target after proving Discord.

---

## The Universal Adapter Architecture

### Core Concept: Adapter Pattern

```
┌─────────────────────────────────────────┐
│      Empirica Core (We Build)           │
│  - EpistemicEngine                      │
│  - CASCADE workflow                     │
│  - Vector assessment                    │
│  - Storage (SQLite + Git + Qdrant)     │
└─────────────────────────────────────────┘
                    ▲
                    │ Standard Interface
                    │
┌───────────────────┴─────────────────────┐
│     Adapter Layer (Plugin SDK)          │
│  - Message ingestion                    │
│  - Context extraction                   │
│  - Response formatting                  │
│  - Event handling                       │
└─────────────────────────────────────────┘
                    ▲
        ┌───────────┼───────────┐
        │           │           │
   ┌────▼────┐ ┌───▼────┐ ┌────▼─────┐
   │ Discord │ │ Slack  │ │  Teams   │
   │ Adapter │ │Adapter │ │  Adapter │
   └─────────┘ └────────┘ └──────────┘
   
   Community builds these ↑
```

---

## Standard Interface (What Every Adapter Provides)

### 1. Message Context

```python
@dataclass
class MessageContext:
    """Standard message format for all platforms"""
    
    # Core fields
    message_id: str
    content: str
    author_id: str
    author_name: str
    timestamp: datetime
    
    # Context
    channel_id: str
    channel_name: str
    thread_id: Optional[str] = None
    
    # History
    previous_messages: List['MessageContext'] = field(default_factory=list)
    
    # Metadata
    platform: str  # "discord", "slack", "teams"
    raw_data: Dict[str, Any] = field(default_factory=dict)
```

### 2. Adapter Interface

```python
class MeetingAdapter(ABC):
    """Base class for all platform adapters"""
    
    @abstractmethod
    async def authenticate(self, credentials: Dict[str, str]) -> bool:
        """Platform-specific auth"""
        pass
    
    @abstractmethod
    async def listen(self) -> AsyncIterator[MessageContext]:
        """Stream incoming messages"""
        pass
    
    @abstractmethod
    async def send_message(
        self, 
        channel_id: str, 
        content: str,
        thread_id: Optional[str] = None
    ) -> str:
        """Send a message, return message_id"""
        pass
    
    @abstractmethod
    async def get_thread_history(
        self,
        thread_id: str,
        limit: int = 50
    ) -> List[MessageContext]:
        """Get conversation history"""
        pass
    
    @abstractmethod
    async def react(
        self,
        message_id: str,
        emoji: str
    ) -> bool:
        """Add reaction to message"""
        pass
```

### 3. Epistemic Commands (Platform-Agnostic)

```python
class EpistemicCommands:
    """Commands work the same across all platforms"""
    
    async def assess(self, context: MessageContext) -> EpistemicAssessment:
        """Assess epistemic confidence of a statement"""
        pass
    
    async def preflight(self, context: MessageContext) -> PreflightReport:
        """Run PREFLIGHT assessment"""
        pass
    
    async def check(self, context: MessageContext) -> CheckDecision:
        """Run CHECK gate"""
        pass
    
    async def postflight(self, context: MessageContext) -> PostflightReport:
        """Run POSTFLIGHT"""
        pass
    
    async def investigate(self, context: MessageContext) -> InvestigationPlan:
        """Generate investigation strategy"""
        pass
```

---

## Discord Adapter (Reference Implementation)

### Why Discord First?

**1. Simplest API**
```python
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix="/")

@bot.command()
async def assess(ctx, *, claim: str):
    """Epistemic assessment of a claim"""
    
    # Convert to standard MessageContext
    message_ctx = MessageContext(
        message_id=str(ctx.message.id),
        content=claim,
        author_id=str(ctx.author.id),
        author_name=ctx.author.name,
        timestamp=ctx.message.created_at,
        channel_id=str(ctx.channel.id),
        channel_name=ctx.channel.name,
        platform="discord"
    )
    
    # Use Empirica core
    assessment = await empirica_core.assess(message_ctx)
    
    # Format response
    embed = discord.Embed(
        title="📊 Epistemic Assessment",
        color=0x00ff00 if assessment.confidence > 0.7 else 0xff0000
    )
    embed.add_field(name="Confidence", value=f"{assessment.confidence:.0%}")
    embed.add_field(name="Uncertainty", value=f"{assessment.uncertainty:.0%}")
    
    if assessment.unknowns:
        embed.add_field(
            name="❓ Unknowns Detected",
            value="\n".join(f"- {u}" for u in assessment.unknowns),
            inline=False
        )
    
    if assessment.investigation_needed:
        embed.add_field(
            name="💡 Suggestion",
            value=f"Run investigation: `/empirica investigate \"{claim}\"`",
            inline=False
        )
    
    await ctx.send(embed=embed)

bot.run(TOKEN)
```

**2. Real-Time Features**
```python
@bot.event
async def on_message(message):
    """Passive epistemic monitoring"""
    
    # Ignore bot messages
    if message.author.bot:
        return
    
    # Detect uncertainty signals
    uncertainty_markers = [
        "i think", "maybe", "probably", "not sure",
        "might", "could be", "perhaps"
    ]
    
    content_lower = message.content.lower()
    if any(marker in content_lower for marker in uncertainty_markers):
        # Add reaction to indicate uncertainty detected
        await message.add_reaction("🤔")
        
        # Optionally suggest assessment
        if "should we" in content_lower or "we should" in content_lower:
            await message.reply(
                "💡 Detected uncertainty in a decision. "
                "Want to run epistemic assessment? "
                "Use `/assess \"your claim\"`"
            )
```

**3. Thread Support**
```python
@bot.command()
async def preflight(ctx):
    """Run PREFLIGHT on current thread"""
    
    # Get thread history
    messages = []
    async for msg in ctx.channel.history(limit=50):
        if not msg.author.bot:
            messages.append(MessageContext(
                message_id=str(msg.id),
                content=msg.content,
                author_id=str(msg.author.id),
                author_name=msg.author.name,
                timestamp=msg.created_at,
                channel_id=str(ctx.channel.id),
                channel_name=ctx.channel.name,
                platform="discord"
            ))
    
    # Run PREFLIGHT on conversation
    preflight = await empirica_core.preflight(messages)
    
    # Send detailed report
    await ctx.send(embed=create_preflight_embed(preflight))
```

---

## MVP Feature Set (Discord Bot)

### Week 1: Core Commands

**1. `/assess <claim>`**
- Epistemic assessment of a statement
- Returns: confidence, unknowns, suggestions

**2. `/preflight`**
- Assesses current thread/channel
- Returns: What you know, what's uncertain, what to investigate

**3. `/check`**
- Decision gate: proceed or investigate?
- Returns: confidence score + recommendation

**Example Flow:**
```
User: "I think we should rewrite the API in Rust"

/assess "rewrite API in Rust"

Bot: 
📊 Epistemic Assessment:
Confidence: 20% (LOW)
Unknowns:
- Why rewrite? (current pain points unclear)
- Effort estimate? (no data)
- Team Rust experience? (unknown)
- Migration path? (not defined)

💡 Suggestion: Run PREFLIGHT
/preflight

Bot:
🛫 PREFLIGHT Assessment:
Foundation:
- know: 0.3 (low understanding of problem)
- do: 0.4 (moderate Rust skills)
- context: 0.2 (missing requirements)

Recommendation: INVESTIGATE before deciding
Suggested investigations:
1. Document current API pain points
2. Assess team Rust readiness
3. Estimate migration effort
4. Identify risks

/check (later, after investigation)

Bot:
✅ CHECK Gate: PROCEED
Confidence: 0.75 (high)
You've investigated the key unknowns.
Ready to make informed decision.
```

---

## Plugin SDK Structure

### File Structure
```
empirica-meetings-sdk/
├── README.md
├── pyproject.toml
├── examples/
│   ├── discord_bot.py      # Reference implementation
│   ├── slack_bot.py         # Coming soon
│   └── custom_adapter.py    # Template
├── empirica_meetings/
│   ├── __init__.py
│   ├── adapter.py           # Base Adapter class
│   ├── context.py           # MessageContext
│   ├── commands.py          # EpistemicCommands
│   └── utils.py
└── tests/
    └── test_adapter.py
```

### Installation
```bash
pip install empirica-meetings-sdk

# With Discord support
pip install empirica-meetings-sdk[discord]

# With Slack support
pip install empirica-meetings-sdk[slack]

# All platforms
pip install empirica-meetings-sdk[all]
```

### Quick Start (Discord)
```python
from empirica_meetings import DiscordAdapter, EpistemicBot

# Create bot with Empirica integration
bot = EpistemicBot(
    adapter=DiscordAdapter(token=DISCORD_TOKEN),
    empirica_config={
        "project_id": "your-project-id",
        "ai_id": "discord-bot"
    }
)

# Built-in commands work automatically
# /assess, /preflight, /check, /postflight

# Add custom commands
@bot.command()
async def team_health(ctx):
    """Check team epistemic health"""
    health = await bot.empirica.get_team_health(
        channel_id=ctx.channel.id
    )
    await ctx.send(f"Team calibration: {health.calibration:.0%}")

bot.run()
```

---

## Why This Architecture Wins

### 1. Start Simple, Scale Complex

**Week 1:** Discord bot (50-100 lines)
**Week 2:** Slack adapter (reuse 80% of code)
**Week 3:** Teams adapter (reuse 80% of code)
**Week 4:** Community plugins (ecosystem)

### 2. Community-Friendly

**MIT Licensed SDK:**
- Low barrier to entry
- Copy-paste examples work
- Gradual learning curve

**Reference Implementation:**
- Discord bot shows best practices
- Clear patterns to follow
- Easy to adapt for other platforms

### 3. Platform Play

**We Own:**
- Epistemic engine (core IP)
- Assessment logic (moat)
- Learning data (Qdrant)

**Community Owns:**
- Platform connectors
- Custom commands
- Vertical solutions

### 4. Measurable Success

**Week 1 Metrics:**
- ✅ Discord bot deployed to 5 servers
- ✅ 50+ `/assess` commands run
- ✅ 3 community contributors

**Month 1 Metrics:**
- ✅ 100 Discord servers
- ✅ Slack adapter live
- ✅ 10 community plugins

---

## Implementation Plan

### Phase 1: Discord MVP (Week 1)

**Day 1-2:** Core SDK
- MessageContext dataclass
- Adapter base class
- EpistemicCommands integration

**Day 3-4:** Discord Adapter
- Bot setup
- `/assess` command
- `/preflight` command
- `/check` command

**Day 5-7:** Testing & Docs
- Deploy to 3 test servers
- Write documentation
- Create tutorial video

### Phase 2: Slack Adapter (Week 2)

**Day 1-3:** Slack adapter
- Bolt SDK integration
- Reuse MessageContext
- Slash commands

**Day 4-5:** Slack-specific features
- App manifest
- OAuth flow
- App directory submission

**Day 6-7:** Beta testing
- 5 beta teams
- Collect feedback

### Phase 3: SDK Release (Week 3)

**Day 1-3:** Open source
- GitHub repo
- Documentation site
- Example gallery

**Day 4-5:** Community seeding
- 10 developer outreach
- Tutorial content
- Support Discord

**Day 6-7:** Iterate
- Fix bugs
- Improve docs
- Onboard contributors

---

## Competitive Analysis: Why No One Else Has This

**Existing "Meeting Bots":**
- ❌ Transcription bots (Otter, Fireflies) - just record
- ❌ Action item extractors - post-hoc only
- ❌ "AI assistants" - surface-level summaries

**Empirica Difference:**
- ✅ **Epistemic awareness** (know vs guess)
- ✅ **Preventive** (investigate before crash)
- ✅ **Learning measurement** (deltas tracked)
- ✅ **Systematic** (CASCADE workflow)

**The Gap:**
Everyone built **note-takers**.  
No one built **epistemic coaches**.

---

## Revenue Model

### Free Tier
- Self-hosted (run your own bot)
- 100 assessments/month
- Community support

### Pro Tier ($49/month)
- Cloud-hosted bot
- Unlimited assessments
- Epistemic analytics dashboard
- Email support

### Enterprise ($499+/month)
- Multiple platforms
- SSO integration
- Custom commands
- Dedicated support
- SLA guarantees

---

## Final Recommendation

**Build Discord adapter first.**

**Why:**
1. ✅ Simplest API (fastest MVP)
2. ✅ Developer community (natural fit)
3. ✅ No approval process (ship fast)
4. ✅ Real-time native (best UX)
5. ✅ Open source friendly (MIT license alignment)

**Then:**
- Week 2: Slack (enterprise market)
- Week 3: SDK release (community)
- Week 4: Teams (complete triad)

**Within a month:**
- 3 platform adapters
- Community building plugins
- Proven value prop
- Ready for BBC demo (can use Discord for internal testing)

---

**Next Step:** Build Discord adapter prototype this week? 🚀

