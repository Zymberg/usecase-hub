import streamlit as st
import json
from utils.database import get_usecase, save_usecase, get_categories

CATEGORIES = [
    "Recommendation Engine", "Scoring & Analytics", "NLP / Text Analytics",
    "Predictive Analytics", "Fraud & Risk", "Dashboard & Reporting",
    "Automation & Pipelines", "Computer Vision", "Generative AI",
    "Data Engineering", "Other",
]
STATUSES = ["Completed", "In Progress", "Archived"]

def render():
    edit_id = st.session_state.get("edit_id")
    existing = get_usecase(edit_id) if edit_id else None

    title_text = "Edit Use Case" if existing else "Submit a Use Case"
    st.markdown(f'<div class="page-title">{title_text}</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Document your solution so other teams can find and learn from it.</div>', unsafe_allow_html=True)

    def val(key, default=""):
        if existing:
            v = existing.get(key, default)
            return v if v is not None else default
        return default

    def val_list(key):
        if existing:
            try:
                return json.loads(existing.get(key) or "[]")
            except Exception:
                return []
        return []

    with st.form("usecase_form", clear_on_submit=False):
        st.markdown("#### 📋 Basic Information")
        c1, c2 = st.columns(2)
        with c1:
            title = st.text_input("Use Case Title *", value=val("title"),
                                  placeholder="e.g. Action Recommendation System")
        with c2:
            # Merge DB categories with built-in list
            all_cats = list(dict.fromkeys(CATEGORIES + get_categories()))
            cat_idx = all_cats.index(val("category")) if val("category") in all_cats else 0
            category = st.selectbox("Category *", all_cats, index=cat_idx)

        c3, c4, c5 = st.columns([3, 1, 2])
        with c3:
            client = st.text_input("Client Name", value=val("client"),
                                   placeholder="e.g. Client XYZ")
        with c4:
            client_anon = st.checkbox("Anonymize client", value=bool(val("client_anon", False)))
        with c5:
            status_idx = STATUSES.index(val("status", "Completed")) if val("status", "Completed") in STATUSES else 0
            status = st.selectbox("Status", STATUSES, index=status_idx)

        st.markdown("#### 👥 Team")
        c6, c7 = st.columns(2)
        with c6:
            team_name = st.text_input("Team Name", value=val("team_name"),
                                      placeholder="e.g. Team Alpha")
        with c7:
            team_members = st.text_input("Team Members",
                                         value=val("team_members"),
                                         placeholder="Name, Name, Name…")

        c8, c9 = st.columns(2)
        with c8:
            start_date = st.text_input("Start Date", value=val("start_date"),
                                       placeholder="YYYY-MM-DD")
        with c9:
            end_date = st.text_input("End Date", value=val("end_date"),
                                     placeholder="YYYY-MM-DD")

        st.markdown("#### 📝 Content")
        description = st.text_area("Problem Description *",
                                   value=val("description"), height=110,
                                   placeholder="What did the client need? What problem were you solving?")
        solution = st.text_area("Solution Summary *",
                                value=val("solution"), height=110,
                                placeholder="How did you solve it? What approach / architecture did you use?")
        tech_stack = st.text_input("Tech Stack",
                                   value=val("tech_stack"),
                                   placeholder="e.g. Python, FastAPI, PostgreSQL, Docker")
        outcome = st.text_area("Outcome / Results",
                               value=val("outcome"), height=80,
                               placeholder="What was the impact? Metrics, improvements, etc.")

        st.markdown("#### 🔗 Links & Tags")
        links_raw = st.text_area("Links (one per line)",
                                 value="\n".join(val_list("links")), height=80,
                                 placeholder="https://github.com/…\nhttps://docs.google.com/…")
        tags_raw = st.text_input("Tags (comma-separated)",
                                 value=", ".join(val_list("tags")),
                                 placeholder="Recommendation, Python, ML, CRM…")

        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("💾  Save Use Case", use_container_width=True)

    if submitted:
        if not title.strip():
            st.error("Title is required.")
            return
        if not description.strip():
            st.error("Problem description is required.")
            return
        if not solution.strip():
            st.error("Solution summary is required.")
            return

        links = [l.strip() for l in links_raw.splitlines() if l.strip()]
        tags  = [t.strip() for t in tags_raw.split(",") if t.strip()]

        data = {
            "id": edit_id,
            "title": title.strip(),
            "category": category,
            "client": client.strip(),
            "client_anon": int(client_anon),
            "team_name": team_name.strip(),
            "team_members": team_members.strip(),
            "start_date": start_date.strip(),
            "end_date": end_date.strip(),
            "description": description.strip(),
            "solution": solution.strip(),
            "tech_stack": tech_stack.strip(),
            "outcome": outcome.strip(),
            "links": links,
            "tags": tags,
            "status": status,
        }
        uid = save_usecase(data)
        st.success("✅ Use case saved successfully!")
        st.session_state["edit_id"] = None
        st.session_state["view_id"] = uid
        st.session_state["page"] = "detail"
        st.rerun()

    if existing:
        st.markdown("<br>", unsafe_allow_html=True)
        with st.container():
            st.markdown('<div class="btn-secondary">', unsafe_allow_html=True)
            if st.button("← Cancel", key="cancel_edit"):
                st.session_state["edit_id"] = None
                st.session_state["page"] = "library"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
