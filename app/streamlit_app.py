import streamlit as st
import requests
import sys
from pathlib import Path
import json

sys.path.append(str(Path(__file__).parent.parent))

# ─────────────────────────────────────────────
#  PAGE CONFIG  (must be FIRST streamlit call)
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="LexAI · Legal Intelligence",
    page_icon="⚖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  DESIGN SYSTEM — full CSS injection
# ─────────────────────────────────────────────
DARK_CSS = """
<style>
/* ══════════════════════════════════════════
   0.  GOOGLE FONTS
══════════════════════════════════════════ */
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

/* ══════════════════════════════════════════
   1.  DESIGN TOKENS
══════════════════════════════════════════ */
:root {
    --bg-void:        #080B10;
    --bg-base:        #0D1117;
    --bg-surface:     #161B22;
    --bg-elevated:    #1C2333;
    --bg-hover:       #21283A;

    --accent-gold:    #C9A84C;
    --accent-glow:    #E8C97B;
    --accent-dim:     #8A6A20;

    --green-ok:       #2EA84F;
    --red-err:        #E05252;
    --blue-info:      #3B82F6;

    --text-primary:   #E8EDF3;
    --text-secondary: #8B96A8;
    --text-muted:     #4A5568;
    --text-gold:      #C9A84C;

    --border-subtle:  rgba(255,255,255,0.06);
    --border-active:  rgba(201,168,76,0.5);
    --border-card:    rgba(255,255,255,0.08);

    --shadow-card:    0 4px 24px rgba(0,0,0,0.5);
    --shadow-glow:    0 0 30px rgba(201,168,76,0.15);

    --radius-sm:  6px;
    --radius-md:  12px;
    --radius-lg:  20px;
    --radius-xl:  28px;

    --font-display: 'Playfair Display', Georgia, serif;
    --font-body:    'DM Sans', system-ui, sans-serif;
    --font-mono:    'DM Mono', 'Fira Code', monospace;
}

/* ══════════════════════════════════════════
   2.  GLOBAL RESET & BASE
══════════════════════════════════════════ */
*, *::before, *::after { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"],
[data-testid="stApp"], .main {
    background-color: var(--bg-base) !important;
    color: var(--text-primary) !important;
    font-family: var(--font-body) !important;
}

/* Ambient radial glow top-left */
[data-testid="stApp"]::after {
    content: '';
    position: fixed; top: -200px; left: -200px;
    width: 700px; height: 700px;
    background: radial-gradient(circle, rgba(201,168,76,0.06) 0%, transparent 70%);
    pointer-events: none; z-index: 0;
}

/* ══════════════════════════════════════════
   3.  SCROLLBAR
══════════════════════════════════════════ */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg-base); }
::-webkit-scrollbar-thumb { background: var(--accent-dim); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--accent-gold); }

/* ══════════════════════════════════════════
   4.  SIDEBAR
══════════════════════════════════════════ */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, var(--bg-void) 0%, #0A0F16 100%) !important;
    border-right: 1px solid var(--border-subtle) !important;
    padding-top: 0 !important;
}
[data-testid="stSidebar"] > div:first-child { padding-top: 0 !important; }

.sidebar-brand {
    padding: 28px 20px 24px;
    border-bottom: 1px solid var(--border-subtle);
    margin-bottom: 8px;
    background: linear-gradient(135deg, rgba(201,168,76,0.08) 0%, transparent 60%);
}
.sidebar-brand-icon  { font-size: 2rem; display: block; margin-bottom: 6px; }
.sidebar-brand-name  {
    font-family: var(--font-display); font-size: 1.4rem; font-weight: 900;
    color: var(--accent-gold); letter-spacing: -0.02em; display: block;
}
.sidebar-brand-tagline {
    font-size: 0.72rem; color: var(--text-muted);
    letter-spacing: 0.12em; text-transform: uppercase;
    margin-top: 2px; display: block;
}
.sidebar-section-label {
    font-size: 0.65rem; letter-spacing: 0.18em; text-transform: uppercase;
    color: var(--text-muted); padding: 16px 20px 6px;
    display: block; font-weight: 600;
}
.status-badge {
    display: flex; align-items: center; gap: 8px;
    padding: 10px 14px; border-radius: var(--radius-md);
    font-size: 0.82rem; font-weight: 500; margin: 0 12px 8px;
}
.status-badge.online  { background: rgba(46,168,79,0.12);  border: 1px solid rgba(46,168,79,0.25);  color: #4ADE80; }
.status-badge.offline { background: rgba(224,82,82,0.12); border: 1px solid rgba(224,82,82,0.25); color: #FC8181; }
.status-dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }
.status-dot.online  { background: #4ADE80; box-shadow: 0 0 6px #4ADE80; animation: pulse-green 2s infinite; }
.status-dot.offline { background: #FC8181; }

@keyframes pulse-green {
    0%,100% { box-shadow: 0 0 4px #4ADE80; }
    50%      { box-shadow: 0 0 10px #4ADE80; }
}

/* ══════════════════════════════════════════
   5.  MAIN CONTENT AREA
══════════════════════════════════════════ */
[data-testid="stMainBlockContainer"] {
    padding: 2rem 3rem !important;
    position: relative; z-index: 1;
}

/* ══════════════════════════════════════════
   6.  HERO HEADER
══════════════════════════════════════════ */
.hero-wrap {
    padding-bottom: 32px;
    border-bottom: 1px solid var(--border-subtle);
    margin-bottom: 40px;
    position: relative;
}
.hero-wrap::after {
    content: ''; position: absolute;
    bottom: -1px; left: 0; width: 120px; height: 2px;
    background: linear-gradient(90deg, var(--accent-gold), transparent);
}
.hero-eyebrow {
    font-size: 0.7rem; letter-spacing: 0.22em; text-transform: uppercase;
    color: var(--accent-gold); font-weight: 600; margin-bottom: 10px;
    display: flex; align-items: center; gap: 8px;
}
.hero-eyebrow::before {
    content: ''; display: inline-block; width: 24px; height: 1px;
    background: var(--accent-gold);
}
.hero-title {
    font-family: var(--font-display);
    font-size: clamp(2rem, 4vw, 3.2rem);
    font-weight: 900; line-height: 1.05;
    letter-spacing: -0.03em; color: var(--text-primary); margin-bottom: 14px;
}
.hero-title span { color: var(--accent-gold); }
.hero-subtitle {
    font-size: 0.95rem; color: var(--text-secondary);
    line-height: 1.6; max-width: 540px; font-weight: 300;
}
.tech-pill {
    display: inline-flex; align-items: center; gap: 5px;
    background: var(--bg-surface); border: 1px solid var(--border-card);
    border-radius: 20px; padding: 5px 12px; font-size: 0.72rem;
    color: var(--text-secondary); margin: 3px 2px;
    font-family: var(--font-mono); letter-spacing: 0.02em;
}
.tech-pill-dot { width: 5px; height: 5px; border-radius: 50%; background: var(--accent-gold); }

/* ══════════════════════════════════════════
   7.  SECTION LABELS
══════════════════════════════════════════ */
.section-label {
    font-size: 0.68rem; letter-spacing: 0.2em; text-transform: uppercase;
    color: var(--text-muted); font-weight: 600; margin-bottom: 12px;
    display: flex; align-items: center; gap: 8px;
}
.section-label::after { content: ''; flex: 1; height: 1px; background: var(--border-subtle); }

/* ══════════════════════════════════════════
   8.  TEXT AREA
══════════════════════════════════════════ */
div[data-testid="stTextArea"] textarea {
    background: var(--bg-surface) !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: var(--radius-md) !important;
    font-family: var(--font-body) !important;
    font-size: 0.95rem !important;
    line-height: 1.6 !important;
    padding: 16px !important;
    transition: border-color 0.25s, box-shadow 0.25s !important;
}
div[data-testid="stTextArea"] textarea:focus {
    border-color: var(--accent-dim) !important;
    box-shadow: 0 0 0 3px rgba(201,168,76,0.12) !important;
    outline: none !important;
}
div[data-testid="stTextArea"] textarea::placeholder { color: var(--text-muted) !important; }
div[data-testid="stTextArea"] label { color: var(--text-secondary) !important; font-size: 0.82rem !important; }

/* ══════════════════════════════════════════
   9.  BUTTONS
══════════════════════════════════════════ */
div[data-testid="stButton"] > button[kind="primary"] {
    background: linear-gradient(135deg, #C9A84C, #E8C97B, #C9A84C) !important;
    color: #080B10 !important; border: none !important;
    border-radius: var(--radius-md) !important;
    font-family: var(--font-body) !important; font-size: 0.88rem !important;
    font-weight: 700 !important; letter-spacing: 0.05em !important;
    padding: 13px 24px !important; text-transform: uppercase !important;
    box-shadow: 0 4px 20px rgba(201,168,76,0.3) !important;
    transition: all 0.25s !important; width: 100% !important;
}
div[data-testid="stButton"] > button[kind="primary"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(201,168,76,0.45) !important;
    filter: brightness(1.08) !important;
}
div[data-testid="stButton"] > button:not([kind="primary"]) {
    background: transparent !important; color: var(--text-secondary) !important;
    border: 1px solid var(--border-card) !important;
    border-radius: var(--radius-md) !important;
    font-family: var(--font-body) !important; font-size: 0.82rem !important;
    padding: 10px 16px !important; transition: all 0.2s !important;
    width: 100% !important;
}
div[data-testid="stButton"] > button:not([kind="primary"]):hover {
    border-color: var(--accent-dim) !important;
    color: var(--accent-glow) !important;
    background: rgba(201,168,76,0.06) !important;
    transform: translateX(3px) !important;
}

/* ══════════════════════════════════════════
   10.  SLIDER & CHECKBOX
══════════════════════════════════════════ */
div[data-testid="stSlider"] > div > div > div > div { background: var(--accent-gold) !important; }
div[data-testid="stSlider"] label,
div[data-testid="stCheckbox"] label { color: var(--text-secondary) !important; font-size: 0.82rem !important; }

/* ══════════════════════════════════════════
   11.  ANSWER CARD
══════════════════════════════════════════ */
.answer-card {
    background: var(--bg-surface); border: 1px solid var(--border-card);
    border-radius: var(--radius-lg); padding: 28px 32px; margin: 24px 0;
    position: relative; overflow: hidden; box-shadow: var(--shadow-card);
}
.answer-card::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, var(--accent-gold), transparent);
}
.answer-card-header { display: flex; align-items: center; gap: 10px; margin-bottom: 16px; }
.answer-card-icon {
    width: 32px; height: 32px; background: rgba(201,168,76,0.15);
    border-radius: 8px; display: flex; align-items: center;
    justify-content: center; font-size: 0.9rem; flex-shrink: 0;
}
.answer-card-title { font-size: 0.7rem; letter-spacing: 0.2em; text-transform: uppercase; color: var(--accent-gold); font-weight: 600; }
.answer-text { font-size: 1rem; line-height: 1.75; color: var(--text-primary); font-weight: 300; }

/* ══════════════════════════════════════════
   12.  NATIVE METRIC OVERRIDES
══════════════════════════════════════════ */
div[data-testid="stMetric"] {
    background: var(--bg-surface) !important;
    border: 1px solid var(--border-card) !important;
    border-radius: var(--radius-md) !important;
    padding: 16px !important;
}
div[data-testid="stMetric"] label {
    color: var(--text-muted) !important; font-size: 0.68rem !important;
    letter-spacing: 0.12em !important; text-transform: uppercase !important;
}
div[data-testid="stMetricValue"] {
    color: var(--text-primary) !important;
    font-family: var(--font-display) !important; font-size: 1.6rem !important;
}

/* ══════════════════════════════════════════
   13.  SOURCES
══════════════════════════════════════════ */
.sources-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px; }
.sources-count {
    background: rgba(201,168,76,0.12); border: 1px solid var(--accent-dim);
    color: var(--accent-gold); border-radius: 20px; padding: 3px 12px;
    font-size: 0.75rem; font-family: var(--font-mono); font-weight: 500;
}
div[data-testid="stExpander"] {
    background: var(--bg-surface) !important;
    border: 1px solid var(--border-card) !important;
    border-radius: var(--radius-md) !important; margin-bottom: 8px !important;
}
div[data-testid="stExpander"]:hover { border-color: var(--border-active) !important; }
div[data-testid="stExpander"] summary {
    color: var(--text-primary) !important; font-size: 0.85rem !important;
    font-weight: 500 !important; padding: 14px 16px !important;
}
div[data-testid="stExpander"] > div[role="group"] {
    border-top: 1px solid var(--border-subtle) !important;
    background: var(--bg-elevated) !important; padding: 16px !important;
}
.source-meta { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 14px; }
.source-meta-item { background: var(--bg-surface); border-radius: var(--radius-sm); padding: 10px 14px; border: 1px solid var(--border-subtle); }
.source-meta-label { font-size: 0.65rem; letter-spacing: 0.12em; text-transform: uppercase; color: var(--text-muted); margin-bottom: 4px; }
.source-meta-value { font-family: var(--font-mono); font-size: 0.82rem; color: var(--text-primary); }
.source-text-block {
    background: var(--bg-void); border: 1px solid var(--border-subtle);
    border-radius: var(--radius-sm); padding: 14px;
    font-family: var(--font-mono); font-size: 0.8rem;
    color: var(--text-secondary); line-height: 1.65; white-space: pre-wrap;
}
.similarity-bar-wrap { margin-top: 10px; }
.similarity-bar-label { display: flex; justify-content: space-between; font-size: 0.72rem; color: var(--text-muted); margin-bottom: 5px; }
.similarity-bar { height: 4px; border-radius: 2px; background: var(--bg-void); overflow: hidden; }
.similarity-fill { height: 100%; border-radius: 2px; background: linear-gradient(90deg, var(--accent-dim), var(--accent-gold)); transition: width 0.6s ease; }

/* ══════════════════════════════════════════
   14.  DOWNLOAD BUTTONS
══════════════════════════════════════════ */
div[data-testid="stDownloadButton"] > button {
    background: transparent !important; color: var(--text-secondary) !important;
    border: 1px solid var(--border-card) !important;
    border-radius: var(--radius-sm) !important;
    font-family: var(--font-mono) !important; font-size: 0.78rem !important;
    padding: 8px 16px !important; transition: all 0.2s !important;
}
div[data-testid="stDownloadButton"] > button:hover {
    border-color: var(--accent-dim) !important;
    color: var(--accent-glow) !important;
    background: rgba(201,168,76,0.06) !important;
}

/* ══════════════════════════════════════════
   15.  DIVIDERS / ALERTS / JSON
══════════════════════════════════════════ */
hr[data-testid="stDivider"] { border-color: var(--border-subtle) !important; margin: 28px 0 !important; }

div[data-testid="stAlert"][data-type="error"]   { background: rgba(224,82,82,0.1) !important; border: 1px solid rgba(224,82,82,0.3) !important; color: #FC8181 !important; border-radius: var(--radius-md) !important; }
div[data-testid="stAlert"][data-type="info"]    { background: rgba(59,130,246,0.1) !important; border: 1px solid rgba(59,130,246,0.25) !important; color: #93C5FD !important; border-radius: var(--radius-md) !important; }
div[data-testid="stAlert"][data-type="success"] { background: rgba(46,168,79,0.1) !important; border: 1px solid rgba(46,168,79,0.25) !important; color: #6EE7B7 !important; border-radius: var(--radius-md) !important; }

div[data-testid="stJson"] { background: var(--bg-void) !important; border-radius: var(--radius-sm) !important; font-family: var(--font-mono) !important; font-size: 0.78rem !important; }

/* ══════════════════════════════════════════
   16.  FOOTER
══════════════════════════════════════════ */
.lex-footer {
    margin-top: 60px; padding-top: 24px;
    border-top: 1px solid var(--border-subtle);
    display: flex; align-items: center; justify-content: space-between;
    color: var(--text-muted); font-size: 0.75rem; flex-wrap: wrap; gap: 12px;
}
.lex-footer-brand { font-family: var(--font-display); color: var(--accent-dim); font-weight: 700; font-size: 0.9rem; }
.lex-footer-stack { display: flex; gap: 8px; flex-wrap: wrap; }
.lex-footer-tag {
    background: var(--bg-surface); border: 1px solid var(--border-subtle);
    border-radius: 4px; padding: 2px 8px;
    font-family: var(--font-mono); font-size: 0.7rem; color: var(--text-muted);
}
</style>
"""

st.markdown(DARK_CSS, unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  CONSTANTS
# ─────────────────────────────────────────────
try:
    from src.config import config
    API_URL = f"http://localhost:{config.API_PORT}"
except Exception:
    API_URL = "http://localhost:8000"


# ─────────────────────────────────────────────
#  BACKEND HELPERS  (logic unchanged)
# ─────────────────────────────────────────────
def check_api_health():
    try:
        r = requests.get(f"{API_URL}/health", timeout=3)
        return r.json()
    except Exception:
        return None

def query_api(question: str, top_k: int, return_sources: bool):
    try:
        r = requests.post(
            f"{API_URL}/query",
            json={"question": question, "top_k": top_k, "return_sources": return_sources},
            timeout=30,
        )
        r.raise_for_status()
        return r.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {e}")
        return None

def get_api_stats():
    try:
        r = requests.get(f"{API_URL}/stats", timeout=3)
        return r.json()
    except Exception:
        return None


# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:

    # Brand block
    st.markdown("""
    <div class="sidebar-brand">
        <span class="sidebar-brand-icon">⚖</span>
        <span class="sidebar-brand-name">LexAI</span>
        <span class="sidebar-brand-tagline">Legal Intelligence Platform</span>
    </div>
    """, unsafe_allow_html=True)

    # API Status
    st.markdown('<span class="sidebar-section-label">System Status</span>', unsafe_allow_html=True)
    health = check_api_health()

    if health and health.get("status") == "healthy":
        idx_size = health.get("index_size", 0)
        st.markdown(f"""
        <div class="status-badge online">
            <span class="status-dot online"></span>
            API Connected &nbsp;·&nbsp; {idx_size} chunks indexed
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="status-badge offline">
            <span class="status-dot offline"></span>
            API Offline — run <code>python api/main.py</code>
        </div>
        """, unsafe_allow_html=True)
        st.stop()

    st.markdown("<br>", unsafe_allow_html=True)

    # Retrieval settings
    st.markdown('<span class="sidebar-section-label">Retrieval Settings</span>', unsafe_allow_html=True)
    top_k = st.slider("Documents to retrieve", 1, 10, 5)
    return_sources = st.checkbox("Show source evidence", value=True)

    st.divider()

    # Example questions
    st.markdown('<span class="sidebar-section-label">Quick Queries</span>', unsafe_allow_html=True)
    examples = [
        "What are the termination clauses?",
        "What are the payment terms?",
        "Who are the parties to the contract?",
        "What are the confidentiality obligations?",
        "What is the governing law?",
        "What are the intellectual property rights?",
        "What is the limitation of liability?",
        "What are the non-compete restrictions?",
    ]
    for eq in examples:
        if st.button(eq, key=f"ex_{eq}", use_container_width=True):
            st.session_state.question = eq

    st.divider()

    # System stats (collapsed by default)
    with st.expander("📊 System Statistics"):
        stats = get_api_stats()
        if stats:
            st.json(stats)
        else:
            st.caption("Unable to fetch stats")


# ─────────────────────────────────────────────
#  MAIN — HERO HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero-wrap">
    <div class="hero-eyebrow">Sentence-BERT · FAISS · GPT-3.5</div>
    <h1 class="hero-title">Legal <span>Contract</span><br>Intelligence</h1>
    <p class="hero-subtitle">
        Ask any question about your contracts. Our retrieval-augmented system
        surfaces precise answers from your document corpus in seconds.
    </p>
    <div style="margin-top:18px">
        <span class="tech-pill"><span class="tech-pill-dot"></span>Sentence-BERT</span>
        <span class="tech-pill"><span class="tech-pill-dot"></span>FAISS</span>
        <span class="tech-pill"><span class="tech-pill-dot"></span>LangChain</span>
        <span class="tech-pill"><span class="tech-pill-dot"></span>GPT-3.5</span>
        <span class="tech-pill"><span class="tech-pill-dot"></span>RAG</span>
    </div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  MAIN — QUERY INPUT
# ─────────────────────────────────────────────
st.markdown('<div class="section-label">Your Query</div>', unsafe_allow_html=True)

col_input, col_btn = st.columns([5, 1])

with col_input:
    question = st.text_area(
        label="Question",
        label_visibility="collapsed",
        value=st.session_state.get("question", ""),
        height=110,
        placeholder="e.g.  What are the termination conditions and required notice period?",
        key="query_input",
    )

with col_btn:
    st.write("")
    st.write("")
    run = st.button("⚡  Search", type="primary", use_container_width=True)
    st.write("")
    if st.button("✕  Clear", use_container_width=True):
        st.session_state.question = ""
        st.rerun()


# ─────────────────────────────────────────────
#  MAIN — RESULTS
# ─────────────────────────────────────────────
if run and question:
    with st.spinner("Retrieving and synthesising…"):
        result = query_api(question, top_k, return_sources)

    if result:
        st.session_state.last_result = result

        # Answer card
        st.markdown(f"""
        <div class="answer-card">
            <div class="answer-card-header">
                <div class="answer-card-icon">✦</div>
                <span class="answer-card-title">Generated Answer</span>
            </div>
            <p class="answer-text">{result['answer']}</p>
        </div>
        """, unsafe_allow_html=True)

        # Performance metrics
        if result.get("metadata"):
            meta = result["metadata"]
            st.markdown('<div class="section-label">Performance Metrics</div>', unsafe_allow_html=True)
            c1, c2, c3, c4 = st.columns(4)
            with c1:
                st.metric("Sources", meta["num_sources"])
            with c2:
                st.metric("Retrieval", f"{meta['retrieval_time']:.2f}s")
            with c3:
                st.metric("Generation", f"{meta['generation_time']:.2f}s")
            with c4:
                st.metric("Avg Similarity", f"{meta['avg_similarity']:.3f}")

        # Source evidence
        if return_sources and result.get("sources"):
            st.divider()
            st.markdown(f"""
            <div class="sources-header">
                <div class="section-label" style="margin-bottom:0;flex:1">Source Evidence</div>
                <span class="sources-count">{len(result['sources'])} documents retrieved</span>
            </div>
            """, unsafe_allow_html=True)

            for idx, src in enumerate(result["sources"], 1):
                score = src["similarity_score"]
                bar_w = int(score * 100)
                with st.expander(
                    f"[{idx:02d}]  {src['source_file']}  ·  score {score:.4f}",
                    expanded=(idx == 1),
                ):
                    st.markdown(f"""
                    <div class="source-meta">
                        <div class="source-meta-item">
                            <div class="source-meta-label">File</div>
                            <div class="source-meta-value">{src['source_file']}</div>
                        </div>
                        <div class="source-meta-item">
                            <div class="source-meta-label">Chunk ID</div>
                            <div class="source-meta-value">#{src['chunk_id']}</div>
                        </div>
                    </div>
                    <div class="similarity-bar-wrap">
                        <div class="similarity-bar-label">
                            <span>Similarity Score</span>
                            <span style="color:var(--accent-gold);font-family:var(--font-mono)">{score:.4f}</span>
                        </div>
                        <div class="similarity-bar">
                            <div class="similarity-fill" style="width:{bar_w}%"></div>
                        </div>
                    </div>
                    <br>
                    <div class="source-meta-label" style="margin-top:4px">Content Excerpt</div>
                    <div class="source-text-block">{src['text']}</div>
                    """, unsafe_allow_html=True)

        # Export
        st.divider()
        st.markdown('<div class="section-label">Export Results</div>', unsafe_allow_html=True)
        dcol1, dcol2, _ = st.columns([1, 1, 3])
        result_json = json.dumps(result, indent=2)
        with dcol1:
            st.download_button("⬇ JSON", result_json, "lex_result.json", "application/json", use_container_width=True)
        result_txt = f"Question: {result['question']}\n\nAnswer:\n{result['answer']}\n\nSources:\n"
        if result.get("sources"):
            for i, s in enumerate(result["sources"], 1):
                result_txt += f"\n{i}. {s['source_file']} (score: {s['similarity_score']:.4f})\n{s['text'][:300]}...\n"
        with dcol2:
            st.download_button("⬇ TXT", result_txt, "lex_result.txt", "text/plain", use_container_width=True)


# ─────────────────────────────────────────────
#  EMPTY STATE
# ─────────────────────────────────────────────
elif not question:
    st.markdown("""
    <div style="text-align:center;padding:60px 20px;color:var(--text-muted)">
        <div style="font-size:3rem;margin-bottom:16px;opacity:0.25">⚖</div>
        <div style="font-family:'Playfair Display',Georgia,serif;font-size:1.2rem;
                    color:var(--text-muted);margin-bottom:8px">
            Ready to analyse your contracts
        </div>
        <div style="font-size:0.85rem;max-width:380px;margin:0 auto;line-height:1.6">
            Enter a question above or pick a quick query from the sidebar
        </div>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div class="lex-footer">
    <span class="lex-footer-brand">LexAI</span>
    <span>Sentence-BERT RAG · Portfolio Project</span>
    <div class="lex-footer-stack">
        <span class="lex-footer-tag">FastAPI</span>
        <span class="lex-footer-tag">Streamlit</span>
        <span class="lex-footer-tag">FAISS</span>
        <span class="lex-footer-tag">PyTorch</span>
        <span class="lex-footer-tag">OpenAI</span>
    </div>
</div>
""", unsafe_allow_html=True)