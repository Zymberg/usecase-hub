import streamlit as st
from pathlib import Path
import sys
from dotenv import load_dotenv
import os 

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))

load_dotenv(ROOT / ".env")

st.set_page_config(
    page_title="TeamSync Use Case Hub",
    page_icon="🔗",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Force sidebar always visible — belt-and-suspenders approach
st.markdown("""<style>
[data-testid="stSidebarCollapseButton"]{display:none!important}
[data-testid="stSidebarCollapsedControl"]{display:none!important}
[data-testid="collapsedControl"]{display:none!important}
section[data-testid="stSidebarCollapsedControl"]{display:none!important}
[data-testid="stSidebar"]{transform:translateX(0)!important;width:18rem!important;min-width:18rem!important;visibility:visible!important}
</style>""", unsafe_allow_html=True)

from utils.styles import inject_styles
from utils.database import init_db
from utils.session import init_session

inject_styles()
init_db()
init_session()

# ── Admin credentials — change these ────────────────────────────────────────
# ── Admin credentials — change these ────────────────────────────────────────
ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")

# ── Session state defaults ───────────────────────────────────────────────────
if "user_role"        not in st.session_state: st.session_state["user_role"]        = "Viewer"
if "admin_logged_in"  not in st.session_state: st.session_state["admin_logged_in"]  = False
if "show_admin_login" not in st.session_state: st.session_state["show_admin_login"] = False

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        """
        <div class="sidebar-logo">
            <span class="logo-mark" style="color:#ffffff;">SDG</span>
            <span class="logo-text" style="color:#ffffff;">TeamSync</span>
            <span class="logo-sub" style="color:rgba(255,255,255,0.7);">Use Case Hub</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    nav_items = {
        "🏠  Home":            "home",
        "📚  Browse Library":  "library",
        "➕  Submit Use Case": "submit",
        "🤖  AI Assistant":    "chat",
        "⚙️  Admin":           "admin",
    }

    for label, key in nav_items.items():
        if st.button(label, key=f"nav_{key}", use_container_width=True):
            st.session_state["page"] = key
            st.rerun()

    st.markdown("---")

    # ── Role selector ────────────────────────────────────────────────────────
    role_options = ["Viewer", "Admin"]
    current_role = st.session_state["user_role"]
    selected_role = st.selectbox("Role", role_options,
                                  index=role_options.index(current_role),
                                  key="_role_selector")

    # Switching TO Admin → show login form
    if selected_role == "Admin" and not st.session_state["admin_logged_in"]:
        st.session_state["show_admin_login"] = True
        st.session_state["user_role"] = current_role  # don't grant yet

    # Switching AWAY from Admin → log out
    elif selected_role != "Admin" and st.session_state["admin_logged_in"]:
        st.session_state["admin_logged_in"]  = False
        st.session_state["show_admin_login"] = False
        st.session_state["user_role"]        = selected_role
        st.rerun()

    elif selected_role != "Admin":
        st.session_state["user_role"]        = selected_role
        st.session_state["show_admin_login"] = False

    # ── Admin login form (shows inline in sidebar) ───────────────────────────
    if st.session_state["show_admin_login"] and not st.session_state["admin_logged_in"]:
        st.markdown('<div style="background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.15);border-radius:8px;padding:14px 14px 10px;">', unsafe_allow_html=True)
        st.markdown('<p style="font-size:11px;font-weight:600;color:#6e7e99;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:8px;">Admin Login</p>', unsafe_allow_html=True)
        username = st.text_input("Username", key="admin_user_input", placeholder="username")
        password = st.text_input("Password", type="password", key="admin_pass_input", placeholder="••••••••")
        col_login, col_cancel = st.columns(2)
        with col_login:
            if st.button("Login", key="admin_login_btn", use_container_width=True):
                if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
                    st.session_state["admin_logged_in"]  = True
                    st.session_state["show_admin_login"] = False
                    st.session_state["user_role"]        = "Admin"
                    st.rerun()
                else:
                    st.error("Wrong credentials")
        with col_cancel:
            if st.button("Cancel", key="admin_cancel_btn", use_container_width=True):
                st.session_state["show_admin_login"] = False
                st.session_state["user_role"]        = "Viewer"
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Status caption ───────────────────────────────────────────────────────
    role_display = st.session_state["user_role"]
    lock = "🔒" if role_display == "Admin" else ""
    st.caption(f"Logged in as: **Demo User** · {role_display} {lock}")

    if st.session_state["admin_logged_in"]:
        if st.button("🔓 Logout Admin", key="admin_logout", use_container_width=True):
            st.session_state["admin_logged_in"]  = False
            st.session_state["show_admin_login"] = False
            st.session_state["user_role"]        = "Viewer"
            st.rerun()

# ── Page routing ─────────────────────────────────────────────────────────────
page = st.session_state.get("page", "home")

if page == "home":
    from views.home import render
elif page == "library":
    from views.library import render
elif page == "submit":
    from views.submit import render
elif page == "chat":
    from views.chat import render
elif page == "admin":
    from views.admin import render
elif page == "detail":
    from views.detail import render
else:
    from views.home import render

render()
