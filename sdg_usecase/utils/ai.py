import json
import os
import requests
from pathlib import Path
from dotenv import load_dotenv

# Load .env from project root (safe to call multiple times)
load_dotenv(Path(__file__).parent.parent / ".env")

OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
MODEL = "gpt-4o"  # change to "gpt-3.5-turbo" if preferred


def _call_openai(system: str, user: str, max_tokens: int = 1024) -> str:
    api_key = os.environ.get("OPENAI_API_KEY", "")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": MODEL,
        "max_tokens": max_tokens,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user",   "content": user},
        ],
    }
    resp = requests.post(OPENAI_API_URL, headers=headers, json=payload, timeout=30)
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]


def ai_search(query: str, usecases: list) -> dict:
    """
    Returns {"matches": [...], "reply": str}
    Falls back to keyword search if no API key.
    """
    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        return _keyword_fallback(query, usecases)

    catalogue = []
    for uc in usecases:
        tags = []
        try:
            tags = json.loads(uc.get("tags") or "[]")
        except Exception:
            pass
        catalogue.append({
            "id": uc["id"],
            "title": uc["title"],
            "category": uc.get("category", ""),
            "description": (uc.get("description") or "")[:300],
            "solution": (uc.get("solution") or "")[:300],
            "tags": tags,
            "team": uc.get("team_name", ""),
            "status": uc.get("status", ""),
        })

    system = """You are a semantic search assistant for an internal use-case knowledge hub.
Given a user query and a JSON list of use cases, return the most relevant matches.
Respond ONLY with valid JSON — no markdown fences, no explanation outside the JSON.
Format:
{
  "matches": [
    {"id": <int>, "relevance": "High|Medium|Low", "reason": "<one sentence>"},
    ...
  ],
  "reply": "<2-3 sentence natural language summary of what you found>"
}
Sort by relevance descending. Include up to 5 matches. If nothing is relevant, return an empty matches array."""

    user = f"Query: {query}\n\nUse cases:\n{json.dumps(catalogue, indent=2)}"

    try:
        raw = _call_openai(system, user, max_tokens=1000)
        # Strip accidental markdown fences if the model adds them
        raw = raw.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
        result = json.loads(raw)
        id_map = {uc["id"]: uc for uc in usecases}
        enriched = []
        for m in result.get("matches", []):
            if m["id"] in id_map:
                enriched.append({**id_map[m["id"]], "_relevance": m["relevance"], "_reason": m["reason"]})
        result["matches"] = enriched
        return result
    except Exception as e:
        return _keyword_fallback(query, usecases)


def ai_chat_response(messages: list, usecases: list) -> str:
    """
    Full conversational response for the chat page.
    messages = [{"role": "user"|"assistant", "content": str}, ...]
    """
    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        return "⚠️ No OPENAI_API_KEY found. Set it in your environment to enable the AI assistant. Keyword search still works."

    catalogue = []
    for uc in usecases:
        tags = []
        try:
            tags = json.loads(uc.get("tags") or "[]")
        except Exception:
            pass
        catalogue.append({
            "id": uc["id"],
            "title": uc["title"],
            "category": uc.get("category", ""),
            "description": (uc.get("description") or "")[:400],
            "solution": (uc.get("solution") or "")[:400],
            "tech_stack": uc.get("tech_stack", ""),
            "tags": tags,
            "team": uc.get("team_name", ""),
            "outcome": (uc.get("outcome") or "")[:200],
            "status": uc.get("status", ""),
        })

    system = f"""You are a helpful AI assistant for TeamSync, an internal use-case knowledge hub used by consulting/data teams.
Your job is to help users find relevant past projects and solutions built by other teams.
You have access to the following use-case library:

{json.dumps(catalogue, indent=2)}

IMPORTANT RULES:
- Only recommend use cases that are genuinely relevant to the user's specific query.
- Do NOT list all use cases unless the user explicitly asks to see everything.
- If the user describes a specific problem or technology, match only the closest 1-3 use cases.
- For each match, mention the title, team name, and one sentence explaining why it is relevant.
- If nothing matches well, say so and suggest refining the search.
- Format responses in clear, concise markdown. Keep answers short and focused."""

    # Build the full message list: system + conversation history
    api_messages = [{"role": "system", "content": system}] + messages

    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": MODEL,
            "max_tokens": 1000,
            "messages": api_messages,
        }
        resp = requests.post(OPENAI_API_URL, headers=headers, json=payload, timeout=30)
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"❌ OpenAI error: {e}"


def _keyword_fallback(query: str, usecases: list) -> dict:
    """Simple keyword match fallback when no API key is set."""
    q = query.lower()
    matches = []
    for uc in usecases:
        haystack = " ".join([
            uc.get("title", ""), uc.get("description", ""),
            uc.get("solution", ""), uc.get("category", ""),
            uc.get("tags", ""), uc.get("tech_stack", ""),
        ]).lower()
        if any(word in haystack for word in q.split() if len(word) > 2):
            matches.append({**uc, "_relevance": "Medium", "_reason": "Keyword match"})
    return {
        "matches": matches[:5],
        "reply": f"Found {len(matches[:5])} use case(s) matching your query (keyword search — set OPENAI_API_KEY for semantic AI search).",
    }
