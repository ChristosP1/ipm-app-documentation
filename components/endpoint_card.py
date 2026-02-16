"""Reusable endpoint card component for listing pages."""

from __future__ import annotations

from typing import Any

import streamlit as st

from components.styles import method_badge_html


def render_endpoint_card(endpoint: dict[str, Any], *, show_auth: bool = True) -> bool:
    """Render a clickable endpoint card. Returns True if clicked."""
    method = endpoint["method"]
    path = endpoint["path"]
    title = endpoint["title"]
    summary = endpoint.get("summary", "")
    auth = endpoint.get("auth", "")

    badge = method_badge_html(method)
    auth_html = (
        f'<span class="auth-badge">{auth}</span>' if show_auth and auth else ""
    )

    html = f"""
    <div class="endpoint-card">
        <div style="display:flex; align-items:center; gap:10px; flex-wrap:wrap;">
            {badge}
            <span class="endpoint-path">{path}</span>
            {auth_html}
        </div>
        <div style="margin-top:6px; font-size:0.92rem; font-weight:600; color:#0F172A;">
            {title}
        </div>
        <div style="margin-top:2px; font-size:0.82rem; color:#64748B;">
            {summary}
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

    # Use a small button as the clickable trigger (styled minimally)
    return st.button(
        f"View details",
        key=f"card_{endpoint['id']}",
        type="tertiary",
        icon=":material/arrow_forward:",
    )
