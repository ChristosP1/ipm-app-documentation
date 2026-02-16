"""Global CSS styles for the developer documentation app."""

from __future__ import annotations

import streamlit as st

# ---------------------------------------------------------------------------
# Colour palette
# ---------------------------------------------------------------------------
METHOD_COLORS: dict[str, dict[str, str]] = {
    "GET": {"bg": "#DCFCE7", "fg": "#166534"},
    "POST": {"bg": "#DBEAFE", "fg": "#1E40AF"},
    "DELETE": {"bg": "#FEE2E2", "fg": "#991B1B"},
    "PUT": {"bg": "#FEF3C7", "fg": "#92400E"},
    "PATCH": {"bg": "#F3E8FF", "fg": "#6B21A8"},
}

# ---------------------------------------------------------------------------
# Global CSS injected once per page
# ---------------------------------------------------------------------------
GLOBAL_CSS = """
<style>
/* ---- Import font ---- */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

/* ---- Root variables ---- */
:root {
    --primary: #2563EB;
    --primary-dark: #1D4ED8;
    --primary-light: #DBEAFE;
    --success: #22C55E;
    --danger: #EF4444;
    --warning: #F59E0B;
    --slate-50: #F8FAFC;
    --slate-100: #F1F5F9;
    --slate-200: #E2E8F0;
    --slate-300: #CBD5E1;
    --slate-500: #64748B;
    --slate-700: #334155;
    --slate-900: #0F172A;
    --radius-sm: 4px;
    --radius-md: 8px;
    --radius-lg: 12px;
}

/* ---- Method badges ---- */
.method-badge {
    display: inline-block;
    padding: 2px 10px;
    border-radius: var(--radius-sm);
    font-weight: 700;
    font-size: 0.72rem;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: 0.03em;
    text-transform: uppercase;
    line-height: 1.6;
    min-width: 56px;
    text-align: center;
}
.method-get    { background: #DCFCE7; color: #166534; }
.method-post   { background: #DBEAFE; color: #1E40AF; }
.method-delete { background: #FEE2E2; color: #991B1B; }
.method-put    { background: #FEF3C7; color: #92400E; }
.method-patch  { background: #F3E8FF; color: #6B21A8; }

/* ---- Endpoint path ---- */
.endpoint-path {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.88rem;
    color: var(--slate-700);
}

/* ---- Auth badge ---- */
.auth-badge {
    display: inline-block;
    background: #FEF3C7;
    color: #92400E;
    padding: 2px 10px;
    border-radius: 12px;
    font-size: 0.7rem;
    font-weight: 500;
}

/* ---- Complexity badge ---- */
.complexity-simple   { background: #DCFCE7; color: #166534; }
.complexity-moderate { background: #FEF3C7; color: #92400E; }
.complexity-complex  { background: #FEE2E2; color: #991B1B; }

/* ---- Cards ---- */
.endpoint-card {
    border: 1px solid var(--slate-200);
    border-radius: var(--radius-md);
    padding: 14px 18px;
    margin: 6px 0;
    transition: box-shadow 0.2s, border-color 0.2s;
    cursor: pointer;
    background: white;
}
.endpoint-card:hover {
    box-shadow: 0 4px 14px rgba(0,0,0,0.08);
    border-color: var(--primary);
}

/* ---- Section headers ---- */
.tag-header {
    font-size: 1.3rem;
    font-weight: 700;
    color: var(--slate-900);
    margin-top: 1.4rem;
    margin-bottom: 0.2rem;
    padding-bottom: 6px;
    border-bottom: 2px solid var(--primary);
}
.subcategory-header {
    font-size: 1rem;
    font-weight: 600;
    color: var(--slate-700);
    margin-top: 1rem;
    margin-bottom: 0.3rem;
}

/* ---- Stat pills ---- */
.stat-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 14px;
    border-radius: 20px;
    font-size: 0.82rem;
    font-weight: 600;
    background: var(--slate-100);
    color: var(--slate-700);
    margin-right: 8px;
}

/* ---- Schema table ---- */
.schema-table {
    width: 100%;
    border-collapse: collapse;
    margin: 12px 0;
    font-size: 0.88rem;
}
.schema-table th {
    background: var(--slate-100);
    text-align: left;
    padding: 8px 12px;
    font-weight: 600;
    color: var(--slate-700);
    border-bottom: 2px solid var(--slate-200);
}
.schema-table td {
    padding: 6px 12px;
    border-bottom: 1px solid var(--slate-200);
    color: var(--slate-700);
}
.schema-table .field-name {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.84rem;
    color: var(--primary-dark);
}
.schema-table .field-type {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.82rem;
    color: var(--slate-500);
}

/* ---- Process step cards ---- */
.process-step {
    display: flex;
    align-items: flex-start;
    gap: 14px;
    padding: 12px 16px;
    margin: 6px 0;
    border-left: 3px solid var(--primary);
    background: var(--slate-50);
    border-radius: 0 var(--radius-md) var(--radius-md) 0;
}
.process-step-number {
    display: flex;
    align-items: center;
    justify-content: center;
    min-width: 28px;
    height: 28px;
    border-radius: 50%;
    background: var(--primary);
    color: white;
    font-weight: 700;
    font-size: 0.8rem;
}

/* ---- Status code table ---- */
.status-code {
    display: inline-block;
    padding: 1px 8px;
    border-radius: var(--radius-sm);
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    font-weight: 600;
}
.status-2xx { background: #DCFCE7; color: #166534; }
.status-4xx { background: #FEF3C7; color: #92400E; }
.status-5xx { background: #FEE2E2; color: #991B1B; }

/* ---- Divider ---- */
.section-divider {
    border: none;
    border-top: 1px solid var(--slate-200);
    margin: 1.5rem 0;
}
</style>
"""


def inject_global_css() -> None:
    """Inject the global CSS once into the current Streamlit page."""
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)


def method_badge_html(method: str) -> str:
    """Return an HTML span for an HTTP method badge."""
    css_class = f"method-{method.lower()}"
    return f'<span class="method-badge {css_class}">{method}</span>'


def status_code_html(code: int) -> str:
    """Return an HTML span for a status code badge."""
    if code < 300:
        css_class = "status-2xx"
    elif code < 500:
        css_class = "status-4xx"
    else:
        css_class = "status-5xx"
    return f'<span class="status-code {css_class}">{code}</span>'
