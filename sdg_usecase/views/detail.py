import streamlit as st
import json
from utils.database import get_usecase, delete_usecase, search_usecases

def render():
    uid = st.session_state.get("view_id")
    if not uid:
        st.warning("No use case selected.")
        return

    uc = get_usecase(uid)
    if not uc:
        st.error("Use case not found.")
        return

    # Back button
    if st.button("← Back to Library"):
        st.session_state["page"] = "library"
        st.rerun()

    client = "Anonymized" if uc.get("client_anon") else (uc.get("client") or "—")
    status = uc.get("status", "Completed")
    status_color = {"Completed": "#059669", "In Progress": "#7c3aed", "Archived": "#7a90a8"}.get(status, "#7a90a8")

    tags = []
    try:
        tags = json.loads(uc.get("tags") or "[]")
    except Exception:
        pass
    tags_html = "".join(f'<span class="tag">{t}</span>' for t in tags)

    links = []
    try:
        links = json.loads(uc.get("links") or "[]")
    except Exception:
        pass

    st.markdown(f"""
    <div class="detail-header">
        <div style="display:flex;align-items:center;gap:12px;margin-bottom:6px;">
            <span style="font-size:11px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;
                color:{status_color};background:rgba(79,142,247,.08);
                border:1px solid {status_color}44;border-radius:99px;padding:3px 10px;">{status}</span>
            <span style="font-size:12px;color:#8a97b0;">{uc.get('category','')}</span>
        </div>
        <div class="detail-title">{uc.get('title','')}</div>
        <div style="display:flex;gap:24px;font-size:13px;color:#8a97b0;margin-top:8px;">
            <span>🏢 {client}</span>
            <span>👥 {uc.get('team_name','—')}</span>
            <span>👤 {uc.get('team_members','—')}</span>
            <span>📅 {uc.get('start_date','?')} → {uc.get('end_date','?')}</span>
        </div>
        <div style="margin-top:12px;">{tags_html}</div>
    </div>
    """, unsafe_allow_html=True)

    col_main, col_side = st.columns([3, 1])

    with col_main:
        st.markdown('<div class="section-heading">Problem Description</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="info-block">{uc.get("description","—")}</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-heading">Solution Summary</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="info-block">{uc.get("solution","—")}</div>', unsafe_allow_html=True)

        if uc.get("outcome"):
            st.markdown('<div class="section-heading">Outcome & Results</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="info-block">{uc.get("outcome")}</div>', unsafe_allow_html=True)

    with col_side:
        st.markdown('<div class="section-heading">Tech Stack</div>', unsafe_allow_html=True)
        tech = uc.get("tech_stack","—")
        tech_items = [t.strip() for t in tech.split(",") if t.strip()]
        for t in tech_items:
            st.markdown(f'<span class="tag">{t}</span>', unsafe_allow_html=True)

        if links:
            st.markdown('<div class="section-heading" style="margin-top:20px;">Links</div>', unsafe_allow_html=True)
            for link in links:
                # Show as a styled button-like link
                st.markdown(f'''
                <a href="{link}" target="_blank" style="
                    display:inline-block;
                    background:#ffffff;border:none;border-radius:6px;padding:10px 20px;font-size:14px;font-weight:600;color:#ffffff;text-decoration:none;margin-bottom:6px;box-shadow:0 2px 8px rgba(0,112,210,0.25);
                ">🔗 Open in Google Drive</a>
                ''', unsafe_allow_html=True)

        role = st.session_state.get("user_role","Viewer")
        if role in ("Admin"):
            st.markdown('<div class="section-heading" style="margin-top:20px;">Actions</div>', unsafe_allow_html=True)
            if st.button("✏️  Edit", use_container_width=True):
                st.session_state["edit_id"] = uc["id"]
                st.session_state["page"] = "submit"
                st.rerun()
            if role == "Admin":
                if st.button("🗑️  Delete", use_container_width=True):
                    delete_usecase(uc["id"])
                    st.success("Deleted.")
                    st.session_state["page"] = "library"
                    st.rerun()

    # ── Similar use cases ──────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### 🔁 Similar Use Cases")
    keywords = " ".join(tags[:3]) + " " + (uc.get("category") or "")
    similar = [u for u in search_usecases(keywords) if u["id"] != uc["id"]][:4]
    if similar:
        cols = st.columns(2)
        for i, s in enumerate(similar):
            with cols[i % 2]:
                from utils.session import render_card
                render_card(s)
    else:
        st.caption("No similar use cases found yet.")
