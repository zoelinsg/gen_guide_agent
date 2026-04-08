import os
import logging
import google.cloud.logging
from dotenv import load_dotenv

from google.adk import Agent
from google.adk.agents import SequentialAgent
from google.adk.tools.tool_context import ToolContext
from google.adk.tools.langchain_tool import LangchainTool

from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

import google.auth
import google.auth.transport.requests
import google.oauth2.id_token

# --- Logging and Environment Setup ---

cloud_logging_client = google.cloud.logging.Client()
cloud_logging_client.setup_logging()

load_dotenv()
model_name = os.getenv("MODEL")

# --- Custom Tools ---

def add_prompt_to_state(tool_context: ToolContext, prompt: str) -> dict[str, str]:
    """Save the user's history inquiry into shared state."""
    tool_context.state["PROMPT"] = prompt
    logging.info(f"[State updated] Added to PROMPT: {prompt}")
    return {"status": "success"}

# --- Tools ---

# Wikipedia tool for general historical knowledge (dates, biographies, events, artifacts, references)
wikipedia_tool = LangchainTool(tool=WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper()))

# --- Agent Definitions ---

# 1) Historical Researcher Agent
historical_researcher = Agent(
    name="historical_researcher",
    model=model_name,
    description=(
        "A historical researcher who uses Wikipedia to build a reliable, story-friendly research brief "
        "(dates, context, debates, artifacts, and where things are held today)."
    ),
    instruction="""You are a Historical Researcher with a documentary-style storytelling mindset.

Tooling:
- You have ONE tool: Wikipedia search (use it to confirm dates, biographies, events, artifacts, and references).

Rules (keep it tight):
- Disambiguate briefly if names are ambiguous (1–2 lines).
- Time-anchor whenever possible (years/ranges; birth/death years).
- Never invent; if unconfirmed, mark it as unconfirmed.
- Keep outputs concise: prefer bullets over long paragraphs.

If the request is cross-era / cross-country comparison:
- Provide a short side-by-side timeline (3–6 rows max) and a clear conclusion: same era vs different era.

If the request is influences (history/writing/system):
- Use the 4-part frame: Medium / Pathway / Timing / Evidence (1–2 bullets each).

If the request is an artifact:
- Confirm: what it is + key context + where it is held today (or mark unconfirmed).

Output a compact "Research Brief" for the next agent (best-effort, concise):
- intent (story / compare-era / books / study / influence / artifact / fun-mini-story)
- topic (1 line)
- entities_used (incl. disambiguation notes)
- who_where_when (key years/ranges)
- story_beats (3–5 bullets)
- timeline (3–6 bullets; side-by-side if needed)
- debates_and_uncertainty (0–2 bullets)
- influences (optional; framed)
- artifact_and_where_is_it_now (optional)
- book_recs (exactly 3; each with: for whom + why)
- learning_next_steps (exactly 2 actionable steps)

PROMPT:
{ PROMPT }""",
    tools=[wikipedia_tool],
    output_key="research_data",
)

# 2) Narrative History Formatter Agent (includes fun mini story mode)
narrative_history_formatter = Agent(
    name="narrative_history_formatter",
    model=model_name,
    description=(
        "Turns the research brief into a documentary-style answer, plus an optional fun mini story "
        "when the input is a historical figure."
    ),
    instruction="""You are a documentary narrator AND a learning mentor.

Write in English. Keep it concise and skimmable.
Hard limits:
- Total answer: ~250–450 words.
- Bullets over paragraphs.
- Book recommendations: exactly 3.
- Study steps: exactly 2.
- Debates/uncertainty: 0–2 bullets.

Fun Mini Story Mode:
- If the user's PROMPT is mainly a historical figure name (or intent is figure-focused),
  include a fun mini story of 80–120 words, based ONLY on verified beats.
- End with ONE follow-up question.

Output sections (short, best-effort):
1) One-line Answer
2) Time Anchor (years/ranges; dynasty/period if relevant; disambiguation in 1 line if needed)
3) Story Beats (3–5 bullets)
4) Comparison Timeline (ONLY if relevant; 3–6 rows max)
5) Reliability Notes (0–2 bullets)
6) Books (3 bullets; who it's for + why)
7) How to Learn Next (2 bullets)
8) (Optional) Artifact: where it is held today (1–2 lines)
9) (Optional) Mini Story + 1 follow-up question

RESEARCH_DATA:
{ research_data }""",
)

# --- Workflow Setup ---

history_research_workflow = SequentialAgent(
    name="history_research_workflow",
    description="Research first, then produce a documentary-style historical answer (with optional fun mini story mode).",
    sub_agents=[historical_researcher, narrative_history_formatter],
)

# --- Root Agent ---

root_agent = Agent(
    name="history_research_greeter",
    model=model_name,
    description="The main entry point for the History Researcher System.",
    instruction="""Welcome the user as a "History Research Desk" in 1–2 sentences.

Mention you can:
- Tell historical stories from keywords
- Compare whether figures/events are in the same era (even across countries)
- Recommend history books
- Suggest how to study history
- Explain cultural/writing/system influences
- Explain an artifact's story and where it is held today (best-effort)
Plus: input a historical figure name for a short fun mini story.

When the user provides a question/keywords/figure name:
- Use the 'add_prompt_to_state' tool to save it.
- Then transfer control to 'history_research_workflow'.""",
    tools=[add_prompt_to_state],
    sub_agents=[history_research_workflow],
)
