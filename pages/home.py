"""Home page – Interactive architecture diagram of the IPM platform."""

from __future__ import annotations

import streamlit as st
import streamlit.components.v1 as components

from components.architecture_diagram import build_diagram_html
from components.styles import inject_global_css

inject_global_css()

st.title("IPM Partners Backend")
st.markdown(
    "Interactive architecture overview of the platform. "
    "**Hover** on any entity to see its endpoints or data fields. "
    "**Click** an endpoint link to view its full documentation."
)

st.markdown("---")

# Legend
st.markdown(
    '<div style="display:flex;gap:20px;margin-bottom:12px;flex-wrap:wrap;">'
    '<div style="display:flex;align-items:center;gap:6px;">'
    '<div style="width:16px;height:16px;border-radius:4px;background:linear-gradient(135deg,#2563EB,#1D4ED8);"></div>'
    '<span style="font-size:0.82rem;color:#475569;">Human actor (hover for endpoints)</span></div>'
    '<div style="display:flex;align-items:center;gap:6px;">'
    '<div style="width:16px;height:16px;border-radius:4px;background:linear-gradient(135deg,#475569,#334155);"></div>'
    '<span style="font-size:0.82rem;color:#475569;">Data entity (hover for fields)</span></div>'
    "</div>",
    unsafe_allow_html=True,
)

# Render diagram
diagram_html = build_diagram_html()
components.html(diagram_html, height=620, scrolling=False)

st.markdown("---")

# Quick navigation cards
st.markdown("### Quick Navigation")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        '<div style="background:#F1F5F9;border-radius:8px;padding:16px;">'
        '<div style="font-weight:600;font-size:1rem;color:#0F172A;">All Endpoints</div>'
        '<div style="font-size:0.82rem;color:#64748B;margin-top:4px;">'
        "Browse all 48 endpoints organized by category and sub-category.</div></div>",
        unsafe_allow_html=True,
    )
    if st.button("Browse endpoints", icon=":material/list_alt:", key="nav_ep"):
        st.switch_page("pages/all_endpoints.py")

with col2:
    st.markdown(
        '<div style="background:#F1F5F9;border-radius:8px;padding:16px;">'
        '<div style="font-weight:600;font-size:1rem;color:#0F172A;">Processes</div>'
        '<div style="font-size:0.82rem;color:#64748B;margin-top:4px;">'
        "Detailed guides for transcription, diarization, speaker recognition, and more.</div></div>",
        unsafe_allow_html=True,
    )
    if st.button("View processes", icon=":material/settings_suggest:", key="nav_proc"):
        st.switch_page("pages/processes.py")

with col3:
    st.markdown(
        '<div style="background:#F1F5F9;border-radius:8px;padding:16px;">'
        '<div style="font-weight:600;font-size:1rem;color:#0F172A;">Authentication</div>'
        '<div style="font-size:0.82rem;color:#64748B;margin-top:4px;">'
        "Understand the three-tier auth system: Firebase, QR+PIN, and access permissions.</div></div>",
        unsafe_allow_html=True,
    )
    if st.button("Auth details", icon=":material/lock:", key="nav_auth"):
        st.switch_page("pages/processes.py")
