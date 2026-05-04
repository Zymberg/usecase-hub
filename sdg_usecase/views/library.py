import streamlit as st
from utils.database import get_all_usecases, get_categories, get_teams, search_usecases
from utils.session import render_card

def render():
    st.markdown('<div class="page-title">Browse Library</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">All use cases submitted by teams across all clients and projects.</div>', unsafe_allow_html=True)

    categories = ["All"] + get_categories()
    teams = ["All"] + get_teams()
    statuses = ["All", "Completed", "In Progress", "Archived"]

    # ── Filters ────────────────────────────────────────────────────────────
    f1, f2, f3, f4 = st.columns([3, 2, 2, 2])
    with f1:
        q = st.text_input("", placeholder="🔍  Search…", label_visibility="collapsed",
                          key="lib_search")
    with f2:
        default_cat = st.session_state.pop("filter_category", "All")
        idx = categories.index(default_cat) if default_cat in categories else 0
        sel_cat = st.selectbox("Category", categories, index=idx, key="lib_cat")
    with f3:
        sel_team = st.selectbox("Team", teams, key="lib_team")
    with f4:
        sel_status = st.selectbox("Status", statuses, key="lib_status")

    cat_filter    = None if sel_cat == "All" else sel_cat
    team_filter   = None if sel_team == "All" else sel_team
    status_filter = None if sel_status == "All" else sel_status

    results = search_usecases(
        query=q or "",
        category=cat_filter,
        status=status_filter,
        team=team_filter,
    )

    st.markdown(f"<div style='color:#8a97b0;font-size:13px;margin-bottom:16px;'>{len(results)} use case(s) found</div>",
                unsafe_allow_html=True)

    if not results:
        st.info("No use cases match your filters. Try broadening your search or submit a new one.")
        if st.button("➕  Submit a Use Case"):
            st.session_state["page"] = "submit"
            st.rerun()
        return

    # Two-column card grid
    cols = st.columns(2)
    for i, uc in enumerate(results):
        with cols[i % 2]:
            render_card(uc)
