import streamlit as st
from utils.database import get_all_usecases, get_categories, search_usecases
from utils.session import render_card
import json

def render():
    st.markdown('<div class="page-title">Use Case Hub</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Discover what other teams have already built. Share your solutions. Avoid reinventing the wheel.</div>', unsafe_allow_html=True)

    all_uc = get_all_usecases()
    categories = get_categories()

    # ── Stats ──────────────────────────────────────────────────────────────
    teams = set(uc.get("team_name") for uc in all_uc if uc.get("team_name"))
    cats  = set(uc.get("category") for uc in all_uc if uc.get("category"))
    completed = sum(1 for uc in all_uc if uc.get("status") == "Completed")

    c1, c2, c3, c4 = st.columns(4)
    for col, num, label in [
        (c1, len(all_uc), "Total Use Cases"),
        (c2, len(teams), "Teams"),
        (c3, len(cats), "Categories"),
        (c4, completed, "Completed"),
    ]:
        col.markdown(f"""
        <div class="stat-card">
            <div class="stat-num">{num}</div>
            <div class="stat-label">{label}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Quick search ───────────────────────────────────────────────────────
    col_s, col_b = st.columns([5, 1])
    with col_s:
        q = st.text_input("", placeholder="🔍  Search use cases…", label_visibility="collapsed")
    with col_b:
        if st.button("AI Assistant 🤖", use_container_width=True):
            st.session_state["page"] = "chat"
            st.rerun()

    if q:
        results = search_usecases(q)
        st.markdown(f"**{len(results)} result(s)** for *{q}*")
        for uc in results:
            render_card(uc)
        return

    st.markdown("---")

    # ── Recent submissions ─────────────────────────────────────────────────
    st.markdown("### 🕐 Recent Submissions")
    recent = all_uc[:6]
    if not recent:
        st.info("No use cases yet. Be the first to submit one!")
    else:
        cols = st.columns(2)
        for i, uc in enumerate(recent):
            with cols[i % 2]:
                render_card(uc)

    st.markdown("---")

    # ── Browse by category ─────────────────────────────────────────────────
    st.markdown("### 📂 Browse by Category")
    if categories:
        st.markdown('<div class="cat-btns">', unsafe_allow_html=True)
        cat_cols = st.columns(min(len(categories), 4))
        for i, cat in enumerate(categories):
            with cat_cols[i % 4]:
                count = sum(1 for uc in all_uc if uc.get("category") == cat)
                if st.button(f"{cat} ({count})", key=f"cat_{i}", use_container_width=True):
                    st.session_state["page"] = "library"
                    st.session_state["filter_category"] = cat
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

    # ── Submit CTA ─────────────────────────────────────────────────────────
    st.markdown("""
    <div style="background:linear-gradient(135deg,#e8f2fd 0%,#f0f6ff 100%);border:1px solid rgba(0,112,210,0.15);border-radius:12px;padding:32px 36px;text-align:center;">
        <div style="font-family:'Plus Jakarta Sans',sans-serif;font-weight:700;font-size:22px;letter-spacing:-0.01em;margin-bottom:8px;color:#0a3878;">
            Have a use case to share?
        </div>
        <div style="color:#3d5166;font-size:14px;margin-bottom:4px;font-weight:400;">
            Help your colleagues by documenting your solution. It only takes a few minutes.
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    col_cta = st.columns([2,1,2])[1]
    with col_cta:
        st.markdown('<div class="submit-cta-btn">', unsafe_allow_html=True)
        if st.button("➕  Submit a Use Case", use_container_width=True):
            st.session_state["page"] = "submit"
            st.session_state["edit_id"] = None
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
