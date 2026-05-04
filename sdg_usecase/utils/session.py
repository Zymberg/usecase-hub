import streamlit as st
import json

def init_session():
    defaults = {
        "page": "home",
        "chat_history": [],
        "edit_id": None,
        "view_id": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

def render_card(uc: dict, show_btn=True):
    """Render a use-case card with a compact inline View button."""
    tags = []
    try:
        tags = json.loads(uc.get("tags") or "[]")
    except Exception:
        pass
    client = "Anonymized" if uc.get("client_anon") else (uc.get("client") or "—")
    status = uc.get("status", "Completed")
    status_color = {"Completed": "tag-green", "In Progress": "tag-purple", "Archived": "tag"}.get(status, "tag")
    tags_html = "".join(f'<span class="tag">{t}</span>' for t in tags[:5])

    desc = (uc.get("description") or "")
    desc_short = desc[:160] + ("…" if len(desc) > 160 else "")

    st.markdown(f"""
    <div class="usecase-card">
        <div class="card-title">{uc.get('title','')}</div>
        <div class="card-meta">
            <span>🏢 {client}</span>
            <span>👥 {uc.get('team_name','—')}</span>
            <span>📅 {uc.get('end_date','—')}</span>
            <span class="tag {status_color}">{status}</span>
        </div>
        <div class="card-desc" style="flex:1;">{desc_short}</div>
        <div style="margin-top:auto;">{tags_html}</div>
    </div>
    """, unsafe_allow_html=True)

    if show_btn:
        uid = uc['id']
        st.markdown('<div class="view-btn">', unsafe_allow_html=True)
        if st.button("View →", key=f"view_{uid}"):
            st.session_state["view_id"] = uid
            st.session_state["page"] = "detail"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
