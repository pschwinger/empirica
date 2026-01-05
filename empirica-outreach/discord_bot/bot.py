"""
Empirica Discord Bot - Epistemic AI Community Bot

Uses Empirica for:
- Session tracking per conversation (thread-based)
- Sentinel gates for response control (PROCEED/HALT/BRANCH/REVISE)
- Turtle grounding checks before responding
- Learning delta tracking per interaction

Architecture:
- Layer 0: Breadcrumb trail (findings, unknowns)
- Layer 1: CASCADE workflow per message
- Layer 2: Epistemic agent spawning for complex questions
- Layer 3: Sentinel gating with moon phase indicators
"""

import os
import asyncio
import subprocess
import json
import uuid
from datetime import datetime
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field

import discord
from discord import app_commands
from discord.ext import commands

# Optional: Anthropic for Claude responses (API key method)
try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

# Optional: aiohttp for Ollama (local AI)
try:
    import aiohttp
    AIOHTTP_AVAILABLE = True
except ImportError:
    AIOHTTP_AVAILABLE = False

# Empirica integration via CLI (subprocess calls)
# This avoids import issues and uses the stable CLI interface

# Maximum conversation history to keep (Discord best practice: ~25 messages)
MAX_CONVERSATION_HISTORY = 25


@dataclass
class ConversationSession:
    """Tracks Empirica session per Discord thread/conversation."""
    session_id: str
    thread_id: int
    user_id: int
    created_at: datetime = field(default_factory=datetime.now)
    message_count: int = 0
    last_vectors: Optional[Dict[str, float]] = None
    moon_phase: str = "🌓"  # Default: EMERGENT
    conversation_history: List[Dict[str, str]] = field(default_factory=list)

    def add_message(self, role: str, content: str):
        """Add message to conversation history, maintaining max size."""
        self.conversation_history.append({"role": role, "content": content})
        # Trim oldest messages if exceeding limit
        if len(self.conversation_history) > MAX_CONVERSATION_HISTORY:
            self.conversation_history = self.conversation_history[-MAX_CONVERSATION_HISTORY:]


class EmpricaBot(commands.Bot):
    """Discord bot with Empirica epistemic integration."""

    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True  # Privileged intent - needed for conversation
        intents.guilds = True
        # intents.members = True  # Optional - only if you need member info

        super().__init__(
            command_prefix="!",
            intents=intents,
            description="Empirica - Epistemic AI Community Bot"
        )

        # Session tracking: thread_id -> ConversationSession
        self.sessions: Dict[int, ConversationSession] = {}

        # Sentinel gate modes
        self.gate_modes = {
            "auto": True,      # Auto-respond if PROCEED
            "draft": False,    # Always draft for approval
            "escalate": False  # Always escalate to humans
        }

        # Bot's own epistemic state
        self.bot_session_id: Optional[str] = None

        # LLM backend selection (priority: Ollama > Anthropic API > placeholder)
        self.llm_backend = "placeholder"
        self.claude_client = None
        self.ollama_url = os.getenv("OLLAMA_URL", "http://localhost:11434")
        self.ollama_model = os.getenv("OLLAMA_MODEL", "llama3.2")  # or mistral, qwen, etc.

        # Check for Ollama first (local, free, private)
        if AIOHTTP_AVAILABLE and os.getenv("USE_OLLAMA", "").lower() in ("1", "true", "yes"):
            self.llm_backend = "ollama"
            print(f"[Empirica] Using Ollama backend: {self.ollama_url} model={self.ollama_model}")
        # Then check for Anthropic API
        elif ANTHROPIC_AVAILABLE:
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if api_key:
                self.claude_client = anthropic.Anthropic(api_key=api_key)
                self.llm_backend = "anthropic"
                print("[Empirica] Using Anthropic API backend")

        if self.llm_backend == "placeholder":
            print("[Empirica] No LLM backend configured. Using placeholder responses.")
            print("  Options: USE_OLLAMA=1 (local) or ANTHROPIC_API_KEY (cloud)")

        # System prompt for Claude (epistemic-aware)
        self.system_prompt = """You are Empirica Bot, an AI assistant in a Discord community focused on epistemic self-awareness for AI agents.

Your key traits:
- You track your own knowledge and uncertainty honestly
- You say "I don't know" when uncertain rather than guessing
- You help users understand Empirica's epistemic framework
- You're friendly but precise in technical discussions

Current epistemic state will be provided in each message. Use it to calibrate your confidence.

Keep responses concise for Discord (under 2000 chars). Use markdown formatting."""

    async def generate_response(
        self,
        session: ConversationSession,
        user_message: str,
        epistemic_context: dict
    ) -> str:
        """Generate response using configured LLM backend with epistemic context."""

        # Build epistemic context prefix
        vectors = epistemic_context.get("metacog", {}).get("corrected_vectors", {})
        context_msg = (
            f"[EPISTEMIC STATE: know={vectors.get('know', 'N/A')}, "
            f"uncertainty={vectors.get('uncertainty', 'N/A')}, "
            f"moon_phase={session.moon_phase}]\n\n"
        )

        # Add user message to history
        session.add_message("user", user_message)

        if self.llm_backend == "placeholder":
            return (
                f"{session.moon_phase} Hello! I'm the Empirica Discord bot. "
                f"This is message #{session.message_count} in our conversation.\n\n"
                f"**No LLM configured.** Options:\n"
                f"• `USE_OLLAMA=1` - Use local Ollama (free, private)\n"
                f"• `ANTHROPIC_API_KEY` - Use Claude API\n\n"
                f"Current epistemic state: know={vectors.get('know', 'N/A')}, uncertainty={vectors.get('uncertainty', 'N/A')}"
            )

        try:
            # Build messages list
            messages = list(session.conversation_history)

            # Add epistemic context to the last user message
            if messages and messages[-1]["role"] == "user":
                messages[-1] = {"role": "user", "content": context_msg + messages[-1]["content"]}

            if self.llm_backend == "ollama":
                assistant_response = await self._call_ollama(messages)
            else:  # anthropic
                assistant_response = await self._call_anthropic(messages)

            # Add response to history
            session.add_message("assistant", assistant_response)

            # Prefix with moon phase
            return f"{session.moon_phase} {assistant_response}"

        except Exception as e:
            print(f"[Empirica] LLM error ({self.llm_backend}): {e}")
            return f"{session.moon_phase} Sorry, I encountered an error generating a response. Please try again."

    async def _call_ollama(self, messages: list) -> str:
        """Call Ollama API for local LLM inference."""
        async with aiohttp.ClientSession() as http_session:
            # Convert to Ollama format
            prompt = self.system_prompt + "\n\n"
            for msg in messages:
                role = "User" if msg["role"] == "user" else "Assistant"
                prompt += f"{role}: {msg['content']}\n\n"
            prompt += "Assistant:"

            payload = {
                "model": self.ollama_model,
                "prompt": prompt,
                "stream": False,
                "options": {"num_predict": 1024}
            }

            async with http_session.post(
                f"{self.ollama_url}/api/generate",
                json=payload,
                timeout=aiohttp.ClientTimeout(total=60)
            ) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data.get("response", "").strip()
                else:
                    error = await resp.text()
                    raise Exception(f"Ollama API error: {resp.status} - {error}")

    async def _call_anthropic(self, messages: list) -> str:
        """Call Anthropic API for Claude inference."""
        response = self.claude_client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            system=self.system_prompt,
            messages=messages
        )
        return response.content[0].text

    async def spawn_epistemic_agent(
        self,
        session: ConversationSession,
        task: str,
        epistemic_context: dict
    ) -> str:
        """
        Spawn an epistemic agent via Claude API for deep investigation.

        This is called when Sentinel returns INVESTIGATE - the bot needs
        more information before responding confidently.
        """
        # Check if we have Claude API available for investigation
        if not self.claude_client:
            # Fallback: try to use Ollama with investigation prompt
            if self.llm_backend == "ollama":
                return await self._investigate_with_ollama(session, task, epistemic_context)
            return "Unable to spawn epistemic agent - no Claude API configured."

        vectors = epistemic_context.get("metacog", {}).get("corrected_vectors", {})

        investigation_prompt = f"""You are an epistemic investigation agent. Your task is to deeply analyze a question and provide findings.

CURRENT EPISTEMIC STATE:
- know: {vectors.get('know', 'N/A')}
- uncertainty: {vectors.get('uncertainty', 'N/A')}
- The Sentinel gate returned INVESTIGATE, meaning confidence is too low to respond directly.

TASK TO INVESTIGATE:
{task}

INSTRUCTIONS:
1. Break down what knowledge is needed to answer this
2. Identify what you DO know vs DON'T know
3. Provide your best analysis with explicit uncertainty markers
4. Format findings as bullet points

Be epistemically honest - say "I don't know" when uncertain."""

        try:
            response = self.claude_client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1500,
                system="You are an epistemic investigation agent that analyzes questions deeply and reports findings with honest uncertainty assessment.",
                messages=[{"role": "user", "content": investigation_prompt}]
            )

            findings = response.content[0].text

            # Log the investigation findings to Empirica
            await self._log_finding(
                session.session_id,
                f"Agent investigation: {task[:50]}... → Found {len(findings.split('•'))} insights",
                impact=0.7
            )

            return findings

        except Exception as e:
            print(f"[Empirica] Claude investigation error: {e}")
            return f"Investigation failed: {e}"

    async def _investigate_with_ollama(
        self,
        session: ConversationSession,
        task: str,
        epistemic_context: dict
    ) -> str:
        """Fallback: use Ollama for investigation if Claude unavailable."""
        vectors = epistemic_context.get("metacog", {}).get("corrected_vectors", {})

        prompt = f"""You are an epistemic investigation agent. Analyze deeply:

EPISTEMIC STATE: know={vectors.get('know', 'N/A')}, uncertainty={vectors.get('uncertainty', 'N/A')}

TASK: {task}

Provide findings with honest uncertainty. Use bullet points."""

        messages = [{"role": "user", "content": prompt}]
        return await self._call_ollama(messages)

    async def setup_hook(self):
        """Called when bot is ready. Initialize Empirica session."""
        # Create bot's main session
        result = await self._run_empirica([
            "session-create",
            "--ai-id", "empirica-discord-bot",
            "--output", "json"
        ])

        if result and result.get("ok"):
            self.bot_session_id = result.get("session_id")
            print(f"[Empirica] Bot session created: {self.bot_session_id}")

            # Run PREFLIGHT for bot initialization
            await self._submit_preflight(
                session_id=self.bot_session_id,
                vectors={"know": 0.5, "uncertainty": 0.5, "context": 0.3, "do": 0.7},
                reasoning="Bot starting up. Limited context, ready to learn from interactions."
            )

        # Sync slash commands
        await self.tree.sync()
        print("[Empirica] Slash commands synced")

    async def _run_empirica(self, args: list) -> Optional[Dict[str, Any]]:
        """Run Empirica CLI command and return JSON result."""
        try:
            cmd = ["empirica"] + args
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()

            if process.returncode == 0 and stdout:
                return json.loads(stdout.decode())
            else:
                print(f"[Empirica] Command failed: {stderr.decode()}")
                return None
        except Exception as e:
            print(f"[Empirica] Error running command: {e}")
            return None

    async def _run_empirica_stdin(self, args: list, input_data: dict) -> Optional[Dict[str, Any]]:
        """Run Empirica CLI command with JSON stdin."""
        try:
            cmd = ["empirica"] + args
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            input_json = json.dumps(input_data).encode()
            stdout, stderr = await process.communicate(input=input_json)

            if process.returncode == 0 and stdout:
                return json.loads(stdout.decode())
            else:
                print(f"[Empirica] Command failed: {stderr.decode()}")
                return None
        except Exception as e:
            print(f"[Empirica] Error running command: {e}")
            return None

    async def _submit_preflight(self, session_id: str, vectors: dict, reasoning: str) -> Optional[dict]:
        """Submit PREFLIGHT assessment."""
        data = {
            "session_id": session_id,
            "vectors": {
                "engagement": vectors.get("engagement", 0.5),
                "foundation": {
                    "know": vectors.get("know", 0.5),
                    "do": vectors.get("do", 0.5),
                    "context": vectors.get("context", 0.5)
                },
                "comprehension": {
                    "clarity": 0.5,
                    "coherence": 0.5,
                    "signal": 0.5,
                    "density": 0.5
                },
                "execution": {
                    "state": 0.3,
                    "change": 0.3,
                    "completion": 0.0,
                    "impact": 0.3
                },
                "uncertainty": vectors.get("uncertainty", 0.5)
            },
            "reasoning": reasoning
        }
        return await self._run_empirica_stdin(["preflight-submit", "-"], data)

    async def _submit_check(self, session_id: str, action: str, vectors: dict, reasoning: str) -> Optional[dict]:
        """Submit CHECK gate assessment."""
        data = {
            "session_id": session_id,
            "action_description": action,
            "vectors": vectors,
            "reasoning": reasoning
        }
        return await self._run_empirica_stdin(["check-submit", "-"], data)

    async def _log_finding(self, session_id: str, finding: str, impact: float = 0.5) -> Optional[dict]:
        """Log a finding to Empirica."""
        return await self._run_empirica([
            "finding-log",
            "--session-id", session_id,
            "--finding", finding,
            "--impact", str(impact)
        ])

    async def _log_unknown(self, session_id: str, unknown: str) -> Optional[dict]:
        """Log an unknown to Empirica."""
        return await self._run_empirica([
            "unknown-log",
            "--session-id", session_id,
            "--unknown", unknown
        ])

    async def get_or_create_session(self, thread_id: int, user_id: int) -> ConversationSession:
        """Get existing session or create new one for this thread."""
        if thread_id in self.sessions:
            return self.sessions[thread_id]

        # Create new Empirica session for this conversation
        result = await self._run_empirica([
            "session-create",
            "--ai-id", f"discord-thread-{thread_id}",
            "--output", "json"
        ])

        session_id = result.get("session_id") if result else str(uuid.uuid4())

        session = ConversationSession(
            session_id=session_id,
            thread_id=thread_id,
            user_id=user_id
        )
        self.sessions[thread_id] = session

        # Initial PREFLIGHT for conversation
        await self._submit_preflight(
            session_id=session_id,
            vectors={"know": 0.3, "uncertainty": 0.7, "context": 0.2, "do": 0.5},
            reasoning=f"New conversation started with user {user_id}. Low initial context."
        )

        return session

    async def sentinel_gate(self, session: ConversationSession, message_content: str) -> tuple[str, dict]:
        """
        Run Sentinel gate check before responding.

        Returns:
            (decision, check_result) where decision is PROCEED/HALT/BRANCH/REVISE
        """
        # Assess current epistemic state
        know = 0.5 + (0.02 * min(session.message_count, 10))  # Grows with conversation
        uncertainty = max(0.3, 0.7 - (0.03 * min(session.message_count, 10)))

        # Check for uncertain language in message
        uncertain_markers = ["?", "how", "why", "what", "confused", "help", "explain"]
        has_question = any(marker in message_content.lower() for marker in uncertain_markers)

        if has_question:
            uncertainty += 0.1

        result = await self._submit_check(
            session_id=session.session_id,
            action=f"Respond to Discord message: {message_content[:100]}",
            vectors={
                "know": min(1.0, know),
                "uncertainty": min(1.0, uncertainty),
                "context": 0.5 + (0.1 * min(session.message_count, 5)),
                "scope": 0.4  # Single message response is low scope
            },
            reasoning=f"Message {session.message_count + 1} in conversation. Assessing response readiness."
        )

        if result:
            decision = result.get("decision", "proceed")
            sentinel = result.get("sentinel", {})

            # Update session with moon phase
            if "metacog" in result:
                corrected = result["metacog"].get("corrected_vectors", {})
                if corrected.get("know", 0) >= 0.85:
                    session.moon_phase = "🌕"  # CRYSTALLINE
                elif corrected.get("know", 0) >= 0.70:
                    session.moon_phase = "🌔"  # SOLID
                elif corrected.get("know", 0) >= 0.50:
                    session.moon_phase = "🌓"  # EMERGENT
                elif corrected.get("know", 0) >= 0.30:
                    session.moon_phase = "🌒"  # FORMING
                else:
                    session.moon_phase = "🌑"  # DARK

            session.last_vectors = result.get("vectors", {})
            return sentinel.get("decision", decision), result

        return "proceed", {}

    def get_moon_phase_emoji(self, confidence: float) -> str:
        """Convert confidence to moon phase emoji."""
        if confidence >= 0.85:
            return "🌕"
        elif confidence >= 0.70:
            return "🌔"
        elif confidence >= 0.50:
            return "🌓"
        elif confidence >= 0.30:
            return "🌒"
        else:
            return "🌑"


# Initialize bot
bot = EmpricaBot()


# Slash Commands

@bot.tree.command(name="empirica", description="Check Empirica epistemic state")
async def empirica_status(interaction: discord.Interaction):
    """Show current epistemic state."""
    session = bot.sessions.get(interaction.channel_id)

    if session:
        status = f"""**Empirica Epistemic State**

{session.moon_phase} **Moon Phase:** {session.moon_phase}
📊 **Messages:** {session.message_count}
🔗 **Session:** `{session.session_id[:8]}...`

**Last Vectors:**
- know: {session.last_vectors.get('know', 'N/A') if session.last_vectors else 'N/A'}
- uncertainty: {session.last_vectors.get('uncertainty', 'N/A') if session.last_vectors else 'N/A'}
"""
    else:
        status = "No active session in this channel. Start a conversation to initialize."

    await interaction.response.send_message(status, ephemeral=True)


@bot.tree.command(name="gate", description="Set Sentinel gate mode")
@app_commands.choices(mode=[
    app_commands.Choice(name="Auto (respond if PROCEED)", value="auto"),
    app_commands.Choice(name="Draft (always draft for approval)", value="draft"),
    app_commands.Choice(name="Escalate (always ask humans)", value="escalate")
])
async def set_gate_mode(interaction: discord.Interaction, mode: str):
    """Set the Sentinel gate mode for responses."""
    # Reset all modes
    for key in bot.gate_modes:
        bot.gate_modes[key] = False
    bot.gate_modes[mode] = True

    await interaction.response.send_message(
        f"✓ Sentinel gate mode set to **{mode}**",
        ephemeral=True
    )


@bot.tree.command(name="bootstrap", description="Load Empirica project context")
async def bootstrap(interaction: discord.Interaction):
    """Load project context from Empirica."""
    await interaction.response.defer(ephemeral=True)

    result = await bot._run_empirica([
        "project-bootstrap",
        "--output", "json"
    ])

    if result and result.get("ok"):
        findings = result.get("breadcrumbs", {}).get("findings", [])
        unknowns = result.get("breadcrumbs", {}).get("unknowns", [])

        response = f"""**📚 Project Context Loaded**

**Recent Findings:** {len(findings)}
**Open Unknowns:** {len(unknowns)}

Top finding: {findings[0].get('finding', 'None')[:100] if findings else 'None'}
"""
        await interaction.followup.send(response, ephemeral=True)
    else:
        await interaction.followup.send("Failed to load project context", ephemeral=True)


# Message handling with Sentinel gates

@bot.event
async def on_message(message: discord.Message):
    """Handle incoming messages with epistemic tracking."""
    # Ignore bot's own messages
    if message.author == bot.user:
        return

    # Only respond to mentions or DMs
    if not (bot.user in message.mentions or isinstance(message.channel, discord.DMChannel)):
        await bot.process_commands(message)
        return

    # Get or create session for this conversation
    thread_id = message.channel.id
    session = await bot.get_or_create_session(thread_id, message.author.id)
    session.message_count += 1

    # Run Sentinel gate
    decision, check_result = await bot.sentinel_gate(session, message.content)

    # Handle gate decision
    if decision == "halt":
        # HALT: Don't respond, log unknown
        await bot._log_unknown(session.session_id, f"Halted response to: {message.content[:100]}")
        await message.add_reaction("🛑")
        return

    elif decision == "branch" or decision == "investigate":
        # BRANCH/INVESTIGATE: Spawn epistemic agent for deep analysis
        await message.add_reaction("🔍")

        # Send initial message
        thinking_msg = await message.reply(
            f"{session.moon_phase} Spawning epistemic agent for deeper analysis..."
        )

        # Actually spawn the agent and investigate
        findings = await bot.spawn_epistemic_agent(
            session=session,
            task=message.content,
            epistemic_context=check_result
        )

        # Update with findings (Discord has 2000 char limit)
        if len(findings) > 1900:
            findings = findings[:1900] + "...\n\n*[truncated]*"

        await thinking_msg.edit(
            content=f"{session.moon_phase} **Investigation Complete**\n\n{findings}"
        )

        # Log the investigation
        await bot._log_unknown(session.session_id, f"Investigated: {message.content[:100]}")
        return

    elif decision == "revise":
        # REVISE: Draft for human review
        await message.add_reaction("📝")
        await message.reply(
            f"{session.moon_phase} **[DRAFT - Pending Review]**\n\n"
            "This response needs human approval before I can send it."
        )
        return

    # PROCEED: Generate response
    if bot.gate_modes["draft"]:
        # Always draft mode
        await message.add_reaction("📝")
        response = f"{session.moon_phase} **[DRAFT]** Ready to respond. React ✅ to approve."
    elif bot.gate_modes["escalate"]:
        # Always escalate mode
        await message.add_reaction("👆")
        response = f"{session.moon_phase} **[ESCALATED]** Waiting for human guidance."
    else:
        # Auto mode - respond normally with Claude
        await message.add_reaction(session.moon_phase)

        # Generate response using configured LLM backend
        response = await bot.generate_response(
            session=session,
            user_message=message.content,
            epistemic_context=check_result
        )

    await message.reply(response)

    # Log successful interaction as finding
    await bot._log_finding(
        session.session_id,
        f"Responded to user {message.author.name}: {message.content[:50]}...",
        impact=0.4
    )

    await bot.process_commands(message)


@bot.event
async def on_ready():
    """Called when bot is connected and ready."""
    print(f"[Empirica] Bot ready as {bot.user}")
    print(f"[Empirica] Bot session: {bot.bot_session_id}")
    print(f"[Empirica] Guilds: {len(bot.guilds)}")


def main():
    """Run the bot."""
    token = os.getenv("DISCORD_BOT_TOKEN")
    if not token:
        print("Error: DISCORD_BOT_TOKEN environment variable not set")
        print("Set it with: export DISCORD_BOT_TOKEN='your-token-here'")
        return

    print("[Empirica] Starting Discord bot...")
    bot.run(token)


if __name__ == "__main__":
    main()
