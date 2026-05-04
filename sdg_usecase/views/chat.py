import streamlit as st
from utils.database import get_all_usecases
from utils.ai import ai_search, ai_chat_response
import os

SUGGESTIONS = [
    "I need a recommendation system for a retail client",
    "Client wants to predict customer churn",
    "We're building a fraud detection pipeline",
    "Need to automatically classify support tickets",
    "Client wants a scoring system for user engagement",
]

def render():
    st.markdown('<div class="page-title">AI Assistant</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Describe your use case in plain language. The AI will find the most relevant past solutions.</div>', unsafe_allow_html=True)

    has_key = bool(os.environ.get("OPENAI_API_KEY", ""))
    if not has_key:
        st.warning("⚠️ **OPENAI_API_KEY not set.** The assistant will use keyword search as a fallback.")

    all_uc = get_all_usecases()

    # Counter used to reset the text input widget after each submission
    if "chat_input_key" not in st.session_state:
        st.session_state["chat_input_key"] = 0

    # ── Suggested prompts — 2-column chip grid ────────────────────────────
    st.markdown('<p style="font-size:11px;font-weight:600;color:#6e7e99;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:10px;">💡 Try these</p>', unsafe_allow_html=True)
    st.markdown('<div class="sug-btns">', unsafe_allow_html=True)
    cols = st.columns(2)
    for i, sug in enumerate(SUGGESTIONS):
        with cols[i % 2]:
            if st.button(sug, key=f"sug_{i}", use_container_width=True):
                st.session_state["chat_history"] = []
                st.session_state["chat_history"].append({"role": "user", "content": sug})
                result = ai_search(sug, all_uc)
                _add_bot_result(result)
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

    # ── Chat history ───────────────────────────────────────────────────────
    for idx, msg in enumerate(st.session_state.get("chat_history", [])):
        if msg["role"] == "user":
            st.markdown(f'<div class="chat-user">{msg["content"]}</div>', unsafe_allow_html=True)
        elif msg["role"] == "assistant":
            st.markdown(f'<div class="chat-bot">{msg["content"]}</div>', unsafe_allow_html=True)
        elif msg["role"] == "results":
            for uc in msg["matches"]:
                _render_match_card(uc, idx)

    # ── Input ──────────────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    col_inp, col_send, col_clear = st.columns([5, 1, 1])
    with col_inp:
        user_input = st.text_input(
            "", placeholder="Describe your use case or ask a question…",
            label_visibility="collapsed", key=f"chat_input_{st.session_state['chat_input_key']}"
        )
    with col_send:
        send = st.button("Send →", use_container_width=True)
    with col_clear:
        if st.button("🗑️ Clear", use_container_width=True, key="clear_chat"):
            st.session_state["chat_history"] = []
            st.rerun()

    if send and user_input.strip():
        q = user_input.strip()
        st.session_state["chat_history"].append({"role": "user", "content": q})
        # Increment key to force the text input widget to re-render empty
        st.session_state["chat_input_key"] += 1

        if has_key:
            # Only pass user/assistant turns (not result cards) to the API
            api_messages = [
                m for m in st.session_state["chat_history"]
                if m["role"] in ("user", "assistant")
            ]
            reply = ai_chat_response(api_messages, all_uc)
            st.session_state["chat_history"].append({"role": "assistant", "content": reply})

            # Only show clickable result cards for specific queries (not browse-all requests)
            browse_all_phrases = [
                "all use cases", "show me all", "list all", "see all",
                "every use case", "all cases", "all teams", "all projects"
            ]
            is_browse_all = any(p in q.lower() for p in browse_all_phrases)
            if not is_browse_all:
                result = ai_search(q, all_uc)
                if result.get("matches"):
                    st.session_state["chat_history"].append({"role": "results", "matches": result["matches"]})
        else:
            result = ai_search(q, all_uc)
            _add_bot_result(result)

        st.rerun()


def _add_bot_result(result: dict):
    reply = result.get("reply", "")
    matches = result.get("matches", [])
    if reply:
        st.session_state["chat_history"].append({"role": "assistant", "content": reply})
    if matches:
        st.session_state["chat_history"].append({"role": "results", "matches": matches})


def _render_match_card(uc: dict, parent_idx: int):
    relevance = uc.get("_relevance", "")
    reason    = uc.get("_reason", "")
    rel_color = {"High": "#059669", "Medium": "#0070d2", "Low": "#7a90a8"}.get(relevance, "#6b7280")
    client    = "Anonymized" if uc.get("client_anon") else (uc.get("client") or "—")

    st.markdown(f"""
    <div class="chat-result-card">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:6px;">
            <div style="font-family:'Syne',sans-serif;font-weight:700;font-size:15px;">{uc.get('title','')}</div>
            {f'<span style="font-size:11px;font-weight:700;padding:2px 8px;border-radius:99px;background:rgba(79,142,247,.1);color:{rel_color};border:1px solid {rel_color}44;white-space:nowrap;margin-left:8px;">{relevance}</span>' if relevance else ''}
        </div>
        <div style="font-size:12px;color:#7a90a8;margin-bottom:6px;">
            👥 {uc.get('team_name','—')} &nbsp;·&nbsp; 🏢 {client} &nbsp;·&nbsp; {uc.get('category','')}
        </div>
        {f'<div style="font-size:13px;color:#3d5166;margin-bottom:6px;">{reason}</div>' if reason else ''}
    </div>
    """, unsafe_allow_html=True)

    if st.button("View full case →", key=f"chat_view_{uc['id']}_{parent_idx}"):
        st.session_state["view_id"] = uc["id"]
        st.session_state["page"] = "detail"
        st.rerun()
