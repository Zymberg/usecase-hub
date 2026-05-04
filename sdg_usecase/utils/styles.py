import streamlit as st

def inject_styles():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Plus+Jakarta+Sans:wght@500;600;700&display=swap');

    :root {
        --bg:          #f0f4f9;
        --bg2:         #ffffff;
        --bg3:         #f8fafc;
        --bg4:         #eef2f7;
        --border:      #dde3ed;
        --border2:     #c8d3e3;
        --navy:        #0a3878;
        --navy2:       #1554a0;
        --navy3:       #1e6fcc;
        --accent:      #0070d2;
        --accent-dim:  rgba(0,112,210,0.10);
        --accent-soft: #e8f2fd;
        --text:        #0b1f3a;
        --text2:       #3d5166;
        --text3:       #7a90a8;
        --card-bg:     #ffffff;
        --shadow:      0 1px 4px rgba(10,40,80,0.08), 0 0 0 1px rgba(10,40,80,0.04);
        --shadow-md:   0 4px 16px rgba(10,40,80,0.10), 0 1px 4px rgba(10,40,80,0.06);
        --shadow-blue: 0 4px 16px rgba(0,112,210,0.15);
    }

    html, body, [data-testid="stAppViewContainer"] {
        background: var(--bg) !important;
        color: var(--text) !important;
        font-family: 'Inter', sans-serif !important;
    }

    /* ── Global text ─────────────────────────────────────────────────────── */
    [data-testid="stAppViewContainer"] p,
    [data-testid="stAppViewContainer"] span,
    [data-testid="stAppViewContainer"] div,
    [data-testid="stAppViewContainer"] h1,
    [data-testid="stAppViewContainer"] h2,
    [data-testid="stAppViewContainer"] h3,
    [data-testid="stAppViewContainer"] h4,
    [data-testid="stAppViewContainer"] li {
        color: var(--text);
    }

    /* ── Sidebar ─────────────────────────────────────────────────────────── */
    [data-testid="stSidebar"] {
        background: var(--navy) !important;
        border-right: none !important;
        box-shadow: 2px 0 12px rgba(10,40,80,0.12) !important;
    }
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] div,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] caption,
    [data-testid="stSidebar"] small,
    [data-testid="stSidebar"] .stCaption,
    [data-testid="stSidebar"] .stCaption p,
    [data-testid="stSidebar"] [data-testid="stCaptionContainer"] p { color: #ffffff !important; }

    /* ── Lock sidebar open, hide all collapse controls ─────────────────── */
    [data-testid="stSidebarCollapseButton"],
    [data-testid="stSidebarCollapsedControl"],
    button[data-testid="baseButton-headerNoPadding"],
    [data-testid="collapsedControl"],
    section[data-testid="stSidebarCollapsedControl"] {
        display: none !important;
        visibility: hidden !important;
        width: 0 !important;
        pointer-events: none !important;
    }
    /* Force sidebar always visible and correct width */
    [data-testid="stSidebar"] {
        width: 18rem !important;
        min-width: 18rem !important;
        transform: translateX(0) !important;
        visibility: visible !important;
        display: block !important;
        position: relative !important;
    }
    [data-testid="stSidebar"][aria-expanded="false"],
    [data-testid="stSidebar"][aria-expanded="true"] {
        transform: translateX(0) !important;
        width: 18rem !important;
        min-width: 18rem !important;
        visibility: visible !important;
    }

    .sidebar-logo {
        padding: 16px 0 14px;
        border-bottom: 1px solid rgba(255,255,255,0.1);
        margin-bottom: 12px;
    }
    .logo-mark,
    [data-testid="stSidebar"] .logo-mark,
    [data-testid="stSidebar"] span.logo-mark {
        display: inline-block !important;
        background: rgba(255,255,255,0.15) !important;
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 800 !important;
        font-size: 13px !important;
        letter-spacing: 0.14em !important;
        padding: 3px 9px !important;
        border-radius: 4px !important;
        margin-bottom: 10px !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
    }
    .logo-text,
    [data-testid="stSidebar"] .logo-text,
    [data-testid="stSidebar"] span.logo-text {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 700 !important;
        font-size: 20px !important;
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        letter-spacing: -0.01em !important;
        line-height: 1 !important;
        display: block !important;
    }
    .logo-sub,
    [data-testid="stSidebar"] .logo-sub,
    [data-testid="stSidebar"] span.logo-sub {
        font-size: 10px !important;
        color: rgba(255,255,255,0.75) !important;
        -webkit-text-fill-color: rgba(255,255,255,0.75) !important;
        letter-spacing: 0.16em !important;
        text-transform: uppercase !important;
        font-weight: 500 !important;
        display: block !important;
        margin-top: 5px !important;
    }

    /* ── Sidebar nav buttons ─────────────────────────────────────────────── */
    [data-testid="stSidebar"] .stButton > button {
        background: transparent !important;
        border: none !important;
        color: #ffffff !important;
        text-align: left !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 13px !important;
        font-weight: 500 !important;
        padding: 9px 12px !important;
        border-radius: 6px !important;
        transition: all 0.15s ease !important;
        text-transform: none !important;
        box-shadow: none !important;
        letter-spacing: 0 !important;
    }
    [data-testid="stSidebar"] .stButton > button:hover {
        background: rgba(255,255,255,0.12) !important;
        color: #ffffff !important;
        box-shadow: none !important;
        transform: none !important;
    }

    /* ── All buttons base ────────────────────────────────────────────────── */
    .stButton > button {
        background: var(--accent) !important;
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        border: none !important;
        border-radius: 6px !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        font-size: 13px !important;
        letter-spacing: 0.01em !important;
        text-transform: none !important;
        padding: 7px 16px !important;
        transition: all 0.15s !important;
        white-space: nowrap !important;
        line-height: 1.5 !important;
        min-height: 0 !important;
        height: auto !important;
        box-shadow: 0 1px 3px rgba(0,112,210,0.3) !important;
    }
    .stButton > button:hover {
        background: var(--navy2) !important;
        box-shadow: var(--shadow-blue) !important;
        transform: translateY(-1px) !important;
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
    }
    .stButton > button:active { transform: translateY(0) !important; }

    /* ── Suggestion chips .sug-btns ──────────────────────────────────────── */
    .sug-btns .stButton > button {
        background: var(--bg2) !important;
        border: 1px solid var(--border) !important;
        border-radius: 8px !important;
        color: var(--text2) !important;
        font-size: 13px !important;
        font-weight: 400 !important;
        text-align: left !important;
        white-space: normal !important;
        word-break: break-word !important;
        padding: 9px 14px !important;
        line-height: 1.45 !important;
        height: auto !important;
        min-height: 40px !important;
        box-shadow: var(--shadow) !important;
        transform: none !important;
        letter-spacing: 0 !important;
    }
    .sug-btns .stButton > button:hover {
        border-color: var(--accent) !important;
        color: var(--accent) !important;
        box-shadow: 0 0 0 2px var(--accent-dim) !important;
        transform: none !important;
        background: var(--accent-soft) !important;
    }

    /* ── Category pills .cat-btns ────────────────────────────────────────── */
    .cat-btns .stButton > button {
        background: var(--bg2) !important;
        border: 1px solid var(--border) !important;
        border-radius: 20px !important;
        color: var(--text2) !important;
        font-size: 12px !important;
        font-weight: 500 !important;
        text-align: center !important;
        white-space: nowrap !important;
        padding: 5px 14px !important;
        min-height: 0 !important;
        height: auto !important;
        line-height: 1.5 !important;
        box-shadow: var(--shadow) !important;
        transform: none !important;
        letter-spacing: 0.01em !important;
    }
    .cat-btns .stButton > button:hover {
        background: var(--accent-soft) !important;
        border-color: var(--accent) !important;
        color: var(--accent) !important;
        box-shadow: none !important;
        transform: none !important;
    }

    /* ── Card view pill .view-btn ────────────────────────────────────────── */
    .view-btn .stButton > button {
        background: var(--accent-soft) !important;
        border: 1px solid var(--border2) !important;
        border-radius: 20px !important;
        color: var(--accent) !important;
        font-size: 12px !important;
        font-weight: 500 !important;
        padding: 4px 14px !important;
        min-height: 0 !important;
        height: auto !important;
        white-space: nowrap !important;
        box-shadow: none !important;
        transform: none !important;
    }
    .view-btn .stButton > button:hover {
        background: var(--accent) !important;
        border-color: var(--accent) !important;
        color: #fff !important;
        box-shadow: none !important;
        transform: none !important;
    }

    /* ── Submit CTA .submit-cta-btn ──────────────────────────────────────── */
    .submit-cta-btn .stButton > button {
        background: var(--accent) !important;
        border: none !important;
        border-radius: 8px !important;
        color: #ffffff !important;
        font-size: 14px !important;
        font-weight: 600 !important;
        padding: 10px 28px !important;
        box-shadow: var(--shadow-blue) !important;
        transform: none !important;
    }
    .submit-cta-btn .stButton > button:hover {
        background: var(--navy2) !important;
        box-shadow: 0 6px 20px rgba(0,112,210,0.25) !important;
        transform: translateY(-1px) !important;
    }

    /* ── Column buttons default ──────────────────────────────────────────── */
    div[data-testid="column"] .stButton > button {
        background: var(--bg2) !important;
        border: 1px solid var(--border) !important;
        border-radius: 6px !important;
        color: var(--text2) !important;
        font-size: 13px !important;
        font-weight: 500 !important;
        padding: 6px 16px !important;
        line-height: 1.5 !important;
        box-shadow: var(--shadow) !important;
        transform: none !important;
    }
    div[data-testid="column"] .stButton > button:hover {
        background: var(--accent-soft) !important;
        border-color: var(--accent) !important;
        color: var(--accent) !important;
        box-shadow: none !important;
        transform: none !important;
    }

    /* ── Inputs ───────────────────────────────────────────────────────────── */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: var(--bg2) !important;
        border: 1px solid var(--border) !important;
        color: var(--text) !important;
        border-radius: 6px !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 15px !important;
        font-weight: 400 !important;
        box-shadow: var(--shadow) !important;
    }
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 3px var(--accent-dim) !important;
    }
    .stTextInput > div > div > input::placeholder,
    .stTextArea > div > div > textarea::placeholder {
        color: var(--text3) !important;
    }
    label {
        color: var(--text3) !important;
        font-size: 11px !important;
        font-weight: 600 !important;
        letter-spacing: 0.08em !important;
        text-transform: uppercase !important;
    }

    /* ── Selectbox ────────────────────────────────────────────────────────── */
    [data-testid="stSelectbox"] > div > div,
    .stSelectbox > div > div {
        background: var(--bg2) !important;
        border: 1px solid var(--border) !important;
        border-radius: 6px !important;
        color: var(--text) !important;
        font-size: 15px !important;
        box-shadow: var(--shadow) !important;
    }
    /* Sidebar selectbox — white text on navy */
    [data-testid="stSidebar"] [data-testid="stSelectbox"] > div > div,
    [data-testid="stSidebar"] .stSelectbox > div > div {
        background: rgba(255,255,255,0.15) !important;
        border: 1px solid rgba(255,255,255,0.25) !important;
        color: #ffffff !important;
    }
    [data-testid="stSidebar"] [data-testid="stSelectbox"] span,
    [data-testid="stSidebar"] [data-testid="stSelectbox"] div { color: #ffffff !important; }

    /* ── Cards ────────────────────────────────────────────────────────────── */
    .usecase-card {
        background: var(--card-bg);
        border: 1px solid var(--border);
        border-radius: 10px;
        padding: 20px 22px;
        margin-bottom: 12px;
        transition: all 0.18s ease;
        box-shadow: var(--shadow);
        position: relative;
        overflow: hidden;
        flex: 1;
        display: flex;
        flex-direction: column;
        min-height: 220px;
        box-sizing: border-box;
    }
    .usecase-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: linear-gradient(90deg, var(--navy2), var(--accent));
        opacity: 0;
        transition: opacity 0.18s;
    }
    .usecase-card:hover {
        border-color: var(--accent);
        box-shadow: var(--shadow-blue);
        transform: translateY(-2px);
    }
    .usecase-card:hover::before { opacity: 1; }

    .card-title {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-weight: 600;
        font-size: 16px;
        color: var(--text) !important;
        margin-bottom: 7px;
        letter-spacing: -0.01em;
    }
    .card-meta {
        font-size: 11px;
        color: var(--text3) !important;
        margin-bottom: 10px;
        display: flex;
        gap: 14px;
        flex-wrap: wrap;
        font-weight: 500;
        letter-spacing: 0.03em;
        text-transform: uppercase;
    }
    .card-desc {
        font-size: 13px;
        color: var(--text2) !important;
        line-height: 1.7;
        margin-bottom: 14px;
        font-weight: 400;
        flex: 1;
    }
    .tag {
        display: inline-block;
        background: var(--accent-soft);
        color: var(--accent) !important;
        font-size: 10px;
        font-weight: 600;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        padding: 3px 9px;
        border-radius: 4px;
        border: 1px solid rgba(0,112,210,0.15);
        margin-right: 5px;
        margin-bottom: 4px;
    }
    .tag-green {
        background: #e6f9f0;
        color: #0a7a4a !important;
        border-color: rgba(10,122,74,0.2);
    }
    .tag-purple {
        background: #f0ecfd;
        color: #5b21b6 !important;
        border-color: rgba(91,33,182,0.2);
    }

    /* ── Page headings ────────────────────────────────────────────────────── */
    .page-title {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-weight: 700;
        font-size: 30px;
        color: var(--navy) !important;
        letter-spacing: -0.02em;
        margin-bottom: 5px;
        line-height: 1.15;
    }
    .page-subtitle {
        font-size: 15px;
        color: var(--text2) !important;
        margin-bottom: 28px;
        font-weight: 400;
        letter-spacing: 0;
    }

    /* ── Stat cards ───────────────────────────────────────────────────────── */
    .stat-card {
        background: var(--bg2);
        border: 1px solid var(--border);
        border-radius: 10px;
        padding: 20px 22px;
        text-align: left;
        box-shadow: var(--shadow);
        transition: all 0.18s;
        border-top: 3px solid var(--accent);
    }
    .stat-card:hover {
        box-shadow: var(--shadow-md);
        transform: translateY(-1px);
    }
    .stat-num {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-weight: 700;
        font-size: 36px;
        color: var(--navy) !important;
        line-height: 1;
        letter-spacing: -0.03em;
    }
    .stat-label {
        font-size: 11px;
        color: var(--text3) !important;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        font-weight: 600;
        margin-top: 5px;
    }

    /* ── Chat ─────────────────────────────────────────────────────────────── */
    .chat-user {
        background: var(--accent);
        color: #ffffff !important;
        border-radius: 14px 14px 3px 14px;
        padding: 11px 16px;
        max-width: 68%;
        margin-left: auto;
        margin-bottom: 10px;
        font-size: 15px;
        line-height: 1.55;
        box-shadow: 0 2px 8px rgba(0,112,210,0.25);
    }
    .chat-bot {
        background: var(--bg2);
        border: 1px solid var(--border);
        color: var(--text) !important;
        border-radius: 3px 14px 14px 14px;
        padding: 14px 18px;
        max-width: 88%;
        margin-bottom: 10px;
        font-size: 15px;
        line-height: 1.7;
        font-weight: 400;
        box-shadow: var(--shadow);
    }
    .chat-result-card {
        background: var(--bg2);
        border: 1px solid var(--border);
        border-left: 3px solid var(--accent);
        border-radius: 8px;
        padding: 14px 16px;
        margin: 8px 0;
        box-shadow: var(--shadow);
    }

    /* ── Detail ───────────────────────────────────────────────────────────── */
    .detail-header {
        background: linear-gradient(135deg, var(--accent-soft) 0%, #f0f6ff 100%);
        border: 1px solid rgba(0,112,210,0.15);
        border-radius: 12px;
        padding: 28px 32px;
        margin-bottom: 24px;
    }
    .detail-title {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-weight: 700;
        font-size: 24px;
        color: var(--navy) !important;
        letter-spacing: -0.02em;
        margin-bottom: 10px;
    }
    .section-heading {
        font-size: 10px;
        color: var(--text3) !important;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        margin-bottom: 8px;
        margin-top: 20px;
    }
    .info-block {
        background: var(--bg2);
        border: 1px solid var(--border);
        border-radius: 8px;
        padding: 14px 16px;
        font-size: 15px;
        color: var(--text2) !important;
        line-height: 1.75;
        font-weight: 400;
        box-shadow: var(--shadow);
    }

    /* ── Equal height cards ──────────────────────────────────────────────── */
    div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {
        display: flex !important;
        flex-direction: column !important;
    }
    div[data-testid="stHorizontalBlock"] > div[data-testid="column"] > div[data-testid="stVerticalBlock"] {
        flex: 1 !important;
        display: flex !important;
        flex-direction: column !important;
    }
    .usecase-card > div:last-child { margin-top: auto !important; }

    /* ── Alerts ───────────────────────────────────────────────────────────── */
    .stAlert { border-radius: 8px !important; }
    .stSuccess { background: #ecfdf5 !important; border: 1px solid #a7f3d0 !important; }
    .stSuccess * { color: #065f46 !important; }
    .stInfo    { background: var(--accent-soft) !important; border: 1px solid rgba(0,112,210,0.2) !important; }
    .stInfo *  { color: var(--navy2) !important; }
    .stWarning { background: #fffbeb !important; border: 1px solid #fcd34d !important; }
    .stWarning * { color: #92400e !important; }
    .stError   { background: #fff1f2 !important; border: 1px solid #fecdd3 !important; }
    .stError * { color: #9f1239 !important; }

    /* ── Expanders ────────────────────────────────────────────────────────── */
    [data-testid="stExpander"] {
        border: 1px solid var(--border) !important;
        border-radius: 8px !important;
        background: var(--bg2) !important;
        box-shadow: var(--shadow) !important;
        margin-bottom: 8px !important;
    }
    [data-testid="stExpander"] * { color: var(--text) !important; }
    [data-testid="stExpander"] .stCaption,
    [data-testid="stExpander"] .stCaption * { color: var(--text3) !important; }

    /* ── Misc ─────────────────────────────────────────────────────────────── */
    hr { border: none !important; border-top: 1px solid var(--border) !important; margin: 24px 0 !important; }
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding-top: 2rem !important; max-width: 1100px !important; }
    [data-testid="stDecoration"] { display: none; }
    a { color: var(--accent) !important; text-decoration: none !important; }
    a:hover { color: var(--navy2) !important; text-decoration: underline !important; }
    .stCaption, .stCaption p { color: var(--text3) !important; }
    .stMarkdown p, .stMarkdown li, .stMarkdown span { color: var(--text2) !important; }
    </style>
    """, unsafe_allow_html=True)
